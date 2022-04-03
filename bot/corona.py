import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
from matplotlib import pyplot as plt

page = requests.get("https://coronavirusstat.ru")
soup = BeautifulSoup(page.text, "html.parser")
way = soup.find("div", {"class": "row justify-content-md-center"}).find_all("div",
                                                                            {"class": "col col-6 col-md-3 pt-4"})
data_sost = soup.find("h6", {"class": "text-muted"}).find("strong")

def get_new(region, ans):
    """ в строку добавляются новые данные со статистикой по региону """
    s = region.text.split()
    ans += s[0] + ": " + s[1] + "\n"
    return ans

def in_regions(reg):
    """статистика короны в регионах """
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
    ans = "По состоянию на " + data_sost.text + ":\n"
    for x in way:
        s = x.text.split()
        ans += s[6] + ": " + s[4] + " " + s[5] + "(" + s[0] + " сегодня)\n"
    return ans


def in_world():
    """статистика по коронавирус в мире"""
    url_world = 'https://index.minfin.com.ua/reference/coronavirus/'
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    r = requests.get(url_world, headers=header)
    df = (pd.read_html(r.text))[0]
    ans = "По состоянию на " + data_sost.text + ":\n"
    ans+= "Всего случаев: "+ df.iat[0,1] + "\n"
    ans += "Умерло: " + df.iat[1, 1] + "\n"
    ans += "Вылечено: " + df.iat[0, 1] + "\n"
    ans += "Активные: " + df.iat[0, 1]

    url = url_world + (str(datetime.date.today()))[:-3] + '/'
    print(url)
    r = requests.get(url, headers=header)

    df = (pd.read_html(r.text))[0]
    df.rename(columns={'Всегозара­жений': 'Всего случаев', 'Смер­тельныеслучаи': 'Умерло',
                       'Выздоро­вевшие': 'Вылечено', 'Боле­ющие': 'Активных'}, inplace=True)

    fig = df.plot(x="Дата", y=["Всего случаев", "Умерло", "Вылечено", "Активных"])
    fig.set_ylabel('кол-во, [млн] ')
    plt.title('Статистика за месяц', fontsize=10)

    pic = fig.figure
    pic.savefig('images/covid.png')
    return ans

print(in_world())