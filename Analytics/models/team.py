from .structure import Structure
from types import MappingProxyType


class Player(Structure):
    """
    :param player: Player name and surname # year_player
    :param position: Position
    :param appearances: Number of appearances
    :param minutes: Time spent in the game
    :param goals: Count of goals
    :param npg: Not penalty goals
    :param a: Passes led to goal
    :param sh90: Shorts per 90 minutes
    :param kp90: Passes led to short per 90 minutes
    :param xg: Expected goals
    :param npxg: Not penalty expected Goals
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
    """

    _fields = MappingProxyType({"player": str, "position": str, "appearances": int, "minutes": int, "goals": int,
                                "npg": int, "a": int, "sh90": float, "kp90": float, "xg": float, "npxg": float,
                                "xa": float, "xgchain": float, "xgbuildup": float, "xg90": float, "npxg90": float,
                                "xa90": float, "xg90xa90": float, "npxg90xa90": float, "xgchain90": float,
                                "xgbuildup90": float, "yellow": int, "red": int})
    _collection = MappingProxyType({"name": "players", "key": "player"})


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
    :param players: List of players
    """

    _fields = MappingProxyType({"name": str, "gp": int, "w": int, "d": int, "l": int, "gf": int, "ga": int, "gd": int,
                                "pts": int, "ppg": float, "last8": float, "cs": float, "fts": float, "xg": float,
                                "npxg": float, "xga": float, "npxga": float, "npxgd": float, "ppda": float,
                                "oppda": float, "dc": int, "odc": int, "xpts": float, "players": list})
    _collection = MappingProxyType({"name": "teams", "key": "name"})

    def dict(self):
        if not self.players:
            raise AttributeError("Team model haven't list of players")
        return super().dict()
