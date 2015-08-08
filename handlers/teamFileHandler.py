#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import time
import datetime

import tornado.web


from db import connection
from bson import ObjectId

import xlwt

from baseHandler import BaseHandler
from log import logger

from utils import get_week_str
from utils import get_year_month_day_str_ch
from utils import get_hour_minute_str
from utils import get_hour_minute_second_str
from utils import get_year_week_day_str
from utils import get_year_month_day_str
from utils import get_year_week_str
from utils import get_year_week_day_str_ch
from utils import get_year_week_day_str_ch_from_format_str


class TeamTaskGetExcelHandler(BaseHandler):

    def _getData(self, teamID):
        team = connection.Team.find_one({'_id': ObjectId(teamID)})

        _n = datetime.datetime.now()
        _l = [str(_n.year), str(_n.month), str(_n.day), str(0),str(0) ,str(0)]
        now_day = eval("datetime.datetime(" + ",".join(_l) + ")")

        all_will_list = []
        all_doing_list = []
        all_done_list = []
        all_late_will_doing_list = []
        all_late_list = []

        members_will_list = {}
        members_done_list = {}
        members_doing_list = {}
        members_late_will_doing_list = []
        members_late_list = {}

        teamName = ""

        if team:
            teamName = team['name']
            for m in team['members']:

                key = m['email'] + "#" + m['name']

                members_will_list[key] = []
                members_done_list[key] = []
                members_doing_list[key] = []
                members_late_will_doing_list[key] = []
                members_late_list[key] = []

                # -------------will---------------
                tasks = connection.Task.find({"status": 0,"teamID": ObjectId(teamID), "useremail": m['email']})

                for t in tasks:
                    all_will_list.append(t)
                    members_will_list[key].append(t)

                # -------------doing---------------
                tasks = connection.Task.find({"status": 1,"teamID": ObjectId(teamID), "useremail": m['email']})

                for t in tasks:
                    all_doing_list.append(t)
                    members_doing_list[key].append(t)

                # -------------done---------------
                tasks = connection.Task.find({"status": 2,"teamID": ObjectId(teamID), "useremail": m['email'], "done_time": now_day})

                for t in tasks:
                    all_done_list.append(t)
                    members_done_list[key].append(t)

                # -------------late---------------
                tasks = connection.Task.find({"status": 4,"teamID": ObjectId(teamID), "useremail": m['email'],    "done_time": now_day})

                for t in tasks:
                    all_late_list.append(t)
                    members_late_list[key].append(t)

                # -------------late will or doing---------------
                # db.things.find({"$or":[{"name":"BuleRiver"}, {"name":"BuleRiver2"}]}); // or
                # db.things.find({"createTime":{"$gt":"2014-10-29 0:0:0"}}) // 大于某个时间
                # db.things.find({"createTime":{"$lt":"2014-10-29 0:0:0"}}) // 小于某个时间
                # db.things.find({"$and":[{"createTime":{"$gt":"2014-10-29 0:0:0"}},{"createTime":{"$lt":"2014-10-29 0:0:0"}}]}) // 某个时间段
                tasks = connection.Task.find({"$or":[{"status":0}, {"status":1}], "teamID": ObjectId(teamID), "useremail": m['email'], "dead_line_time":{"$gt": now_day}})
                for t in tasks:
                    all_late_will_doing_list.append(t)
                    members_late_will_doing_list[key].append(t)

        return teamName, all_will_list, all_doing_list, all_done_list, all_late_will_doing_list, all_late_list, members_will_list, members_doing_list, members_done_list, members_late_will_doing_list, members_late_list

    def _getExcel(self, teamName, all_will_list, all_doing_list, all_done_list, all_late_will_doing_list, all_late_list, members_will_list, members_doing_list, members_done_list, members_late_will_doing_list, members_late_list):
        # print teamName
        # print all_will_list
        # print all_doing_list
        # print all_done_list
        # print all_late_list
        # print members_will_list
        # print members_doing_list
        # print members_done_list
        # print members_late_list

        if teamName:
            pass
        else:
            return None

        filename = teamName + "-" + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + ".xlsx"

        w = xlwt.Workbook()
        sheet = w.add_sheet(u'全部')
        # for i in range(len(buf)):
        #   sheet.write(i,0,"你好".decode("utf-8"))
        sheet.write_merge(0, 0, 0, 10,   u'teamName' + u" Team 任务表")
        sheet.write(1, 0, u"日期")
        sheet.write(1, 1, datetime.datetime.now().strftime('%Y/%m/%d'))
        sheet.write(1, 2, u"任务总数")
        sheet.write(1, 3, str(len(all_will_list) + len(all_doing_list) + len(all_done_list) + len(all_late_list)) + u"个")
        sheet.write(1, 4, u"已完成数")
        sheet.write(1, 5, str(len(all_done_list)) + u"个")
        sheet.write(1, 6, u"未完成数")
        sheet.write(1, 7, str(len(all_will_list)) + u"个")
        sheet.write(1, 8, u"延期数")
        sheet.write(1, 9, str(len(all_will_list)) + u"个")

        w.save("upload/" + filename)
        # w.close()

        return filename


    def get(self):

        teamID = "55ab182a7d25d60d99eea15c"

        teamName, all_will_list, all_doing_list, all_done_list, all_late_will_doing_list, all_late_list, members_will_list, members_doing_list, members_done_list, members_late_will_doing_list, members_late_list = self._getData(teamID)

        filename = self._getExcel(teamName, all_will_list, all_doing_list, all_done_list, all_late_will_doing_list, all_late_list, members_will_list, members_doing_list, members_done_list, members_late_will_doing_list, members_late_list)

        if filename:
            pass
        else:
            self.write("Error.")
        

        # filename = "读取的模式需-20150715233445.3456.xls"

        # self.set_header ('Content-Type', 'application/octet-stream')
        # self.set_header ('Content-Disposition', 'attachment; filename='+filename)

        # with open("upload/" + filename, 'rb') as f:
        #     while True:
        #         data = f.read(1024)
        #         if not data:
        #             break
        #         self.write(data)
        # self.finish()

    def post(self):
        return self.write("Hello Test Handler")


class TeamTaskGetPDFHandler(BaseHandler):
    def get(self):
        return self.write("Hello Test Handler")

    def post(self):
        return self.write("Hello Test Handler")
