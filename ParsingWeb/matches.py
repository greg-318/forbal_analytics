import random
import json
import sys
import logging
sys.path.extend(["../Analytics/models/", "../DataBase/", "../Analytics/"])
import requests
from bs4 import BeautifulSoup
import game_indicators as model
from standard import check_standard_teams
from config import json_matches, json_statistics, json_incidents, json_players


def proxy_gen():
    while True:
        yield {"https": f"https://185.130.105.106:{random.randint(22000, 26000)}"}


def periods_dict(all, first, second):
    periods = {
        'all': '',
        'first': '',
        'second': ''
    }
    for period, data in {"all": all, "first": first, "second": second}.items():
        team_home_data = {'name': home_team}
        team_away_data = {'name': away_team}
        for item in data:
            if '(' in item['home'] or '(' in item['away']:
                team_home_data[item['name'].lower().replace(" ", "_")] = item["home"].split(" ")[0]
                team_away_data[item['name'].lower().replace(" ", "_")] = item["away"].split(" ")[0]
            else:
                team_home_data[item['name'].lower().replace(" ", "_")] = item['home'].replace("%", "")
                team_away_data[item['name'].lower().replace(" ", "_")] = item['away'].replace("%", "")
        periods[period] = [model.TeamIndicators(**team_home_data).dict(), model.TeamIndicators(**team_away_data).dict()]
    return periods


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
    leagues = {"RFPL": "russia/premier-liga/203", "EPL": "england/premier-league/17", "La_liga": "spain/laliga/8",
               "Bundesliga": "germany/bundesliga/35", "Serie_A": "italy/serie-a/23", "Ligue_1": "france/ligue-1/34"}
    link = "https://www.sofascore.com/tournament/football/"
    proxies = proxy_gen()

    for league_key, league in leagues.items():
        logging.info(f'Starting {league_key}...')
        r = requests.get(link+league, proxies=next(proxies), verify=False).content
        soup = BeautifulSoup(r, 'html.parser')
        script = soup.find('script', id='__NEXT_DATA__')
        obj = json.loads(script.contents[0])
        seasons_ids = obj['props']['initialProps']['pageProps']['seasons']

        for season in seasons_ids:
            year = '20'+season['year'].split("/")[1]
            logging.info(f'Season year - {year}')
            matches = json_matches.replace("LEAGUE", str(league.split("/")[-1])).replace("ID", str(season["id"]))
            try:
                response = requests.get(matches, proxies=next(proxies), verify=False, timeout=30).json()
            except:
                logging.warning(f'Response error {matches}')
                with open('error_parsing_main_url.txt', 'a') as f:
                    f.write(f'{season["id"]}\n\n')
            else:
                for values in response['teamEvents'].values():
                    for ids in values.values():
                        for object_match in ids['total']:

                            url_statistics = json_statistics.replace("ID", str(object_match["id"]))
                            url_incidents = json_incidents.replace("ID", str(object_match["id"]))
                            url_players = json_players.replace("ID", str(object_match["id"]))

                            try:
                                get_statistics = requests.get(url_statistics, proxies=next(proxies), verify=False, timeout=30).json()
                                get_incidents = requests.get(url_incidents, proxies=next(proxies), verify=False, timeout=30).json()
                                get_players = requests.get(url_players, proxies=next(proxies), verify=False, timeout=30).json()
                            except:
                                logging.warning(f'Response error getting data')
                                with open('error_parsing_url.txt', 'a') as f:
                                    f.write(f'{object_match["id"]}\n\n')
                                break

                            try:
                                home_team = check_standard_teams(league_key, object_match['homeTeam']['name'])
                                away_team = check_standard_teams(league_key, object_match['awayTeam']['name'])
                            except:
                                logging.warning(f'Error name team')
                                with open('error_parsing_name.txt', 'a') as f:
                                    f.write(f'{url_statistics}\n{url_incidents}\n{url_players}\n\n')
                                break

                            home_result = get_incidents['incidents'][0]['homeScore']
                            away_result = get_incidents['incidents'][0]['awayScore']
                            home_players = {player['player']['name']: player['statistics'] for player in get_players['home']['players'] if not player['substitute']}
                            away_players = {player['player']['name']: player['statistics'] for player in get_players['away']['players'] if not player['substitute']}

                            period_all = sum([item['statisticsItems'] for item in get_statistics['statistics'][0]['groups']], [])
                            period_first = sum([item['statisticsItems'] for item in get_statistics['statistics'][1]['groups']], [])
                            period_second = sum([item['statisticsItems'] for item in get_statistics['statistics'][2]['groups']], [])

                            periods = periods_dict(period_all, period_first, period_second)

                            m = model.GameIndicators(**periods)
                            m.match = year+'_'+home_team+'_'+str(home_result)+str(away_result)+"_"+away_team
                            m.players_home = {home_team: home_players}
                            m.players_away = {away_team: away_players}
                            m.sendToMongo()
                            logging.info(f'Success wrote to Mongo')
