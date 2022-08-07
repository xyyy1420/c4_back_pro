import logging
import os
from threading import Thread
from multiprocessing import Process
import time

from .log_deal.log_mode.snort_log import LogReceive
from .log_deal.log_sender import log_sender
from .file_mode.file_create import create_new_path
from .sensor_control import SensorController
from .predict.deep_learn_control import DeepLearnControl
# id

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s -%(funcName)s"

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

# sensor={
#     '1001':class
# }
# sensor.update({'1001':class})
# sensor['1001'].start()
# sensor['1001'].stop()


class Sensor(object):
    def __init__(self, data) -> None:

        # "sensor_path",
        # "log_path",
        # "rule_path"
        self.base_path = '/home/jxy/final_test/'

        self.data = data
        logging.info(f"sensor init from data: {self.data}")
        self.path = create_new_path(self.base_path, self.data['id'])

        for i, v in self.path.items():
            self.data.update({i: v})
            logging.info(f"data update key:{i},value:{v}")
        self.data.update({"sock_file": os.path.join(
            self.data['log_path'], "snort_alert")})
        self.data.update(
            {"deep_rule": '/usr/local/snort/rule/deep_learn.rules'})

        # self.data.update({"log_path": self.path['log_path']})
        # self.data.update({"rule_path": self.path['rule_path']})
        # logging.info(f"data update:{data}")

        # self.snort_log = LogReceive(self.data)

        self.sensor = SensorController(self.data)

        self.deep_learn_control = DeepLearnControl(self.data)

        self.process_pool = {}
        # self.deep_learn = 'deep_learn'

        # self.file_monitor = 'file_monitor'

    def start(self):
        self.load_log_deal()
        self.load_sensor()
        # DONE：需要判断是否成功

    def load_deep_learn(self):
        self.deep_learn_control.start()
        if self.deep_learn_control.is_alive():
            logging.info("DeepLearn mode start")
        else:
            logging.error("DeepLearn mode start error")
        # TODO：需要判断是否成功

    def load_sensor(self):
        res = self.sensor.start_sensor()

        if res == -1:
            logging.error(f"Sensor start error , code:{res}")
            self.error_close()
        else:
            logging.info("Sensor start")

        self.load_deep_learn()

    def load_log_deal(self):
        # log_pro = Process(target=self.snort_log.get_msg)
        log_receive = LogReceive(self.data)
        log_pro = Process(target=start_loop, args=())
        print("error")
        log_pro.start()
        if log_pro.is_alive():
            logging.info("Log listener start")
        else:
            logging.error("Log listener start error")
        self.process_pool.update({"log_pro": log_pro})
        logging.info("Logging mode create , start listening...")

    def reload(self):
        pass

    def stop(self):
        self.sensor.stop_sensor()
        self.process_pool["log_pro"].terminate()
        if self.process_pool['log_pro'].is_alive():
            logging.error("Log mode can not stop")
        if self.data['mode'] == 'deep_learn_ids':
            self.deep_learn_control.stop()
            if self.deep_learn_control.is_alive() == False:
                pass
            else:
                logging.error("DeepLearn can not stop")

        logging.warn("All controller stop")

    def delete(self):
        pass

    def send_log(self):
        log_sender()

        # TODO:改为data sender

    def error_close(self):
        pass


def start_loop():
    while True:
        time.sleep(1)
        print("sleep")
