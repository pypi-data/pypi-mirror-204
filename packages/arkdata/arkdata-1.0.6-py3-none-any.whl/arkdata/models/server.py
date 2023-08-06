from arkdata.database.cursor import sqlalchemy
from arkdata.database.table import Table
from sqlalchemy import Column, String, Integer
from arkdata import models


class Server(sqlalchemy.db.Model, Table):
    name = Column(String(100), unique=False, nullable=False, default="UNKNOWN")
    service_id = Column(Integer, unique=False, nullable=True, default=None)
    map = Column(String(100), unique=False, nullable=True, default=None)

    @classmethod
    def server_by_service_id(cls, service_id: int):
        return cls.find_by(service_id=service_id)

    def commands(self) -> list:
        return models.Command.find_all_by(server_id=self.id)

