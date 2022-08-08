import requests
import logging
header = ''
req = None


def log_sender(data, url):
    url = url
    req = requests.post(url=url, data=data)
    logging.warn(req.text)
