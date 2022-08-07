import re
file_pattern = r'.*[0-9]*\/log\/(.*)'
file_patt_rule = re.compile(file_pattern)
file_name = '/home/jxy/final_test/1001/log/log.pacp.16598645648'
output_name = file_patt_rule.match(file_name)[1]
print(output_name)
