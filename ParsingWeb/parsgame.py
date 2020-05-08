import re
import time
import logging
from selenium import webdriver
from bs4 import BeautifulSoup
from config import url, years, ligues
from parsweb import lig
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')


def pars(html):
    """
    :param html: - получает html код страницы .
    :ball_possesion: - получает три значения changes .
    :return: - возвращает список где первый элемент это название команды чьи значения указаны с левой стороны таблицы
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
    values = (7, 9, 8, 10)
    for value in values:
        result = soup.find_all('div', class_='progress-value')[value].get_text()
        if not result:
            logging.warning('team game values not found.')
            continue
        if '.'in result:
            indicators.append(float(result))
        else:
            indicators.append(int(result))
    result = soup.find_all('div', class_='progress-bar')[1]
    ball_possesion = re.findall(r'title="([\d]+)', str(result)) # пока не работаем с ними.
    indicators.append(ball_possesion)
    return indicators


if __name__ == '__main__':

    while True:
        for ligue in ligues:
            teams = lig(ligue)
            for year in years:
                for team in teams:
                    http = url + team + '/' + year
                    driver = webdriver.ChromeOptions()
                    driver.add_argument('headless')
                    driver.add_argument('window-size=1920x935')
                    driver = webdriver.Chrome(chrome_options=driver)
                    driver.get(http)
                    quantity = driver.find_elements_by_tag_name("a")
                    links = tuple(x.get_attribute("href")for x in quantity if "match" in str(x.get_attribute("href")))
                    if not links:
                        logging.warning("not possible to find team matches")
                        continue
                    name_team = re.findall(r'team/([\w]+)', str(http))  # название домашней команды .
                    data = [0, 0, 0, 0]
                    for link in links:
                        driver.get(link)
                        driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/div[1]/div/div[1]/div/label[3]'
                                                     ).click()
                        pes = driver.page_source
                        page = pars(pes)
                        if not page:
                            continue
                        if name_team == page[0]:
                            data[0] += page[1]
                            data[1] += page[2]
                            data[2] += page[3]
                            data[3] += page[4]
                        else:
                            data[0] += page[3]
                            data[1] += page[4]
                            data[2] += page[1]
                            data[3] += page[2]
                    print(data)
        time.sleep(345600)
