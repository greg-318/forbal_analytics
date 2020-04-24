from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
import time
from ParsingWeb.config import url, teams, years
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
import sys
sys.path.append("..\DataBase")
from models.player import Player
from mongo_default import MongoDefault


def click(url):
    """
    получает ссылку на страницу и нажимает на кнопки для расскрытия всех элементов таблицы с игроками
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
        driver.find_element_by_xpath('//*[@id="team-players"]/div[1]/button').click()
        positions = (7, 12, 14, 15, 17, 19, 20, 21, 22, 23, 24)
        for pos in positions:
            driver.find_element_by_xpath(f'//*[@id="team-players"]/div[2]/div[2]/div/div[{pos}]/div[2]').click()
        driver.find_element_by_xpath('//*[@id="team-players"]/div[2]/div[3]/a[2]').click()
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
    :param string: - получает строку в виде '1.02-2.06' и разделяет ее на две части, разделитель + либо -.
    :return: возврашает словарь - {'value': 1.02, dynamic: '-2.06'}
    """
    if '-' in string:
        values = string.split('-')
        symbol = '-'
    else:
        values = string.split('+')
        symbol = '+'
    return {'value': float(values[0]), "dynamic": symbol+values[1]}


def send(data, player='players'):
    """
    :param data: - словарь данных для отправки в базу данных
    :param player: - название базы данных
    :return: - ошибок вставки данных в бд, или открытия класса
    """
    try:
        with MongoDefault(player) as instance:
            answer = instance.insert(data)
            if 'Error' in answer:
                logging.warning('Key already created, did not manage to send data to the database.')
    except ConnectionError:
        logging.warning('Could not contact class MongoDefault')


if __name__ == '__main__':

    while True:
        for year in years:
            for team in teams:
                http = url+team+'/'+year
                parser = click(http)
                if not parser:
                    continue
                soup = pars(parser)
                if not soup:
                    continue
                for i in soup:
                    information = Player()
                    elem = tuple(j.text for j in i)
                    information.player = f"{http[-4:]}_{elem[1]}"
                    information.position = elem[2]
                    information.appearances = int(elem[3])
                    information.minutes = int(elem[4])
                    information.goals = int(elem[5])
                    information.npg = int(elem[6])
                    information.a = int(elem[7])
                    information.sh90 = float('{:.2f}'.format(float(elem[8])))
                    information.kp90 = float('{:.2f}'.format(float(elem[9])))
                    information.xgchain = float('{:.2f}'.format(float(elem[13])))
                    information.xgbuildup = float('{:.2f}'.format(float(elem[14])))
                    information.xg90 = float('{:.2f}'.format(float(elem[15])))
                    information.npxg90 = float('{:.2f}'.format(float(elem[16])))
                    information.xa90 = float('{:.2f}'.format(float(elem[17])))
                    information.xg90xa90 = float('{:.2f}'.format(float(elem[18])))
                    information.npxg90xa90 = float('{:.2f}'.format(float(elem[19])))
                    information.xgchain90 = float('{:.2f}'.format(float(elem[20])))
                    information.xgbuildup90 = float('{:.2f}'.format(float(elem[21])))
                    information.yellow = int(elem[22])
                    information.red = int(elem[23])
                    if elem[10] != '0.00':
                        information.xg = power(elem[10])
                    if elem[11] != '0.00':
                        information.npxg = power(elem[11])
                    if elem[12] != '0.00':
                        information.xa = power(elem[12])
                    players = information.dict()
                    send(players)
        time.sleep(345600)
