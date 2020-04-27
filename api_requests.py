import requests
import hashlib


def get_sig(url, secret):
    sig = hashlib.md5((url[18:] + secret).encode("utf-8")).hexdigest()
    return sig


def post(method, secret, timeout=25, **kwargs):
    kwargs["v"] = 5.103
    kwargs["lang"] = "ru"
    kwargs["https"] = 1
    url = "https://api.vk.com/method/" + method + '?'
    for key, value in kwargs.items():
        url += f"{key}={value}&"
    url = url[:-1]
    while True:
        try:
            r = requests.post(url + f"&sig={get_sig(url, secret)}",
                              timeout=timeout)
            break
        except Exception:
            print('ошибка post запроса')
    return r


def get(url, timeout):
    while True:
        try:
            r = requests.post(url, timeout=timeout)
            break
        except Exception:
            print('ошибка get запроса')
    return r
