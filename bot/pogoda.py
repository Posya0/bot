import PIL.Image as Image
import os.path
import datetime
import requests
import json

key = "6d3f1f18d553999a8ac72752aa8e780e"

"""словарь для нахождения словесного описания силы ветра"""
words = {(0.0, 0.2): 'Штиль', (0.3, 1.5): 'Тихий', (1.6, 3.3): 'Лёгкий', (3.4, 5.4): 'Слабый', (5.5, 7.9): 'Умеренный',
         (8.0, 10.7): 'Свежий', (10.8, 13.8): 'Сильный', (13.9, 17.1): 'Крепкий', (17.2, 20.7): 'Очень_крепкий',
         (20.8, 24.4): 'Шторм', (24.5, 28.4): 'Сильный_шторм', (28.5, 32.6): 'Жестокий_шторм', (33.0, 100.0): 'Ураган'}


def wind_type(wind):
    """функция для нахождения словесного описания силы ветра"""
    for i in words.keys():
        if i[0] <= wind <= i[1]:
            return words[i]


def deg_into_word(deg):
    """определение направления ветра"""
    directions = ['северный', 'северо-восточный', 'восточный', 'юго-восточный', 'южный',
                  'юго-западный', 'западный', 'северл-западный']
    deg = int(deg * 8 / 360)
    deg = (deg + 8) % 8
    return directions[deg]


def get_weather_for_now(city):
    """ получение строки с погодой на данный момент"""
    """"получаем данные по городу на данный момент"""

    data = requests.get("http://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + key + "&units=metric&lang=ru")
    data = json.loads(data.text)

    """ получаем картинку с нужным изображением погоды"""

    image_url = 'http://openweathermap.org/img/w/{}.png'.format(data['weather'][0]['icon'])
    image = requests.get(image_url, stream=True)

    """сохраняем картинку"""

    file_name = 'files/img_for_now.png'
    if os.path.exists(file_name) == False:
        with open(file_name, 'wb') as f:
            f.write(image.content)

    """формируем сообщение с данными о погоде"""

    ans = "Погода сейчас \n"
    ans += "{}, температура {} - {} (°C)\n".format(data['weather'][0]['description'], data['main']['temp_min'], data['main']['temp_max'])
    ans += f"Давление: {data['main']['pressure']} мм рт.ст., влажность {data['main']['humidity']}%\n"
    ans += f"Ветер: {wind_type(data['wind']['speed'])}, {data['wind']['speed']} м/с, {deg_into_word(data['wind']['deg'])}"
    return ans


"""функция объединения картинок"""
def unit_img(img, number):
    """в блок для 4 или 5 фоток(img), добавляется новая картинка
    ее позиция определяется ее порядковым номером(numer)"""
    file_name = 'file' + str(number) + '.png'
    img1 = Image.open(file_name)
    img.paste(img1, (number * 50, 0))
    return img


def get_weather_for_5(city):
    """получение строки с погодой на 5 дней"""
    """"получаем данные по городу на 5 дней"""

    data = requests.get(
        "https://api.openweathermap.org/data/2.5/forecast?q=" + city + "&appid=" + key + "&units=metric&lang=ru")
    data = json.loads(data.text)

    """формируем начало сообщения"""

    ans = "Погода с {} по {}: \n".format((data['list'][0]['dt_txt'])[:-9], (data['list'][39]['dt_txt'])[:-9])
    day_temp = ""
    night_temp = ""

    """создаем "блок" для 5 фотографий 
    (пустое изображение, в которое поместится 5 фото с погодой)"""

    img = Image.new('RGB', (250, 50))

    """заполняем этот блок,
    дописываем сообщение """

    for i in data['list']:

        """определяем время суток:
        00:00:00 - ночь
        12:00:00 - день"""

        if (i['dt_txt'])[-8:] == '00:00:00':

            """добавляем в строку с данными о погде ночью новую температуру"""

            night_temp += "/{}°C/".format(i['main']['temp'])
        elif (i['dt_txt'])[-8:] == '12:00:00':

            """ получаем картинку с нужным изображением погоды"""

            image_url = 'http://openweathermap.org/img/w/{}.png'.format(i['weather'][0]['icon'])
            image = requests.get(image_url, stream=True)

            """ сохраняем картинку,
            всего будет 5 картинок с названиями fileЧИСЛО.png,
            они сохраняются по очереди"""

            for x in range(5):

                file_name = 'file' + str(x) + '.png'

                """проверяем, не занято ли название"""

                if not os.path.exists(file_name):
                    with open(file_name, "wb") as f:
                        f.write(image.content)

                    """ добавляем картинку в блок"""

                    img = unit_img(img, x)
                    break

            """добавляем в строку с данными о погде днем новую температуру"""

            day_temp += "/{}°C/".format(i['main']['temp'])

    """сохраняем  заполненый блок"""

    img.save('files/img_for_5.png')

    """удаляем "одиночные" картинки"""

    for n in range(5):
        file_name = 'file' + str(n) + '.png'
        if os.path.exists(file_name):
            os.remove(file_name)

    """дописываем ответ"""

    ans += day_temp + "ДЕНЬ\n" + night_temp + "НОЧЬ\n"
    return ans


def get_weather_for_time(n, img, data):
    """получение строки и картинки о погоде в определенное время"""
    """ получаем картинку с нужным изображением погоды"""

    image_url = 'http://openweathermap.org/img/w/{}.png'.format(data['list'][n]['weather'][0]['icon'])
    image = requests.get(image_url, stream=True)

    """ сохраняем картинку,
        всего будет 4 картинки с названиями fileЧИСЛО.png,
        они сохраняются по очереди"""

    for x in range(4):
        file_name = 'file' + str(x) + '.png'
        if os.path.exists(file_name) == False:
            with open(file_name, 'wb') as f:
                f.write(image.content)

            """добавляем картинку в блок"""

            img = unit_img(img, x)
            break

    """формируем часть сообщения о погоде в конкретное время дня"""

    ans = "///{}, Температура: {} - {} (°C)\n".format(data['list'][n]['weather'][0]['description'],
                                                      data['list'][n]['main']['temp_min'],
                                                      data['list'][n]['main']['temp_max'])
    ans += f"///Давление: {data['list'][n]['main']['pressure']} мм рт.ст., Влажность {data['list'][n]['main']['humidity']}%\n"
    ans += f"///Ветер: {wind_type(data['list'][n]['wind']['speed'])}, {data['list'][n]['wind']['speed']} м/с, {deg_into_word(data['list'][n]['wind']['deg'])}\n "
    return ans, img


def get_weather_for_day(city):
    """получение строки с погодой на завтра"""
    """ получаем картинку с нужным изображением погоды"""

    data = requests.get(
        "https://api.openweathermap.org/data/2.5/forecast?q=" + city + "&appid=" + key + "&units=metric&lang=ru&cnt=19")
    data = json.loads(data.text)

    """создаем строки, которые будут хранить инфу 
    по погое в разное время суток"""

    morning_w = ''
    day_w = ''
    evening_w = ''
    night_w = ''

    """определяем дату завтрашнего дня"""

    d = datetime.date.today() + datetime.timedelta(days=1)

    """создаем "блок" на 4 картинки"""

    img = Image.new('RGB', (200, 50))

    """формируем начало сообщения"""

    ans = "Погода на завтра:\n\n"

    """заполняем строки с инфой по времени суток
    06:00:00 - утро
    12:00:00 - день
    18:00:00 - вечер
    00:00:00 след.дня - ночь"""

    for i in range(19):

        if (data['list'][i]['dt_txt']) == str(d) + ' 06:00:00':
            morning_w, img = get_weather_for_time(i, img, data)
            ans += "/{}°C/".format(data['list'][i]['main']['temp'])
        if (data['list'][i]['dt_txt']) == str(d) + ' 12:00:00':
            day_w, img = get_weather_for_time(i, img, data)
            ans += "/{}°C/".format(data['list'][i]['main']['temp'])
        if (data['list'][i]['dt_txt']) == str(d) + ' 18:00:00':
            evening_w, img = get_weather_for_time(i, img, data)
            ans += "/{}°C/".format(data['list'][i]['main']['temp'])
        if (data['list'][i]['dt_txt']) == str(d + datetime.timedelta(days=1)) + ' 00:00:00':
            night_w, img = get_weather_for_time(i, img, data)
            ans += "/{}°C/".format(data['list'][i]['main']['temp'])

    """сохраняем  заполненый блок"""

    img.save('files/img_for_day.png')

    """удаляем ненужные фото"""

    for n in range(5):
        file_name = 'file' + str(n) + '.png'
        if os.path.exists(file_name):
            os.remove(file_name)

    """формируем ответ"""

    ans += "\n\nУТРО\n" + morning_w + "ДЕНЬ\n" + day_w + "ВЕЧЕР\n" + evening_w + "НОЧЬ\n" + night_w
    return ans
