from bs4 import BeautifulSoup
import requests

znak = {'овен': 'oven', 'телец': 'telets', 'близнецы': 'bliznetsi', 'рак': 'rac', 'лев': 'lev', 'дева': 'deva', 'весы': 'vesy', 'скорпион': 'scorpion', 'стрелец': 'strelets', 'козерог': 'kozerog', 'водолей': 'vodoley', 'рыбы': 'riby'}
time = {'Сегодня': 'day', 'Неделя': 'week', 'Месяц': 'month'}


def is_zhak(s):
    """проверка, явлеяется ли строка знаком"""
    for znaki in znak.keys():
        if znaki == s.lower():
            return True
    return False


def goroskop_(inp_znak, inp_time):
    """получение гороскопа"""
    request = requests.get("https://www.astrostar.ru/horoscopes/main/" + znak[inp_znak.lower()] + '/' + time[inp_time] + ".html")
    bs = BeautifulSoup(request.text, "html.parser")
    blok = bs.find("p")
    return blok.text

