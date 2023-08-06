import asyncio
import uuid
from random import random
from typing import TypedDict, Optional

import jwt  # noqa pycharm?
from aiohttp import web, WSMsgType  # noqa pycharm?

from kaiju_tools.rpc.etc import JSONRPCHeaders
from kaiju_tools.rpc.services import JSONRPCServer
from kaiju_tools.rpc.client import RPCClientService as BaseRPCClientService

from kaiju_auth.login import AuthService, TokenInfo
from kaiju_auth.sessions import SessionService

__all__ = ['auth_middleware', 'RPCClientService']


class _TokenInfo(TypedDict):
    token: str
    iat: int
    exp: int
    user_id: Optional[uuid.UUID]


class RPCClientService(BaseRPCClientService):
    """RPC client with token authentication and refresh."""

    dt = 60.0  #: interval between a new refresh request and access expiration
    retry_interval = 5.0  #: retries between unsuccessful refresh requests

    def __init__(
        self, *args, username: str = None, password: str = None, auth_service_name=AuthService.service_name, **kws
    ):
        """Initialize."""
        super().__init__(*args, **kws)
        self._auth_service_name = auth_service_name
        self._username = username
        self._password = password
        self._access: Optional[_TokenInfo] = None
        self._refresh: Optional[_TokenInfo] = None
        self._refresh_task: Optional[asyncio.Task] = None

    async def init(self):
        """Initialize."""
        await super().init()
        if self._username and self._password:
            await self._get_tokens()

    async def close(self):
        """Close refresh tasks."""
        if self._refresh_task:
            self._refresh_task.cancel()
            self._refresh_task = None
        await super().close()

    async def _get_tokens(self):
        """Get access and refresh tokens."""
        while 1:
            try:
                tokens: TokenInfo = await self.call(
                    f'{self._auth_service_name}.jwt.get', dict(username=self._username, password=self._password)
                )
            except Exception as exc:
                self.logger.error('Token refresh error', exc_info=exc)
                await asyncio.sleep(self.retry_interval + 1.0 * random())
            else:
                break
        self._set_token_info(tokens['access'], tokens['refresh'])
        self._schedule_next_token_refresh()

    async def _refresh_tokens(self):
        """Refresh existing tokens."""
        while 1:
            try:
                tokens: TokenInfo = await self.call(
                    f'{self._auth_service_name}.jwt.refresh',
                    dict(access=self._access['token'], refresh=self._refresh['token']),
                )
            except Exception as exc:
                self.logger.error('Token refresh error: %s', exc, exc_info=exc)
                await asyncio.sleep(self.retry_interval + 1.0 * random())
            else:
                break
        self._set_token_info(tokens['access'], tokens['refresh'])
        self._schedule_next_token_refresh()

    def _set_token_info(self, access: str, refresh: str) -> None:
        """Extract token information."""
        data = jwt.decode(access, options={'verify_signature': False})
        self._access = _TokenInfo(token=access, iat=data['iat'], exp=data['exp'], user_id=data['data'].get('id'))
        data = jwt.decode(refresh, options={'verify_signature': False})
        self._refresh = _TokenInfo(token=refresh, iat=data['iat'], exp=data['exp'], user_id=data['data'].get('id'))

    def _schedule_next_token_refresh(self):
        dt = max(1.0, self._access['exp'] - self._access['iat'] - self.dt)
        self._refresh_task = asyncio.create_task(self._refresh_after(dt))

    async def _refresh_after(self, dt: float):
        """Call refresh task later."""
        await asyncio.sleep(dt)
        await self._refresh_tokens()

    def _create_request_headers(self, *args, **kws) -> dict:
        headers = super()._create_request_headers(*args, **kws)
        if self._access:
            headers[JSONRPCHeaders.AUTHORIZATION] = f'Bearer {self._access["token"]}'
        return headers


@web.middleware
async def auth_middleware(request: web.Request, handler):
    """Authenticate a user / init session context."""
    app = request.app
    headers = request.headers
    session_service: SessionService = app.services[SessionService.service_name]  # noqa
    auth_service: AuthService = app.services[AuthService.service_name]  # noqa
    rpc: JSONRPCServer = app.services[JSONRPCServer.service_name]  # noqa
    session_cookie_key = '{env}-{app}-session'.format(env=app['env'], app=app['name'])
    user_agent = headers.get('User-Agent')
    cookie_session = False
    session, session_id = None, None
    auth_str = headers.get(JSONRPCHeaders.AUTHORIZATION)
    if auth_str:
        session = await auth_service.auth_from_auth_string(auth_str)
    elif JSONRPCHeaders.SESSION_ID_HEADER in headers:
        session_id = headers[JSONRPCHeaders.SESSION_ID_HEADER]
        session = await session_service.load_session(session_id, user_agent=user_agent)
    else:
        cookie_session = True
        session_id = request.cookies.get(session_cookie_key)
        if session_id:
            session = await session_service.load_session(session_id, user_agent=user_agent)
    if not session:
        session = session_service.get_new_session({}, user_agent=user_agent)

    request['session'] = session

    response = await handler(request)

    if cookie_session:
        new_session_id = response.headers.get(JSONRPCHeaders.SESSION_ID_HEADER, '')
        if session_id != new_session_id:
            response.set_cookie(session_cookie_key, new_session_id, secure=not request.app.debug, httponly=True)  # noqa
        if new_session_id:
            del response.headers[JSONRPCHeaders.SESSION_ID_HEADER]

    return response
