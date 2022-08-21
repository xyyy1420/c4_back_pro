import os
from subprocess import Popen
import logging


class SensorController(object):
    def __init__(self, data) -> None:

        # self.thread_pool = []
        # self.md5 = hashlib.md5()

        self.data = data
        self.test_cmd = 'snort -c %s -R %s '
        self.ids_pcap_cmd = 'snort -c %s -r %s -l %s -m 066 '
        self.ids_interface_cmd = 'snort -c %s -i %s -l %s -m 066 '

        self.log_path = data['log_path']
        self.rule_path = data['rule_path']
        self.rule_file = os.path.join(self.rule_path, data['rule_file'])

        # self.base_rule_path = '/usr/local/snort/rule/'
        # self.deep_learn_rule = os.path.join(
        # self.base_rule_path, 'deep_learn.rules')
        self.deep_learn_rule = self.data['deep_rule']

        self.base_config_path = '/usr/local/snort/etc/snort/snort.lua'

        self.reload_signal = 1
        self.shutdown_signal = 2

        self.control_hook = []

        logging.info("Sensor controler create")

    def start_sensor(self):
        # 命令参数解释
        # -c 配置文件
        # -l日志存储目录
        # -r pcap包的目录
        # -R 规则文件目录
        # -i 接口
        # mode:pcap_ids,interface_ids,interface_ips,deep_learn_ids
        # operate:start,update,stop
        # name
        # description
        # log_file
        # rule_file
        # interface
        # pcap_path
        #
        args = self.data
        logging.warn(args)

        mode = args['mode']
        interface = args['interface']

        if mode == 'pcap_ids':
            pcap_path = args['pcap_path']
            base_cmd = f"snort -c {self.base_config_path} -l {self.log_path} -r {pcap_path} -R {self.rule_file} -m 066"
            self.control_hook.append(self.pcap_ids_start(base_cmd))

        elif mode == 'interface_ids':
            base_cmd = f"snort -c {self.base_config_path} -l {self.log_path} -i {interface} -R {self.rule_file} -m 066"
            self.control_hook.append(self.interface_ids_start(base_cmd))

        elif mode == 'interface_ips':
            base_cmd = f"snort -c {self.base_config_path} -l {self.log_path} -i {interface} -R {self.rule_file} -m 066"
            self.control_hook.append(self.interface_ips_start(base_cmd))
        elif mode == 'deep_learn_ids':
            rule_path = self.deep_learn_rule
            base_cmd = f"snort -c {self.base_config_path} -l {self.log_path} -i {interface} -R {rule_path} -m 066"
            self.control_hook.append(self.deep_learn_ids_start(base_cmd))

        # logging.error(self.control_hook)
        if self.control_hook == -1:
            return -1
        else:
            return self.control_hook

    def pcap_ids_start(self, cmd):
        logging.warn(cmd)
        res = Popen(cmd, shell=True)
        return res
        if res.poll() != 0:
            return res
        else:
            return -1

    def interface_ids_start(self, cmd):
        logging.warn(cmd)
        res = Popen(cmd, shell=True)
        return res
        if res.poll() != 0:
            return res
        else:
            return -1

    def interface_ips_start(self, cmd):
        logging.warn(cmd)
        res = Popen(cmd, shell=True)
        return res
        if res.poll() != 0:
            return res
        else:
            return -1

    def deep_learn_ids_start(self, cmd):
        logging.warn(cmd)
        res = Popen(cmd, shell=True)
        return res
        if res.poll() != 0:
            return res
        else:
            return -1

    # TODO:change mode to operate :(start,stop,update) need:(name,description,and other args)

    def stop_sensor(self, res):
        # name = args['name']
        # description = args['description']
        # sensor_md5 = self.hash_cal(name+description)

        # thread_control = None

        # for i in self.thread_pool and thread_control is None:
        #     for md5, res in i.item():
        #         if md5 == sensor_md5:
        #             thread_control = res
        #             break

        # if thread_control is None:
        #     print("error,thread not fount")
        #     return

        # self.control_hook[0].send_signal(self.shutdown_signal)
        # if self.control_hook[0].poll() != 0:
        #     return 1
        # else:
        #     return -1
        res.send_signal(self.shutdown_signal)
        if res.poll() != 0:
            return 1
        else:
            return -1

    # def test_policy(self, policy_url):
    #     rule_path = os.path.join(self.base_rule_path, policy_url)
    #     local_cmd = self.test_cmd % (self.base_config_path, rule_path)
    #     res = Popen(local_cmd, shell=True)

    #     return res.poll()


# TODO：完成错误返回的部分，处理update与stop部分


# sid
# priority
# classtype
# interface
# src_addr
# src_port
# dst_addr
# dst_port
# protocl
# timestamp
# msg

# src_ip
# dst_ip
# src_port
# dst_port
# timestamp
# attack
