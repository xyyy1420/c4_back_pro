import os
import socket
import logging
from snortunsock import alert
import dpkt
import time
from threading import Thread
from ..log_sender import log_sender


class LogReceive(object):
    def __init__(self, data) -> None:

        self.socket_file = data['sock_file']

        self.protocol = {'1': "ICMP", '2': "IGMP", '3': "GGP",
                         '4': "IPv6", '5': "ST", '6': "TCP",
                         '7': "CBT", '8': "EGP", '9': "IGP",
                         '17': "UDP", '41': "IPv6", '43': "IPv6-Route",
                         '44': "IPv6-Frag", '58': "IPv6-ICMP", '59': "IPv6-NoNxt",
                         '60': "IPv6-Opts", }

        self.classtype = {
            '1': {"name": 'not-suspicious', "priority": 3,
                  "text": 'Not Suspicious Traffic'},

            '2': {"name": 'unknown', "priority": 3,
                  "text": 'Unknown Traffic'},

            '3': {"name": 'bad-unknown', "priority": 2,
                  "text": 'Potentially Bad Traffic'},

            '4': {"name": 'attempted-recon', "priority": 2,
                  "text": 'Attempted Information Leak'},

            '5': {"name": 'successful-recon-limited', "priority": 2,
                  "text": 'Information Leak'},

            '6': {"name": 'successful-recon-largescale', "priority": 2,
                  "text": 'Large Scale Information Leak'},

            '7': {"name": 'attempted-dos', "priority": 2,
                  "text": 'Attempted Denial of Service'},

            '8': {"name": 'successful-dos', "priority": 2,
                  "text": 'Denial of Service'},

            '9': {"name": 'attempted-user', "priority": 1,
                  "text": 'Attempted User Privilege Gain'},

            '10': {"name": 'unsuccessful-user', "priority": 1,
                   "text": 'Unsuccessful User Privilege Gain'},

            '11': {"name": 'successful-user', "priority": 1,
                   "text": 'Successful User Privilege Gain'},

            '12': {"name": 'attempted-admin', "priority": 1,
                   "text": 'Attempted Administrator Privilege Gain'},

            '13': {"name": 'successful-admin', "priority": 1,
                   "text": 'Successful Administrator Privilege Gain'},

            '14': {"name": 'rpc-portmap-decode', "priority": 2,
                   "text": 'Decode of an RPC Query'},

            '15': {"name": 'shellcode-detect', "priority": 1,
                   "text": 'Executable code was detected'},

            '16': {"name": 'string-detect', "priority": 3,
                   "text": 'A suspicious string was detected'},

            '17': {"name": 'suspicious-filename-detect', "priority": 2,
                   "text": 'A suspicious file"name" was detected'},

            '18': {"name": 'suspicious-login', "priority": 2,
                   "text": 'An attempted login using a suspicious user"name" was detected'},

            '19': {"name": 'system-call-detect', "priority": 2,
                   "text": 'A system call was detected'},

            '20': {"name": 'tcp-connection', "priority": 4,
                   "text": 'A TCP connection was detected'},

            '21': {"name": 'trojan-activity', "priority": 1,
                   "text": 'A Network Trojan was detected'},

            '22': {"name": 'unusual-client-port-connection', "priority": 2,
                   "text": 'A client was using an unusual port'},

            '23': {"name": 'network-scan', "priority": 3,
                   "text": 'Detection of a Network Scan'},

            '24': {"name": 'denial-of-service', "priority": 2,
                   "text": 'Detection of a Denial of Service Attack'},

            '25': {"name": 'non-standard-protocol', "priority": 2,
                   "text": 'Detection of a non-standard protocol or event'},

            '26': {"name": 'protocol-command-decode', "priority": 3,
                   "text": 'Generic Protocol Command Decode'},

            '27': {"name": 'web-application-activity', "priority": 2,
                   "text": 'Access to a potentially vulnerable web application'},

            '28': {"name": 'web-application-attack', "priority": 1,
                   "text": 'Web Application Attack'},

            '29': {"name": 'misc-activity', "priority": 3,
                   "text": 'Misc activity'},

            '30': {"name": 'misc-attack', "priority": 2,
                   "text": 'Misc Attack'},

            '31': {"name": 'icmp-event', "priority": 3,
                   "text": 'Generic ICMP event'},

            '32': {"name": 'inappropriate-content', "priority": 1,
                   "text": 'Inappropriate Content was Detected'},

            '33': {"name": 'policy-violation', "priority": 1,
                   "text": 'Potential Corporate Privacy Violation'},

            '34': {"name": 'default-login-attempt', "priority": 2,
                   "text": 'Attempt to login by a default user"name" and password'},

            '35': {"name": 'sdf', "priority": 2,
                   "text": 'Senstive Data'},

            '36': {"name": 'file-format', "priority": 1,
                   "text": 'Known malicious file or file based exploit'},

            '37': {"name": 'malware-cnc', "priority": 1,
                   "text": 'Known malware command and control traffic'},

            '38': {"name": 'client-side-exploit', "priority": 1,
                   "text": 'Known client side exploit attempt'}

        }
        logging.info("log receive create")

    def recv_msg(self):
        BUFSIZE = alert.AlertPkt._ALERTPKT_SIZE
        sockf = self.socket_file
        # DONE:需要设置这个每个log目录下的sock

        if os.path.exists(sockf):
            os.unlink(sockf)

        unsock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

        logging.info(f"{sockf}")
        unsock.bind(sockf)
        logging.warning('unix socket start listening...')

        while True:
            data = unsock.recv(BUFSIZE)
            parsed_msg = alert.AlertPkt.parser(data)
            if parsed_msg:
                #target = Thread(target=self.get_msg, args=(parsed_msg))
                # target.start()
                yield parsed_msg
        # if parsed_msg := alert.AlertPkt.parser(data):
        #   yield parsed_msg

    def get_msg(self):

        # yield parsed_msg
        for msg in self.recv_msg():
            buf = msg.pkt
            sig_id = msg.event.sig_id
            sig_rev = msg.event.sig_rev
            sig_class_type = self.classtype[str(msg.event.classification)]
            priority = msg.event.priority
            event_id = msg.event.event_id
            event_reference = msg.event.event_reference
            ref_time = msg.event.ref_time

            alert_message = ''
            for i in msg.alertmsg[0]:
                if i != 0:
                    alert_message = alert_message+chr(i)
                else:
                    break

            eth = dpkt.ethernet.Ethernet(buf)
            if eth.type != dpkt.ethernet.ETH_TYPE_IP:
                print('Non IP Packet type not supported %s\n' %
                      eth.data.__class__.__name__)

            src_mac_addr = dpkt.utils.mac_to_str(eth.src)
            dst_mac_addr = dpkt.utils.mac_to_str(eth.dst)

            ip = eth.data

            src_ip = dpkt.utils.inet_to_str(ip.src)
            dst_ip = dpkt.utils.inet_to_str(ip.dst)

            if ip.p != 6 or ip.p != 17:
                dport = 0
                sport = 0
            else:
                dport = ip.data.dport
                sport = ip.data.sport

            rel_time = time.strftime("%Y-%m-%d-%X")

            final_msg = {
                'msg': alert_message,
                'sid': sig_id,
                'priority': priority,
                'class': sig_class_type['name'],
                'priority': sig_class_type['priority'],
                # 'interface': interface,
                'src_addr': src_ip,
                'src_port': sport,
                'dst_addr': dst_ip,
                'dst_port': dport,
                'protocol': self.protocol[str(ip.p)],
                'timestamp': rel_time,
                #   'attack': 1

            }
            log_sender(
                url='http://124.220.161.182:8000/api/insertSnortData', data=final_msg)
       #      logging.warn(final_msg)  # TODO:改为回送结果
