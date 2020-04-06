class Team:
    """
    :param name: [str] = Team name
    :param year: [str] = Year data
    :param gp: [int] = Count of matches
    :param w: [int] = Wins
    :param d: [int] = Draws
    :param l: [int] = Loses
    :param gf: [int] = Goals for
    :param ga: [int] = Goals againist
    :param gd: [str] = Goal difference
    :param pts: [int] = Points
    :param form: [list] = Last 6 results # [{"FC Barcelona": 2, "Levante": 1}, ...]
    :param ppg: [float] = Points per game
    :param last8: [float] = Points per game in the last 8 matches
    :param cs: [str] = % clean sheets (matches with no goal conceded)
    :param fts: [str] = % failed to score (matches with no goal scored)
    :param xg: [dict] = Expected goals for
    :param npgx: [float] = Expected goals for without penalties and own goals
    :param xga: [dict] = Expected goals againist
    :param npxga: [float] = Expected goals againist without penalties and own goals
    :param npxgd: [str] = The difference between "for" and "against" expected goals without penalties and own goals
    :param ppda: [float] = Passes allowed per defensive action in the opposition half
    :param oppda: [float] = Opponent passes allowed per defensive action in the opposition half
    :param dc: [int] = Passes completed within an estimated 20 yards of goal (crosses excluded)
    :param odc: [int] = Opponent passes completed within an estimated 20 yards of goal (crosses excluded)
    :param xpts: [dict] = Expected points
    """

    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "")  # year_name
        self.gp = kwargs.get("gp", 0)
        self.w = kwargs.get("w", 0)
        self.d = kwargs.get("d", 0)
        self.l = kwargs.get("l", 0)
        self.gf = kwargs.get("gf", 0)
        self.ga = kwargs.get("ga", 0)
        self.gd = kwargs.get("gd", "")
        self.pts = kwargs.get("pts", 0)
        self.form = kwargs.get("form", [])
        self.ppg = kwargs.get("ppg", 0.0)
        self.last8 = kwargs.get("last8", 0.0)
        self.cs = kwargs.get("cs", "")
        self.fts = kwargs.get("fts", "")
        self.xg = kwargs.get("xg", {})
        self.npgx = kwargs.get("npgx", 0.0)
        self.xga = kwargs.get("xga", {})
        self.npxga = kwargs.get("npxga", 0.0)
        self.npxgd = kwargs.get("npxgd", "")
        self.ppda = kwargs.get("ppda", 0.0)
        self.oppda = kwargs.get("oppda", 0.0)
        self.dc = kwargs.get("dc", 0)
        self.odc = kwargs.get("odc", 0)
        self.xpts = kwargs.get("xpts", {})

    def dict(self):
        data = {
            "name": self.name,
            "gp": self.gp,
            "wins": self.w,
            "draws": self.d,
            "loses": self.l,
            "gf": self.gf,
            "ga": self.ga,
            "gd": self.gd,
            "points": self.pts,
            "form": self.form,
            "ppg": self.ppg,
            "last8": self.last8,
            "cs": self.cs,
            "fts": self.fts,
            "xg": self.xg,
            "npgx": self.npgx,
            "xga": self.xga,
            "npxga": self.npxga,
            "npxgd": self.npxgd,
            "ppda": self.ppda,
            "oppda": self.oppda,
            "dc": self.dc,
            "odc": self.odc,
            "xpts": self.xpts
        }
        return data
