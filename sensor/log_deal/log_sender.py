import requests
import logging
header = ''
req = None


def log_sender(data, url):
    url = url
    try:
        req = requests.post(url=url, data=data)
    except:
        logging.error(f"not send=========={data}")
    try:
        logging.warn(req.text)
    except:
        pass
