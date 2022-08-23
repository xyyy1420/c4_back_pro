import ip_info

ip_info.create_sql()
res, status = ip_info.select_sql("122.228.135.213")
if res:
    pass
else:
    info = ip_info.get_ip_info("122.228.135.213")
    ip_info.insert_sql(info)
    status = info
print(status[0][1])
