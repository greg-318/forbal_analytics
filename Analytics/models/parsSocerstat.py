import requests
import json
from bs4 import BeautifulSoup


r = 'https://understat.com/league/EPL'
g = 'https://www.soccerstats.com/trends.asp?league=spain'

hed = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}



req = requests.get(g, headers=hed)
soup = BeautifulSoup(req.content, 'html.parser')
#f = soup.find_all('div', class_='tabberlive')

print(soup)
