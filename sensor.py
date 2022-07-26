import os
from turtle import home
class Sensor():
    def __init__(self,interface,home_net,log_path='/usr/local/snort/log/') -> None:

        self.snort_base_path='/usr/local/snort/'
        self.daq_base_path='/usr/local/lib/daq/'
        self.snort_log_path=log_path
        self.snort_setting_base_path='/usr/local/snort/etc/snort/'
        self.snort_setting_snort_path=os.path.join(self.snort_setting_base_path,'snort.lua')

        self.interface=interface
        self.home_net=home_net


    def automatic_create_sensor(self):
        pass 

    def self_config_sensor(self):
        pass 