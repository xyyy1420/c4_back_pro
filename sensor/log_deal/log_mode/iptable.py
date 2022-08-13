import subprocess


def insert_rule(src_ip, proto=''):
    cmd_i = f"iptables -I INPUT -s {src_ip} -j DROP"
    subprocess.Popen(cmd_i, shell=True)


def del_rule(src_ip, proto=''):
    cmd_i = f"iptables -D INPUT -s {src_ip} -j DROP"
    subprocess.Popen(cmd_i, shell=True)
