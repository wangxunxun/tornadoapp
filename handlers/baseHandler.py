#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.web

from log import logger
from db import connection


class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        return self.get_secure_cookie("user")

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('404.html')
        elif status_code == 500:
            self.render('500.html')
        else:
            self.write('error:' + str(status_code))


class NoFoundHandler(BaseHandler):
    def get(self):
        title="Not found"
        self.render("404.html", title=title)


class FeedBackHandler(BaseHandler):
    def get(self):
        self.render("feedback.html")

    def post(self):
        email = self.get_argument('email', "")
        username = self.get_argument('username', "")
        message = self.get_argument('message', "")
        connection.FeedBack.create(message, username, email)
        self.write(u"Thanks.")


class ForgotPassword(BaseHandler):
    def get(self):
        title="Forgot password"
        self.render("forgot_password.html", title=title)

    def post(self):
        email = self.get_argument('email', "")
        if email != "":
            self.write("success")
        else:
            self.write("error")

class FeedBackViewHandler(BaseHandler):
    def get(self):
        fbs = connection.FeedBack.get_all()
        self.render("feedbackview.html", fbs=fbs)