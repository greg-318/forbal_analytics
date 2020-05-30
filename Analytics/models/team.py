from structure import Structure
from types import MappingProxyType


class Player(Structure):
    """
    :param player_name: Player name and surname # year_player
    :param position: Position
    :param games: Number of appearances
    :param time: Time spent in the game
    :param goals: Count of goals
    :param npg: Not penalty goals
    :param assists: Passes led to goal
    :param sh90: Shorts per 90 minutes
    :param key_passes: Total passes led to short
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
    :param yellow_cards: Warnings
    :param red_cards: Remove player from field
    """

    _fields = MappingProxyType({"player_name": str, "position": str, "games": int, "time": int, "goals": int,
                                "npg": int, "assists": int, "key_passes": int, "xg": float, "npxg": float, "xa": float,
                                "xgchain": float, "xgbuildup": float, "yellow_cards": int, "red_cards": int})
    _collection = MappingProxyType({"name": "players", "key": "player"})

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sh90 = "{:.2f}".format(self.games/(self.time/90.0))
        self.kp90 = "{:.2f}".format(self.key_passes/(self.time/90.0))
        self.xg90 = "{:.2f}".format(self.xg/(self.time/90.0))
        self.npxg90 = "{:.2f}".format(self.npxg/(self.time/90.0))
        self.xa90 = "{:.2f}".format(self.xa/(self.time/90.0))
        self.xg90xa90 = self.xg90 + self.xa90
        self.npxg90xa90 = self.npxg90 + self.xa90
        self.xgchain90 = "{:.2f}".format(self.xgchain/(self.time/90.0))
        self.xgbuildup90 = "{:.2f}".format(self.xgbuildup/(self.time/90.0))


class Team(Structure):
    """
    :param name: Team name # year_name
    :param games: Count of matches
    :param wins: Wins
    :param draws: Draws
    :param loses: Loses
    :param scored: Goals for
    :param missed: Goals againist
    :param gd: Goal difference
    :param pts: Points
    # :param ppg: Points per game
    # :param last8: Points per game in the last 8 matches
    # :param cs: % clean sheets (matches with no goal conceded)
    # :param fts: % failed to score (matches with no goal scored)
    :param xg: Expected goals for
    :param npxg: Expected goals for without penalties and own goals
    :param xga: Expected goals againist
    :param npxga: Expected goals againist without penalties and own goals
    :param npxgd: The difference between "for" and "against" expected goals without penalties and own goals
    :param ppda: Passes allowed per defensive action in the opposition half
    :param ppda_allowed: Opponent passes allowed per defensive action in the opposition half
    :param deep: Passes completed within an estimated 20 yards of goal (crosses excluded)
    :param deep_allowed: Opponent passes completed within an estimated 20 yards of goal (crosses excluded)
    :param xpts: Expected points
    :param players: List of players
    """

    _fields = MappingProxyType({"name": str, "wins": int, "draws": int, "loses": int, "scored": int, "missed": int,
                                "pts": int, "xg": float, "npxg": float, "xga": float, "npxga": float, "npxgd": float,
                                "ppda": float, "ppda_allowed": float, "deep": int, "deep_allowed": int, "xpts": float,
                                "players": list})
    _collection = MappingProxyType({"name": "teams", "key": "name"})

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.games = self.draws + self.loses + self.wins
        self.gd = self.scored - self.missed

    def dict(self):
        if not self.players:
            raise AttributeError("Team model haven't list of players")
        return super().dict()


class MonteCarlo(Team):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.points = self.wins * 3 + self.draws
        self.winpct = round(self.wins / (self.wins + self.draws + self.loses), 2)
        self.drawpct = round(self.draws / (self.wins + self.draws + self.loses), 2)
