import Keyboard
import json
import random
import copy
from vars import *
from api_requests import *


def default_keyboard(eng_count, prog_count):  # no using more
    queue_label = Keyboard.Button.link(label="Кнопки занятия очереди:")
    eng_button = Keyboard.Button.text(label=f"Английский({eng_count})", payload='1')
    prog_button = Keyboard.Button.text(label=f"Программирование({prog_count})", payload='2')
    queue_button = Keyboard.Button.text(label="Показать очередь", payload='3', color='positive')
    donate_label = Keyboard.Button.link(label="На аренду хоста) (55р/мес)")
    donate_button = Keyboard.Button.vk_pay(_hash='action=transfer-to-group%26group_id=192889258%26aid=10')
    keyboard = Keyboard.create([queue_label],
                               [eng_button, prog_button],
                               [queue_button],
                               [donate_label],
                               [donate_button])
    return keyboard


def send_chat(message):
    queue_label = Keyboard.Button.link(label="Кнопки занятия очереди:")
    eng_button = Keyboard.Button.text(label="Английский", payload='1')
    prog_button = Keyboard.Button.text(label="Программирование", payload='2')
    queue_button = Keyboard.Button.text(label="Очередь", payload='3', color='positive')
    queue_button1 = Keyboard.Button.text(label="Очередь", payload='33', color='positive')
    donate_label = Keyboard.Button.link(label="На аренду хоста) (55р/мес)")
    donate_button = Keyboard.Button.vk_pay(_hash='action=transfer-to-group%26group_id=192889258%26aid=10')
    keyboard = Keyboard.create([queue_label],
                               [eng_button, prog_button],
                               [queue_button, queue_button1],
                               [donate_label],
                               [donate_button])
    r = post("messages.send",
             secret=secret,
             v="5.103",
             access_token=token,
             peer_id=chat_peer,
             random_id=-random.randint(100000000, 999999999),
             message=message,
             keyboard=keyboard)
    print(r)


def send_admin(message):
    eng_button = Keyboard.Button.text(label="Английский", payload='1', color='negative')
    prog_button = Keyboard.Button.text(label="Прога", payload='2', color='negative')
    eng_button1 = Keyboard.Button.text(label="Английский(Without)", payload='11', color='negative')
    prog_button1 = Keyboard.Button.text(label="Прога(Without)", payload='22', color='negative')
    status_button = Keyboard.Button.text(label="Статус", payload='3')
    everyone_button = Keyboard.Button.text(label="@everyone", payload='4', color='positive')
    everyone2_button = Keyboard.Button.text(label="@everyone(My acc)", payload='44', color='positive')
    move_button = Keyboard.Button.text(label="/<table> <now> <need>")
    # test_button = Keyboard.Button.text(label="test payload", payload='\"cancel\"', color='negative')
    keyboard = Keyboard.create([move_button],
                               [everyone_button, everyone2_button],
                               [eng_button, prog_button],
                               [eng_button1, prog_button1],
                               [status_button])
    r = post("messages.send",
             secret=secret,
             v="5.103",
             access_token=token,
             peer_id=admin_peer,
             random_id=-random.randint(100000000, 999999999),
             message=message,
             keyboard=keyboard)
    print(r.json())
    # return keyboard


if __name__ == "__main__":
    # everyone = "[club192889258|@everyone]\n[id53725133|⠀][id77957660|⠀][id116791458|⠀][id132393037|⠀][id151820739|⠀][id157302578|⠀][id162013508|⠀][id172396829|⠀][id189104642|⠀][id191604867|⠀][id230434103|⠀][id254215836|⠀][id274839705|⠀][id282474619|⠀][id299082473|⠀][id311856945|⠀][id326818928|⠀][id347503343|⠀][id413262496|⠀][id479162808|⠀][id481172781|⠀][id535638545|⠀][id540487388|⠀][id560524444|⠀]"
    send_chat("update, разделил очередь")
    # send_admin('move')
