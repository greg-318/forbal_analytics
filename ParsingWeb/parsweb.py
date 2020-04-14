from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
import logging
from DataBase.models.player import Player


def click(url):
    """
    получает ссылку на страницу и нажимает на кнопки для расскрытия всех элементов таблицы с игроками
    возвращает код всей старницы с раскрытой таблицей
    :param url: - прямая ссылка на страницу
    :return:
    """

    driver = webdriver.ChromeOptions()
    driver.add_argument('headless')
    driver.add_argument('window-size=1920x935')
    driver = webdriver.Chrome(chrome_options=driver)
    driver.get(url)
    logging.info('getting page')

    try:
        driver.find_element_by_xpath("//div[@class='players margin-top jTable']/div[@class='table-control-panel']").click()
        flags = driver.find_elements_by_xpath("//div[@class='players margin-top jTable']//div[@class='table-popup']"
                                                  "//div[@class='table-popup-body']//div[@class='table-options']"
                                                   "//div[@class='table-options-row']/div[@class='row-display']")
        flags_position = (6, 11, 13, 14, 16, 18, 19, 20, 21, 22, 23)
        for key, flag in enumerate(flags):
            if key in flags_position:
                flag.click()

        driver.find_element_by_xpath("//div[@class='players margin-top jTable']//div[@class='table-popup']"
                                 "/div[@class='table-popup-footer']/a[@class='button-apply']").click()
    except NoSuchElementException:
        logging.warning("Problems with the push of a button.")
        return
    res = driver.page_source
    return res


def pars(html):
    """
    получает код всей страницы и возврашает только таблицу с игроками
    :param html: - код всей страницы в виде html
    :return:
    """
    soup = BeautifulSoup(html, 'html.parser')
    scripts = soup.find('div', class_='players margin-top jTable')
    if len(scripts) == 0:  # без len() отправляет в return.
        logging.info('Table with player data not found.')
        return

    table = scripts.find('tbody')
    if len(table) == 0:  # без len() отправляет в return.
        logging.warning('The table with the players is empty. ')
        return
    return table


def power(string):
    """
    получает строку в виде '1.02-2.06' и разделяет ее на две части, разделитель + либо -.
    :param string:
    :return:
    """
    if '-' in string:
        values = string.split('-')
        symbol = '-'
    else:
        values = string.split('+')
        symbol = '+'
    return {'value': float(values[0]), "dynamic": symbol+values[1]}


if __name__ == '__main__':

    url = 'https://understat.com/team/'
    teams = ("Augsburg", "Bayer Leverkusen", "Bayern Munich", "Borussia Dortmund",
    "Borussia M.Gladbach", "Darmstadt", "Eintracht Frankfurt", "FC Cologne",
    "Fortuna Duesseldorf", "Freiburg", "Hamburger SV", "Hannover 96", "Hertha Berlin",
    "Hoffenheim", "Ingolstadt", "Mainz 05", "Nuernberg", "Paderborn", "RasenBallsport Leipzig",
    "Schalke 04", "Union Berlin", "VfB Stuttgart", "Werder Bremen", "Wolfsburg")

    years = ('2014', '2015', '2016', '2017', '2018', '2019')
    information = Player()
    for year in years:
        for team in teams:
            http = url+team+'/'+year
            for i in pars(click(http)):
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
                else:
                    information.xg = {}
                if elem[11] != '0.00':
                    information.npxg = power(elem[11])
                else:
                    information.npxg = {}
                if elem[12] != '0.00':
                    information.xa = power(elem[12])
                else:
                    information.xa = {}





