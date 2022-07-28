import os
import re
import subprocess
import sys
import logging

class RuleOp(object):
    def __init__(self):
        self.stdout=''
        self.reg_sid=re.compile(r'.*sid:([0-9]*)')
        self.rule_path="/usr/local/snort/rules/"
        self.setting_path="/usr/local/snort/etc/snort/snort.lua"
        self.rule_path_test="./"
        log_format="%(asctime)s - %(levelname)s - %(funcName)s - %(message)s"
        logging.basicConfig(level=logging.INFO,format=log_format)
        logging.info("RULE OP create")

        
    
    def write_rule(self,file_name,rules):
        #DONE:在file_path中写入一条rules ，使用追加写入，然后需要
        sh_cmd="echo "+rules+' | tee -a '+self.rule_path+file_name
        #echo "hello" | tee -a rule.rules
        sh_cmd=[sh_cmd]
        with subprocess.Popen(sh_cmd,shell=True) as res:
            pass
        if res.returncode!=None:
            logging.info("rule write in"+file_name+"success")
            self.reboot_snort()
        else:
            logging.error("command failed")

    def del_rules(self,file_name,rules):
        #DONE：从filepath中删除rules这一条，可以根据sid匹配
        sid=self.reg_sid.match(rules)[1]
        sh_cmd="sed -i /.*sid:"+str(sid)+"/d "+self.rule_path+file_name
        # sed -i /.*sid:123456/d /usr/local/snort/rules/1111.rules
        with subprocess.Popen(sh_cmd,shell=True) as res:
            pass
        if res.returncode!=None:
            logging.info("rule delete")
            self.reboot_snort()
        else:
            logging.error("delete rule error")

    def write_rule_set(self,file_name):
        #DONE:写入配置文件（include），创建文件
        file_path=self.rule_path+file_name
        if os.path.exists(file_path):
            sh_cmd=["touch",file_path]
            res=subprocess.Popen(sh_cmd)
            logging.info("file create")
        else:
            logging.warning("file is here")
        sh_cmd=["sed '199,199a\include $RULE_PATH/"+file_name+"\' /usr/local/snort/etc/snort/snort.lua -i"]
        #sed '199,199a\include $RULE_PATH/1111.rules\ /usr/local/snort/etc/snort/snort.lua'
        with subprocess.Popen(sh_cmd,shell=True) as proc:
            pass
        if proc.returncode!=None:
            logging.info("write rule set in settings")
            self.reboot_snort()
        else:
            logging.error("write rule set in settings fault")

    def del_rule_res(self,file_name):
        #DONE：从配置中删除规则集
        cmd_str="sed -i '/.*$RULE_PATH\/"+file_name+"/d' /usr/local/snort/etc/snort/snort.lua"
        #sed -i '/.*$RULE_PATH\/1111.rules/d /usr/local/snort/etc/snort/snort.lua'
        sh_cmd=[cmd_str]
        with subprocess.Popen(sh_cmd,shell=True) as proc:
            pass
        if proc.returncode!=None:
            logging.info("rule set delete from settings")
            if os.path.exists("/usr/local/snort/rules/"+file_name):
                subprocess.call("rm","/usr/local/snort/rules/"+file_name)
            self.reboot_snort()
        else:
            logging.error("faile delete rule set")

    def reboot_snort(self):
        #DONE:重启snort
        sh_cmd=["ps -A | grep snort | awk -v FS=' ' '{print($1)}'"]
        with subprocess.Popen(sh_cmd,shell=True,stdout=subprocess.PIPE) as proc:
            self.stdout=proc.stdout.read()
        if proc.returncode==None:
            logging.error("snort is not running")
        else:
            self.stdout=self.stdout.decode("utf-8").replace('\n','')
            kill_res=subprocess.Popen(["kill","-hup",self.stdout])
            logging.info("reload")
    
    def do_cmd(self,sh_cmd):
        with subprocess.Popen(sh_cmd,shell=True,stdout=subprocess.PIPE) as proc:
            pass
        return proc

#if __name__=="__main__":
#
#    obj=RuleOp()
##    obj.del_rules("1111.rules","abc sid:123456")
#    obj.write_rule("1111.rules","aaa")
#    obj.write_rule_set('12211.rules')
#    obj.reboot_snort()
#    obj.del_rule_res('12211.rules')
