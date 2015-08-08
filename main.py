#!/usr/bin/env python
# -*- coding: utf-8 -*-
import thread
import traceback

import gevent
from gevent import Greenlet

from handlers import main
from log import logger
from app import PollingDB, TemplateBuilder, EmailEmitter


def start_gevent():
    try:
        from db.cache import taskQueue
        from db.cache import emailQueue
        pollingDB = PollingDB(taskQueue)
        templateBuilder = TemplateBuilder(taskQueue, emailQueue)
        emailEmitter = EmailEmitter(emailQueue)
        pollingDB.start()
        templateBuilder.start()
        emailEmitter.start()
        gevent.joinall([pollingDB, templateBuilder, emailEmitter])
    except Exception, e:
        s = traceback.format_exc()
        logger.error(s)


if __name__ == "__main__":
    logger.info("app start")

    thread.start_new_thread(start_gevent, ())

    main()
