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
    :param team: Team name
    """

    _fields = MappingProxyType({"player": str, "position": str, "appearances": int, "minutes": int, "goals": int,
                                "npg": int, "a": int, "sh90": float, "kp90": float, "xg": float, "npxg": float,
                                "xa": float, "xgchain": float, "xgbuildup": float, "xg90": float, "npxg90": float,
                                "xa90": float, "xg90xa90": float, "npxg90xa90": float, "xgchain90": float,
                                "xgbuildup90": float, "yellow": int, "red": int, "team": str})
