from pymongo import MongoClient, errors
import logging


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')


class MongoDefault:
    """
    Examples:

    insert_player = ("Jamie Vardy", '2019', "F", 26, 2224, 19, 4, 5, 2.39, 0.65, {"value": 14.24, "dynamic": "-4.76"},
    {"value": 3.42, "dynamic": "-0.58"}, 0.58, 0.14, 2.14, 0.44, 1.14, 0.15, 0.4, 0.13, 0.18, 2, 5, "Leicester")

    insert_team = ("Leicester", '2019', 26, 2224, 19, 4, 5, 6, "+23", 3, [{"FC Barcelona": 2, "Levante": 1}, ...],
    0.58, 0.14, "+3", "-2", {"value": 14.24, "dynamic": "-4.76"}, 0.14, {"value": 3.42, "dynamic": "-0.58"},
    0.58, "-34", 2.14, 0.44, 19, 4, {"value": 14.24, "dynamic": "-4.76"})

    find = {"name": "Jamie Vardy"}

    update = ("name", "Jamie Vardy", "J. V.")

    delete = {"name": "Jamie Vardy"}
    """

    def __init__(self, collection, db="football"):
        """
        :param db: DB name
        :param collection: Collection name [players, teams]
        """
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client[db]
        self.collection = self.db[collection]

    def insert_player(self, player: str, year: str, position: str, appearances: int, minutes: int, goals: int, npg: int,
                      a: int, sh90: float, kp90: float, xg: dict, xa: dict, xgchain: float, xgbuildup: float,
                      xg90: float, npxg90: float, xa90: float, xg90xa90: float, npxg90xa90: float, xgchain90: float,
                      xgbuildup90: float, yellow: int, red: int, team: str, one=1):
        """
        :param player: Player name and surname
        :param year: Year data
        :param position: Position
        :param appearances: Number of appearances
        :param minutes: Time spent in the game
        :param goals: Count of goals
        :param npg: Not penalty goals
        :param a: Passes led to goal
        :param sh90: Shorts per 90 minutes
        :param kp90: Passes led to short per 90 minutes
        :param xg: Expected goals
        :param xa: The sum of expected goals off shots from a player's key passes
        :param xgchain: Total xG of every possession the player is involved in
        :param xgbuildup: Total xG of every possession the player is involved in without key passes and shots
        :param xg90: Expected goals per 90 minutes
        :param npxg90: Not penalty expected Goals per 90 minutes
        :param xa90: Expected assists per 90 minutes
        :param xg90xa90: Expected goals plus expected assists per 90 minutes
        :param npxg90xa90: Not penalty expected goals plus expected assists per 90 minutes
        :param xgchain90: Total xG of every possession the player is involved in per 90 minutes
        :param xgbuildup90: Total xG of every possession the player is involved in without key passes and shots per 90
        minutes
        :param yellow: Yellow cards
        :param red: Red cards
        :param team: Team name
        :param one: Insert one document
        :return: status result
        """
        data = {
            "player": year+"_"+player,
            "position": position,
            "appearances": appearances,
            "minutes": minutes,
            "goals": goals,
            "npg": npg,
            "a": a,
            "sh90": sh90,
            "kp90": kp90,
            "xg": xg,
            "xa": xa,
            "xgchain": xgchain,
            "xgbuildup": xgbuildup,
            "xg90": xg90,
            "npxg90": npxg90,
            "xa90": xa90,
            "xg90xa90": xg90xa90,
            "npxg90xa90": npxg90xa90,
            "xgchain90": xgchain90,
            "xgbuildup90": xgbuildup90,
            "yellow": yellow,
            "red": red,
            "team": team
        }
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

    def insert_team(self, name: str, year: str, gp: int, w: int, d: int, l: int, gf: int, ga: int, gd: str, pts: int,
                    form: list, ppg: float, last8: float, cs: str, fts: str, xg: dict, npgx: float, xga: dict,
                    npxga: float, npxgd: str, ppda: float, oppda: float, dc: int, odc: int, xpts: dict, one=1):
        """
        :param name: Team name
        :param year: Year data
        :param gp: Count of matches
        :param w: Wins
        :param d: Draws
        :param l: Loses
        :param gf: Goals for
        :param ga: Goals againist
        :param gd: Goal difference
        :param pts: Points
        :param form: Last 6 results # [{"FC Barcelona": 2, "Levante": 1}, ...]
        :param ppg: Points per game
        :param last8: Points per game in the last 8 matches
        :param cs: % clean sheets (matches with no goal conceded)
        :param fts: % failed to score (matches with no goal scored)
        :param xg: Expected goals for
        :param npgx: Expected goals for without penalties and own goals
        :param xga: Expected goals againist
        :param npxga: Expected goals againist without penalties and own goals
        :param npxgd: The difference between "for" and "against" expected goals without penalties and own goals
        :param ppda: Passes allowed per defensive action in the opposition half
        :param oppda: Opponent passes allowed per defensive action in the opposition half
        :param dc: Passes completed within an estimated 20 yards of goal (crosses excluded)
        :param odc: Opponent passes completed within an estimated 20 yards of goal (crosses excluded)
        :param xpts: Expected points
        :param one: Insert one document
        :return: status result
        """

        data = {
            "name": year+"_"+name,
            "gp": gp,
            "wins": w,
            "draws": d,
            "loses": l,
            "gf": gf,
            "ga": ga,
            "gd": gd,
            "points": pts,
            "form": form,
            "ppg": ppg,
            "last8": last8,
            "cs": cs,
            "fts": fts,
            "xg": xg,
            "npgx": npgx,
            "xga": xga,
            "npxga": npxga,
            "npxgd": npxgd,
            "ppda": ppda,
            "oppda": oppda,
            "dc": dc,
            "odc": odc,
            "xpts": xpts
        }

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

    def find_db(self, data: dict):
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

    def update_db(self, key, value_old, value_new, one=1):
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

    def delete_db(self, data: dict, one=1):
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

