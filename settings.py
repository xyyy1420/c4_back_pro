import os
class Sensor():
    def __init__(self,log_path='/usr/local/snort/log/') -> None:
        self.snort_base_path='/usr/local/snort/'
        self.daq_base_path='/usr/local/lib/daq/'
        self.snort_log_path=log_path
        self.snort_setting_base_path='/usr/local/snort/etc/snort/'
        self.snort_setting_snortdefault_path=os.path.join(self.snort_setting_base_path,'snort_default.lua')
        self.snort_setting_snort_path=os.path.join(self.snort_setting_base_path,'snort.lua')
        self.snort_setting_talos_path=os.path.join(self.snort_setting_base_path,'talos.lua')
        self.snort_setting_balanced_path=os.path.join(self.snort_setting_base_path,'balanced.lua')
        self.snort_setting_connectivity_path=os.path.join(self.snort_setting_base_path,'connectivity.lua')
        self.snort_setting_file_magic_path=os.path.join(self.snort_setting_base_path,'magic.lua')
        self.snort_setting_inline_path=os.path.join(self.snort_setting_base_path,'inline.lua')
        self.snort_setting_max_detect_path=os.path.join(self.snort_setting_base_path,'max_detect.lua')
        self.snort_setting_security_path=os.path.join(self.snort_setting_base_path,'security.lua')

    