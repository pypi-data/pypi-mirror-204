from typing import TypeVar, Any, Generic, Literal
from abc import ABC, abstractmethod

from passlib.context import CryptContext
from fastapi import Request, BackgroundTasks, Response

from fastapi_all_out.enums import TempCodeTriggers
from .base import BaseUser


USER_MODEL = TypeVar("USER_MODEL", bound=BaseUser)
UNUSED_PASSWORD_PREFIX = '!'


class BaseUserService(Generic[USER_MODEL], ABC):

    user: USER_MODEL
    pwd_context = CryptContext(schemes=["md5_crypt"], deprecated="auto")

    def __init__(self, user: USER_MODEL):
        self.user = user

    def can_login(self) -> bool:
        return self.user.is_active

    async def if_cant_login(self, request: Request, background_tasks: BackgroundTasks, response: Response) -> None:
        pass

    def token_expired(self, iat: int) -> bool:
        return self.user.password_change_dt.timestamp() > iat

    @abstractmethod
    def set_password(self, password: str) -> None: ...

    def get_fake_password(self, password: str) -> str:
        return password + str(self.user.password_change_dt.timestamp()) + self.user.password_salt

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(self.get_fake_password(password))

    def verify_password(self, password: str) -> bool:
        if self.user.password_hash.startswith(UNUSED_PASSWORD_PREFIX):
            return False
        return self.pwd_context.verify(self.get_fake_password(password), self.user.password_hash)

    @abstractmethod
    async def get_or_create_temp_code(self, trigger: TempCodeTriggers) -> Any: ...

    @abstractmethod
    async def update_or_create_temp_code(self, trigger: TempCodeTriggers) -> None: ...

    @abstractmethod
    async def send_activation_email(self) -> None: ...

    @abstractmethod
    async def send_password_reset_email(self) -> None: ...

    async def post_registration(self, request: Request, background_tasks: BackgroundTasks) -> None:
        background_tasks.add_task(self.send_activation_email)

    @abstractmethod
    def check_temp_code_error(self, code: str, trigger: TempCodeTriggers) -> Literal['expired', 'incorrect'] | None: ...

    @abstractmethod
    async def activate(self) -> None: ...
