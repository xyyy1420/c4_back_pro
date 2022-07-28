import dpkt
import socket
import time
from snortunsock import snort_listener
import requests
import sys
import re
import random
import pickle
from iptable import insert_rule, del_rule


def mac_addr(address):
    """Convert a MAC address to a readable/printable string
       Args:
           address (str): a MAC address in hex form (e.g. '\x01\x02\x03\x04\x05\x06')
       Returns:
           str: Printable/readable MAC address
    """
    return ':'.join('%02x' % ord(b) for b in address)


def ip_to_str(address):
    """Print out an IP address given a string
    Args:
        address (inet struct): inet network address
    Returns:
        str: Printable/readable IP address
    """
    return socket.inet_ntop(socket.AF_INET, address)


def main():
    protocol = {'1': "ICMP", '2': "IGMP", '3': "GGP",
                '4': "IPv6", '5': "ST", '6': "TCP", '17': "UDP"}

    with open('data.pickle', 'wb') as f:
        s = set()
        for msg in snort_listener.start_recv("/home/xxx/snort_log/snort_alert"):
            print('alertmsg: %s' % ''.join(str(msg.alertmsg[0], 'utf-8')))
            buf = msg.pkt
            sig_id = msg.event.sig_id
            sig_rev = msg.event.sig_rev
            sig_classification = msg.event.classification
            priority = msg.event.priority
            event_id = msg.event.event_id
            event_reference = msg.event.event_reference
            ref_time = msg.event.ref_time
#            print(sig_id,sig_rev,sig_classification,priority,event_id,event_reference,ref_time.tv_sec,ref_time.tv_usec)

           # print(time.gmtime(ref_time.tv_usec))

            # Unpack the Ethernet frame (mac src/dst, ethertype)
            eth = dpkt.ethernet.Ethernet(buf)
            # print('Ethernet Frame: ', mac_addr(eth.src), mac_addr(eth.dst), eth.type)

            if eth.type != dpkt.ethernet.ETH_TYPE_IP:
                print('Non IP Packet type not supported %s\n' %
                      eth.data.__class__.__name__)

            # Now unpack the data within the Ethernet frame (the IP packet)
            # Pulling out src, dst, length, fragment info, TTL, and Protocol
            ip = eth.data

            # Pull out fragment information (flags and offset all packed into off field, so use bitmasks)
            #do_not_fragment = bool(ip.off & dpkt.ip.IP_DF)
            #more_fragments = bool(ip.off & dpkt.ip.IP_MF)
            #fragment_offset = ip.off & dpkt.ip.IP_OFFMASK

            msg = msg.alertmsg[0].decode("utf-8")
            r = re.compile(r'"(.*)"')
            msg = r.match(msg)[1]
            act = "alert"
            class1 = ["NMAP SCAN", "UNKNOWN attack", "Attempted DDOS",
                      "Attempt login", "Generic ICMP event", "TCP connection"]
            a = random.choice(class1)
            a = "Geneic ICMP event"
            classf = None
            if 'attack' in msg:
                classf = 1
            else:
                classf = 0
            classf = 1
            dport = ''
            sport = ''
            if ip.p != 6 or ip.p != 17:
                dport = 0
                sport = 0
            else:
                dport = ip.data.dport
                sport = ip.data.sport
            src_ip = ip_to_str(ip.src)
            if src_ip in s:
                pass
            else:
                s.add(src_ip)
                insert_rule(src_ip, 'ens192')
            # Print out the info
        #    print('IP: %s -> %s   (len=%d ttl=%d DF=%d MF=%d offset=%d)\n' % \
        #          (ip_to_str(ip.src), ip_to_str(ip.dst), ip.len, ip.ttl, do_not_fragment, more_fragments, fragment_offset))
            # time="2022/06/27:15:16:17"

            time1 = time.strftime("%Y/%m/%d/%X")
            final_msg = {"sid": sig_id, "priority": priority, "class": a, "iface": "ens192", "action": act, "src_addr": ip_to_str(
                ip.src), "src_port": sport, "dst_addr": ip_to_str(ip.dst), "dst_port": dport, "proto": protocol[str(ip.p)], "timestamp": time1, "msg": msg, "is_attack": classf}
            req = requests.post(
                url="http://192.168.1.144:8000/api/insertData", data=final_msg)
            print(req.text)
            print(final_msg)


if __name__ == '__main__':
    main()
