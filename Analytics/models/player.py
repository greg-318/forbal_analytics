class Player:
    """
    :param player: [str] = Player name and surname
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

    def __init__(self, **kwargs):

        self.player = kwargs.get("player", "")  # year_player
        self.position = kwargs.get("position", "")
        self.appearances = kwargs.get("appearances", 0)
        self.minutes = kwargs.get("minutes", 0)
        self.goals = kwargs.get("goals", 0)
        self.npg = kwargs.get("npg", 0)
        self.a = kwargs.get("a", 0)
        self.sh90 = kwargs.get("sh90", 0.0)
        self.kp90 = kwargs.get("kp90", 0.0)
        self.xg = kwargs.get("xg", {})
        self.npxg = kwargs.get("npxg", {})
        self.xa = kwargs.get("xa", {})
        self.xgchain = kwargs.get("xgchain", 0.0)
        self.xgbuildup = kwargs.get("xgbuildup", 0.0)
        self.xg90 = kwargs.get("xg90", 0.0)
        self.npxg90 = kwargs.get("npxg90", 0.0)
        self.xa90 = kwargs.get("xa90", 0.0)
        self.xg90xa90 = kwargs.get("xg90xa90", 0.0)
        self.npxg90xa90 = kwargs.get("npxg90xa90", 0.0)
        self.xgchain90 = kwargs.get("xgchain90", 0.0)
        self.xgbuildup90 = kwargs.get("xgbuildup90", 0.0)
        self.yellow = kwargs.get("yellow", 0)
        self.red = kwargs.get("red", 0)
        self.team = kwargs.get("team", "")

    def dict(self):
        """
        :return: All data for player
        """
        data = {
            "player": self.player,
            "position": self.position,
            "appearances": self.appearances,
            "minutes": self.minutes,
            "goals": self.goals,
            "npg": self.npg,
            "a": self.a,
            "sh90": self.sh90,
            "kp90": self.kp90,
            "xg": self.xg,
            "npxg": self.npxg,
            "xa": self.xa,
            "xgchain": self.xgchain,
            "xgbuildup": self.xgbuildup,
            "xg90": self.xg90,
            "npxg90": self.npxg90,
            "xa90": self.xa90,
            "xg90xa90": self.xg90xa90,
            "npxg90xa90": self.npxg90xa90,
            "xgchain90": self.xgchain90,
            "xgbuildup90": self.xgbuildup90,
            "yellow": self.yellow,
            "red": self.red,
            "team": self.team
        }
        return data
