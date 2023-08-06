from abc import abstractmethod
from typing import Type, Any, TypeVar, Generic, Optional, Callable, Coroutine, TypedDict
from uuid import UUID

from fastapi import Request, BackgroundTasks, Response

from fastapi_all_out.lazy import get_auth_backend
from .filters import BaseFilter


SERVICE = TypeVar('SERVICE', bound="BaseCRUDService")
PK = TypeVar('PK', int, UUID)
DB_MODEL = TypeVar('DB_MODEL')


class ModelPrefix(str):
    def plus(self, field_name: str | int):
        if self == '':
            return self.__class__(field_name)
        else:
            return self.__class__(f'{self}__{field_name}')


class Updated(Generic[DB_MODEL], TypedDict):
    instance: DB_MODEL
    fields: set[str]


class BaseRepository(Generic[DB_MODEL]):
    model: Type[DB_MODEL]
    pk_attr: str
    node_key: str
    pk_field_type: Type[PK]

    defaults: dict[str, dict[str, Any]] = None  # {"field": value, "o2o": {"field": "value"}}
    pass_check_required: dict[str, set[str]] = None  # {"": {'a', 'b'}, "submodel__subsubmodel": {'a', 'b'}}

    request: Optional[Request]
    background_tasks: Optional[BackgroundTasks]
    response: Optional[Response]

    updated: dict[str, Updated]

    def __init__(
            self,
            *,
            request: Optional[Request] = None,
            background_tasks: Optional[BackgroundTasks] = None,
            response: Optional[Response] = None
    ):
        self.request = request
        self.background_tasks = background_tasks
        self.response = response

    @property
    def request_path(self) -> Optional[str]:
        if self.request:
            return self.request.scope['route'].path

    @property
    def request_method(self) -> Optional[str]:
        if self.request:
            return self.request.method.upper()

    @abstractmethod
    def get_queryset(self): ...

    @abstractmethod
    async def get_all(
            self,
            skip: Optional[int],
            limit: Optional[int],
            sort: list[str],
            filters: list[BaseFilter],
    ) -> tuple[list[DB_MODEL], int]: ...

    @abstractmethod
    async def get_many(self, item_ids: list[PK]) -> list[DB_MODEL]: ...

    @abstractmethod
    async def get_one(self, item_id: PK, *, field_name: str = 'pk') -> DB_MODEL: ...

    @abstractmethod
    async def get_tree_node(self, node_id: Optional[PK]) -> list[DB_MODEL]: ...

    @abstractmethod
    async def create(
            self,
            data: dict[str, Any],
            *,
            model: Type[DB_MODEL] = None,
            exclude: set[str] = None,
            defaults: dict[str, Any] = None,
            inside_transaction: bool = False,
            prefix: ModelPrefix = ModelPrefix(),
    ) -> DB_MODEL: ...

    async def post_create(self, instance: DB_MODEL) -> None:
        pass

    async def post_create_background(self, instance: DB_MODEL) -> None:
        pass

    @abstractmethod
    async def edit(
            self,
            instance: DB_MODEL,
            data: dict[str, Any],
            *,
            exclude: set[str] = None,
            defaults: dict[str, Any] = None,
            inside_transaction: bool = False,
            prefix: ModelPrefix = ModelPrefix(),
    ) -> DB_MODEL: ...

    async def post_edit(self, updated: dict[str, Updated[DB_MODEL]]) -> None:
        pass

    async def post_edit_background(self, updated: dict[str, Updated[DB_MODEL]]) -> None:
        pass

    @abstractmethod
    async def delete_many(self, instances: list[PK]) -> int: ...

    @abstractmethod
    async def delete_one(self, instance: DB_MODEL) -> None: ...

    @classmethod
    def with_model_permissions(cls, name: str) -> Callable[[...], Coroutine[Any, Any, None]]:
        return get_auth_backend().with_permissions((cls.model.__name__, name))

    @classmethod
    def with_create_permissions(cls) -> Callable[[...], Coroutine[Any, Any, None]]:
        return cls.with_model_permissions('create')

    @classmethod
    def with_get_permissions(cls) -> Callable[[...], Coroutine[Any, Any, None]]:
        return cls.with_model_permissions('get')

    @classmethod
    def with_edit_permissions(cls) -> Callable[[...], Coroutine[Any, Any, None]]:
        return cls.with_model_permissions('edit')

    @classmethod
    def with_delete_permissions(cls) -> Callable[[...], Coroutine[Any, Any, None]]:
        return cls.with_model_permissions('delete')

    @classmethod
    @abstractmethod
    def get_default_sort_fields(cls) -> set[str]: ...

    def get_defaults(self, prefix: ModelPrefix) -> dict[str, Any]:
        if self.defaults:
            return self.defaults.get(prefix, {})
        return {}

    def get_pass_check_required(self, prefix: ModelPrefix) -> set[str]:
        if self.pass_check_required:
            return self.pass_check_required.get(prefix, set())
        return set()

    @abstractmethod
    def _fk_get_default(self, model: Type[DB_MODEL], pk: PK) -> DB_MODEL: ...
