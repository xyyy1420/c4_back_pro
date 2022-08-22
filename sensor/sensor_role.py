import logging
import os
from multiprocessing import Process
import time
from shutil import copyfile
from .log_deal.log_mode.snort_log import LogReceive
from .file_mode.file_create import create_new_path
from .sensor_control import SensorController
from .predict.deep_learn_control import DeepLearnControl

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s -%(funcName)s"

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

global process_pool

process_pool = {}


class Sensor(object):
    def __init__(self, data) -> None:

        # "sensor_path",
        # "log_path",
        # "rule_path"
        self.base_path = '/home/jxy/final_test/'

        self.data = data
        self.data['id'] = str(self.data['id'])
        logging.info(f"sensor init from data: {self.data}")
        self.path = create_new_path(self.base_path, self.data['id'])

        for i, v in self.path.items():
            if i == "rule_path":
                v = os.path.join(v, f"{self.data['id']}.rules")
                copyfile(data['rule_file'], v)
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
        # self.deep_learn_control = None

        self.process_pool = {}

    def start(self):
        if self.data['mode'] != 'deep_learn_ids':
            self.load_log_deal()
        self.load_sensor()
        if self.data['mode'] == 'deep_learn_ids':
            time.sleep(0.1)
            self.load_deep_learn()

        return self.process_pool
        # logging.info(process_pool)
        # DONE：需要判断是否成功

    def load_deep_learn(self):
        self.deep_learn_control.start()
        self.process_pool.update(
            {"deep_learn_control": self.deep_learn_control})

    def load_sensor(self):
        res = self.sensor.start_sensor()

        if res == -1:
            logging.error(f"Sensor start error , code:{res}")
        else:
            logging.info("Sensor start")
            self.process_pool.update({"sensor": res})

        # self.load_deep_learn()

    def load_log_deal(self):
        log_pro = Process(target=self.snort_log.get_msg,
                          args=(str(self.data['id']),))
        log_pro.start()
        if log_pro.is_alive():
            logging.info("Log listener start")
        else:
            logging.error("Log listener start error")
        self.process_pool.update({"log_pro": log_pro})

        logging.info("Logging mode create , start listening...")

    def reload(self, pool, data):
        self.stop(pool)
        self.data = self.merge_data(self.data, data)
        try:
            self.start()
        except:
            pass

    def stop(self, pool):
        self.process_pool = pool
        logging.error(self.process_pool)
        try:
            self.sensor.stop_sensor(self.process_pool['sensor'])
            logging.info("sensor stop+++++++++++")
        except:
            logging.error("sensor not stop-----------")

        try:
            self.process_pool["log_pro"].terminate()
            logging.info("log pro stop++++++++++")
        except:
            logging.error("log_pro not stop---------")

        try:
            self.deep_learn_control.stop()
            logging.info("deep_learn stop+++++++++++")
        except:
            logging.error("deep_learn stop error---------")
        # if self.process_pool['log_pro'].is_alive():
        #     logging.error("Log mode can not stop")
        # else:
        #     logging.info("log mode stop")

        # if self.data['mode'] == 'deep_learn_ids':
        #     self.deep_learn_control.stop()
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
