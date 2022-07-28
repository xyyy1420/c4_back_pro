from urllib import response
import requests
import json
import subprocess


#DONE：自batch中引入，不需要在monitor中再引入
class DataSend(object):
    #DONE：补充好默认参数
    def __init__(self,url='http://192.168.1.144:8000/api/insertToDeepLearn',header=''):
        self.url=url
        self.header=header
        self.req=None
        ip="192.168.1.144"
        if subprocess.call(["ping","-p","8000","-c","2",ip]):
            self.state=0
        else:
            self.state=1

    def send_data(self,msg):
#        self.req=requests.post(url=self.url,headers=self.header,data=msg)
        if self.state==0:
            print("host is unalive")
            return 
        else:
            print(msg)
            data1={"xxx":"key"}
            self.req=requests.post(url=self.url,data=msg)
            print(self.req.text)



#DONE：在这里删除剩下不需要的测试内容
# data3={
#     "timestamp" : "07/07-01:19:02.802509", "iface" : "bad.pcap", "src_addr" : "192.168.10.8", "src_port" : 53966, "dst_addr" : "205.174.165.73", "dst_port" : 444, "proto" : "TCP", "action" : "allow", "msg" : "INDICATOR-COMPROMISE Microsoft cmd.exe banner", "priority" : 1, "class" : "Unknown Traffic", "sid" : 46983 
# }

# data1 = {'xxxxxx':'hello'}

# headers={'Content-Type':'application/json'}

# response=requests.post(url='http://192.168.43.135:8000/api/getdata',data=data3)

# print(response)
# print(response.text)
