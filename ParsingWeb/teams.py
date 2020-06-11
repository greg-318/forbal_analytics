import asyncio
import logging
import sys
import aiohttp
from understat import Understat
sys.path.extend(["../Analytics/models/", "../DataBase/", "../Analytics/"])
import team as team_model
from standard import check_standard_teams

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')


async def get_understat_teams(league, year):
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        teams = await understat.get_teams(league, year)
        list_of_teams = []
        for team in teams:
            team_dict = {**team_model.Team._fields}
            team_form = {"name": f'{int(year)+1}_{team["title"]}'}
            for key in team["history"][0].keys():
                if key not in ("h_a", "date", "result", "ppda", "ppda_allowed"):
                    value = sum([x[key] for x in team["history"]])
                    if isinstance(value, float):
                        value = "{:.2f}".format(value)
                    team_form[key.lower()] = value
                elif key in ("ppda", "ppda_allowed"):
                    val1 = sum([x[key]["att"] for x in team["history"]])
                    val2 = sum([x[key]["def"] for x in team["history"]])
                    team_form[key] = "{:.2f}".format(val1/val2)
            team_dict.update({k.lower(): v for k, v in team_form.items() if k.lower() in team_dict.keys()})
            list_of_teams.append(team_dict)
        return list_of_teams


async def get_understat_players(teams, year):
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)

        for team in teams:
            players = await understat.get_team_players(team['name'][5:], year)
            list_of_players = []
            for player in players:
                player_dict = {**team_model.Player._fields}
                p = {key: "{:.2f}".format(float(val)) for key, val in player.items() if key.lower() in
                     ("xg", "xa", "npxg", "xgchain", "xgbuildup")}
                player.update({k: v for k, v in p.items()})
                player_dict.update({k.lower(): v for k, v in player.items() if k.lower() in player_dict.keys()})
                list_of_players.append(player_dict)
            team["players"] = list_of_players

        return teams


if __name__ == "__main__":

    leagues = ("RFPL", "EPL", "La_liga", "Bundesliga", "Serie_A", "Ligue_1")
    years = ('2014', '2015', '2016', '2017', '2018', '2019')
    loop = asyncio.get_event_loop()

    for league in leagues:
        logging.info(f"Starting parsing data for league: {league}...")

        for year in years:

            run_teams = [get_understat_teams(league, year)]
            result_teams, _ = loop.run_until_complete(asyncio.wait(run_teams))
            all_teams_league = sum([_team.result() for _team in result_teams], [])

            run_players = [get_understat_players(all_teams_league, year)]
            result_players, _ = loop.run_until_complete(asyncio.wait(run_players))
            all_players_league = sum([_player.result() for _player in result_players], [])

            for data in all_players_league:
                model = team_model.Team(**data)
                split_name = model.name.split("_")
                model.name = split_name[0]+"_"+check_standard_teams(league, split_name[1])
                model.sendToMongo()

        logging.info(f"Finished parsing data for league: {league}...")
