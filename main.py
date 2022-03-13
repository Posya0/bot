import json
import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


instructions = """ инструкция"""


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

def main():
    vk_session = vk_api.VkApi(
        token='1a30228cd685c3224500ad7eb8f4a74770adb0b2cc84e5760382f92bee0d6538d311e82a91ac97b1830fd')
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        def send_mes(mes):
            vk.messages.send(user_id=event.user_id, random_id=get_random_id(), message=mes)

        if event.type == VkEventType.MESSAGE_NEW and event.text and event.to_me:
            person = str(event.user_id)

            if (person not in users_data):
                users_data.update({person: ["москва", "москва"]})
                send_mes('Привет, ' + vk.users.get(user_id=event.user_id)[0]['first_name'])
                send_mes(instructions)

            elif event.text.lower() == 'привет' or event.text.lower() == 'начать' or event.text.lower() == 'меню':
                send_mes('Привет, ' + vk.users.get(user_id=event.user_id)[0]['first_name'])
                send_mes(instructions)

            elif event.text == "?":
                send_mes(instructions)

            else:
                send_mes('Неопознанная команда')


if __name__ == '__main__':
    main()
