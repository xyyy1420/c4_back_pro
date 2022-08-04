import subprocess
import logging
from multiprocessing import Process
from watchdog.observers import Observer


from file_monitor.file_monitor import FileEventHandler
from file_monitor.std_trash import suppress_stdout_stderr
from deep_learn.batch_predict import DataAnalysis


class DeepLearnControl():
    def __init__(self, aim_path, id) -> None:
        self.aim_path = aim_path
        self.file_monitor = FileEventHandler(id)
        self.observer = Observer()
        self.observer.schedule(self.file_monitor, self.aim_path, False)

    def create_monitor(self, aim_path):
        pass
