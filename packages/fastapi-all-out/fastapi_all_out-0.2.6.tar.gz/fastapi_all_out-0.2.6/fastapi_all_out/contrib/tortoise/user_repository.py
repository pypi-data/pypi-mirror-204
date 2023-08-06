from typing import Type, Any

from fastapi_all_out.lazy import get_user_model, get_user_service
from .repository import TortoiseRepository
from .user_service import USER_MODEL
from ...routers.base_repository import ModelPrefix

UserService = get_user_service()


class TortoiseUserRepository(TortoiseRepository[USER_MODEL]):
    model = get_user_model()

    pass_check_required: dict[str, set[str]] = {'': {'password_hash', 'password_change_dt', 'password_salt'}}

    async def handle_create_(
            self,
            model: Type["USER_MODEL"],
            data: dict[str, Any],
            exclude: set[str],
            prefix: ModelPrefix,
            defaults: dict[str, Any] = None,
            commit: bool = True,
    ) -> USER_MODEL:
        password = data.pop('password')
        user = await self._handle_create_default(
            model=model,
            data=data,
            exclude=exclude,
            prefix=prefix,
            defaults=defaults,
            commit=False,
        )
        UserService(user).set_password(password)
        if commit:
            await user.save(force_create=True)
        return user
