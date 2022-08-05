# from system_info import SystemInfo

# x=SystemInfo()

# from gloabl_info import GlobalInfo

# x=GlobalInfo()

# print(x.interface_info)
# print(x.config_info)
# print(x.get_network_info())
# print(x.get_ip_country())


from sensor.sensor_role import Sensor

if __name__ == '__main__':
    data = {
        'id': '1001',

    }
    role = Sensor(data)
