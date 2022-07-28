import subprocess
import os

def insert_rule(src_ip,iface,proto=''):
    cmd_i="iptables -I INPUT -s %s -i %s -j DROP" % (src_ip,iface)
    subprocess.Popen(cmd_i,shell=True)
def del_rule(src_ip,iface,proto=''):
    cmd_i="iptables -D INPUT -s %s -i %s -j DROP" % (src_ip,iface)
    subprocess.Popen(cmd_i,shell=True)


