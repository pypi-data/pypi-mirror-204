from arkdata.database.cursor import sqlalchemy
from arkdata.database.table import Table
from sqlalchemy import Column, String, Integer, Boolean
from pathlib import Path
import os
import arkdata


class Command(sqlalchemy.db.Model, Table):
    admin_xuid = Column(String(100), unique=False, nullable=True)
    player_xuid = Column(String(100), unique=False, nullable=True)
    code = Column(String(500), unique=False, nullable=False)
    executed = Column(Boolean, unique=False, nullable=False, default=False)
    service_id = Column(String(100), unique=False, nullable=True, default=None)

    def __init__(
            self,
            admin_xuid: str = None,
            player_xuid: str = None,
            code: str = None,
            executed: bool = False,
            service_id: str = None
    ):
        self.admin_xuid = admin_xuid    # Admin who executed the code
        self.player_xuid = player_xuid  # Player who requested the code
        self.code = code
        self.executed = executed
        self.service_id = service_id

    @classmethod
    def seed_table(cls) -> None:
        dir = Path(os.path.dirname(arkdata.__file__))
        path = dir / Path('seeds/commands.json')
        super()._seed_table(path)

    @classmethod
    def queued_commands(cls, service_id: str) -> list:
        return cls.find_all_by(service_id=service_id, executed=False)

    @classmethod
    def completed_commands(cls, service_id: str) -> list:
        return cls.find_all_by(service_id=service_id, executed=True)

    @classmethod
    def player_commands(cls, xuid: str) -> list:
        return cls.find_all_by(player_xuid=xuid)

