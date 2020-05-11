from .structure import Structure
from types import MappingProxyType


class TeamIndicators(Structure):
    """
    :param name: Team name
    :param chances: Actual win chance
    :param g: Goals scored
    :param xg: Expected goals
    :param sh: Total hits
    :param sh_target: Total hits on target
    :param deep: Number of passes 18m from the opponent's goal
    :param ppda: High pressure (not less than 40 meters from goal)
    :param xpts: How many ops hit on goal % overall
    :param ball_possession: % ball possession
    :param players: Players in current match
    """
    _fields = MappingProxyType({"name": str, "chances": int, "g": int, "xg": float, "sh": int, "sh_target": int,
                                "deep": int, "ppda": float, "xpts": float, "bp": int, "players": list})


class GameIndicators(Structure):
    """
    :param match: Match name # year_team1_result_team2 (2014_MyTeam_10_YourTeam)
    :param chances_draw: Actual draw chance
    :param team1: All data from Team 1
    :param team2: All data from Team 2
    """
    _fields = MappingProxyType({"match": str, "chances_draw": int, "team1": dict, "team2": dict})

    def dict(self):
        self.team1 = self.team1 or TeamIndicators().dict()
        self.team2 = self.team2 or TeamIndicators().dict()
