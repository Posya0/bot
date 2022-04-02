import requests
from bs4 import BeautifulSoup

def get_new(region, ans):
    """ в строку добавляются новые данные со статистикой по региону """
    s = region.text.split()
    ans += s[0] + ": " + s[1] + "\n"
    return ans

def in_regions(reg):
    """статистика короны в регионах """
    page = requests.get("https://coronavirusstat.ru")
    soup = BeautifulSoup(page.text, "html.parser")
    data_sost = soup.find("h6", {"class": "text-muted"}).find("strong")
    in_region = soup.find_all("div", {"class": "row border border-bottom-0 c_search_row"})
    ans = "По состоянию на " + data_sost.text + ":\n"
    path = soup
    for x in in_region:
        name = x.find("a")
        if reg.lower() in name.text.lower():
            path = x
            break
    if path == soup:
        return "не знаю такого региона"
    ans += "Регион: " + x.find("a").text + "\n"
    path = path.find("div", {"class": "p-1 col-7 row m-0"}).find("div", {"class": "p-1 col-4 col-sm-2"})
    ans = get_new(path, ans)
    path = path.find_next_sibling()
    ans = get_new(path, ans)
    path = path.find_next_sibling()
    ans = get_new(path, ans)
    path = path.find_next_sibling()
    ans = get_new(path, ans)
    return ans

def in_russia():
    """статистика по коронавирусу в России"""
    page = requests.get("https://coronavirusstat.ru")
    soup = BeautifulSoup(page.text, "html.parser")
    way = soup.find("div", {"class": "row justify-content-md-center"}).find_all("div",
                                                                                {"class": "col col-6 col-md-3 pt-4"})
    data_sost = soup.find("h6", {"class": "text-muted"}).find("strong")
    ans = "По состоянию на " + data_sost.text + ":\n"
    for x in way:
        s = x.text.split()
        ans += s[6] + ": " + s[4] + " " + s[5] + "(" + s[0] + " сегодня)\n"
    return ans

print(in_russia())
