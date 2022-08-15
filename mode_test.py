# from system_info import SystemInfo

# x=SystemInfo()

# from gloabl_info import GlobalInfo

# x=GlobalInfo()

# print(x.interface_info)
# print(x.config_info)
# print(x.get_network_info())
# print(x.get_ip_country())
from multiprocessing import Process
import logging
from sensor.sensor_role import Sensor

if __name__ == '__main__':
    data = {
        'id': '10000001',
        'rule_file': '/usr/local/snort/rules/local.rules',
        'mode': 'interface_ids',
        'interface': 'ens192',



    }
    role = Sensor(data)
    role1 = Process(target=role.start, args=())
    role1.start()
    role1.join()
    logging.info("start")
    try:
        while 1:
            pass
    except KeyboardInterrupt:
        role.stop()
    logging.info("stop")
