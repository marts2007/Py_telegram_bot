import requests
from logger import log
from config import config


def get_url(url: str = "", param={}) -> dict:
    try:
        r = requests.post(url, params=param, proxies=config.proxies)
        return r.json()
    except Exception as e:
        log(e)



