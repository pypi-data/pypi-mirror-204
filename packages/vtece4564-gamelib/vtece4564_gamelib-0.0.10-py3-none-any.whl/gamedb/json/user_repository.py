import logging
from datetime import datetime
from typing import Dict


from ..user_repository import User, UserRepository, NoSuchUserError, DuplicateUserIdError
from .json_db import JsonDatabase


_UID_KEY = "uid"
_CREATION_DATE_KEY = "creation_date"
_FULL_NAME_KEY = "full_name"
_NICKNAME_KEY = "nickname"
_PASSWORD_KEY = "password"

logger = logging.getLogger(__name__)


class JsonUser(User):

    @classmethod
    def from_dict(cls, rec: dict):
        record = User(uid=rec.get(_UID_KEY),
                      password=rec.get(_PASSWORD_KEY),
                      is_encrypted=True,
                      creation_date=datetime.fromisoformat(rec.get(_CREATION_DATE_KEY)))
        record.nickname = rec.get(_NICKNAME_KEY)
        record.full_name = rec.get(_FULL_NAME_KEY)
        return record

    def to_dict(self) -> Dict:
        record = {
            _UID_KEY: self.uid,
            _PASSWORD_KEY: self.password,
            _CREATION_DATE_KEY: self.creation_date.astimezone().isoformat(),
        }
        if self.full_name:
            record.update({_FULL_NAME_KEY: self.full_name})
        if self.nickname:
            record.update({_NICKNAME_KEY: self.nickname})
        return record


class JsonUserRepository(UserRepository):

    def __init__(self, db: JsonDatabase):
        self.db = db

    def create_user(self, uid: str, password: str, nickname: str = None, full_name: str = None):
        user = JsonUser(uid, password, is_encrypted=False, nickname=nickname, full_name=full_name)
        user_doc = user.to_dict()
        logger.debug(f"inserting user: {user_doc}")

        def do_create(users):
            if uid in users:
                raise DuplicateUserIdError(f"user with ID {user.uid} already exists")
            users[uid] = user_doc

        self.db.with_users(do_create)
        return user

    def delete_user(self, uid: str):
        def do_delete(users):
            if uid in users:
                del users[uid]

        self.db.with_users(do_delete)

    def find_user(self, uid: str) -> User:
        def do_find(users):
            if uid not in users:
                raise NoSuchUserError(f"user ID {uid} not found")
            user_doc = users[uid]
            return JsonUser.from_dict(user_doc)

        return self.db.with_users(do_find)