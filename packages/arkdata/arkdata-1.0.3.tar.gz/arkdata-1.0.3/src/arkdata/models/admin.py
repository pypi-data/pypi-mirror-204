from sqlalchemy import Column, String, DateTime
from arkdata.database.cursor import sqlalchemy
from arkdata.database.table import Table
from arkdata import models
from pathlib import Path
import arkdata
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import bcrypt
import base64
from datetime import datetime


class Admin(sqlalchemy.db.Model, Table):
    xuid = Column(String(100), nullable=False, unique=True)
    nitrado_api_key_digest = Column(String(500), nullable=True)
    subscription_start = Column(DateTime, nullable=False, default=datetime.now())
    subscription_end = Column(DateTime, nullable=False, default=datetime.now())

    @classmethod
    def cipher(cls, password: str) -> Fernet:
        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=None,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(hkdf.derive(password.encode()))
        return Fernet(key)

    @classmethod
    def create_admin(cls, xuid: str, password: str, nitrado_api_key: str = None):
        user = models.User.find_by(xuid=xuid)
        if user is None:
            raise Exception("User does not exist")
        is_password_valid = bcrypt.checkpw(password.encode(), user.password_digest.encode())
        if not is_password_valid:
            raise Exception("User password is invalid")
        if nitrado_api_key is None:
            return cls(xuid=xuid)
        cipher = cls.cipher(password)
        nitrado_api_key_digest = cipher.encrypt(nitrado_api_key.encode()).decode()
        admin = cls(xuid=xuid, nitrado_api_key_digest=nitrado_api_key_digest)
        admin.create()
        return admin

    def __init__(self, xuid=None, nitrado_api_key_digest=None, subscription_start=None, subscription_end=None):
        self.xuid: str = xuid
        self.subscription_start: datetime = subscription_start
        self.subscription_end: datetime = subscription_end
        self.nitrado_api_key_digest: str = nitrado_api_key_digest

    @classmethod
    def seed_table(cls) -> None:
        dir = Path(os.path.dirname(arkdata.__file__))
        path = dir / Path('seeds/admins.json')
        super()._seed_table(path)

    def update_subscription_start(self, month: int, day: int, year: int):
        self(subscription_start=datetime(year=year, month=month, day=day))

    def update_subscription_end(self, month: int, day: int, year: int):
        self(subscription_end=datetime(year=year, month=month, day=day))

    def subscription(self, start: DateTime = None, end: DateTime = None):
        subscription_start = start or self.subscription_start or datetime.now()
        subscription_end = end or self.subscription_end or datetime.now()
        self(subscription_start=subscription_start, subscription_end=subscription_end)

    def change_nitrado_api_key(self, nitrado_api_key: str, password: str):
        if not isinstance(nitrado_api_key, str):
            return
        cipher = self.cipher(password)
        nitrado_api_key_digest = cipher.encrypt(nitrado_api_key.encode()).decode()
        self(nitrado_api_key_digest=nitrado_api_key_digest)

    def nitrado_api_key(self, password):
        cipher = self.cipher(password)
        return cipher.decrypt(self.nitrado_api_key_digest.encode()).decode()
