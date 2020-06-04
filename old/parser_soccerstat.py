import logging
from bs4 import BeautifulSoup
import requests

def soccerstat(url):
    logging.info(f"Getting data all teams for league: {url.split('=')[1]} from soccerstat...")
    response = requests.get(url).content
    soup = BeautifulSoup(response, "html")
    table = soup.find("table", id="btable")
    data = []
    try:
        for row in table.findAll("tr"):
            cols = [cell.text.strip().replace("\n", "").replace("\r", "") for cell in row.find_all("td")]
            if len(cols) > 3:
                data.append([item for item in cols if item])
    except AttributeError:
        soccerstat(url[:-5])
    logging.info(f"Done getting data for league: {url.split('=')[1]} from soccerstat!")
    return {item.pop(1): item[-4:] for item in data}



url_soccerstat = f"https://www.soccerstats.com/latest.asp?league="

all_teams_league_soccer = {year: soccerstat(url_soccerstat+f"{ligue_soccer}_{int(year)+1}") for year in years}