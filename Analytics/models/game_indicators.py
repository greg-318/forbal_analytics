from structure import Structure


class TeamIndicators(Structure):
    """
    :param name: [str] = Team name
    :param chances: [int] = Actual win chance
    :param g: [int] = Goals scored
    :param xg: [float] = Expected goals
    :param sh: [int] = Total hits
    :param sh_target: [int] = Total hits on target
    :param deep: [int] = Number of passes 18m from the opponent's goal
    :param ppda: [float] = High pressure (not less than 40 meters from goal)
    :param xpts: [float] = How many ops hit on goal % overall
    :param players: [list] = Players in current match
    """
    _fields = ["name", "chances", "g", "xg", "sh", "sh_target", "deep", "ppda", "xpts", "players"]
    _type = [str, int, int, float, int, int, int, float, float, list]


class GameIndicators(Structure):
    """
    :param match: [str] = Match name # year_team1_result_team2 (2014_MyTeam_10_YourTeam)
    :param chances_draw: [float] = Actual draw chance
    :param team1: [dict] = All data from Team 1
    :param team2: [dict] = All data from Team 2
    """
    _fields = ["match", "chances_draw", "team1", "team2"]
    _type = [str, int, TeamIndicators().dict, TeamIndicators().dict]
