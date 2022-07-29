import logging

import logging
from file_monitor import MyEventHandler
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time


class Sensor(object):
    def __init__(self) -> None:
        LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
        logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

        self.snort = 'snort'  # TODO:添加一个snort对象

        self.deep_learn = 'deep_learn'

        self.snort_log = 'snort_log'

        self.file_monitor = 'file_monitor'

    def create_file_monitor(self):
        observer = Observer()
        file_handler = MyEventHandler

        aim_path = sys.argv[1] if len(sys.argv) > 1 else '.'

        observer.schedule(file_handler, aim_path, False)

        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer, deamon = True
        observer.join()

        return observer
