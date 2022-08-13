import re

file_pattern = r'.*[0-9]*\/log\/(.*)'
patt = re.compile(file_pattern)
name = patt.match('/home/jxy/final_test/1001/log/log.pcap.1659864563')
print(name[0], name[1])
