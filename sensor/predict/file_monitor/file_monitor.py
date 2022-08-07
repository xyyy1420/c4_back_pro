from fileinput import filename
import time
import sys
import logging
import re
import os

import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from multiprocessing import Queue, Process
from ..deep_learn.batch_predict import DataAnalysis
from .std_trash import suppress_stdout_stderr


class FileEventHandler(FileSystemEventHandler):
    def __init__(self, aim_path, csv_path, id):
        self.id = id
        self.aim_path = aim_path
        self.csv_path = csv_path
        file_pattern = r'.*[0-9]*\/csvs\/(.*)'
        self.file_patt_rule = re.compile(file_pattern)
        self.act_file = None
        logging.info("file monitor create")
    # 文件移动
#    def on_moved(self, event):
#        print("文件移动触发")
#        print(event)

    def on_created(self, event):
        file_name = event.src_path
        # print(file_name, self.act_file)
        if file_name != self.act_file:
            file_name = self.act_file

            logging.info(f"文件创建触发 {file_name}")

            output_name = self.file_patt_rule.match(file_name)[1]
            if output_name != None:
                logging.info("文件名已分割"+output_name[1])
                output_name = output_name[1]
            # print(output_name)
            # cicflow=Process(target=run_cicflow,args=(file_name,"/home/xxx/flow_dir/"+output_name+".csv"))
            # cicflow.start()

            run_cicflow(file_name, self.csv_path+output_name+".csv")
        # print(file_name)


#    def on_deleted(self, event):
#        print("文件删除触发")
#        print(event)
#


    def on_modified(self, event):
        if "pcap" in event.src_path:
            self.act_file = event.src_path

#        print("文件编辑触发")
#        print(event)


def cicflow(input_path, output_path):
    with suppress_stdout_stderr():
        res = subprocess.call(
            ["cicflowmeter", "-f", input_path, "-c", output_path])
    if res == 0:
        logging.info("cicflow 文件数据统计完成")
    else:
        logging.error("cicflow error,文件数据未完成统计")
        return
    run_analysis(output_path)


def run_cicflow(input_path, output_path):
    cic = Process(target=cicflow, args=(input_path, output_path,))
    cic.start()
    cic.join()
#    cic=Process(target=subprocess.call,args=(["cicflowmeter","-f",input_path,"-c",output_path]))
#    cic.start()


# Done:在这里写关于运行cicflow的部分，使用subprocess库

def analysis(path):
    logging.info(path/n/n/n)
    data = DataAnalysis(path)
    logging.info("数据分析.......")
 #   with suppress_stdout_stderr():

    data.run_module()


def run_analysis(path):
    module = Process(target=analysis, args=(path,))
    module.start()
    module.join()


# if __name__ == '__main__':
#     LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

#     logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

#     observer = Observer()  # 创建观察者对象
#     file_handler = MyEventHandler()  # 创建事件处理对象

#     aim_path = sys.argv[1] if len(sys.argv) > 1 else '.'

#     observer.schedule(file_handler, aim_path, False)  # 向观察者对象绑定事件和目录

#     observer.start()  # 启动
#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         observer.stop()
#     observer, daemon = True
#     observer.join()  # 阻塞主线程，直到observer结束
