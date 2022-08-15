import logging
import subprocess
import re
reg_sid = re.compile(r'.*sid:([0-9]*)')


def write_rule(self, file_path, rules):
    # DONE:在file_path中写入一条rules ，使用追加写入，然后需要
    sh_cmd = f"echo {rules} | tee -a {file_path}"
    # sh_cmd="echo "+rules+' | tee -a '+self.rule_path+file_name
    # echo "hello" | tee -a rule.rules
    sh_cmd = [sh_cmd]
    with subprocess.Popen(sh_cmd, shell=True) as res:
        pass
    if res.returncode != None:
        logging.info(f"rule write in {file_path} success")

    else:
        logging.error("command failed")


def del_rules(self, file_path, rules):
    # DONE：从filepath中删除rules这一条，可以根据sid匹配
    sid = reg_sid.match(rules)[1]
    sh_cmd = f"sed -i /.*sid:{sid}/d {file_path}"
    # sh_cmd = "sed -i /.*sid:"+str(sid)+"/d "+self.rule_path+file_name
    # sed -i /.*sid:123456/d /usr/local/snort/rules/1111.rules
    with subprocess.Popen(sh_cmd, shell=True) as res:
        pass
    if res.returncode != None:
        logging.info("rule delete")

    else:
        logging.error("delete rule error")
