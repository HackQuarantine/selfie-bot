import sys
import logging
import datetime
from . import storage
from . import config

def init():
    global logger
    logging.addLevelName(logging.WARNING, 'WARN')
    logging.addLevelName(logging.CRITICAL, 'FATAL')
    logger = logging.getLogger('hq_selfie')
    logger.setLevel(logging.DEBUG)

    console_format = logging.Formatter('%(asctime)s %(levelname)5s %(module)11s: %(message)s'
                                       , '%H:%M:%S')
    file_format = logging.Formatter('%(asctime)s %(levelname)5s %(module)11s: %(message)s'
                                    , '%d/%m/%y %H:%M:%S')

    storage.make_path(config.creds['logging_dir'])
    file_name = "{}/hq_log_{}.log".format(config.creds['logging_dir'], datetime.datetime.now().strftime('%d-%m-%Y_%H:%M:%S'))
    file_handler = logging.FileHandler(filename=file_name, encoding='utf-8', mode='w')
    file_handler.setFormatter(file_format)
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_format)
    console_handler.setLevel(logging.DEBUG)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
