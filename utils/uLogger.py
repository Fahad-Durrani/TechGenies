import logging
import os
from logging.handlers import RotatingFileHandler

app_root = os.getcwd()
abs_root_path = os.path.abspath(app_root)
print(abs_root_path)
log_dir = os.path.join(abs_root_path, "log_dir")
if not os.path.exists(log_dir):
    os.mkdir(log_dir)
log_file = os.path.join(log_dir, "log_file.log")
print(log_file)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

rotating_handler = RotatingFileHandler(
    log_file, maxBytes=5*1024*1024, backupCount=2 
)
rotating_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
rotating_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO) 
console_handler.setFormatter(formatter)
logger.addHandler(rotating_handler)
logger.addHandler(console_handler)




