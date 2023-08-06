import uuid
from base64 import b64decode
from binascii import Error as B64Error
from enum import Enum
from typing import TypedDict, Tuple, final, cast

from kaiju_tools.exceptions import NotAuthorized, MethodNotAllowed
from kaiju_tools.services import Service, Session
from kaiju_tools.rpc import AbstractRPCCompatible
from kaiju_tools.rpc.context import REQUEST_CONTEXT, REQUEST_SESSION

from kaiju_auth.tokens import JWTService
from kaiju_auth.users import UserService
from kaiju_auth.sessions import SessionService

__all__ = ['AuthType', 'AuthService', 'TokenInfo']


class TokenInfo(TypedDict):
    """JWT methods output."""

    access: str
    refresh: str


class UserType(TypedDict):
    """User data."""

    id: uuid.UUID
    permissions: frozenset


@final
class AuthType(Enum):
    """Client authentication types."""

    PASSWORD = 'PASSWORD'  #: login-password auth
    TOKEN = 'TOKEN'  #: token based auth
    BASIC = 'BASIC'  #: basic auth


class AuthService(Service, AbstractRPCCompatible):
    """Authentication services."""

    service_name = 'auth'

    def __init__(
        self,
        app,
        *,
        user_service: UserService = None,
        token_service: JWTService = None,
        session_service: SessionService = None,
        enable_basic_auth: bool = False,
        enable_token_auth: bool = True,
        logger=None,
    ):
        """Initialize.

        :param app:
        :param enable_basic_auth:
        :param enable_token_auth:
        :param logger:
        """
        super().__init__(app, logger=logger)
        self.enable_basic_auth = enable_basic_auth
        self.enable_token_auth = enable_token_auth
        self._users: UserService = self.discover_service(user_service, cls=UserService)
        self._tokens: JWTService = self.discover_service(token_service, cls=JWTService, required=False)
        self._sessions: SessionService = self.discover_service(session_service, cls=SessionService)

    @property
    def routes(self) -> dict:
        return {
            'login': self.password_auth,
            'jwt.get': self.get_token,
            'jwt.refresh': self.refresh_token,
            'logout': self.logout,
        }

    @property
    def permissions(self) -> dict:
        return {
            'login': self.PermissionKeys.GLOBAL_GUEST_PERMISSION,
            'logout': self.PermissionKeys.GLOBAL_USER_PERMISSION,
            'jwt.get': self.PermissionKeys.GLOBAL_GUEST_PERMISSION,
            'jwt.refresh': self.PermissionKeys.GLOBAL_GUEST_PERMISSION,
        }

    async def auth_from_auth_string(self, auth_string: str) -> Session:
        """Authenticate user from auth header or string."""
        if auth_string.startswith('Bearer '):
            return await self.token_auth(auth_string.replace('Bearer ', '', 1))
        elif auth_string.startswith('Basic '):
            return await self.basic_auth(auth_string.replace('Basic ', '', 1))
        else:
            raise NotAuthorized('Unsupported authentication type.')

    async def basic_auth(self, auth_string: str) -> Session:
        """Try basic auth.

        Supports both plain '<user>:<password>' strings and b64 encoded (preferred).

        :raises AuthenticationFailed:
        """
        username, password = self._parse_auth_str(auth_string)
        user = await self._users.auth(username=username, password=password, columns=None)
        session = self._sessions.get_new_session({})
        self._update_session(session, user, AuthType.BASIC)
        self.logger.info('login completed', auth_type=AuthType.BASIC.value, user_id=user['id'])
        return session

    @staticmethod
    def _parse_auth_str(auth_str: str) -> Tuple[str, str]:
        """Parse basic auth string (both b64 and not b64 encoded)."""
        if ':' not in auth_str:
            try:
                auth_str = b64decode(auth_str).decode('utf-8')
            except (B64Error, UnicodeDecodeError):
                raise NotAuthorized('Invalid credentials.')
            if ':' not in auth_str:
                raise NotAuthorized('Invalid credentials.')
        login, password = auth_str.split(':')
        return login, password

    async def password_auth(self, username: str, password: str) -> Session:
        """Authenticate a user by directly providing a login / password.

        :raises AuthenticationFailed:
        """
        ctx = REQUEST_CONTEXT.get()
        if not ctx:
            raise NotImplementedError('Not implemented for non-context calls.')
        session = REQUEST_SESSION.get()
        if session and session.user_id:
            await self.logout()
        user = await self._users.auth(username=username, password=password, columns=None)
        new_session = self._sessions.get_new_session({}, user_agent=session.h_agent if session else '')
        self._update_session(new_session, user, AuthType.PASSWORD)
        ctx['session_id'] = new_session.id
        REQUEST_SESSION.set(new_session)
        self.logger.info('login completed', auth_type=AuthType.PASSWORD.value, user_id=user['id'])
        return new_session

    async def get_token(self, username: str, password: str) -> TokenInfo:
        """Authenticate and get a new token pair."""
        if not self._tokens or not self.enable_token_auth:
            raise MethodNotAllowed('Token auth is disabled.')
        user = await self._users.auth(username=username, password=password, columns=None)
        session = self._sessions.get_new_session({})
        self._update_session(session, user, AuthType.TOKEN)
        access, refresh = await self._tokens.generate_token_pair(
            data={'permissions': session.permissions, 'id': session.user_id}
        )
        return TokenInfo(access=access.serialize(), refresh=refresh.serialize())

    async def refresh_token(self, access: str, refresh: str) -> TokenInfo:  # noqa
        """Refresh token pair."""
        if not self._tokens or not self.enable_token_auth:
            raise MethodNotAllowed('Token auth is disabled.')
        access, refresh = await self._tokens.refresh_token(refresh)
        return TokenInfo(access=access.serialize(), refresh=refresh.serialize())

    async def logout(self) -> None:
        ctx = self.get_request_context()
        if not ctx:
            raise NotImplementedError('Not implemented for non-context calls.')
        session = self.get_session()
        if session:
            session = cast(Session, session)
            if session.loaded:
                await self._sessions.delete_session(session)
            self.logger.info('logged out', user_id=session.user_id)
            new_session = self._sessions.get_new_session({}, user_agent=session.h_agent)
            ctx['session_id'] = new_session.id
            REQUEST_SESSION.set(new_session)

    async def token_auth(self, token: str) -> Session:
        """Try token auth (JWT or similar).

        :raises AuthenticationFailed:
        """
        token = await self._tokens.verify_token(token)
        user: UserType = token.claims_data['data']
        session = self._sessions.get_new_session({})
        self._update_session(session, user, AuthType.TOKEN)
        self.logger.info('login completed', auth_type=AuthType.TOKEN.value, user_id=user['id'])
        return session

    @staticmethod
    def _update_session(session: Session, user: UserType, auth_type: AuthType) -> None:
        """Store user data in a provided session."""
        if session and user:
            session.user_id = user['id']
            session.permissions = user['permissions']
            session._changed = True
            session._stored = auth_type == AuthType.PASSWORD
