from structure import Structure


class TeamIndicators(Structure):
    """
    :param name: [str] = Team name
    :param possesion_ah: [float] = Average Ball Possession
    :param sh_ah: [int] = Number of strokes total (general)
    :param sh_target_ah: [int] = Shots on target (general)
    :param sh_s: [int] = Number of strokes total (season)
    :param sh_target_s: [int] = Shots on target (season)
    :param median_xg_ah: [float] = xG total
    :param sum_xg_s: [float] = xG season
    :param percent_sh_opp: [float] = How many ops hit on goal % overall
    :param percent_sh_target_opp: [float] = How many opposing shots on target %
    :param players: [list] = Players in current match
    """
    _fields = ["name", "possesion_ah", "sh_ah", "sh_target_ah", "sh_s", "sh_target_s", "median_xg_ah", "sum_xg_s",
               "percent_sh_opp", "percent_sh_target_opp", "players"]
    _type = [str(), float(), int(), int(), int(), int(), float(), float(), float(), float(), list()]


class GameIndicators(Structure):
    """
    :param match: [str] = Match name # year_team1_result_team2 (2014_MyTeam_10_YourTeam)
    :param team1: [dict] = All data from Team 1
    :param team2: [dict] = All data from Team 2
    """
    _fields = ["match", "team1", "team2"]
    _type = [str(), TeamIndicators().dict(), TeamIndicators().dict()]
