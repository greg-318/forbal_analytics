from selenium import webdriver
from bs4 import BeautifulSoup


def data(url):

    driver = webdriver.ChromeOptions()
    driver.add_argument('headless')  # запрет на открытие барузера
    driver.add_argument('window-size=1920x935')  # запрет на открытие барузера
    driver = webdriver.Chrome(chrome_options=driver)  # запрет на открытие барузера

    driver.get(url)
    driver.find_element_by_xpath("//div[@class='players margin-top jTable']/div[@class='table-control-panel']").click()  #раскрывает дополнительную таблицу
    click_flag = driver.find_elements_by_xpath("//div[@class='players margin-top jTable']//div[@class='table-popup']"
                                               "//div[@class='table-popup-body']//div[@class='table-options']"
                                               "//div[@class='table-options-row']/div[@class='row-display']")  #находит все флажки в дополнительной талице
    j = 0
    for i in click_flag:  # проход по всем флажкам. активация скрытых элементов основной таблицы
        j += 1
        if j == 7:
            i.click()
        if j == 12:
            i.click()
        if j == 14:
            i.click()
        if j == 15:
            i.click()
        if j == 17:
            i.click()
        if j == 19:
            i.click()
        if j == 20:
            i.click()
        if j == 21:
            i.click()
        if j == 22:
            i.click()
        if j == 23:
            i.click()
        if j == 24:
            i.click()

    driver.find_element_by_xpath("//div[@class='players margin-top jTable']//div[@class='table-popup']"
                                 "/div[@class='table-popup-footer']/a[@class='button-apply']").click() # нажатие на кнопку apply в дополнительной таблице

    res = driver.page_source  # получение кода всей траницы. со всеми данными игроков .
    soup = BeautifulSoup(res, 'lxml')
    scripts = soup.find('div', class_='players margin-top jTable') # получение данных таблицы игроков

    player = {'player': None, 'year': None, 'position': None, 'appearances': None, 'minutes': None, 'goals': None,
                  'npg': None, 'a': None, 'sh90': None, 'kp90': None, 'xg': {'value': None, "dynamic": None},
              'NPxG': {'value': None, "dynamic": None}, 'xa': {'value': None, "dynamic": None}, 'xgchain': None,
                  'xgbuildup': None, 'xg90': None, 'npxg90': None, 'xa90': None, 'xg90xa90': None, 'npxg90xa90': None,
                  'xgchain90': None, 'xgbuildup90': None, 'yellow': None, 'red': None}  # в этом словаре будут присваиваться данные одного игрока

    table = scripts.find('tbody')  #данные таблицы игроков
    elem = []  # Будут сохраняться все данные одного игрока
    sending = {}  # Будут сохраняться только те данные игрока у которых значения не равны нулю готовые для отправки в БД.
    for i in table:
        for j in i:
            elem.append(j.text)
        if '-' in elem[10]:        # получение данных степени
            f = elem[10]
            for z in f:
                if z.isdigit():
                    g = f.split('-')
                    player['xg']['value'] = g[0]
                    player['xg']['dynamic'] = f"-{g[1]}"
                break

        if '+' in elem[10]:     # получение данных степени
            f = elem[10]
            for z in f:
                if z.isdigit():
                    g = f.split('+')
                    player['xg']['value'] = g[0]
                    player['xg']['dynamic'] = f"+{g[1]}"
                    break

        if '-' in elem[11]:   # получение данных степени
            f = elem[11]
            for z in f:
                if z.isdigit():
                    g = f.split('-')
                    player['NPxG']['value'] = g[0]
                    player['NPxG']['dynamic'] = f"-{g[1]}"
                break

        if '+' in elem[11]:   # получение данных степени
            f = elem[11]
            for z in f:
                if z.isdigit():
                    g = f.split('+')
                    player['NPxG']['value'] = g[0]
                    player['NPxG']['dynamic'] = f"+{g[1]}"
                break

        if '-' in elem[12]:   # получение данных степени
            f = elem[12]
            for z in f:
                if z.isdigit():
                    g = f.split('-')
                    player['xa']['value'] = g[0]
                    player['xa']['dynamic'] = f"-{g[1]}"
                    break

        if '+' in elem[12]:   # получение данных степени
            f = elem[12]
            for z in f:
                if z.isdigit():
                    g = f.split('+')
                    player['xa']['value'] = g[0]
                    player['xa']['dynamic'] = f"+{g[1]}"
                    break

        player['player'] = f"{elem[1]}_{url[-4:]}"  # доббавление к имени игрока год
        player['position'] = elem[2]
        player['appearances'] = int(elem[3])
        player['minutes'] = int(elem[4])
        player['goals'] = int(elem[5])
        player['npg'] = int(elem[6])
        player['a'] = int(elem[7])
        player['sh90'] = float('{:.2f}'.format(float(elem[8])))  # сокрашение цифр после точки до двух символов
        player['kp90'] = float('{:.2f}'.format(float(elem[9])))
        #player['xg'] = elem[10]   # dict
        #player['NPxG'] = elem[11]   #dict
        #player['xa'] = elem[12] # dict
        player['xgchain'] = float('{:.2f}'.format(float(elem[13])))
        player['xgbuildup'] = float('{:.2f}'.format(float(elem[14])))
        player['xg90'] = float('{:.2f}'.format(float(elem[15])))
        player['npxg90'] = float('{:.2f}'.format(float(elem[16])))
        player['xa90'] = float('{:.2f}'.format(float(elem[17])))
        player['xg90xa90'] = float('{:.2f}'.format(float(elem[18])))
        player['npxg90xa90'] = float('{:.2f}'.format(float(elem[19])))
        player['xgchain90'] = float('{:.2f}'.format(float(elem[20])))
        player['xgbuildup90'] = float('{:.2f}'.format(float(elem[21])))
        player['yellow'] = int(elem[22])
        player['red'] = int(elem[23])

        for key, item in player.items():  # отбирет только те данные у которых значения не равны нулю. и вставляет в словарь sending для отправки в бд.
            if item is None:
                continue
            if item == 0:
                continue
            if type(item) == dict:  # проверка значений элементов степени, на ноль .
                for z, x in item.items():
                    if x is not None:
                        sending[key] = item
                    else:
                        continue
            else:
                sending[key] = item
        print(sending)
        sending = {}
        elem = []

        player = {'player': None, 'year': None, 'position': None, 'appearances': None, 'minutes': None, 'goals': None,
                  'npg': None, 'a': None, 'sh90': None, 'kp90':  None,
                  'xg': {'value': None, "dynamic": None}, 'NPxG': {'value': None, "dynamic": None},
                  'xa': {'value': None, "dynamic": None}, 'xgchain': None,
                  'xgbuildup': None, 'xg90': None, 'npxg90': None, 'xa90': None, 'xg90xa90': None, 'npxg90xa90': None,
                  'xgchain90': None, 'xgbuildup90': None, 'yellow': None, 'red': None}  # присвоение всем ззначения None


def web():
    """получение ссылок команд"""
    url = 'https://understat.com/team/'
    team = ["Augsburg","Bayer Leverkusen", "Bayern Munich", "Borussia Dortmund",
    "Borussia M.Gladbach", "Darmstadt" ,"Eintracht Frankfurt","FC Cologne",
    "Fortuna Duesseldorf","Freiburg","Hamburger SV","Hannover 96","Hertha Berlin",
    "Hoffenheim","Ingolstadt","Mainz 05","Nuernberg","Paderborn","RasenBallsport Leipzig",
    "Schalke 04","Union Berlin","VfB Stuttgart","Werder Bremen","Wolfsburg"]

    yar = ['2014','2015','2016','2017','2018','2019']

    for i in yar:
        for j in team:
            http = url+j+'/'+i
            data(http)


if __name__ == '__main__':

    web()












