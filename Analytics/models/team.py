from structure import Structure


class Team(Structure):
    """
    :param name: [str] = Team name # year_name
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

    _fields = ["name", "gp", "w", "d", "l", "gf", "ga", "gd", "pts", "form", "ppg", "last8", "cs", "fts", "xg", "npgx",
               "xga", "npxga", "npxgd", "ppda", "oppda", "dc", "odc", "xpts"]
    _type = [str(), int(), int(), int(), int(), int(), int(), str(), int(), list(), float(), float(), str(), str(),
             dict(), float(), dict(), float(), str(), float(), float(), int(), int(), dict()]

    def dict(self):
        """
        :return: All data for team
        """
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
