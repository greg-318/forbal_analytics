import random
import json
import sys
import logging
import itertools
sys.path.extend(["../Analytics/models/", "../DataBase/", "../Analytics/"])
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from bs4 import BeautifulSoup
import game_indicators as model
from standard import check_standard_teams
from config import json_matches, json_statistics, json_incidents, json_players


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


def get_data(match_id, proxy):
    url_statistics = json_statistics.replace("ID", str(object_match["id"]))
    url_incidents = json_incidents.replace("ID", str(object_match["id"]))
    url_players = json_players.replace("ID", str(object_match["id"]))
    try:
        get_statistics = requests.get(url_statistics, proxies=proxy, verify=False, timeout=30).json()
        get_incidents = requests.get(url_incidents, proxies=proxy, verify=False, timeout=30).json()
        get_players = requests.get(url_players, proxies=proxy, verify=False, timeout=30).json()
        return get_statistics, get_incidents, get_players
    except:
        logging.info(f"Error in during getting urls - {proxy}. Reload with new proxy")
        return get_data(match_id, next(proxies))


def get_seasons(link, proxy):
    try:
        response = requests.get(link, proxies=proxy, verify=False).content
        soup = BeautifulSoup(response, 'html.parser')
        script = soup.find('script', id='__NEXT_DATA__')
        obj = json.loads(script.contents[0])
        return obj['props']['initialProps']['pageProps']['seasons']
    except:
        return get_seasons(link, next(proxies))


def get_matches(url, proxy):
    try:
        result = requests.get(url, proxies=proxy, verify=False, timeout=30)
        if result.status_code != 200:
            return
        return result.json()
    except:
        return get_matches(url, next(proxies))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
    leagues = {"RFPL": "russia/premier-liga/203", "EPL": "england/premier-league/17", "La_liga": "spain/laliga/8",
                   "Bundesliga": "germany/bundesliga/35", "Serie_A": "italy/serie-a/23", "Ligue_1": "france/ligue-1/34"}
    link = "https://www.sofascore.com/tournament/football/"
    proxies = (x for x in iter(lambda: {"https": f"https://185.130.105.106:{random.randint(22000, 26000)}"}, True))

    for league_key, league in leagues.items():
        logging.info(f'Starting {league_key}...')
        seasons_ids = get_seasons(link+league, next(proxies))
        for season in seasons_ids:
            year = '20'+season['year'].split("/")[1]
            if int(year) < 2014:
                break
            logging.info(f'Season year - {year}')
            for i in itertools.count(start=1, step=1):
                matches = json_matches.replace("LEAGUE_ID", str(league.split("/")[-1])).replace(
                    "SEASON_ID", str(season["id"])).replace("NUM", str(i))
                response = get_matches(matches, next(proxies))
                if not response:
                    break
                for object_match in response['events']:
                    data_statistics, data_incidents, data_players = get_data(object_match["id"], next(proxies))

                    try:
                        home_team = check_standard_teams(league_key, object_match['homeTeam']['name'])
                        away_team = check_standard_teams(league_key, object_match['awayTeam']['name'])
                    except:
                        logging.warning(f'Error name team')
                        with open('error_parsing_name.txt', 'a') as f:
                            f.write(f'{data_statistics}\n{data_incidents}\n{data_players}\n'
                                    f'{object_match["homeTeam"]["name"]}-{object_match["awayTeam"]["name"]}\n\n')
                        continue

                    try:
                        home_result = data_incidents['incidents'][0]['homeScore']
                        away_result = data_incidents['incidents'][0]['awayScore']
                        home_players = {player['player']['name']: player['statistics'] for player in data_players['home']['players'] if not player['substitute']}
                        away_players = {player['player']['name']: player['statistics'] for player in data_players['away']['players'] if not player['substitute']}
                        period_all = sum([item['statisticsItems'] for item in data_statistics['statistics'][0]['groups']], [])
                        period_first = sum([item['statisticsItems'] for item in data_statistics['statistics'][1]['groups']], [])
                        period_second = sum([item['statisticsItems'] for item in data_statistics['statistics'][2]['groups']], [])
                    except:
                        continue

                    periods = periods_dict(period_all, period_first, period_second)

                    m = model.GameIndicators(**periods)
                    m.match = year+'_'+home_team+'_'+str(home_result)+str(away_result)+"_"+away_team
                    m.players_home = {home_team: home_players}
                    m.players_away = {away_team: away_players}
                    m.sendToMongo()
                    logging.info(f'Success wrote to Mongo | year - {year}; league - {league_key}')
