#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.web

from log import logger

from db import connection

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_secure_cookie("user", "")
        self.render("login.html", errormessage = "")

    def post(self):
        email = self.get_argument("email")
        password = self.get_argument("password")
        flag, errormessage = connection.User.login_action(email, password)
        if flag:
            self.set_secure_cookie("user", email)
            self.redirect("/")
        else:
            self.render("login.html", errormessage = errormessage)


class LogoutHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_secure_cookie("user", "")
        self.redirect("login")


class RegistHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_secure_cookie("user", "")
        self.render("regist.html", regist=False, errormsg="")

    def post(self):
        email = self.get_argument("email")
        username = self.get_argument("username")
        password = self.get_argument("password")
        password_t = self.get_argument("password_t")

        flag, errormsg = connection.User.regist(email, username, password)

        if flag:
            self.set_secure_cookie("user", email)
            self.render("regist.html", regist=True, username=username, errormsg=errormsg)
        else:
            self.render("regist.html", regist=False, errormsg=errormsg)
