# Стягивает информацию о результатах матчей всех команд с сайта understat.com
import logging
from selenium import webdriver
from bs4 import BeautifulSoup
from config import url, years, ligues
from ParsingWeb.parsweb import lig
import sys
sys.path.append("..\DataBase")
from mongo_default import MongoDefault
from Analytics.models.game_indicators import GameIndicators, TeamIndicators


if __name__ == "__main__":

    driver = webdriver.ChromeOptions()
    driver.add_argument('headless')
    driver.add_argument('window-size=1920x935')
    driver = webdriver.Chrome(chrome_options=driver)

    for ligue in ligues:
        teams = lig(ligue)
        for year in years:
            for team in teams:
                http = url + team + '/' + year
                driver.get(http)

                quantity = driver.find_elements_by_tag_name("a")
                links = tuple(x.get_attribute("href") for x in quantity if "match" in str(x.get_attribute("href")))
                if not links:
                    logging.warning("not possible to find team matches")
                    continue
                for link in links:
                    driver.get(link)
                    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/div[1]/div/div[1]/div/label[3]'
                                                 ).click()
                    html = driver.page_source
                    soup = BeautifulSoup(html, 'html.parser')
                    team = TeamIndicators()
                    team1 = {}
                    team2 = {}
                    draw = 0
                    table = soup.find_all('div', class_='progress-bar')
                    for item, ti in zip(table, team.dict().keys()):
                        if 'CHANCES' in str(item.find_all('div', class_='progress-title')):
                            data = tuple(x.get('title') for x in item.find_all('div')if x.get('title'))
                            data = tuple(i[:-1] for i in data)
                        else:
                            data = tuple(x.text for x in item.find_all('div', class_='progress-value'))
                        team1[ti] = data[0]
                        team2[ti] = data[-1]
                        if len(data) == 3:
                            draw = data[1]

                    d = soup.find('tbody')
                    team1['players'] = sum([[y.text for i, y in enumerate(x) if i == 1]
                                            for x in d.find_all('tr')if "Sub" not in str(x)], [])

                    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[4]/div/div[1]/div/label[2]').click()
                    page_plaers = driver.page_source
                    page_plaers_way = BeautifulSoup(page_plaers, 'html.parser')
                    plaers_wau = page_plaers_way.find('tbody')
                    team2['players'] = sum([[y.text for i, y in enumerate(x) if i == 1]
                                            for x in plaers_wau.find_all('tr') if "Sub" not in str(x)], [])

                    match = f'{year}_{team1["name"]}_{team1["g"]}{team2["g"]}_{team2["name"]}'
                    result = GameIndicators(match=match, chances_draw=draw, team1=team1, team2=team2)
                    with MongoDefault('gameIndicators') as md:
                        response = md.insertUpdate(match, result.dict())
