from selenium import webdriver


def get_content(url):
    # driver.get("https://www.sofascore.com/granada-espanyol/ogbsEAn")
    driver.get(url)
    driver.implicitly_wait(20)
    rounds = driver.find_element_by_css_selector('#pjax-container-main > div > div.page-container > div.l__grid.js-page-layout > div.l__col--1 > div.js-event-page-statistics-container > div > ul')
    rounds_li = rounds.find_elements_by_tag_name("li")
    names = driver.find_element_by_class_name("js-event-page-event-name").text
    result_match = driver.find_element_by_class_name("u-t2 u-t16").text
    print("name: ", names)
    print("result: ", result_match)
    for row in rounds_li:
        row.click()
        text = driver.find_element_by_css_selector('#pjax-container-main > div > div.page-container > div.l__grid.js-page-layout > div.l__col--1 > div.js-event-page-statistics-container > div > div').text
        result = text.split("\n")
        new_list = []
        while result:
            t = [result.pop(0) for _ in range(3)]
            new_list.append(t)
        print(new_list)


def get_all_links():
    links_matches = []
    i = 0
    while True:
        i += 1
        try:
            list_wrapper = driver.find_element_by_class_name('list-wrapper')
            elems = list_wrapper.find_elements_by_tag_name('a')
            links_matches.extend([elem.get_attribute("href") for elem in elems][1:])
            # print([elem.get_attribute("href") for elem in elems][1:])
            driver.implicitly_wait(20)
            print(f"Page - {i} done")
            previous = driver.find_element_by_css_selector('#__next > main > div > div.Content__PageContainer-sc-14479gi-0.iPKjyT > div > div.Col-pm5mcz-0.jrtcdI > div.u-mV12 > div > div.Tabs__Content-vifb7j-1.jppjfQ > div > div > div > div:nth-child(1) > div > div.Cell-decync-0.styles__EventListHeader-b3g57w-0.bSxBJT > div:nth-child(1) > div')
            previous.click()
            driver.implicitly_wait(20)
        except Exception as e0:
            print(e0)
            break
    return set(links_matches)


if __name__ == "__main__":
    driver = webdriver.ChromeOptions()
    driver.add_argument('headless')
    driver.add_argument('window-size=1920x935')
    driver = webdriver.Chrome(executable_path="./chromedriver", chrome_options=driver)

    leagues = {"RFPL": "russia/premier-liga/203", "EPL": "england/premier-league/17", "La_liga": "spain/laliga/8",
               "Bundesliga": "germany/bundesliga/35", "Serie_A": "italy/serie-a/23", "Ligue_1": "france/ligue-1/34"}
    link = "https://www.sofascore.com/tournament/football/"
    try:
        for league in leagues.values():
            print(link+league)
            driver.get(link+league)
            driver.implicitly_wait(30)
            print(driver.find_elements_by_css_selector("*"))
            years_dropdown = driver.find_element_by_css_selector('#__next > main > div > div.Content__PageContainer-sc-14479gi-0.iPKjyT > div > div.Col-pm5mcz-0.jrtcdI > div.Cell-decync-0.styles__HeaderInfoCell-sc-1gqlp92-0.cEyplv > div.Section-sc-1a7xrsb-0.styles__MainSection-sc-1gqlp92-4.eYQPZb.u-mH12 > div > div > div.Section-sc-1a7xrsb-0.styles__SeasonSelectContainer-sc-1gqlp92-2.calSYU > div > div > div')
            years_dropdown.click()
            driver.implicitly_wait(10)
            years_list = years_dropdown.find_elements_by_tag_name("li")[:7]
            start_year = 2020
            for index, year in enumerate(years_list):
                # driver.implicitly_wait(20)
                # years_dropdown.click()
                # if index != 0:
                #     print(dir(year))
                #     year.click()
                # driver.implicitly_wait(20)
                # ligue_matches = get_all_links()
                # start_year -= 1
                get_content("https://www.sofascore.com/granada-espanyol/ogbsEAn")
    finally:
        driver.quit()
