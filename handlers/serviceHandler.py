#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import datetime

import tornado.web

from db import connection
from bson import ObjectId

from baseHandler import BaseHandler
from log import logger


class DayServicehandler(BaseHandler):

    def get(self, key=None):
        def return_week_str(s):
            if s == "1":
                return "周一"
            elif s == "2":
                return "周二"
            elif s == "3":
                return "周三"
            elif s == "4":
                return "周四"
            elif s == "5":
                return "周五"
            elif s == "6":
                return "周六"
            elif s == "7":
                return "周日"
            else:
                return "见鬼了"

        if key is not None and key != "" and len(key) == 24:
            day_detail = connection.DayDetail.find_by_id_verbose(key)

            if day_detail:
                week  = return_week_str(day_detail["year_week_day"].split("-")[2])
                c_date = day_detail["create_time"]
                date = str(c_date.year) + u"年" + str(c_date.month) + u"月" + str(c_date.day) + u"日"
                day_detail['format_week'] = week
                day_detail['format_date'] = date
                self.render("editor_journal.html", detail=day_detail)
            else:
                return self.redirect("/404")

        else:
            return self.redirect("/404")

    def post(self, key=None):
        if key is not None and key != "" and len(key) == 24:
            pre_text = self.get_argument("pre_text", "").strip()
            next_text = self.get_argument("next_text", "").strip()
            problem_text = self.get_argument("problem_text", "").strip()
            expend_time = self.get_argument("expend_time", "8").strip()
            if problem_text == u"今天遇到的问题做具体描述":
                problem_text = ""

            if pre_text != "" and next_text != "":
                connection.DayDetail.pushDetail(key, pre_text, next_text, problem_text, expend_time)
                self.write("Success")
            else:
                self.write("Error")
        else:
            return self.redirect("/404")


class WeekServiceHandler(BaseHandler):

    def get(self, key=None):
        if key is not None and key != "" and len(key) == 24:
            week_detail = connection.WeekDetail.find_by_id_verbose(key)

            if week_detail:
                year_week  = week_detail["year_week"].split("-")
                date =year_week[0] + u"年 第" + year_week[1] + u"周"
                week_detail['format_date'] = date
                self.render("editor_weekly.html", detail=week_detail)
            else:
                return self.redirect("/404")

        else:
            return self.redirect("/404")

    def post(self, key=None):
        if key is not None and key != "" and len(key) == 24:
            pre_text = self.get_argument("pre_text", "").strip()
            next_text = self.get_argument("next_text", "").strip()
            problem_text = self.get_argument("problem_text", "").strip()
            expend_time = self.get_argument("expend_time", "8").strip()
            if problem_text == u"本周遇到的问题做具体描述":
                problem_text = ""

            if pre_text != "" and next_text != "":
                connection.WeekDetail.pushDetail(key, pre_text, next_text, problem_text, expend_time)
                self.write("Success")
            else:
                self.write("Error")
        else:
            return self.redirect("/404")


class TaskServiceHandler(BaseHandler):
    def get(self, key=None):
        if key is not None and key != "" and len(key) == 24:
            task = connection.Task.find_by_id_verbose(key)
            if task:
                self.render("personal_task.html", task=task)
            else:
                return self.redirect("/404")

        else:
            return self.redirect("/404")

    def post(self, key=None):
        if key is not None and key != "" and len(key) == 24:
            status = int(self.get_argument("status", "0").strip())
            pub = int(self.get_argument("pub", "0").strip())
            pub_text = self.get_argument("pub_text", "").strip()
            update_task_remarks = self.get_argument("update_task_remarks", "").strip()
            update_task_done_100 = int(self.get_argument("update_task_done_100", "0").strip())
            real_time = self.get_argument("real_time", "")

            real_time = ",".join(real_time.split(" "))
            real_time = eval("datetime.datetime(" + real_time + ")")

            message = connection.Task.updateByService(key, status, pub, pub_text, update_task_remarks, update_task_done_100, real_time)
            
            self.write(message)
        else:
            return self.redirect("/404")


class TaskMemberSummaryServiceHandler(BaseHandler):
    def get(self, key=None):
        if key is not None and key != "" and len(key) == 24:
            tms = connection.TaskMemberSummary.find_one({"_id": ObjectId(key)})
            if tms:
                self.write(tms['html'])
            else:
                return self.redirect("/404") 
        else:
           return self.redirect("/404") 


class TaskTeamSummaryServiceHandler(BaseHandler):
    def get(self, key=None):
        if key is not None and key != "" and len(key) == 24:
            tms = connection.TaskTeamSummary.find_one({"_id": ObjectId(key)})
            if tms:
                self.write(tms['html'])
            else:
                return self.redirect("/404") 
        else:
           return self.redirect("/404")
