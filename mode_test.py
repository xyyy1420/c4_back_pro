# from system_info import SystemInfo

# x=SystemInfo()

# from gloabl_info import GlobalInfo

# x=GlobalInfo()

# print(x.interface_info)
# print(x.config_info)
# print(x.get_network_info())
# print(x.get_ip_country())
import time

import logging
from sensor.sensor_role import Sensor

if __name__ == '__main__':
    data = {
        'id': '1001',
        'rule_file': '1001.rules',
        'mode': 'interface_ids',
        'interface': 'ens192',



    }
    role = Sensor(data)
    role.start()
    logging.info("start")
    time.sleep(10)
    role.stop()
    logging.warn("stop")
