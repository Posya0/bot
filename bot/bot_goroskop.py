from bs4 import BeautifulSoup
from PIL import Image
import requests

if __name__ == "__main__":
    znak = {'Овен': 'oven', 'Телец': 'telets', 'Близнецы': 'bliznetsi', 'Рак': 'rac', 'Лев': 'lev', 'Дева': 'deva', 'Весы': 'vesy', 'Скорпион': 'scorpion', 'Стрелец': 'strelets', 'Козерог': 'kozerog', 'Водолей': 'vodoley', 'Рыбы': 'riby'}
    inp_znak = input().capitalize()
    time = {'Сегодня': 'day', 'Неделя': 'week', 'Месяц': 'month'}
    inp_time = input().capitalize()

    request = requests.get("https://www.astrostar.ru/horoscopes/main/" + znak[inp_znak] + '/' + time[inp_time] + ".html")
    bs = BeautifulSoup(request.text, "html.parser")
    blok = bs.find("p")
    print(blok.text)

    picture = 'C:\\Users\\podvo\\source\\Posya0\\bot\\znaki_pictures\\' + inp_znak + '.jpg'
    img=Image.open('C:\\Users\\podvo\\source\\Posya0\\bot\\znaki_pictures\\Oven.jpg')
    img.show()