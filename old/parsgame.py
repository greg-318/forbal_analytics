import time
import logging
from selenium import webdriver
from bs4 import BeautifulSoup
from config import url, years, ligues
from parsweb import lig
import sys
sys.path.append("..\DataBase")
from mongo_default import MongoDefault
from Analytics.models.game_indicators import GameIndicators, TeamIndicators
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')


def links(page):
    """
    :param page: Ссылка команды на сайте understat.com
    :return: [list] Возвращает список ссылок всех игр команды.
    """
    driver.get(page)
    quantity = driver.find_elements_by_tag_name("a")
    games = tuple(x.get_attribute("href") for x in quantity
                  if "match" in str(x.get_attribute("href")))
    if not games:
        return
    return games


def game(http):
    """
    :param http: Сылка на стараницу с данными сыгронной игры .
    :return: team1 - [dict] данные сыгроной первой команды .
    :return: team2 - [dict] данные сыгроной второй команды .
    :return: draw - [str] показатель возможной ничьи  игры .
    """
    driver.get(http)
    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]'
                                 '/div[1]/div/div[1]/div/label[3]').click()
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    indicator = TeamIndicators()
    team_one = TeamIndicators().dict()
    team_duo = TeamIndicators().dict()
    draw = 0
    table = soup.find_all('div', class_='progress-bar')
    for item, ti in zip(table, indicator.dict().keys()):
        if 'CHANCES' in str(item.find_all('div', class_='progress-title')):
            data = tuple(x.get('title')[:-1]
                         for x in item.find_all('div')if x.get('title'))
        else:
            data = tuple(x.text for x in item.find_all
            ('div', class_='progress-value'))
        team_one[ti] = data[0]
        team_duo[ti] = data[-1]
        if len(data) == 3:
            draw = data[1]
    return team_one, team_duo, draw


def players(url):
    """
    :param url: ссылка на страницу игры
    :return: Возвращает два списка с теми игроками которые играли
    в данном матче одний команды и второй .
    """
    driver.get(url)
    html_players = driver.page_source
    soup = BeautifulSoup(html_players, 'html.parser')
    table = soup.find('tbody')
    team_1 = sum([[y.text for i, y in enumerate(x) if i == 1]
                  for x in table.find_all('tr') if "Sub" not in str(x)], [])
    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[4]'
                                 '/div/div[1]/div/label[2]').click()
    html_Players1 = driver.page_source
    soup1 = BeautifulSoup(html_Players1, 'html.parser')
    table1 = soup1.find('tbody')
    team_2 = sum([[y.text for i, y in enumerate(x) if i == 1]
                  for x in table1.find_all('tr') if "Sub" not in str(x)], [])
    return team_1, team_2


def insert( draw, team1, team2):
    """
    :return: team1 - [dict] данные сыгроной первой команды .
    :return: team2 - [dict] данные сыгроной второй команды .
    :return: draw - [str] показатель возможной ничьи  игры .
    :return: Результат отпраки в базу данных
    """
    match = f'{year}_{team1["name"]}_{team1["g"]}-{team2["g"]}_{team2["name"]}'
    result = GameIndicators(match=match, chances_draw=draw,
                            team1=team1, team2=team2)
    with MongoDefault('gameIndicators') as md:
        response, _ = md.insertUpdate(value_uniq_key=match, value_to=result.dict())
    return response


if __name__ == "__main__":
    driver = webdriver.ChromeOptions()
    driver.add_argument('headless')
    driver.add_argument('window-size=1920x935')
    driver = webdriver.Chrome(chrome_options=driver)

    while True:
        for ligue in ligues:
            teams = lig(ligue)
            for year in years:
                for counter, team in enumerate(teams):
                    http = url + team + '/' + year
                    logging.info(f'page {http}  number of'
                                 f' teams completed {counter}.')
                    links_page = links(http)
                    if not links:
                        logging.warning(f"not possible to find "
                                        f"team matches{http}")
                        continue
                    for link in links_page:
                        game_indicator = game(link)
                        players_indicator = players(link)
                        game_indicator[0]['players'] = players_indicator[0]
                        game_indicator[1]['players'] = players_indicator[1]
                        team1 = game_indicator[0]
                        team2 = game_indicator[1]
                        draw = game_indicator[2]
                        status = insert(draw, team1, team2)
                        print(status)
                        if not status:
                            logging.warning(f'Something happened '
                                            f'during insertion'
                                            f' {link} into the database')
        time.sleep(345600)
