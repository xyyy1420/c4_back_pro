from re import sub
import subprocess
#"iptables -A INPUT -s {} -p {} -dport {} -j DROP"


def drop(ip, protocol):
    cmd = f'iptabltes -A INPUT -s {ip} -p {protocol} -j DROP'
    subprocess.Popen(cmd=cmd, shell=True)


def acceept(ip, protocol):
    cmd = f'iptabltes -D INPUT -s {ip} -p {protocol} -j DROP'
    subprocess.Popen(cmd=cmd, shell=True)
