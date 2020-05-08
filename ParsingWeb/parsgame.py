from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
import time
from ParsingWeb.config import url, years, ligues
import logging
import requests
import re
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
import sys
#sys.path.append("..\DataBase")
#from models.player import Player
#from mongo_default import MongoDefault
#import sys
sys.path.append("..\ParsingWeb")
from parsweb import lig


def pars(html):
    """
    :param html: - получает html код страницы .
    :return: - возвращает списко где первый элемент это название команды чьи значения указаны с левой стороны таблицы
     2 и 3 пренадлежат все тожей команже а 4 и 5 команде которая с права . Последний элемент списка это список значений
     changes.
    """
    soup = BeautifulSoup(html, 'html.parser')
    indicators = []
    name_team_home = soup.find('div', class_='progress-home progress-over').get_text()
    if not name_team_home:
        logging.warning('The name of the team that plays at home was not found.')
        return None
    indicators.append(name_team_home[1:-1])
    divas = (7, 9, 8, 10)
    for div in divas:
        result = soup.find_all('div', class_='progress-value')[div].get_text()
        if not result:
            logging.warning('team game values ​​not found.')
            return None
        elif '.'in result:
            indicators.append(float(result))
        else:
            indicators.append(int(result))
    result = soup.find_all('div', class_='progress-bar')[1]
    teams = re.findall(r'title="([\d]+)', str(result))
    indicators.append(teams)
    return indicators


def click(http):
    """
    заходит на все матчи данной команды и складывает все значения xg и shots всех матчей .
    :param http: ссылка страницы команды
    :return: возвращает список где первые два значения это значения данной команды а остальные две значения команд
    с которыми команда играла .
    """
    driver = webdriver.ChromeOptions()
    driver.add_argument('headless')
    driver.add_argument('window-size=1920x935')
    driver = webdriver.Chrome(chrome_options=driver)
    driver.get(http)
    logging.info('getting page function, click')
    try:
        quantity = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[2]/div/div[2]/div[1]/div").find_elements_by_tag_name("a")
        links = tuple(x.get_attribute("href") for x in quantity if "match" in x.get_attribute("href"))
    except NoSuchElementException:
        logging.warning("It is not possible to get links of all matches of a team.", http)
        return
    name_team = re.findall(r'team/([\w]+)', str(http))

    result = [0, 0, 0, 0]
    for link in links:
        driver.get(link)
        try:
            driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/div[1]/div/div[1]/div/label[3]').click()
        except NoSuchElementException:
            logging.warning("It’s not possible to click on the disclosure button of the game indicators.", http)
            return
        time.sleep(1)
        pes = driver.page_source
        if not pes:
            logging.warning('не получаю кода страницы для нажатия кнопки')
        page = pars(pes)
        if not page:
            logging.warning('функуия pars не возвращает данные ')
            continue
        if name_team == page[0]:
            result[0] += page[1]
            result[1] += page[2]
            result[2] += page[3]
            result[3] += page[4]
        else:
            result[0] += page[3]
            result[1] += page[4]
            result[2] += page[1]
            result[3] += page[2]
    return result


if __name__ == '__main__':

    for ligue in ligues:
        teams = lig(ligue)
        if not teams:
            continue
        for year in years:
            for team in teams:
                http = url + team + '/' + year
                parser = click(http)
                if not parser:
                    continue
                logging.info(parser)
