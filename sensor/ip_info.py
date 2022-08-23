import requests
import logging
import sqlite3
import json


def get_country(ip):
    ip_api = 'http://ip-api.com/json/'
    ip_api = "https://ipapi.co/"
    api_req = f'{ip_api}{ip}/country/'
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36"}
    print(api_req)
    res = requests.get(url=api_req, headers=header)
    logging.info(res)
    # print(dict(res.text))
    return res.text


def create_sql():
    conn = sqlite3.connect('ip_db.db')
    cur = conn.cursor()
    try:
        cur.execute(
            "create table ip_country(ip TEXT,country TEXT,city TEXT,latitude TEXT,longitude TEXT)")
    except:
        logging.info("db exists")
    conn.commit()


def insert_sql(info):
    conn = sqlite3.connect('ip_db.db')
    cur = conn.cursor()
    try:
        cur.execute(
            f'''insert into ip_country values("{info['ip']}","{info['country']}","{info['city']}","{info['latitude']}","{info['longitude']}")''')
    except:
        pass
    conn.commit()


def select_sql(ip):
    conn = sqlite3.connect('ip_db.db')
    cur = conn.cursor()
    try:
        cur.execute(f'''select * from ip_country where ip="{ip}"''')
    except:
        pass
    conn.commit()
    res = cur.fetchall()
    if res == []:
        return (False, res)
    else:
        return (True, res)


def get_ip_info(ip):
    url = f'https://ipapi.co/{ip}/json/'
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36"}
    res = requests.get(url=url, headers=header)
    try:
        res = json.loads(res.text)
    except:
        res = []
    return res


if __name__ == "__main__":
    get_ip_info("60.12.58.71")

    # import sqlite3
    # from typing import Counter
    # conn = sqlite3.connect('ip_db.db')
    # cur = conn.cursor()

    # ip = "192.168.1.2"
    # src_ip = "192.168.1.5"
    # country = "EN"
    # cmd1 = f'''select * from ip_country where ip="{src_ip}"'''
    # cur.execute(cmd1)

    # fet_res = cur.fetchall()
    # if fet_res != []:
    #     print(fet_res[0][1])
    # else:
    #     cur.execute(f'''insert into ip_country values("{src_ip}","{country}")''')
    #     conn.commit()
