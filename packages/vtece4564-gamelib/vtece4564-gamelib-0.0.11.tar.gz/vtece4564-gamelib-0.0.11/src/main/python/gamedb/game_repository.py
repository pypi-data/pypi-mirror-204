import uuid
from abc import ABC, abstractmethod

from datetime import datetime
from typing import Iterable, Optional


class NoSuchGameError(Exception):
    pass


class Game:

    def __init__(self, creator: str, players: Iterable[str], gid: str = None, creation_date: datetime = None):
        self.creator = creator
        self.players = tuple(players)
        self.gid = gid if gid else str(uuid.uuid4())
        self.creation_date = creation_date if creation_date else datetime.utcnow()


class GameRepository(ABC):

    @abstractmethod
    def create_game(self, creator: str, players: Iterable[str]) -> Game:
        pass

    @abstractmethod
    def delete_game(self, gid: str):
        pass

    @abstractmethod
    def find_game(self, gid: str) -> Optional[Game]:
        pass

    @abstractmethod
    def find_games_for_user(self, uid: str) -> Iterable[Game]:
        pass
