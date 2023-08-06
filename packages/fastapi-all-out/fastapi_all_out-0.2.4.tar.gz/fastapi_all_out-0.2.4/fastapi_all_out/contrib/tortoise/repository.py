from collections import defaultdict
from typing import Any, Optional, TypeVar, TYPE_CHECKING, Type

from tortoise.models import MetaInfo
from tortoise.fields import ManyToManyRelation, Field, DateField, DatetimeField, TimeField
from tortoise.queryset import QuerySet
from tortoise.transactions import in_transaction

from fastapi_all_out.routers.base_repository import BaseRepository, PK, ModelPrefix, Updated
from fastapi_all_out.routers.exceptions import ItemNotFound, ObjectErrors, FieldError, NotUnique, ListFieldError,\
    NotFoundFK, FieldRequired
from .repository_meta import TortoiseRepositoryMeta
from .models import BaseModel

if TYPE_CHECKING:
    from fastapi_all_out.routers.filters import BaseFilter


DB_MODEL = TypeVar('DB_MODEL', bound=BaseModel)


class TortoiseRepository(BaseRepository[DB_MODEL], metaclass=TortoiseRepositoryMeta):
    opts: MetaInfo
    node_key = 'parent_id'

    select_related: tuple[str]
    prefetch_related: tuple[str]

    root_instance: Optional[DB_MODEL]
    BFK_REMOVE_FIELDS_PATTERN = '_{}_remove'
    M2M_REMOVE_FIELDS_PATTERN = '_{}_remove'
    M2M_ADD_FIELDS_PATTERN = '_{}_add'

    def __init__(self, *args, select_related: tuple[str] = (), prefetch_related: tuple[str] = (), **kwargs):
        super().__init__(*args, **kwargs)
        self.select_related = select_related
        self.prefetch_related = prefetch_related
        self.root_instance = None

    def get_queryset(self):
        query = self.model.all()
        if default_filters := self.qs_default_filters():
            query = query.filter(**default_filters)
        if annotate_fields := self.qs_annotate_fields():
            query = query.annotate(**annotate_fields)
        if final_select_related := {*self.qs_select_related(), *self.select_related}:
            query = query.select_related(*final_select_related)
        if final_prefetch_related := {*self.qs_prefetch_related(), *self.prefetch_related}:
            query = query.prefetch_related(*final_prefetch_related)
        return query

    def qs_default_filters(self) -> dict[str, Any]:
        return {}

    def qs_annotate_fields(self) -> dict[str, Any]:
        return {}

    def qs_select_related(self) -> set[str]:
        return set()

    def qs_prefetch_related(self) -> set[str]:
        return set()

    async def get_all(
            self,
            skip: Optional[int],
            limit: Optional[int],
            sort: list[str],
            filters: list["BaseFilter"],
    ) -> tuple[list[DB_MODEL], int]:
        query = self.get_queryset()
        for f in filters:
            query = f.filter(query)
        base_query = query
        if sort:
            query = query.order_by(*sort)
        if skip:
            query = query.offset(skip)
        if limit:
            query = query.limit(limit)
        async with in_transaction():
            result = await query
            count = await base_query.count()
        return result, count

    def _get_many_queryset(self, item_ids: list[PK]) -> QuerySet[DB_MODEL]:
        return self.get_queryset().filter(pk__in=item_ids)

    async def get_many(self, item_ids: list[PK]) -> list[DB_MODEL]:
        return await self._get_many_queryset(item_ids)

    async def get_one(self, item_id: PK, *, field_name: str = 'pk') -> Optional[DB_MODEL]:
        if field_name in self.model.IEXACT_FIELDS:
            field_name = field_name + '__iexact'
        instance = await self.get_queryset()\
            .get_or_none(**{field_name: item_id})
        if instance is None:
            raise ItemNotFound()
        return instance

    async def get_tree_node(self, node_id: Optional[PK]) -> list[DB_MODEL]:
        return await self.get_queryset().filter(**{self.node_key: node_id})

    async def create(
            self,
            data: dict[str, Any],
            *,
            model: Type[DB_MODEL] = None,
            exclude: set[str] = None,
            defaults: dict[str, Any] = None,
            inside_transaction: bool = False,
            prefix: ModelPrefix = ModelPrefix(),
    ) -> DB_MODEL:
        model: Type[DB_MODEL] = model or self.model
        fk_fields, bfk_fields, o2o_fields, bo2o_fields, m2m_fields = exclude_fk_bfk_o2o_bo2o_m2m(model, data)
        exclude_dict = get_exclude_dict(exclude or set())
        errors = ObjectErrors()
        defaults = defaults or {}

        async def get_new_instance() -> DB_MODEL:
            try:
                await self.clean_data(
                    model=model, data=data, prefix=prefix, create=True,
                    fk_fields=fk_fields,
                    bfk_fields=bfk_fields,
                    o2o_fields=o2o_fields,
                    bo2o_fields=bo2o_fields,
                    m2m_fields=m2m_fields,
                )
            except ObjectErrors as e:
                raise errors.merge(e)
            try:
                await self.check_unique(data=data, model=model, prefix=prefix)
            except ObjectErrors as e:
                errors.merge(e)

            # Сначала создаём o2o и fk, потому что они могут быть not null, из-за этого вылетает ошибка.
            created_o2o, picked_fks = {}, {}

            for o2o_field_name in o2o_fields:
                try:
                    created_o2o[o2o_field_name] = await self.create_o2o(
                        model=model,
                        field_name=o2o_field_name,
                        data=data,
                        exclude=exclude_dict[o2o_field_name],
                        prefix=prefix.plus(o2o_field_name),
                    )
                except ObjectErrors as e:
                    errors.add(o2o_field_name, e)

            try:
                picked_fks = await self.pick_fks(model=model, fk_fields=fk_fields, data=data, prefix=prefix)
            except ObjectErrors as e:
                errors.merge(e)

            if errors:
                raise errors

            try:
                instance: Optional[DB_MODEL] = await self.handle_create(
                    model=model,
                    data=data,
                    exclude={*exclude_dict['__root__'], *fk_fields},
                    prefix=prefix,
                    defaults={**self.get_defaults(prefix), **defaults, **created_o2o, **picked_fks},
                )
            except ObjectErrors as e:
                raise errors.merge(e)

            for bo2o_field_name in bo2o_fields:
                try:
                    await self.create_backward_o2o(
                        instance=instance,
                        field_name=bo2o_field_name,
                        data=data,
                        exclude=exclude_dict[bo2o_field_name],
                        prefix=prefix.plus(bo2o_field_name)
                    )
                except ObjectErrors as e:
                    errors.add(bo2o_field_name, e)

            for bfk_field_name in bfk_fields:
                try:
                    await self.create_backward_fk(
                        instance=instance,
                        field_name=bfk_field_name,
                        data=data,
                        exclude=exclude_dict[bfk_field_name],
                        prefix=prefix.plus(bfk_field_name),
                    )
                except ListFieldError as e:
                    errors.add(bfk_field_name, e)

            if errors:
                raise errors

            for m2m_field_name in m2m_fields:
                await self.save_m2m(
                    instance=instance,
                    data=data,
                    field_name=m2m_field_name,
                    prefix=prefix.plus(m2m_field_name),
                )

            return instance

        if inside_transaction:
            return await get_new_instance()
        else:
            async with in_transaction():
                new_instance = await get_new_instance()
            await self.post_create(new_instance)
            if self.background_tasks:
                self.background_tasks.add_task(self.post_create_background, new_instance)
            return await self.get_one(new_instance.pk)

    async def create_o2o(
            self,
            model: Type[DB_MODEL],
            field_name: str,
            data: dict[str, Any],
            exclude: set[str],
            prefix: ModelPrefix,
    ) -> Optional[DB_MODEL]:
        o2o_data = data.get(field_name)
        if o2o_data is None:
            return None
        o2o_model: Type[DB_MODEL] = model._meta.fields_map[field_name].related_model
        return await self.create(
            data=o2o_data,
            model=o2o_model,
            exclude=exclude,
            inside_transaction=True,
            prefix=prefix,
        )

    async def create_backward_o2o(
            self,
            instance: DB_MODEL,
            field_name: str,
            data: dict[str, Any],
            exclude: set[str],
            prefix: ModelPrefix,
    ) -> None:
        back_o2o_data = data.get(field_name)
        if back_o2o_data is None:
            return
        back_o2o_field = instance._meta.fields_map[field_name]
        back_o2o_model: Type[DB_MODEL] = back_o2o_field.related_model
        back_o2o_source_field = back_o2o_model._meta\
            .fields_map[back_o2o_field.relation_source_field]\
            .reference.model_field_name
        await self.create(
            data=back_o2o_data,
            model=back_o2o_model,
            exclude=exclude,
            defaults={back_o2o_source_field: instance},
            inside_transaction=True,
            prefix=prefix
        )

    async def create_backward_fk(
            self,
            instance: DB_MODEL,
            field_name: str,
            data: dict[str, Any],
            exclude: set[str],
            prefix: ModelPrefix,
    ) -> None:
        list_errors = ListFieldError()
        back_fk_field = instance._meta.fields_map[field_name]
        back_fk_model: Type[DB_MODEL] = back_fk_field.related_model
        back_fk_source_field = back_fk_model._meta \
            .fields_map[back_fk_field.relation_source_field] \
            .reference.model_field_name
        for index, back_fk_data in enumerate(data.get(field_name)):
            try:
                await self.create(
                    data=back_fk_data,
                    model=back_fk_model,
                    exclude=exclude,
                    defaults={back_fk_source_field: instance},
                    inside_transaction=True,
                    prefix=prefix,
                )
            except ObjectErrors as e:
                list_errors.append(index, e)
        if list_errors:
            raise list_errors

    async def edit(
            self,
            instance: DB_MODEL,
            data: dict[str, Any],
            *,
            exclude: set[str] = None,
            defaults: dict[str, Any] = None,
            inside_transaction: bool = False,
            prefix: ModelPrefix = ModelPrefix(),
    ) -> DB_MODEL:
        model: Type[DB_MODEL] = instance.__class__
        fk_fields, bfk_fields, o2o_fields, bo2o_fields, m2m_fields = exclude_fk_bfk_o2o_bo2o_m2m(model, data)
        exclude_dict = get_exclude_dict(exclude or set())
        errors = ObjectErrors()
        defaults = defaults or {}

        async def get_changed_instance() -> DB_MODEL:
            await self.clean_data(
                model=model, data=data, prefix=prefix, instance=instance, create=False,
                fk_fields=fk_fields,
                bfk_fields=bfk_fields,
                o2o_fields=o2o_fields,
                bo2o_fields=bo2o_fields,
                m2m_fields=m2m_fields,
            )
            try:
                await self.check_unique(data=data, model=model, prefix=prefix)
            except ObjectErrors as e:
                errors.merge(e)

            created_o2o, picked_fks = {}, {}
            for o2o_field_name in o2o_fields:
                try:
                    o2o_instance = await self.edit_o2o(
                        instance=instance,
                        field_name=o2o_field_name,
                        data=data,
                        exclude=exclude_dict[o2o_field_name],
                        prefix=prefix.plus(o2o_field_name),
                    )
                    if o2o_instance:
                        created_o2o[o2o_field_name] = o2o_instance
                except ObjectErrors as e:
                    errors.add(o2o_field_name, e)

            try:
                picked_fks = await self.pick_fks(model=model, fk_fields=fk_fields, data=data, prefix=prefix)
            except ObjectErrors as e:
                errors.merge(e)

            if errors:
                raise errors

            await self.handle_edit(
                instance=instance,
                data=data,
                exclude={*exclude_dict['__root__'], *fk_fields},
                prefix=prefix,
                defaults={**defaults, **created_o2o, **picked_fks},
            )

            for bo2o_field_name in bo2o_fields:
                try:
                    await self.edit_backward_o2o(
                        instance=instance,
                        field_name=bo2o_field_name,
                        data=data,
                        exclude=exclude_dict[bo2o_field_name],
                        prefix=prefix.plus(bo2o_field_name)
                    )
                except ObjectErrors as e:
                    errors.add(bo2o_field_name, e)

            for bfk_source_field_name in bfk_fields:
                try:
                    await self.edit_backward_fk(
                        instance=instance,
                        field_name=bfk_source_field_name,
                        data=data,
                        exclude=exclude_dict[bfk_source_field_name],
                        prefix=prefix.plus(bfk_source_field_name)
                    )
                except ListFieldError as e:
                    errors.add(bfk_source_field_name, e)

            for m2m_field_name in m2m_fields:
                await self.save_m2m(
                    instance=instance,
                    data=data,
                    field_name=m2m_field_name,
                    prefix=prefix.plus(m2m_field_name),
                    clear=True,
                )

            if errors:
                raise errors

            return instance

        if inside_transaction:
            return await get_changed_instance()
        else:
            self.root_instance = instance
            self.updated = {}
            async with in_transaction():
                changed_instance = await get_changed_instance()
            await self.post_edit(self.updated)
            if self.background_tasks:
                self.background_tasks.add_task(self.post_edit_background, self.updated)
            return await self.get_one(changed_instance.pk)

    async def edit_o2o(
            self,
            instance: DB_MODEL,
            field_name: str,
            data: dict[str, Any],
            exclude: set[str],
            prefix: ModelPrefix,
    ) -> Optional[DB_MODEL]:
        o2o_instance: Optional[DB_MODEL] = getattr(instance, field_name)
        o2o_data = data.get(field_name)
        if o2o_data is None:
            if o2o_instance is not None:
                await o2o_instance.delete()
            return None
        if o2o_instance is not None:
            await self.edit(
                instance=o2o_instance,
                data=o2o_data,
                exclude=exclude,
                inside_transaction=True,
                prefix=prefix,
            )
        else:
            return await self.create(
                data=o2o_data,
                exclude=exclude,
                model=instance._meta.fields_map[field_name].related_model,
                inside_transaction=True,
                prefix=prefix,
            )

    async def edit_backward_o2o(
            self,
            instance: DB_MODEL,
            field_name: str,
            data: dict[str, Any],
            exclude: set[str],
            prefix: ModelPrefix,
    ) -> None:
        back_o2o_instance = getattr(instance, field_name)
        back_o2o_data = data.get(field_name)
        back_o2o_field = instance._meta.fields_map[field_name]
        back_o2o_model: Type[DB_MODEL] = back_o2o_field.related_model
        back_o2o_source_field = back_o2o_model._meta \
            .fields_map[back_o2o_field.relation_source_field] \
            .reference.model_field_name
        if back_o2o_instance is not None:
            await self.edit(
                instance=back_o2o_instance,
                data=back_o2o_data,
                exclude=exclude,
                inside_transaction=True,
                prefix=prefix,
            )
        else:
            await self.create(
                data=back_o2o_data,
                model=back_o2o_model,
                exclude=exclude,
                defaults={back_o2o_source_field: instance},
                inside_transaction=True,
                prefix=prefix,
            )

    async def edit_backward_fk(
            self,
            instance: DB_MODEL,
            field_name: str,
            data: dict[str, Any],
            exclude: set[str],
            prefix: ModelPrefix,
    ) -> None:
        def get_fk_instance(instances: list[DB_MODEL], pk_value) -> DB_MODEL | None:
            for i in instances:
                if i.pk == pk_value:
                    return i

        list_errors = ListFieldError()
        back_fk_instances: list[DB_MODEL] = getattr(instance, field_name)
        back_fk_field = instance._meta.fields_map[field_name]
        back_fk_model: Type[DB_MODEL] = back_fk_field.related_model
        back_fk_source_field = back_fk_model._meta \
            .fields_map[back_fk_field.relation_source_field] \
            .reference.model_field_name
        back_pk_attr = self._get_pk_attr(back_fk_model)
        for index, back_fk_data in enumerate(data.get(field_name)):
            back_fk_data: dict[str, Any]
            if pk := back_fk_data.get(back_pk_attr):
                fk_instance = get_fk_instance(back_fk_instances, pk)
                if fk_instance:
                    coro = self.edit(
                        instance=fk_instance,
                        data=back_fk_data,
                        exclude=exclude,
                        inside_transaction=True,
                        prefix=prefix.plus(index),
                    )
                else:
                    list_errors.append(index, NotFoundFK)
                    continue
            else:
                coro = self.create(
                    data=back_fk_data,
                    model=back_fk_model,
                    exclude=exclude,
                    defaults={back_fk_source_field: instance},
                    inside_transaction=True,
                    prefix=prefix.plus(index),
                )
            try:
                await coro
            except ObjectErrors as e:
                list_errors.append(index, e)

        if list_errors:
            raise list_errors

        remove_pks = data.get(self.BFK_REMOVE_FIELDS_PATTERN.format(field_name))
        if remove_pks:
            await back_fk_model.filter(pk__in=remove_pks).delete()

    async def pick_fk(
            self,
            model: Type[DB_MODEL],
            fk_source_field_name: str,
            data: dict[str, Any],
            prefix: ModelPrefix,
    ) -> tuple[str, Optional[DB_MODEL]]:
        opts = model._meta
        rel_model, field_name = None, None
        for field in opts.fk_fields:
            if (f_opts := opts.fields_map[field]).source_field == fk_source_field_name:
                rel_model = f_opts.related_model
                field_name = field

        value = data.get(fk_source_field_name)
        if value is None:
            return field_name, None

        fk_get_func = getattr(self, f'fk_get_{prefix}', self._fk_get_default)
        rel_instance = await fk_get_func(model=rel_model, pk=value)
        if rel_instance is None:
            raise NotFoundFK
        return field_name, rel_instance

    async def pick_fks(
            self,
            model: Type[DB_MODEL],
            fk_fields: set[str],
            data: dict[str, Any],
            prefix: ModelPrefix,
    ) -> dict[str, Optional[DB_MODEL]]:
        picked_fks = {}
        errors = ObjectErrors()
        for fk_source_field_name in fk_fields:
            try:
                fk_field_name, fk_instance = await self.pick_fk(
                    model=model,
                    fk_source_field_name=fk_source_field_name,
                    data=data,
                    prefix=prefix.plus(fk_source_field_name)
                )
                picked_fks[fk_field_name] = fk_instance
            except NotFoundFK:
                errors.add(fk_source_field_name, NotFoundFK)
        if errors:
            raise errors
        return picked_fks

    async def save_m2m(
            self,
            instance: DB_MODEL,
            data: dict[str, Any],
            field_name: str,
            prefix: ModelPrefix,
            clear=False,
    ) -> None:
        rel: ManyToManyRelation = getattr(instance, field_name)
        ids: list[PK] = data.get(field_name)
        if ids is None:
            return
        if clear:
            await rel.clear()
        if ids:
            await rel.add(*(await rel.remote_model.filter(pk__in=ids)))

    async def delete_many(self, item_ids: list[PK]) -> int:
        return await self._get_many_queryset(item_ids).delete()

    async def delete_one(self, instance: DB_MODEL) -> None:
        await instance.delete()

    async def handle_create(
            self,
            model: Type[DB_MODEL],
            data: dict[str, Any],
            exclude: set[str],
            prefix: ModelPrefix,
            defaults: dict[str, Any] = None,
    ) -> DB_MODEL:
        if hasattr(self, f'handle_create_{prefix}'):
            handler = getattr(self, f'handle_create_{prefix}')
        else:
            handler = self._handle_create_default
        return await handler(
            model=model,
            data=data,
            exclude=exclude,
            prefix=prefix,
            defaults=defaults,
        )

    async def _handle_create_default(
            self,
            model: Type[DB_MODEL],
            data: dict[str, Any],
            exclude: set[str],
            prefix: ModelPrefix,
            defaults: dict[str, Any] = None,
            commit: bool = True,
    ) -> DB_MODEL:
        errors = ObjectErrors()
        include_fields = model._meta.db_fields.difference(exclude)
        final_data = {field: value for field, value in data.items() if field in include_fields}
        if defaults is not None:
            final_data.update(defaults)
        instance = model(**final_data)
        opts = model._meta
        pass_check_required = self.get_pass_check_required(prefix)
        for field_name in opts.db_fields:
            if field_name in pass_check_required:
                continue
            if field_is_required(opts.fields_map[field_name]) and getattr(instance, field_name) is None:
                errors.add(field_name, FieldRequired)
        if errors:
            raise errors
        if commit:
            await instance.save(force_create=True)
        return instance

    async def handle_edit(
            self,
            instance: DB_MODEL,
            data: dict[str, Any],
            exclude: set[str],
            prefix: ModelPrefix,
            defaults: dict[str, Any] = None,
    ) -> None:
        if hasattr(self, f'handle_edit_{prefix}'):
            handler = getattr(self, f'handle_edit_{prefix}')
        else:
            handler = self._handle_edit_default
        await handler(
            instance=instance,
            data=data,
            exclude=exclude,
            prefix=prefix,
            defaults=defaults,
        )

    async def _handle_edit_default(
            self,
            instance: DB_MODEL,
            data: dict[str, Any],
            exclude: set[str],
            prefix: ModelPrefix,
            defaults: dict[str, Any] = None,
    ) -> None:
        errors = ObjectErrors()
        include_fields = instance._meta.db_fields.difference(exclude)
        final_data = {field: value for field, value in data.items() if field in include_fields}
        if defaults is not None:
            final_data.update(defaults)
        instance.update_from_dict(final_data)
        opts = instance._meta
        for field_name in opts.db_fields:
            if field_is_required(opts.fields_map[field_name]) and getattr(instance, field_name) is None:
                errors.add(field_name, FieldRequired)
        if errors:
            raise errors
        if final_data:
            await instance.save(force_update=True)
            self.updated[prefix] = Updated(instance=instance, fields=set(final_data.keys()))

    async def clean_data(
            self,
            model: Type[DB_MODEL],
            data: dict[str, Any],
            prefix: ModelPrefix,
            fk_fields: set[str],
            bfk_fields: set[str],
            o2o_fields: set[str],
            bo2o_fields: set[str],
            m2m_fields: set[str],
            instance: Optional[DB_MODEL] = None,
            create: bool = True,
    ) -> dict[str, Any]:
        related_fields = {*model._meta.db_fields, *fk_fields, *bfk_fields, *o2o_fields, *bo2o_fields, *m2m_fields}
        errors = ObjectErrors()
        for field_name in related_fields:
            if field_name not in data:
                continue
            func_name = f'clean_field_{prefix.plus(field_name)}'
            if hasattr(self, func_name):
                func = getattr(self, func_name)
            elif field_name in fk_fields:
                func = self._clean_fk_field_default
            elif field_name in bfk_fields:
                func = self._clean_bfk_field_default
            elif field_name in o2o_fields:
                func = self._clean_o2o_field_default
            elif field_name in bo2o_fields:
                func = self._clean_bo2o_field_default
            elif field_name in m2m_fields:
                func = self._clean_m2m_field_default
            else:
                func = self._clean_field_default
            try:
                if await func(
                        model=model, data=data,
                        field_name=field_name, instance=instance, create=create
                ):
                    for set_ in (fk_fields, bfk_fields, o2o_fields, bo2o_fields, m2m_fields):
                        if field_name in set_:
                            set_.remove(field_name)
                    try:
                        del data[field_name]
                    except KeyError:
                        pass
            except FieldError as e:
                errors.add(field_name, e)
        if errors:
            raise errors
        return data

    async def _clean_field_default(
            self, model: Type[DB_MODEL], data: dict[str, Any], field_name: str,
            instance: Optional[DB_MODEL], create: bool
    ) -> bool:
        if create:
            return False
        return getattr(instance, field_name) == data[field_name]

    async def _clean_fk_field_default(
            self, model: Type[DB_MODEL], data: dict[str, Any], field_name: str,
            instance: Optional[DB_MODEL], create: bool
    ) -> bool:
        return await self._clean_field_default(
            model=model, data=data, field_name=field_name,
            instance=instance, create=create
        )

    async def _clean_bfk_field_default(
            self, model: Type[DB_MODEL], data: dict[str, Any], field_name: str,
            instance: Optional[DB_MODEL], create: bool
    ) -> bool:
        if not create:
            value: list[dict[str, Any]] = data[field_name]
            bfk_model = self._get_bfk_model(model=model, field_name=field_name)
            bfk_pk_attr = self._get_pk_attr(bfk_model)
            data_before: list[DB_MODEL] = await getattr(instance, field_name).all()
            remove_pks = []
            current_pks = [item_pk for item in value if (item_pk := item.get(bfk_pk_attr)) is not None]
            for item in data_before:
                if item.pk not in current_pks:
                    remove_pks.append(item.pk)
            if remove_pks:
                data[self.BFK_REMOVE_FIELDS_PATTERN.format(field_name)] = remove_pks
        return False

    async def _clean_o2o_field_default(
            self, model: Type[DB_MODEL], data: dict[str, Any], field_name: str,
            instance: Optional[DB_MODEL], create: bool
    ) -> bool:
        return False

    async def _clean_bo2o_field_default(
            self, model: Type[DB_MODEL], data: dict[str, Any], field_name: str,
            instance: Optional[DB_MODEL], create: bool
    ) -> bool:
        return False

    async def _clean_m2m_field_default(
            self, model: Type[DB_MODEL], data: dict[str, Any], field_name: str,
            instance: Optional[DB_MODEL], create: bool
    ) -> bool:
        return False

    async def check_unique(self, data: dict[str, Any], model: Type[DB_MODEL], prefix: ModelPrefix) -> None:
        errors = ObjectErrors()
        for field_name in model._meta.db_fields:
            field = model._meta.fields_map[field_name]
            if not field.unique or field.generated:
                continue
            if (value := data.get(field_name)) is not None:
                if hasattr(self, f'check_unique_{prefix.plus(field_name)}'):
                    check_unique_func = getattr(self, f'check_unique_{prefix.plus(field_name)}')
                else:
                    check_unique_func = self._check_unique_default
                if not await check_unique_func(model=model, field_name=field_name, value=value):
                    errors.add(field_name, NotUnique)
        if errors:
            raise errors

    async def _check_unique_default(self, model: Type[DB_MODEL], field_name: str, value: Any) -> bool:
        if field_name in model.IEXACT_FIELDS:
            field_name = field_name + '__iexact'
        return not await model.filter(**{field_name: value}).exists()

    @classmethod
    def _get_bfk_model(cls, model: Type[BaseModel], field_name: str) -> Type[BaseModel]:
        return model._meta.fields_map[field_name].related_model

    @classmethod
    def _get_pk_attr(cls, model: Type[BaseModel]) -> str:
        return model._meta.pk_attr

    @classmethod
    def get_default_sort_fields(cls) -> set[str]:
        return {*cls.opts.db_fields}

    async def _fk_get_default(self, model: Type[DB_MODEL], pk: PK) -> DB_MODEL:
        return await model.get_or_none(pk=pk)


def get_exclude_dict(fields: set[str]) -> dict[str, set[str]]:
    """
    Из {a, b, c.d, c.e, f.g.h, f.g.i} делает
    {
        '__root__': {'a', 'b'},
        'c': {'d', 'e'},
        'f': {'g.h', 'g.i'}
    }
    """
    exclude_dict = defaultdict(set)
    for field in fields:
        if '.' not in field:
            exclude_dict['__root__'].add(field)
        else:
            base, _, field_in_related = field.partition('.')
            exclude_dict[base].add(field_in_related)
    return exclude_dict


def exclude_fk_bfk_o2o_bo2o_m2m(
        model: Type[DB_MODEL], data: dict[str, Any]
) -> tuple[set[str], set[str], set[str], set[str], set[str]]:
    opts = model._meta
    return (
        exclude_fields_from_data(data, *(opts.fields_map[f].source_field for f in opts.fk_fields)),
        exclude_fields_from_data(data, *opts.backward_fk_fields),
        exclude_fields_from_data(data, *opts.o2o_fields),
        exclude_fields_from_data(data, *opts.backward_o2o_fields),
        exclude_fields_from_data(data, *opts.m2m_fields)
    )


def exclude_fields_from_data(data: dict[str, Any], *fields: str) -> set[str]:
    return_fields: set[str] = set()
    for field_name in fields:
        if field_name in data:
            return_fields.add(field_name)
    return return_fields


def field_is_required(field: Field) -> bool:
    if isinstance(field, (DateField, DatetimeField, TimeField)) and (field.auto_now or field.auto_now_add):
        return False
    if field.required:
        return True
    return False
