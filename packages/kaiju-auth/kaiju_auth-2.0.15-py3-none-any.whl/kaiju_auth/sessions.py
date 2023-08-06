from kaiju_db.services import DatabaseService, SQLService
from kaiju_tools.rpc.sessions import BaseSessionService
from kaiju_tools.rpc.abc import AbstractRPCCompatible
from kaiju_auth.tables import sessions_table

__all__ = ['SessionService']


class SessionService(BaseSessionService, SQLService, AbstractRPCCompatible):
    """Session store base class."""

    table = sessions_table
    session_key = 'session:{session_id}'
    select_columns_blacklist = {'h_agent'}

    def __init__(self, app, *, database_service: DatabaseService = None, logger=None, **kws):
        """Initialize.

        :param app:
        :param database_service:
        :param cache_service:
        :param session_idle_timeout: (s) Idle life timeout each session.
        :param exp_renew_interval: (s)
        :param salt: set your salt
        :param logger:
        """
        SQLService.__init__(self, app, database_service=database_service, logger=logger)
        BaseSessionService.__init__(self, app, **kws, logger=logger)

    async def _save_session(self, session_data: dict) -> None:
        on_conflict_values = session_data.copy()
        del on_conflict_values['id']
        del on_conflict_values['h_agent']
        del on_conflict_values['created']
        await self.create(
            session_data,
            columns=[],
            on_conflict='do_update',
            on_conflict_keys=['id'],
            on_conflict_values=on_conflict_values,
        )

    async def _update_session_exp(self, session_id, exp) -> None:
        await self.update(session_id, {'expires': exp}, columns=[])

    async def _delete_session(self, session_id) -> None:
        await self.delete(session_id, columns=[])

    async def _get_session(self, session_id) -> dict:
        return await self.get(session_id, columns='*')
