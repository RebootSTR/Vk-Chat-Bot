import Keyboard
import time
import random
from DataBase import DataBase
from api_requests import post, get
from vars import admin_peer
from vars import chat_peer
from vars import token
from vars import secret
from vars import group_id


def update_keys(data):
    print("Обновляю ключи")
    r = post("groups.getLongPollServer",
             secret=secret,
             access_token=token,
             group_id=group_id).json()['response']
    wait = data[2]
    base.delete_all("settings")
    base.append("settings", r['server'], r['key'], wait, r['ts'])
    return get_update()


def get_update():
    print("Поиск обновлений")
    data = base.get_all("settings")[0]
    r = get("{server}?act=a_check&key={key}&ts={ts}&wait={wait}".format(server=data[0],
                                                                        key=data[1],
                                                                        wait=data[2],
                                                                        ts=data[3]),
            timeout=90).json()
    if 'failed' in r.keys():
        r = update_keys(data)
    print("Обновлено")
    base.edit("settings", "ts", r['ts'])
    return r


def set_timer(id, lesson):
    timer = base.get(lesson, "timer", f'id={id}')
    if timer == 0:
        base.edit(lesson, 'timer', int(time.time()))
        last_name = base.get('peoples', "last_name", f'id={id}')
        send_cancel(f"@id{id}({last_name}), Ваше место в очереди будет удалено через 3 минуты.",
                    f"\"{lesson}\"")
    else:
        timer_delete(id, lesson)


def timer_delete(id, lesson):
    timer = base.get(lesson, "timer", f'id={id}')
    if timer != 0:
        if timer+180 < time.time():
            base.delete(lesson, 'id', id)


def add_in_queue(message, lesson):
    check_all_on_timer()
    id = message['from_id']
    if base.get(lesson, "*", f'id={id}') is not None:
        set_timer(id, lesson)
    else:
        last_name = base.get('peoples', 'last_name', f'id={id}')
        base.append(lesson, id, last_name, 0)


def cancel(message, lesson):
    id = message['from_id']
    timer = base.get(lesson, "timer", f'id={id}')
    if timer != 0:
        base.edit(lesson, "timer", 0)
        last_name = base.get('peoples', 'last_name', f'id={id}')
        send_message(f"@id{id}({last_name}), действие отменено.")


def handle_chat(message):
    if 'payload' not in message:
        return
    payload = message['payload']
    if payload == '1':
        add_in_queue(message, "english")
    elif payload == '2':
        add_in_queue(message, 'programing')
    elif payload == '3':
        if not first_start:
            send_message(get_queue(), chat_peer, notify_off=1)
    elif payload == '"english"':
        cancel(message, 'english')
    elif payload == '"programing"':
        cancel(message, 'programing')


def handle_admin(message):
    if 'payload' not in message:
        return
    payload = message['payload']
    if payload == "1":
        base.delete_all("english")
    elif payload == '2':
        base.delete_all("programing")
    elif payload == '3':
        send_message("All work!", admin_peer)


def send_message(message, peer, notify_off=0):
    r = post("messages.send",
             secret=secret,
             v="5.103",
             access_token=token,
             peer_id=peer,
             random_id=-random.randint(100000000, 999999999),
             message=message,
             disable_mentions=notify_off)


def send_cancel(message, payload):
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
        timer_delete(eng[i-1][0], "english")
    prog = base.get_all("programing")
    for i in range(len(prog), 0, -1):
        timer_delete(prog[i - 1][0], "programing")


def get_queue():
    text = "Очередь на английский:\n"
    eng = base.get_all("english")
    for i in range(len(eng)):
        text += f"{i+1}. @id{eng[i][0]}({eng[i][1]})\n"
    prog = base.get_all("programing")
    text += "\n\nОчередь на програмирование:\n"
    for i in range(len(prog)):
        text += f"{i+1}. @id{prog[i][0]}({prog[i][1]})\n"
    return text


def debug():
    print(update['updates'][0]['object']['message']['payload'])
    input()


if __name__ == "__main__":
    base = DataBase("base.db")
    first_start = True
    try:
        while True:
            print(time.ctime())
            update = get_update()
            #debug()
            for obj in update['updates']:
                message = obj['object']['message']
                peer = message['peer_id']
                if peer == chat_peer:
                    handle_chat(message)
                elif peer == admin_peer:
                    handle_admin(message)
            first_start = False
    except Exception as err:
        e = err
    send_message("Я сломался, мать!", admin_peer)
    raise e
