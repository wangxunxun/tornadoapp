#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gevent
from gevent import Greenlet

from log import logger

from utils.zmail import send_mail

import traceback

class EmailEmitter(gevent.Greenlet):

    def __init__(self, emailQueue):
        Greenlet.__init__(self)
        self.running = True
        self.emailQueue = emailQueue

    def sendEmail(self, data):
        logger.info("start send mail...")
        if send_mail(data['emails'], data['subject'], data['msg']):
            logger.info("send email success subject:%s, mails:%s.", data["subject"], data['emails'])
        else:
            logger.error("send email success subject:%s, mails:%s, msg:\n%s.", data["subject"], data['emails'], data['msg'])

    def _run(self):
        try:
            while self.running:
                data = self.emailQueue.get()
                self.sendEmail(data)
        except Exception, e:
            s = traceback.format_exc()
            logger.error(s)
