
def create(*args):
    buttons_array = []
    for arg in args:
        line = []
        for button in arg:
            line.append(button)
        buttons_array.append(line)
    keyboard = {
        "one_time": False,
        'buttons': buttons_array
    }
    return keyboard


class Button:
    @staticmethod
    def text(label='text_button', payload='0', color='primary'):
        button = {
            'action': {
                'type': 'text',
                'label': label,
                'payload': payload
            },
            'color': color
        }
        return button

    @staticmethod
    def link(label='link_button', link="https://vk.com"):
        button = {
            'action': {
                'type': 'open_link',
                'link': link,
                'label': label,
                'payload': '0'
            }
        }
        return button

    @staticmethod
    def location(payload='0'):
        button = {
            'action': {
                'type': 'location',
                'payload': payload
            }
        }
        return button

    @staticmethod
    def vk_pay(_hash='action=transfer-to-group&group_id=1&aid=10'):
        button = {
            'action': {
                'type': 'vkpay',
                'payload': '0',
                'hash': _hash
            }
        }
        return button

    @staticmethod
    def vk_apps(app_id, owner_id, payload, label, _hash):
            button = {
                'action': {
                    'type': 'open_app',
                    'app_id': app_id,
                    'owner_id': owner_id,
                    'payload': payload,
                    'label': label,
                    'hash': _hash
                }
            }
            return button
