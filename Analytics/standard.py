from associations import dict_associations


def check_standard_teams(league, team):
    """
    :param league: Team league name
    :param team: Variant name for team
    :return: Standard name
    """
    for l, values in dict_associations.items():
        if league == l or league in values["name"]:
            if team in values["teams"].keys():
                return team
            for standard_name, another_names in values["teams"].items():
                if team in another_names:
                    return standard_name
    raise AttributeError(f"We haven't this name: {team}")
