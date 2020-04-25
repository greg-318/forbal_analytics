class GameIndicators:
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
    """

    def __init__(self, match: str, team1: dict, team2: dict):
        self.match = match  # year_team1_team2
        self.team1 = self.__dict_team(team1)
        self.team2 = self.__dict_team(team2)

    def __dict_team(self, data_team: dict) -> dict:
        """
        :param data_team: Data for formatting dictionary team's
        :return: All data team1
        """
        data = {
            "name": data_team.get("name", ""),
            "possesion_ah": data_team.get("possesion_ah", 0.0),
            "sh_ah": data_team.get("sh_ah", 0),
            "sh_target_ah": data_team.get("sh_target_ah", 0),
            "sh_s": data_team.get("sh_s", 0),
            "sh_target_s": data_team.get("sh_target_s", 0),
            "median_xg_ah": data_team.get("median_xg_ah", 0.0),
            "sum_xg_s": data_team.get("sum_xg_s", 0.0),
            "percent_sh_opp": data_team.get("percent_sh_opp", 0.0),
            "percent_sh_target_opp": data_team.get("percent_sh_target_opp", 0.0),
        }
        return data

    def dict(self) -> dict:
        """
        :return: All data for game_indicators
        """
        data = {
            "match": self.match,
            "team1": self.team1,
            "team2": self.team2,
        }
        return data
