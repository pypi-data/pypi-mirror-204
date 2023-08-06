import logging
from typing import Dict, Iterable, Optional

from pymongo import MongoClient
from pymongo.collection import Collection

from ..game_repository import Game, GameRepository, NoSuchGameError


_GAMES_COLLECTION_NAME = "games"
_ID_KEY = "_id"
_GID_KEY = "gid"
_CREATION_DATE_KEY = "creation_date"
_CREATOR_KEY = "creator"
_PLAYERS_KEY = "players"

logger = logging.getLogger(__name__)


class MongoGame(Game):

    @classmethod
    def from_dict(cls, rec: dict):
        return Game(rec.get(_CREATOR_KEY), rec.get(_PLAYERS_KEY), gid=rec.get(_GID_KEY), creation_date=rec.get(_CREATION_DATE_KEY))

    def to_dict(self) -> Dict:
        return {
            _GID_KEY: self.gid,
            _CREATOR_KEY: self.creator,
            _PLAYERS_KEY: self.players,
            _CREATION_DATE_KEY: self.creation_date,
        }


class MongoGameRepository(GameRepository):

    def __init__(self, mongo: MongoClient):
        self.games: Collection = mongo.get_default_database().get_collection(_GAMES_COLLECTION_NAME)
        self.games.create_index(_GID_KEY, unique=True)

    def create_game(self, creator: str, players: Iterable[str]) -> Game:
        game = MongoGame(creator, players)
        game_doc = game.to_dict()
        logger.debug(f"inserting game: {game_doc}")
        doc_id = self.games.insert_one(game_doc).inserted_id
        game_doc = self.games.find_one({_ID_KEY: doc_id})
        return MongoGame.from_dict(game_doc)

    def delete_game(self, gid: str):
        self.games.delete_one({_GID_KEY: gid})

    def find_game(self, gid: str) -> Optional[Game]:
        game_doc = self.games.find_one({_GID_KEY: gid})
        if not game_doc:
            raise NoSuchGameError(f"game {gid} does not exist")
        return MongoGame.from_dict(game_doc)

    def find_games_for_user(self, uid: str) -> Iterable[Game]:
        return [MongoGame.from_dict(game_doc) for game_doc in self.games.find({_PLAYERS_KEY: uid})]

