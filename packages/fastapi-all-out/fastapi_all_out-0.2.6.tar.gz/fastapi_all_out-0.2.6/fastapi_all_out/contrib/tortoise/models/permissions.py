from tortoise import fields

from .content_type import ContentType
from . import BaseModel


class Permission(BaseModel):
    id: int
    name: str = fields.CharField(max_length=50)
    content_type_id: int
    content_type: fields.ForeignKeyRelation[ContentType] | ContentType = fields.ForeignKeyField(
        'models.ContentType', on_delete=fields.CASCADE, related_name='permissions'
    )

    class Meta:
        table = "permissions"
        ordering = ("content_type_id", "name")
        unique_together = (('name', 'content_type'),)

    def __str__(self):
        return f'Can {self.name} {self.content_type_name}'

    @property
    def content_type_name(self):
        return ContentType.get_by_id(self.content_type_id).name


class PermissionGroup(BaseModel):
    id: int
    name: str = fields.CharField(max_length=100, description='Наименование', unique=True)
    permissions: fields.ManyToManyRelation[Permission] = fields.ManyToManyField(
        'models.Permission', related_name='groups'
    )

    class Meta:
        table = "permission_groups"
        ordering = ('name',)


class PermissionMixin(BaseModel):
    permissions: fields.ManyToManyRelation[Permission] = fields.ManyToManyField(
        'models.Permission', related_name='users'
    )
    groups: fields.ManyToManyRelation[PermissionGroup] = fields.ManyToManyField(
        'models.PermissionGroup', related_name='users'
    )

    class Meta:
        abstract = True

    @property
    def all_permissions(self) -> set[Permission]:
        return {*self.permissions, *(p for g in self.groups for p in g.permissions)}

    def get_permissions_as_tuples(self) -> tuple[tuple[int, str], ...]:
        return tuple((perm.content_type_id, perm.name) for perm in self.all_permissions)

    def has_permissions(self, *permissions: tuple[str, str]) -> bool:
        if not permissions:
            return True
        user_perms = self.get_permissions_as_tuples()
        has = True
        for model_name, perm_name in permissions:
            content_type_id = ContentType.get_by_name(model_name).id
            if (content_type_id, perm_name) not in user_perms:
                has = False
                break
        return has
