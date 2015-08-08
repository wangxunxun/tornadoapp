#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gevent
from gevent import Greenlet
from tornado import template

from db import connection

from log import logger
import traceback

from settings import host_url

from utils import get_week_str
from utils import get_year_month_day_str_ch
from utils import get_hour_minute_str
from utils import get_hour_minute_second_str
from utils import get_year_week_day_str
from utils import get_year_month_day_str
from utils import get_year_week_str
from utils import get_year_week_day_str_ch
from utils import get_year_week_day_str_ch_from_format_str

import sys
reload(sys)
sys.setdefaultencoding('utf8')

def get_week_str_by_num(s):
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


class TemplateBuilder(gevent.Greenlet):

    def __init__(self, taskQueue, emailQueue):
        Greenlet.__init__(self)
        self.running = True
        self.taskQueue = taskQueue
        self.emailQueue = emailQueue
        self.loader = template.Loader("templates/mail")

    def generate(self, filename, data=None):
        return self.loader.load(filename).generate(data=data)

    def createDayAction(self, data):
        teamname = data['value']['team']['name']
        team_day_detail_summary_time = data['value']['team']['day_detail_summary_time']
        subject = teamname +  "小组-日报创建提醒 " + get_year_month_day_str(s="/")

        users = data['users']

        for u in users:
            username = u[0]
            emaillist = [u[1]]
            lnk =  host_url +  "/edit/daydetail/" +  u[2]
            content = self.generate("day_create.html", [teamname, team_day_detail_summary_time, username, lnk])
            self.emailQueue.put({"emails":emaillist, "msg":content, "subject":subject})

    def notifyDayAction(self, data):
        teamname = data['value']['team']['name']
        team_day_detail_summary_time = data['value']['team']['day_detail_summary_time']
        subject = teamname +  "小组-日报提交提醒 " + get_year_month_day_str(s="/")

        users = data['users']

        for u in users:
            username = u[0]
            emaillist = [u[1]]
            lnk =  host_url +  "/edit/daydetail/" +  u[2]
            content = self.generate("day_notify.html", [teamname, team_day_detail_summary_time, username, lnk])
            self.emailQueue.put({"emails":emaillist, "msg":content, "subject":subject})

    def createWeekAction(self, data):
        teamname = data['value']['team']['name']
        team_week_detail_summary_time = data['value']['team']['week_detail_summary_time']
        team_week_detail_summary_time = [get_week_str_by_num(team_week_detail_summary_time.split('-')[0]), team_week_detail_summary_time.split('-')[1]]
        subject = teamname +  "小组-周报创建提醒 " + get_year_month_day_str(s="/")

        users = data['users']

        for u in users:
            username = u[0]
            emaillist = [u[1]]
            lnk =  host_url +  "/edit/weekdetail/" +  u[2]
            content = self.generate("week_create.html", [teamname, team_week_detail_summary_time, username, lnk])
            self.emailQueue.put({"emails":emaillist, "msg":content, "subject":subject})

    def notifyWeekAction(self, data):
        teamname = data['value']['team']['name']
        team_week_detail_summary_time = data['value']['team']['week_detail_summary_time']
        team_week_detail_summary_time = [get_week_str_by_num(team_week_detail_summary_time.split('-')[0]), team_week_detail_summary_time.split('-')[1]]
        subject = teamname +  "小组-周报提交提醒 " + get_year_month_day_str(s="/")

        users = data['users']

        for u in users:
            username = u[0]
            emaillist = [u[1]]
            lnk =  host_url +  "/edit/weekdetail/" +  u[2]
            content = self.generate("week_notify.html", [teamname, team_week_detail_summary_time, username, lnk])
            self.emailQueue.put({"emails":emaillist, "msg":content, "subject":subject})

    def summaryDayAction(self, data):
        teamname = data['team']
        day_flag = [data['now_flag'].split('-')[0], data['now_flag'].split('-')[1], get_week_str_by_num(data['now_flag'].split('-')[2])]

        tem_value = {
            "teamname":teamname,
            "day_flag": day_flag,
            "summary":data['value']
        }
        subject = teamname +  "小组-日报汇总 " + get_year_month_day_str(s="/")
        content = self.generate("day_summary.html", tem_value)
        emaillist = [u[1] for u in data['users']]
        _q = {"emails":emaillist, "msg":content, "subject":subject}
        self.emailQueue.put(_q)

    def summaryWeekAction(self, data):
        teamname = data['team']
        week_flag = data['now_flag'].split("-")
        tem_value = {
            "teamname":teamname,
            "week_flag": week_flag,
            "summary":data['value']
        }
        subject = teamname +  "小组-周报汇总 " + get_year_month_day_str(s="/")
        content = self.generate("week_summary.html", tem_value)
        emaillist = [u[1] for u in data['users']]
        _q = {"emails":emaillist, "msg":content, "subject":subject}
        self.emailQueue.put(_q)
    
    def createTaskAction(self, data):
        subject = data['teamname'] + "小组-新建任务:" + data['name'] + " " + get_year_month_day_str(s="/")
        content = self.generate("task_new.html", data)
        _q = {"emails":[data['email']], "msg":content, "subject":subject}
        self.emailQueue.put(_q)

    def pubTaskAction(self, data): 
        subject = data['teamname'] + "小组-" + data['pubusername'] + "转派任务: " + data['name'] + " " + get_year_month_day_str(s="/")
        content = self.generate("task_pub.html", data)
        _q = {"emails":[data['email']], "msg":content, "subject":subject}
        self.emailQueue.put(_q)

    def taskMemberSummaryAction(self, data):
        subject = data['teamname'] + "小组-个人任务汇总通知" + get_year_month_day_str(s="/")
        html = self.generate("task_summary_member.html", data)
        _db_dict = {
            "teamID": data['teamID'],
            "teamname": data['teamname'],
            "username": data['username'],
            "useremail": data['useremail'],
            "html": html
        }
        idstr = connection.TaskMemberSummary.newHtml(_db_dict)

        lnk =  host_url +  "/show/task/membersummary/" +  idstr

        data['url'] = lnk

        content = self.generate("task_summary_member_email.html", data)

        _q = {"emails":[data['email']], "msg":content, "subject":subject}
        self.emailQueue.put(_q)

    def taskTeamSummaryAction(self, data):
        subject = data['teamname'] + "小组-小组任务汇总通知" + get_year_month_day_str(s="/")
        html = self.generate("task_summary_team.html", data)

        _db_dict = {
            "teamID": data['teamID'],
            "teamname": data['teamname'],
            "html": html
        }
        idstr = connection.TaskTeamSummary.newHtml(_db_dict)

        lnk =  host_url +  "/show/task/teamsummary/" +  idstr

        data['url'] = lnk

        content = self.generate("task_summary_team_email.html", data)

        _q = {"emails":data['emails'], "msg":content, "subject":subject}
        self.emailQueue.put(_q)


    def buildHtml(self, data):
        logger.info("+" * 10)
        logger.info(data)
        logger.info("-" * 10)

        emails = []
        msg = ""
        subject = ""

        _type = data['type']

        if _type == "createDay":
            self.createDayAction(data)
        elif _type == "createWeek":
            self.createWeekAction(data)
        elif _type == "notifyDay":
            self.notifyDayAction(data)
        elif _type == "notifyWeek":
            self.notifyWeekAction(data)
        elif _type == "summaryDay":
            self.summaryDayAction(data)
        elif _type == "summaryWeek":
            self.summaryWeekAction(data)
        elif _type == "createTask":
            self.createTaskAction(data['data'])
        elif _type == "pubTask":
            self.pubTaskAction(data['data'])
        elif _type == "taskMemberSummary":
            self.taskMemberSummaryAction(data['data'])
        elif _type == "taskTeamSummary":
            self.taskTeamSummaryAction(data['data'])
        else:
            logger.warning("template error")

    def _run(self):
        try:
           while self.running:
                data = self.taskQueue.get()
                self.buildHtml(data)
        except Exception, e:
            s = traceback.format_exc()
            logger.error(s)
        
        