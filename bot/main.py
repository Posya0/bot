import json
import os

import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from corona import *
from pogoda import *
from goroskop import *

instructions = """
Приветик)))
Я твой бот-помошник.

Перед началом использования бота, пожалуйста, внесите данные о себе:
"Город *Ваш город*"
"Знак *Ваш знак зодиака*"

Чтобы вызвать меню, напишите "привет", "начать" или "меню".

-Кнопка "Обо мне" выведет Ваш знак зодиака  город, используйте это, чтобы убедится в правильности настроек.

-Кнопка "Корона" откроет для вас раздел статистики по коронавирусу:
    -"мой регион" - статитика на сегодня по вашему региону
    -"Россия" - статистика по России на 10 дней
    -"мир" - статистика по миру на 10 дней
    -"МЕНЮ" - вернет вас в основное меню
    
    
-Кнопка "Погода" откроет для вас раздел прогноза погоды:
    -"сейчас" - погода в вашем городе в данный момент
    -"завтра" - погода в вашем городе завтра
    -"на 5 дней" - краткий прогноз погоды на 5 дней
    -"МЕНЮ" - вернет вас в основное меню

-Кнопка "Гороскоп" откроет для вас раздел гороскопа:
    -"на сегодня" - ваш гороскоп на сегодня
    -"на неделю" - ваш гороскоп на неделю
    -"на месяц" - ваш гороскоп на текущий месяц
    -"МЕНЮ" - вернет вас в основное меню

? - вызов инструкции
"""

f = open('users_data.txt', 'r')
s = f.read()
f.close()
if s == '':
    print("?")
    users_data = {}
else:
    with open('users_data.txt', 'r') as f:
        users_data = json.load(f)
f.close()


def save():
    """обновление данных о пользователях"""
    with open('users_data.txt', 'w') as f:
        json.dump(users_data, f)
    f.close()


def main():
    """ основная функция"""
    vk_session = vk_api.VkApi(
        token='1a30228cd685c3224500ad7eb8f4a74770adb0b2cc84e5760382f92bee0d6538d311e82a91ac97b1830fd')
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    """клавиатура меню"""
    kmenu = VkKeyboard(one_time=True)
    kmenu.add_button("Погода", color=VkKeyboardColor.POSITIVE)
    kmenu.add_button("Корона", color=VkKeyboardColor.POSITIVE)
    kmenu.add_line()
    kmenu.add_button("Гороскоп", color=VkKeyboardColor.POSITIVE)
    kmenu.add_button("Обо мне", color=VkKeyboardColor.PRIMARY)

    """клавиатура корона"""
    kkorona = VkKeyboard(one_time=True)
    kkorona.add_button("Мой регион", color=VkKeyboardColor.POSITIVE)
    kkorona.add_button("Россия", color=VkKeyboardColor.POSITIVE)
    kkorona.add_line()
    kkorona.add_button("Мир", color=VkKeyboardColor.POSITIVE)
    kkorona.add_button("МЕНЮ", color=VkKeyboardColor.PRIMARY)

    """клавиатура гороскоп"""
    khoros = VkKeyboard(one_time=True)
    khoros.add_button("На сегодня ", color=VkKeyboardColor.POSITIVE)
    khoros.add_button("На неделю ", color=VkKeyboardColor.POSITIVE)
    khoros.add_line()
    khoros.add_button("На месяц ", color=VkKeyboardColor.POSITIVE)
    khoros.add_button("МЕНЮ", color=VkKeyboardColor.PRIMARY)

    """клавиатура погода"""
    kweather = VkKeyboard(one_time=True)
    kweather.add_button("сейчас", color=VkKeyboardColor.POSITIVE)
    kweather.add_button("завтра", color=VkKeyboardColor.POSITIVE)
    kweather.add_line()
    kweather.add_button("на 5 дней", color=VkKeyboardColor.POSITIVE)
    kweather.add_button("МЕНЮ", color=VkKeyboardColor.PRIMARY)

    for event in longpoll.listen():
        def send_mes(mes, keyboard=None, attachment=None):
            """функция отправки сообщения"""
            if keyboard: keyboard = keyboard.get_keyboard()
            if attachment: attachment = ','.join(attachments)
            vk.messages.send(user_id=event.user_id, random_id=get_random_id(), message=mes, keyboard=keyboard,
                             attachment=attachment)

        if event.type == VkEventType.MESSAGE_NEW and event.text and event.to_me:
            person = str(event.user_id)

            """если новый пользователь"""
            if (person not in users_data):
                users_data.update({person: ["москва", "овен"]})
                save()
                send_mes('Привет, ' + vk.users.get(user_id=event.user_id)[0]['first_name'])
                send_mes(instructions, keyboard=kmenu)

            elif event.text.lower() == 'привет' or event.text.lower() == 'начать' or event.text.lower() == 'меню':
                send_mes('Привет, ' + vk.users.get(user_id=event.user_id)[0]['first_name'],  keyboard=kmenu)

            elif event.text == "?":
                send_mes(instructions, keyboard=kmenu)



            elif event.text.lower() == "обо мне":
                send_mes("Я думаю, что ваш город - " + users_data[person][0] + ", а ваш знак зодиака - " +
                         users_data[person][1].title())

            elif event.text.lower().startswith("город "):
                s = event.text.lower()
                s = s.split()
                if len(s) == 2 and is_city(s[1]):
                    users_data[person][0] = s[1].title()
                    save()
                    send_mes("Ваш город - " + users_data[person][0] + ". Я запомнил!")
                else:
                    send_mes("Я не знаю такого города")

            elif event.text.lower().startswith("знак "):
                s = event.text.lower()
                s = s.split()
                if len(s) == 2 and is_zhak(s[1]):
                    users_data[person][1] = s[1].title()
                    save()
                    send_mes("Ваш знак зодиака - " + users_data[person][1].title() + ". Я запомнил!")
                else:
                    send_mes("Я не знаю такого знака")


            elif event.text.lower() == "корона":
                send_mes("Статистика по Коронавирусу ", keyboard=kkorona)

            elif event.text.lower() == "россия":
                res = in_russia()
                upload = VkUpload(vk_session)
                attachments = []
                image = 'images/covid.png'
                photo = upload.photo_messages(photos=image)[0]
                attachments.append("photo{}_{}".format(photo["owner_id"], photo["id"]))
                send_mes(res, attachment=','.join(attachments))
                os.remove(image)

            elif event.text.lower() == "мой регион":
                send_mes(in_regions(users_data[person][0]))

            elif event.text.lower() == "мир":
                res = in_world()
                upload = VkUpload(vk_session)
                attachments = []
                image = 'images/covid.png'
                photo = upload.photo_messages(photos=image)[0]
                attachments.append("photo{}_{}".format(photo["owner_id"], photo["id"]))
                send_mes(res, attachment=','.join(attachments))
                os.remove(image)

            elif event.text.lower() == "погода":
                send_mes("Погода " + users_data[person][0], keyboard=kweather)

            elif event.text.lower() == "на 5 дней":
                res = get_weather_for_5(users_data[person][0])
                upload = VkUpload(vk_session)
                attachments = []
                image = 'img_for_5.png'
                photo = upload.photo_messages(photos=image)[0]
                attachments.append("photo{}_{}".format(photo["owner_id"], photo["id"]))
                send_mes(res, attachment=','.join(attachments))
                os.remove(image)

            elif event.text.lower() == "сейчас":
                res = get_weather_for_now(users_data[person][0])
                upload = VkUpload(vk_session)
                attachments = []
                image = 'img_for_now.png'
                photo = upload.photo_messages(photos=image)[0]
                attachments.append("photo{}_{}".format(photo["owner_id"], photo["id"]))
                send_mes(res, attachment=','.join(attachments))
                os.remove(image)

            elif event.text.lower() == "завтра":
                res = get_weather_for_day(users_data[person][0])
                upload = VkUpload(vk_session)
                attachments = []
                image = 'img_for_day.png'
                photo = upload.photo_messages(photos=image)[0]
                attachments.append("photo{}_{}".format(photo["owner_id"], photo["id"]))
                send_mes(res, attachment=','.join(attachments))
                os.remove(image)


            elif event.text.lower() == "гороскоп":
                send_mes("Гороскоп ", keyboard=khoros)

            elif event.text.lower() == "на сегодня":
                res = goroskop_(users_data[person][1],'Сегодня')

                image = 'znaki_pictures/' + znak[users_data[person][1].lower()] + '.jpg'
                upload = VkUpload(vk_session)
                attachments = []

                photo = upload.photo_messages(photos=image)[0]
                attachments.append("photo{}_{}".format(photo["owner_id"], photo["id"]))
                send_mes(res, attachment=','.join(attachments))


            elif event.text.lower() == "на неделю":
                res = goroskop_(users_data[person][1],'Неделя')

                image = 'znaki_pictures/' + znak[users_data[person][1].lower()] + '.jpg'
                upload = VkUpload(vk_session)
                attachments = []

                photo = upload.photo_messages(photos=image)[0]
                attachments.append("photo{}_{}".format(photo["owner_id"], photo["id"]))
                send_mes(res, attachment=','.join(attachments))


            elif event.text.lower() == "на месяц":
                res = goroskop_(users_data[person][1],'Месяц')

                image = 'znaki_pictures/' + znak[users_data[person][1].lower()] + '.jpg'
                upload = VkUpload(vk_session)
                attachments = []

                photo = upload.photo_messages(photos=image)[0]
                attachments.append("photo{}_{}".format(photo["owner_id"], photo["id"]))
                send_mes(res, attachment=','.join(attachments))


            else:
                send_mes('Неопознанная команда')


if __name__ == '__main__':
    main()
