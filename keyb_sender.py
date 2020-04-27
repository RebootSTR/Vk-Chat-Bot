import Keyboard
import json
import random
import copy
from vars import *
from api_requests import *


def send_chat(message):
    queue_label = Keyboard.Button.link(label="Кнопки занятия очереди:")
    eng_button = Keyboard.Button.text(label="Английский", payload='1')
    prog_button = Keyboard.Button.text(label="Программирование", payload='2')
    queue_button = Keyboard.Button.text(label="Показать очередь", payload='3', color='positive')
    donate_label = Keyboard.Button.link(label="На аренду хоста) (55р/мес)")
    donate_button = Keyboard.Button.vk_pay(_hash='action=transfer-to-group%26group_id=192889258%26aid=10')
    keyboard = Keyboard.create([queue_label],
                               [eng_button, prog_button],
                               [queue_button],
                               [donate_label],
                               [donate_button])
    r = post("messages.send",
             secret=secret,
             v="5.103",
             access_token=token,
             peer_id=chat_peer,
             random_id=-random.randint(100000000, 999999999),
             message=message,
             keyboard=json.dumps(keyboard, ensure_ascii=False))
    print(r)


def send_admin(message):
    eng_button = Keyboard.Button.text(label="Очистить Английский", payload='1', color='negative')
    prog_button = Keyboard.Button.text(label="Очистить Прогу", payload='2', color='negative')
    status_button = Keyboard.Button.text(label="Статус", payload='3')
    keyboard = Keyboard.create([eng_button, prog_button],
                               [status_button])
    r = post("messages.send",
             secret=secret,
             v="5.103",
             access_token=token,
             peer_id=admin_peer,
             random_id=-random.randint(100000000, 999999999),
             message=message,
             keyboard=json.dumps(keyboard, ensure_ascii=False))
    print(r.json())
    #return keyboard


if __name__ == "__main__":
    #send_chat("update-mini")
    send_admin("test update")