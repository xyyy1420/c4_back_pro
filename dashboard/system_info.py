import psutil
import time
class SystemInfo():
    def __init__(self,io_path="/",freq=1,multiple=1024):

        self.io_path=io_path
        self.freq=freq
        self.multiple=multiple
        
        self.interface,self.old_recv,self.old_sent=self.get_network_info()

        # for key in self.interface:
        #     if key.startswith("lo") or key.startswith("VMware"):
        #         self.interface.remove(key)

        # self.info_dict=self.info_update()

        # self.start_update()


    
    def get_network_info(self):
        recv={}
        sent={}
        net_total_info=psutil.net_io_counters(pernic=True)
        interfaces=net_total_info.keys()
        for i in interfaces:
            recv.update({i:net_total_info.get(i).bytes_recv})
            sent.update({i:net_total_info.get(i).bytes_sent})

        return interfaces,recv,sent

    def get_network_rate(self,num,multiple):#multiple为1024时输出单位为K/S
        interface,new_recv,new_sent=self.get_network_info()
        interface=self.interface
        network_in={}
        network_out={}
        for i in interface:
            network_in.update({i:float("%.3f" % ((new_recv.get(i)-self.old_recv.get(i))/num/multiple))})
            network_out.update({i:float("%.3f" % ((new_sent.get(i)-self.old_sent.get(i))/num/multiple))})

        self.old_recv=new_recv
        self.old_sent=new_sent

        return interface,network_in,network_out

    def mem_info_update(self):
        mem_total_info=psutil.virtual_memory()
        return [mem_total_info.total,mem_total_info.free]

    def cup_info_update(self):
        return [psutil.cpu_count(),psutil.cpu_percent()]

    def disk_info_update(self):
        disk_total_info=psutil.disk_usage(self.io_path)
        return [disk_total_info.total,disk_total_info.used,disk_total_info.free,disk_total_info.percent]

    def info_update(self):

        disk_total_info=self.disk_info_update()
        mem_total_info=self.mem_info_update()
        cpu_total_info=self.cup_info_update()
        interface,recv_rate,sent_rate=self.get_network_rate(self.freq,self.multiple)

        info_dict={
            "cpu_info":{
                "cpu_count":cpu_total_info[0],
                "cpu_each_persent":cpu_total_info[1],

            },
            "mem_info":{
                "total_mem":mem_total_info[0],
                "use_able":mem_total_info[1]
            },
            "io_info":{
                "disk_mountpoint":self.io_path,
                "total_disk":disk_total_info[0],
                "used_disk":disk_total_info[1],
                "free_disk":disk_total_info[2],
                "used_percent":disk_total_info[3]
            },
            "net_info":{
                "interfaces":self.interface,
                "recv_rate":recv_rate,
                "sent_rate":sent_rate
            }
        }

        return info_dict

    def start_update(self):
        while True:
            time.sleep(self.freq)
            # self.info_send_out(self.info_update())
            print(self.info_update())

    def info_send_out(self):
        pass
    
    