from selenium import webdriver
from bs4 import BeautifulSoup
import selenium
from selenium.common.exceptions import WebDriverException
import logging
from DataBase.models.player import Player


def data(url):
    """

    :param url:
    :return:
    """
    information = Player()
    driver = webdriver.ChromeOptions()
    driver.add_argument('headless')
    driver.add_argument('window-size=1920x935')
    driver = webdriver.Chrome(chrome_options=driver)
    driver.get(url)
    logging.info('true url. go to page')

    try:
        driver.find_element_by_xpath("//div[@class='players margin-top jTable']/div[@class='table-control-panel']").click()
    except selenium.common.exceptions.NoSuchElementException:
        logging.warning("problems with pressing the button for additional arguments")
        return
    flags = driver.find_elements_by_xpath("//div[@class='players margin-top jTable']//div[@class='table-popup']"
                                              "//div[@class='table-popup-body']//div[@class='table-options']"
                                               "//div[@class='table-options-row']/div[@class='row-display']")
    if flags == 0:
        logging.info("No flags found.")
        return
    j = 0
    flags_position = (7, 12, 14, 15, 17, 19, 20, 21, 22, 23, 24)
    for flag in flags:
        j += 1
        if j in flags_position:
            flag.click()
    try:
        driver.find_element_by_xpath("//div[@class='players margin-top jTable']//div[@class='table-popup']"
                                 "/div[@class='table-popup-footer']/a[@class='button-apply']").click()
    except selenium.common.exceptions.NoSuchElementException:
        logging.warning("Problems with clicking the checkbox activation button.")
        return

    res = driver.page_source
    soup = BeautifulSoup(res, 'lxml')
    scripts = soup.find('div', class_='players margin-top jTable')
    if scripts == 0:
        logging.info('Table with player data not found.')
        return

    table = scripts.find('tbody')
    if len(table) != 0:  # не уверен что правильно сделал .
        for i in table:
            elem = [j.text for j in i]
            information.player = f"{elem[1]}_{url[-4:]}"
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
                data.xg = power(elem[10])
            if elem[11] != '0.00':
                data.npxg = power(elem[11])
            if elem[12] != '0.00':
                data.xa = power(elem[12])
    else:
        logging.info('The table with the players is empty. ')


def power(string):
    """

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


def web():
    """

    :return:
    """
    url = 'https://understat.com/team/'
    teams = ("Augsburg", "Bayer Leverkusen", "Bayern Munich", "Borussia Dortmund",
    "Borussia M.Gladbach", "Darmstadt", "Eintracht Frankfurt", "FC Cologne",
    "Fortuna Duesseldorf", "Freiburg", "Hamburger SV", "Hannover 96", "Hertha Berlin",
    "Hoffenheim", "Ingolstadt", "Mainz 05", "Nuernberg", "Paderborn", "RasenBallsport Leipzig",
    "Schalke 04", "Union Berlin", "VfB Stuttgart", "Werder Bremen", "Wolfsburg")

    years = ('2014', '2015', '2016', '2017', '2018', '2019')

    for year in years:
        for team in teams:
            http = url+team+'/'+year
            data(http)


if __name__ == '__main__':

    web()
