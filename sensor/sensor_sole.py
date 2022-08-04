import logging
import time
import sys
import os
from multiprocessing import Process

from predict.file_monitor import MyEventHandler
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


from log_deal.log_mode.snort_log import LogReceive
from log_deal.log_sender import log_sender
from file_mode.file_create import create_new_path
from sensor_control import SensorController
from predict.deep_learn_control import DeepLearnControl
# id


class Sensor(object):
    def __init__(self, data) -> None:
        LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
        logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

        # "sensor_path",
        # "log_path",
        # "rule_path"
        base_path = '/'
        # base_path
        # id
        self.id = data['id']
        self.path = create_new_path(base_path, self.id)

        self.snort_log = LogReceive()

        self.sensor = SensorController(self.path, data)

        self.deep_learn_control = DeepLearnControl(self.path, id)

        self.deep_learn = 'deep_learn'

        self.file_monitor = 'file_monitor'

        self.process_pool = {}

    def start(self, data):
        log_pro = Process(target=self.snort_log.get_msg,
                          args=(os.path.join(self.path['log_path'], 'snort_alert')),)

        log_pro.start()
        log_pro.join()
        self.process_pool.update("log_pro", log_pro)
        self.sensor.start_sensor()  # TODO:需要判断是否成功

        self.deep_learn_control.start()
        # TODO：需要判断是否成功

    def reload():
        pass

    def stop(self):
        self.process.pool["log_pro"].close()
        self.sensor.stop_sensor()

    def delete():
        pass

    def send_log():
        log_sender()

        # TODO:改为data sender
