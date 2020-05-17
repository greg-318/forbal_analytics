from structure import Structure
from types import MappingProxyType


class Team(Structure):
    """
    :param name: Team name # year_name
    :param gp: Count of matches
    :param w: Wins
    :param d: Draws
    :param l: Loses
    :param gf: Goals for
    :param ga: Goals againist
    :param gd: Goal difference
    :param pts: Points
    :param ppg: Points per game
    :param last8: Points per game in the last 8 matches
    :param cs: % clean sheets (matches with no goal conceded)
    :param fts: % failed to score (matches with no goal scored)
    :param xg: Expected goals for
    :param npxg: Expected goals for without penalties and own goals
    :param xga: Expected goals againist
    :param npxga: Expected goals againist without penalties and own goals
    :param npxgd: The difference between "for" and "against" expected goals without penalties and own goals
    :param ppda: Passes allowed per defensive action in the opposition half
    :param oppda: Opponent passes allowed per defensive action in the opposition half
    :param dc: Passes completed within an estimated 20 yards of goal (crosses excluded)
    :param odc: Opponent passes completed within an estimated 20 yards of goal (crosses excluded)
    :param xpts: Expected points
    """

    _fields = MappingProxyType({"name": str, "gp": int, "w": int, "d": int, "l": int, "gf": int, "ga": int, "gd": int,
                                "pts": int, "ppg": float, "last8": float, "cs": float, "fts": float, "xg": float,
                                "npxg": float, "xga": float, "npxga": float, "npxgd": float, "ppda": float,
                                "oppda": float, "dc": int, "odc": int, "xpts": float})
    _collection = MappingProxyType({"name": "teams", "key": "name"})
