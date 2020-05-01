import logging
from typing import Any, Union
from pymongo import MongoClient, errors
sys.path.append("D:\Мои документы\Desktop\R&D\Analytics")
from models import player, team, game_indicators

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')


class MongoDefault:
    """
    Examples:

    insert = dict from Player or Team class

    select = {"name": "Jamie Vardy"}

    update = ("name", "Jamie Vardy", "J. V.")

    delete = {"name": "Jamie Vardy"}
    """

    def __init__(self, collection, db="football"):
        """
        :param db: DB name
        :param collection: Collection name [players, teams, gameIndicators]
        """
        self.db = db
        self.collection = collection

    def __enter__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client[self.db]
        self.collection = self.db[self.collection]
        return self

    def insert(self, data: dict, one: int = 1) -> tuple:
        """
        :param data: All data for insert
        :param one: Insert one document
        :return: status result
        """
        if one:
            try:
                status = self.collection.insert_one(data)
            except errors.DuplicateKeyError:
                return "Error", "Key already created"
            else:
                res = status.inserted_id

        else:
            status = self.collection.insert_many(data)
            res = status.inserted_ids
        return status.acknowledged, res

    def select(self, data: dict) -> dict:
        """
        :param data: Data for search in DB
        :return: Cursor object or empty dict if data not found
        """

        result = self.collection.find(data)
        try:
            next(result)
        except StopIteration:
            return {}
        else:
            method = {
                self.collection.name == "players": player.Player(**next(self.collection.find(data))),
                self.collection.name == "teams": team.Team(**next(self.collection.find(data))),
                self.collection.name == "gameIndicators":
                    game_indicators.GameIndicators(**next(self.collection.find(data)))
            }[True]
            return method

    def update(self, key: Union[int, str], value_old: Any, value_new: Any, one: int = 1) -> tuple:
        """
        :param key: Key in document
        :param value_old: Current value in document
        :param value_new: New value in document
        :param one: Update one document
        :return: status code
        """
        old_data = {key: value_old}
        new_data = {"$set": {key: value_new}}
        if one:
            result = self.collection.update_one(old_data, new_data)
            return result.acknowledged, result.modified_count

        else:
            raise NotImplementedError("Not Implemented case")
            # result = self.collection.update_many()

    def delete(self, data: dict, one: int = 1) -> tuple:
        """
        :param data: Data for delete in DB
        :param one: Delete one document
        :return: status code
        """
        if one:
            result = self.collection.delete_one(data)
            return result.acknowledged, result.deleted_count

        else:
            raise NotImplementedError("Not Implemented case")
            # result = self.collection.delete_many(data)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()
        if exc_val:
            raise
