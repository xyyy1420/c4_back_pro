# from system_info import SystemInfo

# x=SystemInfo()

# from gloabl_info import GlobalInfo

# x=GlobalInfo()

# print(x.interface_info)
# print(x.config_info)
# print(x.get_network_info())
# print(x.get_ip_country())
import time
from multiprocessing import Process
import logging
from sensor.sensor_role import Sensor

if __name__ == '__main__':
    data = {
        'id': '1001',
        'rule_file': '1001.rules',
        'mode': 'deep_learn_ids',
        'interface': 'ens192',



    }
    role = Sensor(data)
    role1 = Process(target=role.start, args=())
    role1.start()
    logging.info("start")
    try:
        while 1:
            pass
    except KeyboardInterrupt:
        role.stop()
    logging.info("stop")
