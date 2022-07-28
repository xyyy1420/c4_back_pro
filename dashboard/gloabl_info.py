
import psutil
import os
from system_info import SystemInfo
import requests

class GlobalInfo(SystemInfo):
    def __init__(self,**mlargs) -> None:
        super().__init__()

        self.interface_info=self.get_interface_info()

        self.config_info=self.get_config_info()

        self.ip_api='http://ip-api.com/json/'



    def get_interface_info(self):
        ip_and_interface=psutil.net_if_addrs()
        final_data={}
        for interface,value in ip_and_interface.items():
            # print(type(v),v)
            final_data.update({interface:value[0].address})

        return final_data

    def get_config_info(self,):
        snort_base_path='/usr/local/snort/'
        snort_setting_base_path=os.path.join(snort_base_path,'etc','snort')
        config_path={
           "snort_base_path":snort_base_path,
           "daq_base_path":'/usr/local/lib/daq/',
           "snort_log_path":'/usr/local/snort/log',
           "snort_setting_base_path":snort_setting_base_path,
           "snort_setting_snortdefault_path":os.path.join(snort_setting_base_path,'snort_default.lua'),
           "snort_setting_snort_path":os.path.join(snort_setting_base_path,'snort.lua'),
           "snort_setting_talos_path":os.path.join(snort_setting_base_path,'talos.lua'),
           "snort_setting_balanced_path":os.path.join(snort_setting_base_path,'balanced.lua'),
           "snort_setting_connectivity_path":os.path.join(snort_setting_base_path,'connectivity.lua'),
           "snort_setting_file_magic_path":os.path.join(snort_setting_base_path,'magic.lua'),
           "snort_setting_inline_path":os.path.join(snort_setting_base_path,'inline.lua'),
           "snort_setting_max_detect_path":os.path.join(snort_setting_base_path,'max_detect.lua'),
           "snort_setting_security_path":os.path.join(snort_setting_base_path,'security.lua'),
           "snort_setting_ipblack_path":os.path.join(snort_base_path,'intel','ip-blocklist'),
           "snort_setting_ipwhite_path":os.path.join(snort_base_path,'intel','ip-allowlist')
        }
        return config_path
    
    def get_ip_country_city(self,ip=''):
        api_url=self.ip_api+ip+'?lang=zh-CN'
        res=requests.get(url=api_url)
        return res.text




