#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import uuid

import tornado.ioloop
import tornado.httpserver
from tornado.options import define, options
import tornado.httpserver
import tornado.web
from tornado.web import URLSpec as U

from log import logger
import settings as globalsettings

from userHandler import RegistHandler, LoginHandler, LogoutHandler
from teamHandler import TeamIndexHandler, TeamActionHandler, TeamDetailHandler, TeamTaskHandler, TeamMemberHandler, TeamNoteamHandler
from teamHandler import TeamSummaryDayHandler, TeamSummaryWeekHandler
from teamFileHandler import TeamTaskGetExcelHandler, TeamTaskGetPDFHandler
from serviceHandler import WeekServiceHandler, DayServicehandler, TaskServiceHandler, TaskMemberSummaryServiceHandler, TaskTeamSummaryServiceHandler
from detailHandler import DetailWeekHandler, DetailDayHandler
from baseHandler import NoFoundHandler, FeedBackHandler, FeedBackViewHandler

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "../templates")
STATIC_PATH = os.path.join(os.path.dirname(__file__), "../static")

define("port", default=globalsettings.host_port, help="run port", type=int)


class TestHandler(tornado.web.RequestHandler):
    def get(self):
        return self.write("Hello Test Handler")

    def post(self):
        return self.write("Hello Test Handler")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            U(r"/edit/daydetail/(.*)", DayServicehandler),
            U(r"/edit/weekdetail/(.*)", WeekServiceHandler),
            U(r"/edit/task/(.*)", TaskServiceHandler),

            U(r"/show/task/membersummary/(.*)", TaskMemberSummaryServiceHandler),
            U(r"/show/task/teamsummary/(.*)", TaskTeamSummaryServiceHandler),

            U(r"/login", LoginHandler),
            U(r"/regist", RegistHandler),
            U(r"/logout", LogoutHandler),

            U(r"/", TeamIndexHandler),
            U(r"/teamaction/(.*)", TeamActionHandler),
            U(r"/createteam", TeamActionHandler),

            U(r"/team/detail/(.*)", TeamDetailHandler),
            U(r"/team/noteam", TeamNoteamHandler),
            U(r"/team/task/(.*)", TeamTaskHandler),
            U(r"/team/taskgetexcel", TeamTaskGetExcelHandler),
            U(r"/team/taskgetpdf", TeamTaskGetPDFHandler),
            U(r"/team/member/(.*)", TeamMemberHandler), 
            U(r"/team/summary/day/(.*)", TeamSummaryDayHandler), 
            U(r"/team/summary/week/(.*)", TeamSummaryWeekHandler), 

            U(r"/detail/week/", DetailWeekHandler),
            U(r"/detail/day/", DetailDayHandler), 
            U(r"/feedback", FeedBackHandler),
            U(r"/viewfeedback", FeedBackViewHandler),
            U(r"/404", NoFoundHandler),
            U(r".*", NoFoundHandler),

            U(r"/(apple-touch-icon\.png)", tornado.web.StaticFileHandler, dict(path=STATIC_PATH))           
        ]
        settings = dict(
            template_path=TEMPLATE_PATH,
            static_path=STATIC_PATH,
            cookie_secret=str(uuid.uuid1()),
            login_url="/login",
            gzip=True,
            xheaders=True,
            debug=True
        )
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
