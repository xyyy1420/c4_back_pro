import logging
import os
from multiprocessing import Process
import time

from .log_deal.log_mode.snort_log import LogReceive
from .file_mode.file_create import create_new_path
from .sensor_control import SensorController
from .predict.deep_learn_control import DeepLearnControl

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s -%(funcName)s"
# fh = logging.FileHandler('./1.log')

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


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
            {"deep_rule": '/usr/local/snort/rules/deep_learn.rules'})

        # self.data.update({"log_path": self.path['log_path']})
        # self.data.update({"rule_path": self.path['rule_path']})
        # logging.info(f"data update:{data}")

        self.snort_log = LogReceive(self.data)

        self.sensor = SensorController(self.data)

        self.deep_learn_control = DeepLearnControl(self.data)

        self.process_pool = {}

    def start(self):
        if self.data['mode'] != 'deep_learn_ids':
            self.load_log_deal()
        self.process_pool.update({"sensor": self.load_sensor()})
        if self.data['mode'] == 'deep_learn_ids':
            time.sleep(1)
            self.load_deep_learn()
        # DONE：需要判断是否成功

    def load_deep_learn(self):
        self.deep_learn_control.start()
        # if self.deep_learn_control.is_alive():
        #     logging.info("DeepLearn mode start")
        # else:
        #     logging.error("DeepLearn mode start error")
        # TODO：需要判断是否成功

    def load_sensor(self):
        res = self.sensor.start_sensor()

        if res == -1:
            logging.error(f"Sensor start error , code:{res}")
        else:
            logging.info("Sensor start")
            return res

        # self.load_deep_learn()

    def load_log_deal(self):
        log_pro = Process(target=self.snort_log.get_msg,
                          args=(self.data['id']))
        log_pro.start()
        if log_pro.is_alive():
            logging.info("Log listener start")
        else:
            logging.error("Log listener start error")
        self.process_pool.update({"log_pro": log_pro})
        logging.info("Logging mode create , start listening...")

    def reload(self, data):
        self.stop()
        self.data = self.merge_data(self.data, data)
        self.start()

    def stop(self):
        self.sensor.stop_sensor(self.process_pool['sensor'])
        logging.info("sensor stop")
        self.process_pool["log_pro"].terminate()
        if self.process_pool['log_pro'].is_alive():
            logging.error("Log mode can not stop")
        else:
            logging.info("log mode stop")
        if self.data['mode'] == 'deep_learn_ids':
            self.deep_learn_control.stop()
        logging.warn("All controller stop")

    def delete(self):
        # TODO:delete dirs
        pass
        # TODO:改为data sender

    def merge_data(self, data1, data2):
        if isinstance(data1, dict) and isinstance(data2, dict):
            new_dict = {}
            d2_keys = list(data2.keys())
            d1_keys = list(data1.keys())
            for k in d2_keys:
                if k in d1_keys:
                    d1_keys.remove(k)
                    new_dict[k] = data2[k]
            for i in d1_keys:
                new_dict[i] = data1[k]
        return new_dict
