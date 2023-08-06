from sqlalchemy import Column, String, Boolean
from arkdata.database.cursor import sqlalchemy
from arkdata.database.table import Table
from secrets import token_urlsafe
from pathlib import Path
import arkdata
import os


class Session(sqlalchemy.db.Model, Table):
    xuid = Column(String(100), nullable=False, unique=True)
    session_token = Column(String(100), default=token_urlsafe)
    security_token = Column(String(100), default=token_urlsafe)
    api_token = Column(String(100), default=token_urlsafe)
    nitrado_code = Column(String(200), default=token_urlsafe)
    nitrado_state = Column(String(200), default=token_urlsafe)
    authenticated = Column(Boolean, default=False)

    def __init__(
            self,
            xuid=None,
            session_token=None,
            security_token=None,
            api_token=None,
            authenticated=False,
            nitrado_code=None,
            nitrado_state=None
    ):
        self.xuid = xuid
        self.session_token = session_token
        self.security_token = security_token
        self.api_token = api_token
        self.authenticated = authenticated
        self.nitrado_code = nitrado_code
        self.nitrado_state = nitrado_state

    @classmethod
    def seed_table(cls):
        dir = Path(os.path.dirname(arkdata.__file__))
        path = dir / Path('seeds/sessions.json')
        super()._seed_table(path)

    def logout(self) -> None:
        with sqlalchemy.app_context():
            self.session_token = token_urlsafe(64)
            sqlalchemy.db.session.commit()

    def new_session_token(self):
        self(session_token=token_urlsafe(64))
        return self.session_token

    def new_security_token(self):
        self(session_token=token_urlsafe(64))
        return self.security_token
        # TODO: Send token to xbox account

    def new_api_token(self):
        self(session_token=token_urlsafe(64))
        return self.api_token

    def new_nitrado_state(self):
        self(nitrado_state=token_urlsafe(64))
        return self.nitrado_state

