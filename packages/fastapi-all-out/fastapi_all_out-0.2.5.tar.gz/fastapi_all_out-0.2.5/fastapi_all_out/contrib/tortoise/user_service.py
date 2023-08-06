from random import choices
from string import hexdigits
from typing import TypeVar, Type, Literal, Optional

from tortoise import timezone

from fastapi_all_out.auth.user_service import BaseUserService, UNUSED_PASSWORD_PREFIX
from fastapi_all_out.lazy import get_user_model, get_mail_sender
from fastapi_all_out.enums import TempCodeTriggers
from .models import UserWithPermissions, BaseTempCode, get_field_param, max_len_of


USER_MODEL = TypeVar("USER_MODEL", bound=UserWithPermissions)
UserModel: Type[UserWithPermissions] = get_user_model()
mail_sender = get_mail_sender()


class TortoiseUserService(BaseUserService[USER_MODEL]):

    def set_password(self, password: Optional[str]) -> None:
        user = self.user
        user.password_change_dt = timezone.now()
        user.password_salt = ''.join(choices(hexdigits, k=max_len_of(UserModel)('password_salt')))
        if password:
            user.password_hash = self.get_password_hash(password)
        else:
            user.password_hash = UNUSED_PASSWORD_PREFIX + self.get_password_hash(''.join(choices(hexdigits, k=30)))

    async def get_or_create_temp_code(self, trigger: TempCodeTriggers) -> tuple[BaseTempCode, bool]:
        await self.user.fetch_related('temp_code')
        temp_code = self.user.temp_code
        created = False
        if temp_code:
            if trigger != temp_code.trigger:
                await temp_code.update(trigger)
                created = True
        else:
            temp_code = await get_field_param(UserModel, 'temp_code', 'related_model') \
                .create(user=self.user, trigger=trigger)
            created = True
        return temp_code, created

    async def update_or_create_temp_code(self, trigger: TempCodeTriggers) -> BaseTempCode:
        temp_code, created = await self.get_or_create_temp_code(trigger)
        if not created:
            await temp_code.update(trigger)
        return temp_code

    async def send_activation_email(self) -> None:
        temp_code = await self.update_or_create_temp_code(trigger=TempCodeTriggers.EmailActivation)
        await mail_sender.activation_email(
            to=self.user.email,
            username=self.user.username,
            uuid=self.user.uuid,
            temp_code=temp_code.code,
            duration=temp_code.DURATION_TEXT,
        )

    async def send_password_reset_email(self) -> None:
        temp_code = await self.update_or_create_temp_code(trigger=TempCodeTriggers.PwdReset)
        await mail_sender.password_reset_email(
            to=self.user.email,
            username=self.user.username,
            uuid=self.user.uuid,
            temp_code=temp_code.code,
            duration=temp_code.DURATION_TEXT,
        )

    def check_temp_code_error(self, code: str, trigger: TempCodeTriggers) -> Literal['expired', 'incorrect'] | None:
        tc = self.user.temp_code
        if tc.expired:
            return 'expired'
        if not tc.correct(code, trigger):
            return 'incorrect'

    async def activate(self) -> None:
        self.user.is_active = True
        await self.user.temp_code.delete()
        await self.user.save(force_update=True, update_fields=['is_active'])
