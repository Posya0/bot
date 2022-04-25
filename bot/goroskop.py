from bs4 import BeautifulSoup
import requests

znak = {'Овен': 'oven', 'Телец': 'telets', 'Близнецы': 'bliznetsi', 'Рак': 'rac', 'Лев': 'lev', 'Дева': 'deva', 'Весы': 'vesy', 'Скорпион': 'scorpion', 'Стрелец': 'strelets', 'Козерог': 'kozerog', 'Водолей': 'vodoley', 'Рыбы': 'riby'}
time = {'Сегодня': 'day', 'Неделя': 'week', 'Месяц': 'month'}


goroskop_spisok = [
    'овен',
    'телец',
    'близнецы',
    'рак',
    'лев',
    'дева',
    'весы',
    'скорпион',
    'стрелец',
    'козерог',
    'водолей',
    'рыбы'
]


def is_zhak(s):
    """проверка, явлеяется ли строка знаком"""
    for znak in goroskop_spisok:
        if znak == s.lower():
            return True
    return False



def goroskop_(inp_znak, inp_time):
    """получение гороскопа"""
    request = requests.get("https://www.astrostar.ru/horoscopes/main/" + znak[inp_znak] + '/' + time[inp_time] + ".html")
    bs = BeautifulSoup(request.text, "html.parser")
    blok = bs.find("p")
    return blok.text

