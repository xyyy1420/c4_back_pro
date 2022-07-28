import os
import socket
import logging
from . import alert
import dpkt


class LogReceive(object):
    def __init__(self) -> None:
        logging.basicConfig(
            format='%(levelname)s:%(message)s', level=logging.DEBUG)

        self.protocol = {'1': "ICMP", '2': "IGMP", '3': "GGP",
                         '4': "IPv6", '5': "ST", '6': "TCP", '17': "UDP"}

        self.classtype = {
            {"name": 'not-suspicious', "priority": 3,
             "text": 'Not Suspicious Traffic', "number": 1},

            {"name": 'unknown', "priority": 3,
             "text": 'Unknown Traffic', "number": 2},

            {"name": 'bad-unknown', "priority": 2,
             "text": 'Potentially Bad Traffic', "number": 3},

            {"name": 'attempted-recon', "priority": 2,
             "text": 'Attempted Information Leak', "number": 4},

            {"name": 'successful-recon-limited', "priority": 2,
             "text": 'Information Leak', "number": 5},

            {"name": 'successful-recon-largescale', "priority": 2,
             "text": 'Large Scale Information Leak', "number": 6},

            {"name": 'attempted-dos', "priority": 2,
             "text": 'Attempted Denial of Service', "number": 7},

            {"name": 'successful-dos', "priority": 2,
             "text": 'Denial of Service', "number": 8},

            {"name": 'attempted-user', "priority": 1,
             "text": 'Attempted User Privilege Gain', "number": 9},

            {"name": 'unsuccessful-user', "priority": 1,
             "text": 'Unsuccessful User Privilege Gain', "number": 10},

            {"name": 'successful-user', "priority": 1,
             "text": 'Successful User Privilege Gain', "number": 11},

            {"name": 'attempted-admin', "priority": 1,
             "text": 'Attempted Administrator Privilege Gain', "number": 12},

            {"name": 'successful-admin', "priority": 1,
             "text": 'Successful Administrator Privilege Gain', "number": 13},

            {"name": 'rpc-portmap-decode', "priority": 2,
             "text": 'Decode of an RPC Query', "number": 14},

            {"name": 'shellcode-detect', "priority": 1,
             "text": 'Executable code was detected', "number": 15},

            {"name": 'string-detect', "priority": 3,
             "text": 'A suspicious string was detected', "number": 16},

            {"name": 'suspicious-filename-detect', "priority": 2,
             "text": 'A suspicious file"name" was detected', "number": 17},

            {"name": 'suspicious-login', "priority": 2,
             "text": 'An attempted login using a suspicious user"name" was detected', "number": 18},

            {"name": 'system-call-detect', "priority": 2,
             "text": 'A system call was detected', "number": 19},

            {"name": 'tcp-connection', "priority": 4,
             "text": 'A TCP connection was detected', "number": 20},

            {"name": 'trojan-activity', "priority": 1,
             "text": 'A Network Trojan was detected', "number": 21},

            {"name": 'unusual-client-port-connection', "priority": 2,
             "text": 'A client was using an unusual port', "number": 22},

            {"name": 'network-scan', "priority": 3,
             "text": 'Detection of a Network Scan', "number": 23},

            {"name": 'denial-of-service', "priority": 2,
             "text": 'Detection of a Denial of Service Attack', "number": 24},

            {"name": 'non-standard-protocol', "priority": 2,
             "text": 'Detection of a non-standard protocol or event', "number": 25},

            {"name": 'protocol-command-decode', "priority": 3,
             "text": 'Generic Protocol Command Decode', "number": 26},

            {"name": 'web-application-activity', "priority": 2,
             "text": 'Access to a potentially vulnerable web application', "number": 27},

            {"name": 'web-application-attack', "priority": 1,
             "text": 'Web Application Attack', "number": 28},

            {"name": 'misc-activity', "priority": 3,
             "text": 'Misc activity', "number": 29},

            {"name": 'misc-attack', "priority": 2,
             "text": 'Misc Attack', "number": 30},

            {"name": 'icmp-event', "priority": 3,
             "text": 'Generic ICMP event', "number": 31},

            {"name": 'inappropriate-content', "priority": 1,
             "text": 'Inappropriate Content was Detected', "number": 32},

            {"name": 'policy-violation', "priority": 1,
             "text": 'Potential Corporate Privacy Violation', "number": 33},

            {"name": 'default-login-attempt', "priority": 2,
             "text": 'Attempt to login by a default user"name" and password', "number": 34},

            {"name": 'sdf', "priority": 2,
             "text": 'Senstive Data', "number": 35},

            {"name": 'file-format', "priority": 1,
             "text": 'Known malicious file or file based exploit', "number": 36},

            {"name": 'malware-cnc', "priority": 1,
             "text": 'Known malware command and control traffic', "number": 37},

            {"name": 'client-side-exploit', "priority": 1,
             "text": 'Known client side exploit attempt', "number": 38}
        }

    def recv_msg(self, socket_file=None):

        BUFSIZE = alert.AlertPkt._ALERTPKT_SIZE
        sockf = socket_file
        # TODO:需要设置这个每个log目录下的sock
        if sockf is None:
            sockf = socket_file

        if os.path.exists(sockf):
            os.unlink(sockf)

        unsock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        unsock.bind(sockf)
        logging.warning('unix socket start listening...')

        while True:
            data = unsock.recv(BUFSIZE)
            # parsed_msg=alert.AlertPkt.parser(data)
            # if parsed_msg:
            #     yield parsed_msg
            if parsed_msg := alert.AlertPkt.parser(data):
                yield parsed_msg

    def get_msg(self):

        with open('data.pickle', 'wb') as f:
            for msg in self.recv_msg():
                buf = msg.pkt
                sig_id = msg.event.sig_id
                sig_rev = msg.event.sig_rev
                sig_class_type = msg.event.classification
                priority = msg.event.priority
                event_id = msg.event.event_id
                event_reference = msg.event.event_reference
                ref_time = msg.event.ref_time
