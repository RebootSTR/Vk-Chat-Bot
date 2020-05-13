import Keyboard
import keyb_sender
import time
import random
from DataBase import DataBase
from api_requests import post, get
from vars import admin_peer
from vars import chat_peer
from vars import token
from vars import secret
from vars import group_id
from vars import F, F1
import threading


def update_keys(data, w):
    print("Обновляю ключи")
    r = post("groups.getLongPollServer",
             secret=secret,
             access_token=token,
             group_id=group_id).json()['response']
    wait = data[2]
    base.delete_all("settings")
    base.append("settings", r['server'], r['key'], wait, r['ts'])
    return get_update(wait=w)


def get_update(wait=-1):
    print("Поиск обновлений")
    data = base.get_all("settings")[0]
    if wait == -1:
        wait = data[2]
    r = get("{server}?act=a_check&key={key}&ts={ts}&wait={wait}".format(server=data[0],
                                                                        key=data[1],
                                                                        wait=wait,
                                                                        ts=data[3]),
            timeout=90).json()
    if 'failed' in r.keys():
        r = update_keys(data, wait)
    print("Обновлено")
    base.edit("settings", "ts", r['ts'], f"ts={data[3]}")
    return r


def set_timer(id, lesson):
    timer = base.get(lesson, "timer", f'id={id}')
    if timer == 0:
        base.edit(lesson, 'timer', int(time.time()) + 180, f"id={id}")
        last_name = base.get('peoples', "last_name", f'id={id}')
        send_cancel_button(f"@id{id}({last_name}), Ваше место в очереди будет удалено через 3 минуты. "
                           f"Повторное нажатие на кнопку очереди, УДАЛИТ вас из очереди СРАЗУ",
                           f"\"{lesson}\"", chat_peer)
    else:
        delete_from_queue(lesson, id)


def add_in_queue(message, lesson):
    id = message['from_id']
    if base.get(lesson, "*", f'id={id}') is not None:
        set_timer(id, lesson)
    else:
        last_name = base.get('peoples', 'last_name', f'id={id}')
        base.append(lesson, id, last_name, 0)


def cancel(message, lesson):
    id = message['from_id']
    timer = base.get(lesson, "timer", f'id={id}')
    print(timer)
    if timer != 0 and timer is not None:
        base.edit(lesson, "timer", 0, f"id={id}")
        last_name = base.get('peoples', 'last_name', f'id={id}')
        send_message(f"@id{id}({last_name}), действие отменено.", chat_peer)


def handle_chat(message):
    if 'payload' not in message:
        return
    payload = message['payload']
    if payload == '1':
        add_in_queue(message, "english")
    elif payload == '2':
        add_in_queue(message, 'programing')
    elif payload == '3':
        if antispam():
            send_message(get_queue('english'), chat_peer, notify_off=1)
    elif payload == '33':
        if antispam():
            send_message(get_queue('programing'), chat_peer, notify_off=1)
    elif payload == '"english"':
        cancel(message, 'english')
    elif payload == '"programing"':
        cancel(message, 'programing')


def prepare(lesson, add=True):
    send_message("Очередь будет очищена через 1 минуту. Бот будет неактивен в течение этого времени", chat_peer)
    time.sleep(60)
    base.delete_all(lesson)
    r = get_update(wait=1)
    send_message("Очередь очищена, запись возобновлена", chat_peer)
    if add:
        F(lesson)


def parse_command(text):
    start = text.find("/") + 1
    text = text[start:]
    space = text.find(" ")
    table = text[:space]
    start = space + 1
    text = text[start:]
    space = text.find(" ")
    now = int(text[:space])
    need = int(text[space + 1:])
    if need > now:
        base.move_down(table, now, need)
    else:
        base.move_up(table, now, need)


def handle_admin(message):
    global typing_active
    if 'payload' not in message:
        text = str(message['text'])
        if "/" not in text:
            return
        try:
            parse_command(text)
            send_message("OK", admin_peer)
        except Exception as e:
            send_message("Не распознал команду", admin_peer)
            print(e)
        return
    payload = message['payload']
    if payload == "1":
        prepare("english")
    elif payload == '2':
        prepare("programing")
    elif payload == '3':
        send_message("All work!", admin_peer)
    elif payload == '11':
        prepare("english", add=False)
    elif payload == '22':
        prepare("programing", add=False)
    elif payload == '4':
        everyone = "ВАЖНО!\n[id53725133|⠀][id77957660|⠀][id116791458|⠀][id132393037|⠀][" \
                   "id151820739|⠀][id157302578|⠀][id162013508|⠀][id172396829|⠀][id189104642|⠀][id191604867|⠀][" \
                   "id230434103|⠀][id254215836|⠀][id274839705|⠀][id282474619|⠀][id299082473|⠀][id311856945|⠀][" \
                   "id326818928|⠀][id347503343|⠀][id413262496|⠀][id479162808|⠀][id481172781|⠀][id535638545|⠀][" \
                   "id540487388|⠀][id560524444|⠀]\n@everyone"
        send_message(everyone, chat_peer)
    elif payload == '44':
        F1()  # everyone N2
    elif payload == '5':
        if typing_active:
            typing_active = False
        else:
            thread.start()


def send_message(message, peer, notify_off=0):
    r = post("messages.send",
             secret=secret,
             v="5.103",
             access_token=token,
             peer_id=peer,
             random_id=-random.randint(100000000, 999999999),
             message=message,
             disable_mentions=notify_off)


def send_cancel_button(message, payload, peer):
    cancel = Keyboard.Button.text(label="Отмена", payload=payload, color='negative')
    keyboard = Keyboard.create([cancel], inline=True)
    r = post("messages.send",
             secret=secret,
             v="5.103",
             access_token=token,
             peer_id=chat_peer,
             random_id=-random.randint(100000000, 999999999),
             message=message,
             keyboard=keyboard)


def check_all_on_timer():
    eng = base.get_all("english")
    for i in range(len(eng), 0, -1):
        timer_delete(eng[i - 1][0], "english")
    prog = base.get_all("programing")
    for i in range(len(prog), 0, -1):
        timer_delete(prog[i - 1][0], "programing")


def timer_delete(id, lesson):
    timer = base.get(lesson, "timer", f'id={id}')
    if timer != 0:
        if timer < time.time():
            delete_from_queue(lesson, id)


def delete_from_queue(lesson, id):
    base.delete(lesson, 'id', id)
    last_name = base.get('peoples', 'last_name', f'id={id}')
    send_message(f"@id{id}({last_name}), был удален из очереди {'ENG' if lesson == 'english' else 'PROG'}.",
                 chat_peer)


def send_with_keyboard(message, peer, keyboard, notify_off=0):  # no using more
    r = post("messages.send",
             secret=secret,
             v="5.103",
             access_token=token,
             peer_id=peer,
             random_id=-random.randint(100000000, 999999999),
             message=message,
             keyboard=keyboard,
             disable_mentions=notify_off)


def get_queue(lesson):
    if lesson == 'english':
        word = 'английский'
    else:
        word = 'программирование'
    text = f"Очередь на {word}:\n"
    data = base.get_all(lesson)
    for i in range(len(data)):
        text += f"{i + 1}. @id{data[i][0]}({data[i][1]})\n"
    return text


def debug():
    global chat_peer
    chat_peer = admin_peer
    print(update)


def antispam():
    global spam
    if spam <= time.time():
        spam = int(time.time()) + 60
        return True
    else:
        return False


def typing():
    while typing_active:
        r = post("messages.setActivity",
                 secret=secret,
                 access_token=token,
                 peer_id=chat_peer,
                 group_id=192889258,
                 type="audiomessage")
        #print(r.json())
        time.sleep(4.5)


if __name__ == "__main__":
    typing_active = False
    thread = threading.Thread(target=typing, daemon=True)
    ban = []
    base = DataBase("base.db")
    spam = 0
    first_start = True
    try:
        while True:
            print(time.ctime())
            update = get_update()
            3 / 0
            check_all_on_timer()
            deb = 0
            if deb != 0:
                debug()
            if not first_start:
                for obj in update['updates']:
                    message = obj['object']['message']
                    peer = message['peer_id']
                    if message['from_id'] in ban:
                        continue
                    if deb != 0:
                        handle_chat(message)
                        handle_admin(message)
                    elif peer == chat_peer:
                        handle_chat(message)
                    elif peer == admin_peer:
                        handle_admin(message)
            first_start = False
    except Exception as err:
        e = err
    send_message("Я сломался, мать!", admin_peer)
    raise e
