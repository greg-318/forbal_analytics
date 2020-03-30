from pymongo import MongoClient
import logging


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')


class MongoDefault:
    """
    Examples:

    insert = ("Jamie Vardy", "F", 26, 2224, 19, 4, 2.39, 0.65, {"value": 14.24, "dynamic": "-4.76"},
                  {"value": 3.42, "dynamic": "-0.58"}, 0.58, 0.14, "Leicester")

    find = {"name": "Jamie Vardy"}

    update = ("name", "Jamie Vardy", "J. V.")

    delete = {"name": "Jamie Vardy"}
    """

    def __init__(self, db="football", collection="players"):
        """
        :param db: DB name
        :param collection: Collection name
        """
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client[db]
        self.collection = self.db[collection]

    def insert_player(self, name: str, position: str, appearances: int, minutes_played: int, goals: int,
                      passes_ltg: int, sh90: float, kp90: float, xg: dict, xa: dict, xg90: float, xa90: float,
                      team: str, one=1):
        """
        :param name: Player name and surname
        :param position: Position
        :param appearances: Number of appearances
        :param minutes_played: Time spent in the game
        :param goals: Count of goals
        :param passes_ltg: Passes led to goal
        :param sh90: Shorts per 90 minutes
        :param kp90: Passes led to short per 90 minutes
        :param xg: Expected goals
        :param xa: The sum of expected Goals off shots from a player's key passes
        :param xg90: Expected goals per 90 minutes
        :param xa90: Expected assists per 90 minutes
        :param team: Team name
        :param one: Insert one document
        :return: status result
        """
        data = {
            "name": name,
            "position": position,
            "appearances": appearances,
            "minutes_played": minutes_played,
            "goals": goals,
            "passes_ltg": passes_ltg,
            "sh90": sh90,
            "kp90": kp90,
            "xg": xg,
            "xa": xa,
            "xg90": xg90,
            "xa90": xa90,
            "team": team
        }
        if one:
            status = self.collection.insert_one(data)
            res = status.inserted_id
        else:
            status = self.collection.insert_many(data)
            res = status.inserted_ids
        return status.acknowledged, res

    def find_player(self, data: dict):
        """
        :param data: Data for search in DB
        :return: Cursor object or False if data not found
        """
        result = self.collection.find(data)
        try:
            next(result)
        except StopIteration:
            return False
        else:
            return self.collection.find(data)

    def update_player(self, key, value_old, value_new, one=1):
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
            logging.warning("Method don't work")
            return False
            # result = self.collection.update_many()

    def delete_player(self, data: dict, one=1):
        """
        :param data: Data for delete in DB
        :param one: Delete one document
        :return:
        """
        if one:
            result = self.collection.delete_one(data)
            return result.acknowledged, result.deleted_count
        else:
            logging.warning("Method don't work")
            return False
            # result = self.collection.delete_many(data)
