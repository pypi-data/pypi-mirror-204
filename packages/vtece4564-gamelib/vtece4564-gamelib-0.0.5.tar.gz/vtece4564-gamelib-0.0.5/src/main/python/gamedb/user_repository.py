from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict

from gameauth.password import encrypt as encrypt_password


class NoSuchUserError(Exception):
    pass


class DuplicateUserIdError(Exception):
    pass


class User:

    def __init__(self, uid: str, password: str, is_encrypted: bool = False,
                 full_name: str = None, nickname: str = None, creation_date: datetime = None):
        if uid is None or password is None:
            raise ValueError("uid and password are required")
        self.uid = uid
        self.password = password if is_encrypted else encrypt_password(password)
        self.full_name = full_name
        self.nickname = nickname
        self.creation_date = creation_date if creation_date else datetime.utcnow()


class UserRepository(ABC):

    @abstractmethod
    def create_user(self, uid: str, password: str, nickname: str, full_name: str):
        pass

    @abstractmethod
    def delete_user(self, uid: str):
        pass

    @abstractmethod
    def find_user(self, uid: str) -> User:
        pass
