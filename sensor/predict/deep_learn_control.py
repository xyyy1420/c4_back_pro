import logging
from watchdog.observers import Observer

from .file_monitor.file_monitor import FileEventHandler


class DeepLearnControl():
    def __init__(self, data) -> None:
        self.id = data['id']
        self.aim_path = data['log_path']
        self.csv_path = data['csv_path']
        self.file_monitor = FileEventHandler(
            self.aim_path, self.csv_path, self.id)
        self.observer = Observer()
        self.observer.schedule(self.file_monitor, self.aim_path, False)

        logging.info("file montior create")

    def start(self):
        self.observer.start()
        logging.info("file monitor start")

    def stop(self):
        self.observer.stop()
        logging.info("file monitor stop")
    # TODO:完成stop的功能

        # TODO:完成deeplearn的实际测试
