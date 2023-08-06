from typing import Callable, Coroutine, Any

from fastapi import APIRouter, Request, BackgroundTasks, Response, Body, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from fastapi_all_out.lazy import get_schema, get_user_model, get_user_repository, get_user_service, get_codes,\
    get_settings_obj
from fastapi_all_out.routers.exceptions import ItemNotFound
from fastapi_all_out.schemas import LoginPasswordSchema, UserMeRead
from ..base import AuthBackend, BaseUser, SimpleUser, UnauthenticatedUser
from .schemas import JWTTokenUser
from .strategy import JWTAuthStrategy


LoginPasswordSchema = get_schema(LoginPasswordSchema)
UserMeRead = get_schema(UserMeRead)
JWTTokenUser = get_schema(JWTTokenUser)
UserModel = get_user_model()
UserRepository = get_user_repository()
UserService = get_user_service()
Codes = get_codes()
settings = get_settings_obj()
oauth2_default = OAuth2PasswordBearer(
    tokenUrl=settings.API_PREFIX + '/auth/jwt/login',
    scheme_name='Bearer',
    auto_error=False,
)


class JWTAuthBackend(AuthBackend):

    strategy: "JWTAuthStrategy"
    oauth: OAuth2PasswordBearer
    _authenticate: Callable[[], Coroutine[Any, Any, None]]
    _auth_required: Callable[[], Coroutine[Any, Any, None]]

    def __init__(self, strategy: "JWTAuthStrategy", oauth: OAuth2PasswordBearer = oauth2_default):
        assert isinstance(strategy, JWTAuthStrategy)
        self.strategy = strategy
        self.oauth = oauth

    def authorize(self, user: BaseUser) -> Any:
        return self.strategy.authorize(user)

    def authenticate(self) -> Callable[[], Coroutine[Any, Any, None]]:
        if not hasattr(self, '_authenticate'):
            oauth_schema = self.oauth
            authenticate_handler = self.strategy.authenticate

            async def wrapper(request: Request, token: str = Depends(oauth_schema)) -> None:
                token_data = await authenticate_handler(token)
                if token_data is None:
                    request.scope['auth'] = None
                    request.scope['user'] = UnauthenticatedUser()
                else:
                    user = token_data.user
                    request.scope['auth'] = token_data
                    request.scope['user'] = SimpleUser(pk=user.get_pk(), username=user.username)

            self._authenticate = wrapper

        return self._authenticate

    def auth_required(self) -> Callable[[], Coroutine[Any, Any, None]]:
        if not hasattr(self, '_auth_required'):
            async def wrapper(request: Request) -> None:
                user: BaseUser = request.user
                if not user.is_authenticated:
                    raise Codes.not_authenticated.err()

            self._auth_required = wrapper
        return self._auth_required

    def with_permissions(self, *permissions: tuple[str, str]) -> Callable[[], Coroutine[Any, Any, None]]:
        async def wrapper(
                request: Request,
                background_tasks: BackgroundTasks,
                response: Response,
        ) -> None:
            user: BaseUser = request.user
            if not user.is_authenticated:
                raise Codes.not_authenticated.err()
            if user.is_simple:
                user: SimpleUser
                try:
                    user_db = await UserRepository(
                        request=request, background_tasks=background_tasks, response=response
                    ).get_one(user.pk)
                    request.scope['user'] = user = user_db
                except ItemNotFound:
                    raise Codes.not_authenticated.err()

            if not (user.is_superuser or user.has_permissions(*permissions)):
                raise Codes.permission_denied.err()

        return wrapper

    def create_router(self, add_refresh_route: bool = True, **kwargs) -> APIRouter:
        router = super().create_router(**kwargs)
        if add_refresh_route:
            self.add_refresh_route(router)
        return router

    def login_responses(self):
        return Codes.responses(Codes.not_authenticated)

    def add_login_route(self, router: APIRouter) -> None:
        @router.post(
            '/login', response_model=self.strategy.authorize_response_model,
            responses=self.login_responses()
        )
        async def login(
                request: Request,
                background_tasks: BackgroundTasks,
                response: Response,
                form: OAuth2PasswordRequestForm = Depends(),
        ):
            login_password = LoginPasswordSchema(login=form.username, password=form.password)
            field, value = login_password.get_auth_field_and_value()
            try:
                user = await UserRepository(request=request, background_tasks=background_tasks, response=response)\
                    .get_one(value, field_name=field)
            except ItemNotFound:
                raise Codes.not_authenticated.err()

            user_service = UserService(user)
            if not user_service.verify_password(password=login_password.password):
                raise Codes.not_authenticated.err()

            if not user_service.can_login():
                await user_service.if_cant_login(request=request, background_tasks=background_tasks, response=response)
                raise Codes.not_authenticated.err()
            return self.strategy.authorize(user)

    def add_logout_route(self, router: APIRouter) -> None:
        pass

    def refresh_responses(self):
        return Codes.responses(Codes.not_authenticated)

    def add_refresh_route(self, router: APIRouter) -> None:
        @router.post(
            '/refresh', response_model=self.strategy.authorize_response_model,
            responses=self.refresh_responses()
        )
        async def refresh(
                request: Request,
                background_tasks: BackgroundTasks,
                response: Response,
                token: str = Body(..., alias='refreshToken')
        ):
            token = self.strategy.get_refresh_token(token)
            try:
                user = await UserRepository(request=request, background_tasks=background_tasks, response=response)\
                    .get_one(token.user.id)
            except ItemNotFound:
                raise Codes.not_authenticated.err()
            if UserService(user).token_expired(token.iat):
                raise Codes.not_authenticated.err()
            return self.strategy.authorize(user)
