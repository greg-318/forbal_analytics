import logging
import re
import time
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.common.exceptions \
    import ElementClickInterceptedException, NoSuchElementException
from Analytics.models.team import Team
from DataBase.mongo_default import MongoDefault

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
driver = webdriver.Chrome(executable_path='./chromedriver', options=driver)
numbers = ("11", "13", "14", "15", "16", "17", "18")


def soccer_handler(req):
    """
    собирает данные по командам с soccerstats и добавляет в словарь
    :param req: - запроса на soccerstats
    :return: - [dict] показатели всех команд soccerstats из лиги за конкретный год
    """
    soccer_inds = dict()
    soccer_soup = bs(req.text, 'html.parser')
    teams = soccer_soup.find('div', class_='eight columns').find_all('tr', class_='odd')
    for team_row in teams:
        team_row = [t.text.strip() for t in team_row.find_all('td')]
        end = team_row[-4:]
        team_row = team_row[1:10]
        team_row.extend(end)
        soccer_inds.update({year + '_' + team_row[0]: team_row[1:]})
    return soccer_inds


def find_under_body(url):
    """
    собирает тело таблицы с understat для разбора по командам
    :param url: - [str] - ссылка на understat по лиге и году
    :return: - таблица с показателями
    """
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
    """
    обрабатывает данные полученные с understat
    :param body: - таблица с показателями команд лиги с understat
    :return: - [dict] показатели всех команд understat из лиги за конкретный год
    """
    under_inds = dict()
    for ind_body in range(len(body)):
        cells = body[ind_body].find_elements_by_tag_name('td')
        cells = [td.text for td in cells[1:]]
        for ind_cell in range(len(cells)):
            if '+' in cells[ind_cell] and ind_cell != 12:
                cells[ind_cell] = cells[ind_cell].split('+')[0]
            elif '-' in cells[ind_cell] and ind_cell != 12 and re.match(r'\d', cells[ind_cell]) is not None:
                cells[ind_cell] = cells[ind_cell].split('-')[0]
        under_inds.update({year + '_' + cells[0]: cells[1:]})
    return under_inds


def model_pack(indicators: list):
    """
    отправка данных в модель
    :param indicators: [list] - список со всеми показателями команды
    :return: - модель Team
    """
    model = Team(
        name=str(indicators[0]),
        gp=int(indicators[1]),
        w=int(indicators[2]),
        d=int(indicators[3]),
        l=int(indicators[4]),
        gf=int(indicators[5]),
        ga=int(indicators[6]),
        gd=int(indicators[7]),
        pts=int(indicators[8]),
        ppg=float(indicators[10]),
        last8=float(indicators[11]),
        cs=float(indicators[12].replace('%', ''))/100,
        fts=float(indicators[13].replace('%', ''))/100,
        xg=float(indicators[14]),
        npxg=float(indicators[15]),
        xga=float(indicators[16]),
        npxga=float(indicators[17]),
        npxgd=float(indicators[18]),
        ppda=float(indicators[19]),
        oppda=float(indicators[20]),
        dc=int(indicators[21]),
        odc=int(indicators[22]),
        xpts=float(indicators[23])
    )
    return model


def insert_to_db(team_name: str, model: Team):
    """
    добавление данных в бд
    :param team_name: [str] - название команды
    :param model: - объект класса Team
    :return: - ответ от базы данных
    """
    with MongoDefault('teams') as md:
        response, _ = md.insertUpdate(value_uniq_key=team_name, value_to=model.dict())
        return response


if __name__ == '__main__':
    while True:
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
                        logging.warning('Something happened with connection to soccerstats, trying again')
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
                        for soccer_team, indic in soccer_dict.items():
                            for value in under_dict.values():
                                if indic[:6] == value[:6]:
                                    while True:  # обработка ошибок при добавлении в бд
                                        all_ind = [
                                            soccer_team, indic[0], indic[1], indic[2], indic[3], indic[4], indic[5], indic[6],
                                            indic[7], indic[8], indic[-4], indic[-3], indic[-2], indic[-1], value[7],
                                            value[8], value[9], value[10], value[11], value[12], value[13], value[14],
                                            value[15], value[16]
                                        ]
                                        team_model = model_pack(all_ind)
                                        status = insert_to_db(soccer_team, team_model)
                                        if not status:
                                            logging.warning(f'Something happened while inserting {soccer_team} in database')
                                            continue
                                        else: break
                        logging.info('Successfully inserted in database')
                        break  # остановка цикла, в котором решаются ошибки
        time.sleep(345600)  # сон на 4 дня
