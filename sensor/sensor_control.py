import hashlib
import os
from subprocess import Popen
import socket
import logging


class SensorController(object):
    def __init__(self, path, data) -> None:

        # self.thread_pool = []
        # self.md5 = hashlib.md5()

        self.test_cmd = 'snort -c %s -R %s '
        self.ids_pcap_cmd = 'snort -c %s -r %s -l %s -m 066 '
        self.ids_interface_cmd = 'snort -c %s -i %s -l %s -m 066 '

        self.log_path = path['log_path']
        self.rule_path = path['rule_path']
        # self.config_path = path['config_path']
        self.rule_file = os.path.join(self.rule_path, data['rule_file'])

        # self.base_rule_path = '/usr/local/snort/rule/'

        self.deep_learn_rule = os.path.join(
            self.base_rule_path, 'deep_learn.rules')

        # self.log_path_base = {
        #     "ids_pcap_log_path": '/usr/local/snort/log/pcap/',
        #     "ids_deep_learn_log_path": '/usr/local/snort/log/deep/',
        #     "ips_deep_learn_log_path": '/usr/local/snort/log/deep/',
        #     "ids_interface_log_path": '/usr/local/snort/log/interface/',
        #     "ips_interface_log_path": '/usr/local/snort/log/interface/'
        # }

        self.base_config_path = '/usr/local/snort/etc/snort/snort.lua'

        self.reload_signal = 1
        self.shutdown_signal = 2

        self.control_hook = None

        # self.rule_path_base = {
        #     "ids_pcap_rule_path": '/usr/local/snort/rule/pcap/',
        #     "ids_deep_learn_rule_path": '/usr/local/snort/rule/deep/',
        #     "ips_deep_learn_rule_path": '/usr/local/snort/rule/deep/',
        #     "ids_interface_rule_path": '/usr/local/snort/rule/interface/',
        #     "ips_interface_rule_path": '/usr/local/snort/rule/interface/',
        # }

        # self.ids_deep_learn_log_path = '/usr/local/snort/log/deep/'
        # self.ips_deep_learn_log_path = '/usr/local/snort/log/deep/'
        # self.ids_pcap_log_path = '/usr/local/snort/log/pcap/'
        # self.ids_interface_log_path = '/usr/local/snort/log/interface/'
        # self.ips_interface_log_path = '/usr/local/snort/log/interface/'

    # 传参数：new_sensor_args_deal(mode='pcap_ids',name='new sensor',........)
        logging.info("sensor controler create")

    def start_sensor(self, **args):
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

        mode = args['mode']

        # log_file = args['log_file']
        # rule_file = args['rule_file']
        interface = args['interface']

        # name = args['name']
        # description = args['description']
        # sensor_md5 = self.hash_cal(name+description)

        if mode == 'pcap_ids':
            pcap_path = args['pcap_path']
            # rule_path = os.path.join(self.base_rule_path, rule_file)

            base_cmd = f"snort -c {self.base_config_path} -l {self.log_path} -r {pcap_path} -R {self.rule_file}"
            self.control_hook = self.pcap_ids_start(base_cmd)

        elif mode == 'interface_ids':
            # rule_path = os.path.join(self.base_rule_path, rule_file)
            base_cmd = f"snort -c {self.base_config_path} -l {self.log_path} -i {interface} -R {self.rule_file}"
            self.control_hook = self.interface_ids_start(base_cmd)

        elif mode == 'interface_ips':
            # rule_path = os.path.join(self.base_rule_path, rule_file)
            base_cmd = f"snort -c {self.base_config_path} -l {self.log_path} -i {interface} -R {self.rule_file}"
            self.control_hook = self.interface_ips_start(base_cmd)
        elif mode == 'deep_learn_ids':
            rule_path = self.deep_learn_rule
            base_cmd = f"snort -c {self.base_config_path} -l {self.log_path} -i {interface} -R {rule_path}"
            self.control_hook = self.deep_learn_ids_start(base_cmd)

    def pcap_ids_start(self, cmd):
        res = Popen(cmd, shell=True)
        if res.poll() != 0:
            return res
        else:
            return -1

    def interface_ids_start(self, cmd):
        res = Popen(cmd, shell=True)
        if res.poll() != 0:
            return res
        else:
            return -1

    def interface_ips_start(self, cmd):
        res = Popen(cmd, shell=True)
        if res.poll() != 0:
            return res
        else:
            return -1

    def deep_learn_ids_start(self, cmd):
        res = Popen(cmd, shell=True)
        if res.poll() != 0:
            return res
        else:
            return -1

    # TODO:change mode to operate :(start,stop,update) need:(name,description,and other args)

    def stop_sensor(self, **args):
        name = args['name']
        description = args['description']
        sensor_md5 = self.hash_cal(name+description)

        thread_control = None

        for i in self.thread_pool and thread_control is None:
            for md5, res in i.item():
                if md5 == sensor_md5:
                    thread_control = res
                    break

        if thread_control is None:
            print("error,thread not fount")
            return

        thread_control.send_singal(self.shutdown_signal)
        self.thread_pool.remove({sensor_md5, thread_control})

    # def stop_update_sensor(self, **args):
    #     name = args['name']
    #     description = args['description']
    #     sensor_md5 = self.hash_cal(name+description)

    #     mode = args['mode']

    #     thread_control = None

    #     for i in self.thread_pool and thread_control is None:
    #         for md5, res in i.item():
    #             if md5 == sensor_md5:
    #                 thread_control = res
    #                 break

    #     if thread_control is None:
    #         print("error,thread not fount")
    #         return

    #     if mode == 'update':
    #         thread_control.send_singal(self.reload_signal)
    #     else:
    #         thread_control.send_singal(self.shutdown_signal)
    #         self.thread_pool.remove({sensor_md5, thread_control})

    #     if thread_control.poll() != 0:
    #         if mode == 'update':
    #             print("thread update")
    #         else:
    #             print("thread shutdown failed")
    #     elif thread_control.poll() == 0:
    #         if mode == 'shutdown':
    #             print("thread shutdown")
    #         else:
    #             print("update failed thread stop")

    def test_policy(self, policy_url):
        rule_path = os.path.join(self.base_rule_path, policy_url)
        local_cmd = self.test_cmd % (self.base_config_path, rule_path)
        res = Popen(local_cmd, shell=True)

        return res.poll()

    # def hash_cal(self, str_value):
    #     self.md5.update(str_value.encode('utf-8'))
    #     return self.md5.hexdigest()


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
