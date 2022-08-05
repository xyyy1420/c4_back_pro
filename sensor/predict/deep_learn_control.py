import subprocess
import logging
from multiprocessing import Process
from watchdog.observers import Observer


from .file_monitor.file_monitor import FileEventHandler
from .file_monitor.std_trash import suppress_stdout_stderr
from .deep_learn.batch_predict import DataAnalysis


class DeepLearnControl():
    def __init__(self, path, id) -> None:
        self.id = id
        self.aim_path = path['log_path']
        self.csv_path = path['csv_path']
        self.file_monitor = FileEventHandler(
            self.aim_path, self.csv_path, self.id)
        self.observer = Observer()
        self.observer.schedule(self.file_monitor, self.aim_path, False)

        logging.info("file montior create")

    def start(self, aim_path):
        self.observer.start()
        self.observer.join()

    def stop(self):
        pass
    # TODO:完成stop的功能

        # TODO:完成deeplearn的实际测试
