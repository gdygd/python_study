
import os
import logging
from threading import Lock
from datetime import datetime

class PyLogger:
    def __init__(self, root_dir, name, level=logging.INFO):        
        self.name = name
        self.root_dir = root_dir
        self.level = level
        self.lock = Lock()
        self.logger = None
        self.path = ""
        self.fp = None
        self.init_logger()

    def get_file_path(self):
        today = datetime.now().strftime("%Y%m%d")
        # todayhm = datetime.now().strftime("%Y%m%d%H%M")
        # print(f"today hhmm {todayhm}")
        dir_path = os.path.join(self.root_dir, today)
        os.makedirs(dir_path, exist_ok=True)
        filename = f"{self.name}-{today}.log"
        return os.path.join(dir_path, filename)

    def init_logger(self):
        self.path = self.get_file_path()
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(self.level)
        # formatter = logging.Formatter(f'%(asctime)s [{self.name}] %(message)s', datefmt='%Y-%m-%d %H:%M:%S.%f')
        formatter = logging.Formatter(fmt='%(asctime)s.%(msecs)03d [%(name)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


        # remove existing handlers
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        file_handler = logging.FileHandler(self.path, mode='a')
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)

    def set_level(self, level):
        self.level = level
        self.logger.setLevel(level)

    def logging(self, level, tag, msg, *args):
        if level < self.level:
            return
        
        self.path = self.get_file_path()
        full_msg = f"{tag:<8} {msg}"
        self.logger.log(level, full_msg, *args)

    def info(self, msg, *args):
        self.logging(logging.INFO, "INFO:", msg, *args)

    def debug(self, msg, *args):
        self.logging(logging.DEBUG, "DEBUG:", msg, *args)

    def warn(self, msg, *args):
        self.logging(logging.WARNING, "WARN:", msg, *args)

    def error(self, msg, *args):
        self.logging(logging.ERROR, "ERROR:", msg, *args)

    def print(self, msg, *args):
        self.logging(level, "PRINT:", msg, *args)

    def always(self, msg, *args):
        self.logging(logging.CRITICAL, "ALWAYS:", msg, *args)

    def debug_dump(self, level, stamp, byte_data):
        if level < self.level:
            return
        hex_lines = []
        for i in range(0, len(byte_data), 20):
            line = "\t" + ' '.join(f'{b:02X}' for b in byte_data[i:i+20])
            hex_lines.append(line)
        dump = f"  {stamp}  [{len(byte_data)}]\n" + '\n'.join(hex_lines)
        self.logging(level, "DUMP:", dump)

logger = PyLogger("./logs", "app", level=logging.DEBUG)
logger.info("Hello world")
logger.debug("Debug message with value: %d", 42)
logger.debug_dump(logging.DEBUG, "Packet", b"Hello, here is a byte dump example")