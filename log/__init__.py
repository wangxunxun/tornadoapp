# -*- coding: utf-8 -*-
import logging
import settings
import tornado.log
import tornado.options
from logging.handlers import RotatingFileHandler
import os

tornado.log.enable_pretty_logging()

tornado.options.options.logging = settings.log['logformat'][settings.log['level']]

logging.root.setLevel(settings.log['level'])
logging.root.propagate = 0
#log write in file
logpath = settings.log['log_path']

fh = RotatingFileHandler(
    logpath,
    maxBytes=settings.log['log_max_bytes'],
    backupCount=settings.log['backup_count']
    )

fh.setLevel(settings.log['level'])

fh.setFormatter(tornado.log.LogFormatter(color=False))

logging.root.addHandler(fh)
logger = logging.root
logger.propagate = 0
