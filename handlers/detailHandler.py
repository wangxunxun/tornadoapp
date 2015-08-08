#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import tornado.web

from db import connection
from bson import ObjectId

from baseHandler import BaseHandler
from log import logger


class DetailWeekHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        detailID = self.get_argument('detailID', "")
        status = int(self.get_argument('status', 0))

        detail = connection.WeekDetail.find_one({'_id': ObjectId(detailID)})
        if detail:
            detail.update({"status": status})
            detail.save()
            self.write("Success")
            if status == 1:
                team = connection.Team.find_one({"_id": detail['teamID']})
                _team = {
                    "name": team['name'],
                    "week_detail_summary_time":team['week_detail_summary_time']
                }

                _users = []
                _userid = detail['userID']
                key = detail['_id']
                _user = connection.User.find_one({"_id":_userid})
                if _user:
                    name = _user['username']
                    email = _user['email']
                    _users.append([name, email, str(key)])

                _value = {
                    "team": _team
                }
                _queue = {"type":"notifyWeek", "value":_value, "users":_users}
                from db.cache import taskQueue
                taskQueue.put(_queue)
        else:
            self.write("Error")


class DetailDayHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        detailID = self.get_argument('detailID', "")
        status = int(self.get_argument('status', 0))

        detail = connection.DayDetail.find_one({'_id': ObjectId(detailID)})

        if detail:
            detail.update({"status": status})
            detail.save()
            self.write("Success")

            if status == 1:
                team = connection.Team.find_one({"_id": detail['teamID']})
                _team = {
                    "name": team['name'],
                    "day_detail_summary_time":team['day_detail_summary_time']
                }

                _users = [[detail["username"], detail["useremail"], str(detail['_id'])]]

                _value = {
                    "team": _team
                }
                _queue = {"type":"notifyDay", "value":_value, "users":_users}
                from db.cache import taskQueue
                taskQueue.put(_queue)
        else:
            self.write("Error")
