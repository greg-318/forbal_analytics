import re
import time

import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.common.exceptions \
    import ElementClickInterceptedException, NoSuchElementException
import logging
from DataBase.models.team import Team


years = ('2014', '2015', '2016', '2017', '2018', '2019')
mini_url_soccerstats = "https://www.soccerstats.com/"
main_url_understat = "https://understat.com/"
main_url_soccerstat = "https://www.soccerstats.com/latest.asp?league="  # year + 1
names = {"russia": "RFPL", "england": "EPL",
                   "spain": "La_liga", "germany": "Bundesliga",
                   "italy": "Serie_A", "france": "Ligue_1"}


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    driver = webdriver.ChromeOptions()
    # driver.add_argument('headless')
    driver.add_argument('--start-maximized')
    driver = webdriver.Chrome(r'chromedriver.exe', options=driver)
    soccer_ligas = []
    under_ligas = []
    numbers = ("11", "13", "14", "15", "16", "17", "18")
    start_under = True

    for soccer_liga, under_liga in names.items():
        for index in range(len(years)):
            year = years[index]
            under_dict = dict()
            soccer_dict = dict()
            # print(soccer_liga, year)
            if year == years[0] and soccer_liga == 'russia':
                continue
            while True:  # если возникнут ошибки - перезапуск итерации для повторной попытки
                if years[index] != years[-1]:
                    soccer_url = main_url_soccerstat + soccer_liga + '_' + str(int(year) + 1)
                else:
                    soccer_url = main_url_soccerstat + soccer_liga
                under_url = main_url_understat + 'league/' + under_liga + '/' + year
                # print(under_url, soccer_url)
                if requests.get(soccer_url).status_code != 404:
                    soccer_soup = bs(requests.get(soccer_url).text, 'html.parser')
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
                                for tr in table:
                                    one_win = dict()
                                    tds = tr.find_all('td')
                                    tds = [td.text.replace('\r', '')
                                    .replace('\n', '') for td in tds]
                                    opponents = tds[1].split('-')
                                    count = tds[2].split('-')
                                    one_win.update({opponents[0].strip(): int(count[0])})
                                    one_win.update({opponents[1].strip(): int(count[1])})
                                    wins.append(one_win)
                                team[i] = wins
                        block_end = team[-4:]
                        team = team[0:11]
                        team.extend(block_end)
                        team.pop(0)
                        soccer_dict.update({year + '_' + team[0]: team[1:]})
                    # print('soccer_dict', soccer_dict)
                else:
                    logging.warning('Something happens with connection to soccerstats')
                    time.sleep(10)
                    continue
                try:
                    driver.get(under_url)
                    index += 1
                    if start_under:
                        driver.find_element_by_class_name('options-button').click()
                        for num in numbers:
                            driver.find_element_by_xpath(
                                "//div[@class='table-options']"
                                "/div[" + num + "]/div[@class='row-display']").click()
                        driver.find_element_by_class_name('button-apply').click()
                        start_under = False
                    bodies = driver.find_element_by_xpath('//table/tbody') \
                        .find_elements_by_xpath('tr')
                except ElementClickInterceptedException:
                    logging.warning('Click error')
                    time.sleep(10)
                    continue
                except NoSuchElementException:
                    logging.warning('Element is not available or connection lost, restart the script')
                    time.sleep(10)
                    continue
                else:
                    under_coms = []
                    for j in range(len(bodies)):
                        tds = bodies[j].find_elements_by_tag_name('td')
                        tds = [td.text for td in tds[1:]]
                        for i in range(len(tds)):
                            if '+' in tds[i] and i != 12 :
                                temp =  tds[i].split('+')
                                tds[i] = {'value': float(temp[0]), 'dynamic': '+' + temp[1]}
                            elif '-' in tds[i] and i != 12 and re.match(r'\d', tds[i]) is not None:
                                temp = tds[i].split('-')
                                tds[i] = {'value': float(temp[0]), 'dynamic': '-' + temp[1]}
                        under_dict.update({year + '_' + tds[0]: tds[1:]})
                    # print('under_dict', under_dict)
                    all_ind = []
                    for team, indic in soccer_dict.items():
                        for key, value in under_dict.items():
                            if indic[0:6] == value[0:6]:
                                all_ind = [
                                    team, indic[0], indic[1], indic[2], indic[3], indic[4], indic[5], indic[6],
                                    indic[7], indic[8], indic[-4], indic[-3], indic[-2], indic[-1], value[7],
                                    value[8], value[9], value[10], value[11], value[12], value[13], value[14],
                                    value[15], value[16]
                                ]
                                mongo = Team(
                                    name = str(all_ind[0]),
                                    gp = int(all_ind[1]),
                                    w = int(all_ind[2]),
                                    d = int(all_ind[3]),
                                    l = int(all_ind[4]),
                                    gf = int(all_ind[5]),
                                    ga = int(all_ind[6]),
                                    gd = str(all_ind[7]),
                                    pts = int(all_ind[8]),
                                    form = all_ind[9],
                                    ppg = float(all_ind[10]),
                                    last8 = float(all_ind[11]),
                                    cs = str(all_ind[12]),
                                    fts = str(all_ind[13]),
                                    xg = all_ind[14],
                                    npgx = all_ind[15],
                                    xga = all_ind[16],
                                    npxga = all_ind[17],
                                    npxgd = all_ind[18],
                                    ppda = float(all_ind[19]),
                                    oppda = float(all_ind[20]),
                                    dc = int(all_ind[21]),
                                    odc = int(all_ind[22]),
                                    xpts = all_ind[23]
                                )
                                # здесь будет запись в бд
                                # print('mongo', mongo.dict())
                    break  # остановка цикла, в котором решаются ошибки







