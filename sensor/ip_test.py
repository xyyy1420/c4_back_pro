import ip_info

ip_info.create_sql()
res, status = ip_info.select_sql("58.220.95.40")
if res:
    pass
else:
    info = ip_info.get_ip_info("58.220.95.40")
    ip_info.insert_sql(info)
    status = info
print(status[0][1])
