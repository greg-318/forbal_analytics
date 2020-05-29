from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
import time
from old.config import url, years, ligues
import logging
import requests
import re
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')
import sys
sys.path.append("..\DataBase")
from Analytics.models.player import Player
from mongo_default import MongoDefault


def click(url):
    """
    получает ссылку на страницу и нажимает на кнопки для расскрытия
    всех элементов таблицы с игроками
    :param url: - прямая ссылка на страницу
    :return: Возвращает код всей старницы с раскрытой таблицей
    """

    driver = webdriver.ChromeOptions()
    driver.add_argument('headless')
    driver.add_argument('window-size=1920x935')
    driver = webdriver.Chrome(chrome_options=driver)
    driver.get(url)
    logging.info('getting page')

    try:
        driver.find_element_by_xpath('//*[@id="team-players"]/div[1]/button')\
            .click()
        positions = (7, 12, 14, 15, 17, 19, 20, 21, 22, 23, 24)
        for pos in positions:
            driver.find_element_by_xpath(f'//*[@id="team-players"]/div[2]/div'
                                         f'[2]/div/div[{pos}]/div[2]').click()
        driver.find_element_by_xpath('//*[@id="team-players"]/div[2]/div[3]'
                                     '/a[2]').click()
    except NoSuchElementException:
        logging.warning("Problems with the push of a button.")
        return
    res = driver.page_source
    return res


def pars(html):
    """
    получает html код всей страницы
    :param html: - код всей страницы в виде html
    :return: -  возврашает только таблицу с игроками
    """
    soup = BeautifulSoup(html, 'html.parser')
    scripts = soup.find('div', class_='players margin-top jTable')
    if not scripts:
        logging.warning('Table with player data not found.')
        return None
    table = scripts.find('tbody')
    if not table:
        logging.warning('The table with the players is empty. ')
        return None
    return table


def power(string):
    """
    :param string: - получает строку в виде '1.02-2.06' и разделяет ее
     на две части, разделитель + либо -.
    :return: возврашает словарь - {'value': 1.02, dynamic: '-2.06'}
    """
    if '-' in string:
        values = string.split('-')
    else:
        values = string.split('+')
    return values[0]


def lig(ligue, url='https://understat.com/league/'):
    """
    :param ligue: - принимает название лиги
    :param url: - часть ссылки
    :return: - возврашает список команд переданной лиги
    """
    http = url+ligue
    res = requests.get(http).content.decode('unicode_escape')
    soup = BeautifulSoup(res, "html.parser")
    pars = soup.find_all('script')[1].get_text()
    if not pars:
        logging.warning('List of teams not found.', ligue)
        return None
    teams = re.findall(r'"title":"([\w\s]+)', pars)
    if not teams:
        logging.warning('List of teams not found, regular.', ligue)
        return None
    return set(teams)


def send(name_player, data):
    """
    :param data: - словарь данных игрока для отправки в базу данных
    :param name_player: - Имя игрока
    :return: - ошибок вставки данных в бд, или открытия класса

    """

    with MongoDefault('players') as md:
        response, _ = md.insertUpdate(value_uniq_key=name_player, value_to=data)
    return response


if __name__ == '__main__':

    while True:
        for ligue in ligues:
            teams = lig(ligue)
            if not teams:
                continue
            for year in years:
                for team in teams:
                    http = url+team+'/'+year
                    logging.info(f'page {http}')
                    parser = click(http)
                    if not parser:
                        continue
                    soup = pars(parser)
                    if not soup:
                        continue
                    for player in soup:
                        information = Player().dict()
                        elem = tuple(players.text for players in player)
                        information['player'] = f"{http[-4:]}_{elem[1]}"
                        information['position'] = elem[2]
                        information['appearances'] = int(elem[3])
                        information['minutes'] = int(elem[4])
                        information['goals'] = int(elem[5])
                        information['npg'] = int(elem[6])
                        information['a'] = int(elem[7])
                        information['sh90'] = float('{:.2f}'.format
                                                    (float(elem[8])))
                        information['kp90'] = float('{:.2f}'.format
                                                    (float(elem[9])))
                        information['xgchain'] = float('{:.2f}'.format
                                                       (float(elem[13])))
                        information['xgbuildup'] = float('{:.2f}'.format
                                                         (float(elem[14])))
                        information['xg90'] = float('{:.2f}'.format
                                                    (float(elem[15])))
                        information['npxg90'] = float('{:.2f}'.format
                                                      (float(elem[16])))
                        information['xa90'] = float('{:.2f}'.format
                                                    (float(elem[17])))
                        information['xg90xa90'] = float('{:.2f}'.format
                                                        (float(elem[18])))
                        information['npxg90xa90'] = float('{:.2f}'.format
                                                          (float(elem[19])))
                        information['xgchain90'] = float('{:.2f}'.format
                                                         (float(elem[20])))
                        information['xgbuildup90'] = float('{:.2f}'.format
                                                           (float(elem[21])))
                        information['yellow'] = int(elem[22])
                        information['red'] = int(elem[23])
                        information['team'] = team
                        information['xg'] = float('{:.2f}'.format
                                                      (float(power(elem[10]))))
                        information['npxg'] = \
                                float('{:.2f}'.format(float(power(elem[11]))))
                        information['xa'] = float('{:.2f}'.format
                                                      (float(power(elem[12]))))
                        send(elem[1], information)
                        if not send:
                            logging.info(f'Paste into database'
                                         f' failed. {http} ')
        time.sleep(345600)
