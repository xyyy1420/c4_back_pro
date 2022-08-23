import ip_info

ip_info.create_sql()
res, status = ip_info.select_sql("192.168.1.144")
if res:
    pass
else:
    info = ip_info.get_ip_info("192.168.1.144")
    ip_info.insert_sql(info)
    status = info
print(status[0][1])
