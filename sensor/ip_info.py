import requests


def get_country(ip):
    ip_api = 'http://ip-api.com/json/'
    ip_api = "https://ipapi.co/"
    api_req = f'{ip_api}{ip}/country/'
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36"}
    print(api_req)
    res = requests.get(url=api_req, headers=header)
    # print(dict(res.text))
    return res.text


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
