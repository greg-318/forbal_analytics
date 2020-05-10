from .structure import Structure


class Player(Structure):
    """
    :param player: [str] = Player name and surname # year_player
    :param position: [str] = Position
    :param appearances: [int] = Number of appearances
    :param minutes: [int] = Time spent in the game
    :param goals: [int] = Count of goals
    :param npg: [int] = Not penalty goals
    :param a: [int] = Passes led to goal
    :param sh90: [float] = Shorts per 90 minutes
    :param kp90: [float] = Passes led to short per 90 minutes
    :param xg: [dict] = Expected goals
    :param npxg: [dict] = Not penalty expected Goals
    :param xa: [dict] = The sum of expected goals off shots from a player's key passes
    :param xgchain: [float] = Total xG of every possession the player is involved in
    :param xgbuildup: [float] = Total xG of every possession the player is involved in without key passes and shots
    :param xg90: [float] = Expected goals per 90 minutes
    :param npxg90: [float] = Not penalty expected Goals per 90 minutes
    :param xa90: [float] = Expected assists per 90 minutes
    :param xg90xa90: [float] = Expected goals plus expected assists per 90 minutes
    :param npxg90xa90: [float] = Not penalty expected goals plus expected assists per 90 minutes
    :param xgchain90: [float] = Total xG of every possession the player is involved in per 90 minutes
    :param xgbuildup90: [float] = Total xG of every possession the player is involved in without key passes and shots
    per 90 minutes
    :param yellow: [int] = Yellow cards
    :param red: [int] = Red cards
    :param team: [str] = Team name
    """

    _fields = ["player", "position", "appearances", "minutes", "goals", "npg", "a", "sh90", "kp90", "xg", "npxg", "xa",
               "xgchain", "xgbuildup", "xg90", "npxg90", "xa90", "xg90xa90", "npxg90xa90", "xgchain90", "xgbuildup90",
               "yellow", "red", "team"]
    _type = [str, str, int, int, int, int, int, float, float, dict, dict, dict, float, float, float, float, float,
             float, float, float, float, int, int, str]
