from selenium import webdriver
from bs4 import BeautifulSoup
import logging


def data(url):
    """парсинг данных футболистов,
    url принимает ссылку на нужную страницу сайта """
    driver = webdriver.ChromeOptions()
    driver.add_argument('headless')  # запрет на открытие барузера
    driver.add_argument('window-size=1920x935')  # запрет на открытие барузера
    driver = webdriver.Chrome(chrome_options=driver)  # запускаеться веб драйвер и передаються настройки в хром .
    driver.get(url)

    try:
        driver.find_element_by_xpath("//div[@class='players margin-top jTable']/div[@class='table-control-panel']").click()  #раскрывает дополнительную таблицу
    except Exception:
        logging.warning("problems with pressing the button for additional arguments")
        return

    flags = driver.find_elements_by_xpath("//div[@class='players margin-top jTable']//div[@class='table-popup']"
                                               "//div[@class='table-popup-body']//div[@class='table-options']"
                                               "//div[@class='table-options-row']/div[@class='row-display']")  #находит все флажки в дополнительной таблице
    j = 0
    flags_position = [7, 12, 14, 15, 17, 19, 20, 21, 22, 23, 24]  # позиции фложков в дополнитерльной таблице
    for flag in flags:  # проход по всем флажкам. активация скрытых элементов основной таблицы
        j += 1
        if j in flags_position:
            flag.click()
    try:
        driver.find_element_by_xpath("//div[@class='players margin-top jTable']//div[@class='table-popup']"
                                 "/div[@class='table-popup-footer']/a[@class='button-apply']").click() # нажатие на кнопку apply в дополнительной таблице
    except Exception:
        logging.warning("Problems with clicking the checkbox activation button.")
        return

    res = driver.page_source  # получение кода всей траницы. со всеми данными игроков .
    soup = BeautifulSoup(res, 'lxml')
    try:
        scripts = soup.find('div', class_='players margin-top jTable') # получение данных таблицы игроков
    except Exception:
        logging.warning("div-'players margin-top jTable' not found.")
        return

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
        player['player'] = f"{elem[1]}_{url[-4:]}"  # доббавление к имени игрока год
        player['position'] = elem[2]
        player['appearances'] = int(elem[3])
        player['minutes'] = int(elem[4])
        player['goals'] = int(elem[5])
        player['npg'] = int(elem[6])
        player['a'] = int(elem[7])
        player['sh90'] = float('{:.2f}'.format(float(elem[8])))  # сокрашение цифр после точки до двух символов
        player['kp90'] = float('{:.2f}'.format(float(elem[9])))
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
        if elem[10] != None:  # если сетепрь не равен нулю то он отправляеться в базу данных .
            player['xg'] = power(elem[10])
        else:
            continue
        if elem[11] != None: # если сетепрь не равен нулю то он отправляеться в базу данных .
            player['NPxG'] = power(elem[10])
        else:
            continue
        if elem[11] != None: # если сетепрь не равен нулю то он отправляеться в базу данных .
            player['xa'] = power(elem[10])
        else:
            continue
        for key, value in player.items():  # отбирет только те данные у которых значения не равны нулю. и вставляет в словарь sending для отправки в бд.
            if value == 0 or None:
                continue
            if isinstance(value, dict):  # проверка значений элементов степени, на ноль .
                for z, x in value.items():
                    if x is not None:
                        sending[key] = value
                    else:
                        continue
            else:
                sending[key] = value
        logging.warning(sending)
        sending = {}
        elem = []

        player = {'player': None, 'year': None, 'position': None, 'appearances': None, 'minutes': None, 'goals': None,
                  'npg': None, 'a': None, 'sh90': None, 'kp90':  None,
                  'xg': {'value': None, "dynamic": None}, 'NPxG': {'value': None, "dynamic": None},
                  'xa': {'value': None, "dynamic": None}, 'xgchain': None,
                  'xgbuildup': None, 'xg90': None, 'npxg90': None, 'xa90': None, 'xg90xa90': None, 'npxg90xa90': None,
                  'xgchain90': None, 'xgbuildup90': None, 'yellow': None, 'red': None}  # присвоение всем ззначения None


def power(value):
    """ value принимает данные со степеью
    функция возвращает два значения, значение числа и его степень """
    if '-' in value:  # получение данных степени
        f = value
        for z in f:
            if z.isdigit():
                g = f.split('-') #данные получаюстья в виде 1,02-2,03 . в этой строке данные деляться на две чсти
                value = float(g[0])
                dynamic = f"-{g[1]}"
            break
        return {'value': value, 'dynamic' : dynamic}
    if '+' in value:  # получение данных степени
        f = value
        for z in f:
            if z.isdigit():
                g = f.split('+')
                value = float(g[0])
                dynamic = f"+{g[1]}"
            break
        return {'value': value, 'dynamic' : dynamic}


def web():
    """получение ссылок команд"""
    url = 'https://understat.com/team/'
    teams = ("Augsburg","Bayer Leverkusen", "Bayern Munich", "Borussia Dortmund",
    "Borussia M.Gladbach", "Darmstadt" ,"Eintracht Frankfurt","FC Cologne",
    "Fortuna Duesseldorf","Freiburg","Hamburger SV","Hannover 96","Hertha Berlin",
    "Hoffenheim","Ingolstadt","Mainz 05","Nuernberg","Paderborn","RasenBallsport Leipzig",
    "Schalke 04","Union Berlin","VfB Stuttgart","Werder Bremen","Wolfsburg")

    years = ('2014', '2015', '2016', '2017', '2018', '2019')

    for year in years:
        for team in teams:
            http = url+team+'/'+year
            data(http)


if __name__ == '__main__':

    web()

id = id
