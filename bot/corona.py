import datetime
import re

import requests
from bs4 import BeautifulSoup
import pandas as pd
from matplotlib import pyplot as plt

page = requests.get("https://coronavirusstat.ru")
soup = BeautifulSoup(page.text, "html.parser")
way = soup.find("div", {"class": "row justify-content-md-center"}).find_all("div",
                                                                            {"class": "col col-6 col-md-3 pt-4"})
data_sost = soup.find("h6", {"class": "text-muted"}).find("strong")

"""сайт блокирует доступ(ошибка 403),
    поэтому мы "притворимся" браузером """

url_world = 'https://index.minfin.com.ua/reference/coronavirus/'
header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }

def get_new(region, ans):
    """ в строку добавляются новые данные со статистикой по региону """
    s = region.text.split()
    ans += s[0] + ": " + s[1] + "\n"
    return ans


def grafic(url_end):
    """ строим график"""
    """получаем ссылку"""

    url = url_world + url_end + (str(datetime.date.today()))[:-3] + '/'
    print(url)
    r = requests.get(url, headers=header)

    """достаем таблицу с сайта, скрываем 
    последний столбец и переименовываем столбцы"""

    if url_end == '':
        flag = 0
    else:
        flag = 1

    df = (pd.read_html(r.text))[flag]
    df.rename(columns={'Всегозара­жений': 'Всего случаев', 'Смер­тельныеслучаи': 'Умерло',
                       'Выздоро­вевшие':'Вылечено','Боле­ющие':'Активных'}, inplace=True)

    """делаем график"""

    fig = df.plot(x="Дата", y=["Всего случаев", "Умерло", "Вылечено", "Активных"])
    fig.set_ylabel('кол-во, [млн] ')
    plt.title('Статистика за месяц', fontsize=10)

    """сохраняем график"""

    pic = fig.figure
    pic.savefig('files/covid.png')


def find_region(city):
    """определить регион по городу"""
    """достаем таблицу, забираем из нее 2 колонки:
     город и область"""

    df = (pd.read_html('https://hramy.ru/regions/city_abc.htm'))[0]
    df.drop(("Район/подчинение"), axis=1, inplace=True)
    df.drop(("Код"), axis=1, inplace=True)
    df.drop(("Центр"), axis=1, inplace=True)

    """ находим область по городу"""

    city = city.title()

    region = ''
    for i in range(df.shape[0]):
        # print(df.iat[i, 0])
        if df.iat[i, 0] == city:
            region = df.iat[i, 1]
    res = (re.findall(r'^\w+', region))[0]

    return res



def is_city(city):
    """Проверяем, существует ли город"""
    df = (pd.read_html('https://hramy.ru/regions/city_abc.htm'))[0]
    df.drop(("Район/подчинение"), axis=1, inplace=True)
    df.drop(("Код"), axis=1, inplace=True)
    df.drop(("Центр"), axis=1, inplace=True)

    for i in range(df.shape[0]):
        if city.lower() in (df.iat[i, 0]).lower():
            return True
    return False


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
    grafic('geography/russia/')
    return ans


def in_world():
    """статистика по коронавирус в мире"""
    r = requests.get(url_world, headers=header)
    df = (pd.read_html(r.text))[0]
    ans = "По состоянию на " + data_sost.text + ":\n"
    ans+= "Всего случаев: "+ df.iat[0,1] + "\n"
    ans += "Умерло: " + df.iat[1, 1] + "\n"
    ans += "Вылечено: " + df.iat[0, 1] + "\n"
    ans += "Активные: " + df.iat[0, 1]
    grafic('')
    return ans

