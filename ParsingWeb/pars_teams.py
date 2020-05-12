import re
import logging
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.common.exceptions \
    import ElementClickInterceptedException, NoSuchElementException
# from Analytics.models.team import Team
# from DataBase.mongo_default import MongoDefault


years = ('2014', '2015', '2016', '2017', '2018', '2019')
MAIN_URL_UNDERSTAT = "https://understat.com/"
MAIN_URL_SOCCERSTATS = "https://www.soccerstats.com/latest.asp?league="  # year + 1
names = {"russia": "RFPL", "england": "EPL",
         "spain": "La_liga", "germany": "Bundesliga",
         "italy": "Serie_A", "france": "Ligue_1"}

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
driver = webdriver.ChromeOptions()
driver.add_argument('headless')
driver.add_argument('--window-size=1920,1080')
#driver.add_argument('--start-maximized')
driver = webdriver.Chrome(executable_path='./chromedriver', options=driver)
numbers = ("11", "13", "14", "15", "16", "17", "18")

# COLLECTION = MongoDefault('teams')


def soccer_handler(req):
    """собирает данные по командам с soccerstats и добавляет в словарь"""
    soccer_inds = dict()
    soccer_soup = bs(req.text, 'html.parser')
    teams = soccer_soup.find('div', class_='eight columns').find_all('tr', class_='odd')
    for team in teams:
        wins = []
        team = team.find_all('td')
        for i in range(len(team)):
            try:
                table = team[i].find('table').find_all('tr')
            except AttributeError:
                team[i] = team[i].text.strip()
            else:
                for row in table:
                    one_win = dict()
                    tds = row.find_all('td')
                    tds = [td.text.replace('\r', '').replace('\n', '') for td in tds]
                    opponents = tds[1].split('-')
                    count = tds[2].split('-')
                    one_win.update({opponents[0].strip(): int(count[0]),
                                    opponents[1].strip(): int(count[1])})
                    wins.append(one_win)
                team[i] = wins
        block_end = team[-4:]
        team = team[0:11]
        team.extend(block_end)
        team.pop(0)
        soccer_inds.update({year + '_' + team[0]: team[1:]})
    return soccer_inds


def find_under_body(url):
    """собирает тело таблицы с understat для разбора по командам"""
    driver.get(url)
    global START_UNDER
    if START_UNDER:
        driver.find_element_by_class_name('options-button').click()
        for num in numbers:
            driver.find_element_by_xpath(
                "//div[@class='table-options']"
                "/div[" + num + "]/div[@class='row-display']").click()
        driver.find_element_by_class_name('button-apply').click()
        START_UNDER = False
    body = driver.find_element_by_xpath('//table/tbody') \
        .find_elements_by_xpath('tr')
    return body


def under_handler(body: list):
    """обрабатывает данные полученные с understat"""
    under_inds = dict()
    for j in range(len(body)):
        tds = body[j].find_elements_by_tag_name('td')
        tds = [td.text for td in tds[1:]]
        for i in range(len(tds)):
            if '+' in tds[i] and i != 12:
                temp = tds[i].split('+')
                tds[i] = {'value': float(temp[0]), 'dynamic': '+' + temp[1]}
            elif '-' in tds[i] and i != 12 and re.match(r'\d', tds[i]) is not None:
                temp = tds[i].split('-')
                tds[i] = {'value': float(temp[0]), 'dynamic': '-' + temp[1]}
        under_inds.update({year + '_' + tds[0]: tds[1:]})
    return under_inds


def model_pack(all_ind: list):
    """отправка данных в модель"""
    model = Team(
        name=str(all_ind[0]),
        gp=int(all_ind[1]),
        w=int(all_ind[2]),
        d=int(all_ind[3]),
        l=int(all_ind[4]),
        gf=int(all_ind[5]),
        ga=int(all_ind[6]),
        gd=str(all_ind[7]),
        pts=int(all_ind[8]),
        form=all_ind[9],
        ppg=float(all_ind[10]),
        last8=float(all_ind[11]),
        cs=str(all_ind[12]),
        fts=str(all_ind[13]),
        xg=all_ind[14],
        npxg=float(all_ind[15]),
        xga=all_ind[16],
        npxga=float(all_ind[17]),
        npxgd=str(all_ind[18]),
        ppda=float(all_ind[19]),
        oppda=float(all_ind[20]),
        dc=int(all_ind[21]),
        odc=int(all_ind[22]),
        xpts=all_ind[23]
    )
    return model


def insert_to_db(model: Team):
    """добавление данных в бд"""
    pass


if __name__ == '__main__':
    START_UNDER = True
    for soccer_liga, under_liga in names.items():
        for index in range(len(years)):
            year = years[index]
            if year == years[0] and soccer_liga == 'russia':
                continue
            while True:  # если возникнут ошибки - перезапуск итерации для повторной попытки
                if years[index] != years[-1]:
                    SOCCER_URL = MAIN_URL_SOCCERSTATS + soccer_liga + '_' + str(int(year) + 1)
                else:
                    SOCCER_URL = MAIN_URL_SOCCERSTATS + soccer_liga
                under_url = MAIN_URL_UNDERSTAT + 'league/' + under_liga + '/' + year
                soccer_request = requests.get(SOCCER_URL)
                if soccer_request.status_code == 200:
                    logging.info(f'Parsing soccerstats for year {year} and league {soccer_liga}')
                    soccer_dict = soccer_handler(soccer_request)
                else:
                    logging.warning('Something happens with connection to soccerstats, trying again')
                    continue
                try:
                    logging.info(f'Parsing understat for year {year} and league {under_liga}')
                    bodies = find_under_body(under_url)
                except ElementClickInterceptedException:
                    logging.warning('Cannot click on element, trying again')
                except NoSuchElementException:
                    logging.warning('Element is not available or connection lost, trying again')
                else:
                    under_dict = under_handler(bodies)
                    for team, indic in soccer_dict.items():
                        for value in under_dict.values():
                            if indic[0:6] == value[0:6]:
                                all_ind = [
                                    team, indic[0], indic[1], indic[2], indic[3], indic[4], indic[5], indic[6],
                                    indic[7], indic[8], indic[-4], indic[-3], indic[-2], indic[-1], value[7],
                                    value[8], value[9], value[10], value[11], value[12], value[13], value[14],
                                    value[15], value[16]
                                ]
                                model = model_pack(all_ind)
                                insert_to_db(model)
                    logging.info(f'Successfully inserted in database')
                    break  # остановка цикла, в котором решаются ошибки
