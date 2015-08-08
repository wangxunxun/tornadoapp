#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import time

import gevent
from gevent import Greenlet

from db import connection

from log import logger
import traceback

from settings import gevent_sleep

from utils import get_week_str
from utils import get_year_month_day_str_ch
from utils import get_hour_minute_str
from utils import get_hour_minute_second_str
from utils import get_year_week_day_str
from utils import get_year_month_day_str
from utils import get_year_week_str
from utils import get_year_week_day_str_ch
from utils import get_year_week_day_str_ch_from_format_str


class PollingDB(gevent.Greenlet):

    def __init__(self, taskQueue):
        Greenlet.__init__(self)
        self.running = True
        self.taskQueue = taskQueue

    def pollingDB(self):
        teams = connection.Team.find({})

        for team in teams:
            self.pollTeam(team)

    def pollTeam(self, team):
        if team['status'] == 0 and (datetime.datetime.now().isocalendar()[2] not in [6, 7]):
            if team['day_or_week'] == 0:
                self.createDayDetail(team)
                self.notifyDayDetail(team)
                self.summaryDayDetail(team)
            else:
                self.createWeekDetail(team)
                self.notifyWeekDetail(team)
                self.summaryWeekDetail(team)

        self.teamSummaryTask(team)
        self.memberSummaryTask(team)

    def memberSummaryTask(self, team):
        year_week_day_str = get_year_week_day_str()
        now_hour_minute_str = get_hour_minute_str()
        member_task_summary_time = team['member_task_summary_time']
        member_task_summary_flag = team['member_task_summary_flag']

        if year_week_day_str == member_task_summary_flag:
            return
        else:
            if now_hour_minute_str < member_task_summary_time:
                return

        team.update({"member_task_summary_flag": year_week_day_str})
        team['status'] = int(team['status'])
        team.save()

        now_date_str = [get_year_month_day_str_ch(), get_week_str()]

        for m in team['members']:
            username = m['name']
            useremail = m['email']
            tasks_db = connection.Task.find({"teamID":team["_id"], "username":username, "useremail":useremail, "$or":[{"status":0} ,{"status":1}, {"status":3}]})
            tasks = []
            i = 0
            for t in tasks_db:
                task = {}
                task['username'] = username
                task['status'] = int(t['status'])
                task['id'] = str(t['_id'])
                task['rfs'] = t['rfs']
                task['name'] = t['name']
                task['pubusername'] = t['pubusername']
                task['explain'] = t['explain']
                task['remarks'] = t['remarks']
                task['priority'] = t['priority']
                task['done_100'] = t['done_100']
                task['dead_line_time'] = [get_year_month_day_str_ch(t['dead_line_time']), get_hour_minute_str(t['dead_line_time'])]
                tasks.append(task)
                i += 1

            if i == 0:
                continue

            data = {
                "username":username,
                "email":useremail,
                "tasks": tasks,
                "now_date_str": now_date_str,
                "teamname": team['name'],
                "teamID": team['_id'],
                "useremail": useremail
            }
            _queue = {"type":"taskMemberSummary", "data":data}
            self.taskQueue.put(_queue)

    def teamSummaryTask(self, team):
        year_week_day_str = get_year_week_day_str()
        now_hour_minute_str = get_hour_minute_str()
        team_task_summary_time = team['team_task_summary_time']
        team_task_summary_flag = team['team_task_summary_flag']

        if year_week_day_str == team_task_summary_flag:
            return
        else:
            if now_hour_minute_str < team_task_summary_time:
                return

        team.update({"team_task_summary_flag": year_week_day_str})
        team['status'] = int(team['status'])
        team.save()

        emailList = []

        userTaskList = []

        now_date_str = [get_year_month_day_str_ch(), get_week_str()]

        i = 0

        for m in team['members']:
            username = m['name']
            useremail = m['email']
            emailList.append(useremail)
            tasks_db = connection.Task.find({"teamID":team["_id"], "username":username, "useremail":useremail, "$or":[{"status":0} ,{"status":1}, {"status":3}]})
            tasks = []
            for t in tasks_db:
                task = {}
                task['username'] = username
                task['status'] = int(t['status'])
                task['name'] = t['name']
                task['id'] = str(t['_id'])
                task['rfs'] = t['rfs']
                task['pubusername'] = t['pubusername']
                task['explain'] = t['explain']
                task['remarks'] = t['remarks']
                task['priority'] = t['priority']
                task['done_100'] = t['done_100']
                task['dead_line_time'] = [get_year_month_day_str_ch(t['dead_line_time']), get_hour_minute_str(t['dead_line_time'])]
                tasks.append(task)
                i += 1
            userTaskList.append({"username": username, "tasks": tasks})
        if i == 0:
            return

        data = {
            "userTaskList": userTaskList,
            "teamID": team['_id'],
            "teamname": team['name'],
            "now_date_str": now_date_str, 
            "emails":emailList
        }

        _queue = {"type":"taskTeamSummary", "data":data}
        self.taskQueue.put(_queue)

    def _getDayNotify(self, day_detail_summary_time, day_detail_remind_interval):
        def f(i):
            if i < 10:
                return "0" + str(i)
            else:
                return str(i)

        s = day_detail_summary_time.split(":")
        h = int(s[0])
        m = int(s[1])
        i = int(day_detail_remind_interval)
        if i > m:
            mis = m - i + 60
            his = h - 1
        elif i == m:
            mis = 0
            his = h
        else:
            mis = m - i
            his = h

        return f(his) + ":" + f(mis)

    def summaryDayDetail(self, team):
        members = team['members']

        day_detail_summary_time =team["day_detail_summary_time"]
        day_detail_summary_flag =team["day_detail_summary_flag"]

        now_time_str = datetime.datetime.now().strftime('%H:%M')

        if now_time_str >= day_detail_summary_time:
            now_flag = get_year_week_day_str()
            if now_flag > day_detail_summary_flag:
                team.update({"day_detail_summary_flag": now_flag})
                team['status'] = int(team['status'])
                team.save()
                day_summary = team.get_summary_day(now_flag)
                users = team.get_users()
                _queue = {"type": "summaryDay", "users": users, "value": day_summary, "team": team['name'], "now_flag":now_flag}
                self.taskQueue.put(_queue)

    def summaryWeekDetail(self, team):
        members = team['members']

        week_detail_summary_time =team["week_detail_summary_time"]
        week_detail_summary_flag =team["week_detail_summary_flag"]

        now_time_str = str(datetime.datetime.now().isocalendar()[2]) + "-" + datetime.datetime.now().strftime('%H:%M')

        if now_time_str >= week_detail_summary_time:
            now_flag = get_year_week_str()
            if now_flag > week_detail_summary_flag:
                team.update({"week_detail_summary_flag": now_flag})
                team['status'] = int(team['status'])
                team.save()
                week_summary = team.get_summary_week(now_flag)
                users = team.get_users()
                _queue = {"type": "summaryWeek", "users": users, "value": week_summary, "team": team['name'], "now_flag":now_flag}
                self.taskQueue.put(_queue)

    def notifyDayDetail(self, team):
        members = team['members']

        day_detail_summary_time =team["day_detail_summary_time"]
        day_detail_remind_interval =team["day_detail_remind_interval"]
        day_detail_notify_flag = team["day_detail_notify_flag"]

        notify_first_time_str = self._getDayNotify(day_detail_summary_time, day_detail_remind_interval)
        now_time_str = datetime.datetime.now().strftime('%H:%M')

        if now_time_str >= notify_first_time_str:
            _now = time.time()
            if day_detail_notify_flag == 0:
                if _now - day_detail_notify_flag >= day_detail_remind_interval * 60:
                    team.update({"day_detail_notify_flag": int(_now)})
                    team['status'] = int(team['status'])
                    team.save()
                    _team = {
                        "name": team['name'],
                        "day_detail_summary_time":team['day_detail_summary_time']
                    }
                    _users = []
                    for member in members:
                        if member['role'] not in [0, 3]:
                            continue
                        dayDetail = connection.DayDetail.find_for_notify(team['_id'], member)
                        if dayDetail:
                            if dayDetail['status'] in [0, 1]:
                                key = dayDetail['_id']
                                name = dayDetail['username']
                                email = dayDetail['useremail']
                                _users.append([name, email, str(key)])
                        else:
                            logger.info("find error")

                    _value = {
                        "team": _team
                    }
                    _queue = {"type":"notifyDay", "value":_value, "users":_users}
                    self.taskQueue.put(_queue)
            elif day_detail_notify_flag == 1:
                return
            else:
                if _now - day_detail_notify_flag >= day_detail_remind_interval * 60 * 2:
                    team.update({"day_detail_notify_flag": 1})
                    team['status'] = int(team['status'])
                    team.save()
                    _team = {
                        "name": team['name'],
                        "day_detail_summary_time":team['day_detail_summary_time']
                    }
                    _users = []
                    for member in members:
                        if member['role'] not in [0, 3]:
                            continue
                        dayDetail = connection.DayDetail.find_for_notify(team['_id'], member)
                        if dayDetail:
                            if dayDetail['status'] in [0, 1]:
                                key = dayDetail['_id']
                                name = dayDetail['username']
                                email = dayDetail['useremail']
                                _users.append([name, email, str(key)])
                        else:
                            logger.info("find error")

                    _value = {
                        "team": _team
                    }
                    _queue = {"type":"notifyDay", "value":_value, "users":_users}
                    self.taskQueue.put(_queue)
            

    def notifyWeekDetail(self, team):
        members = team['members']

        week_detail_summary_time =team["week_detail_summary_time"]
        week_detail_remind_interval =team["week_detail_remind_interval"]
        week_detail_notify_flag = team["week_detail_notify_flag"]

        notify_first_time_str = week_detail_summary_time.split("-")[0] + "-" + self._getDayNotify(week_detail_summary_time.split("-")[1], week_detail_remind_interval)
        now_time_str = str(datetime.datetime.now().isocalendar()[2]) + "-" + datetime.datetime.now().strftime('%H:%M')

        if now_time_str >= notify_first_time_str:
            _now = time.time()
            if week_detail_notify_flag == 0:
                if _now - week_detail_notify_flag >= week_detail_remind_interval * 60:
                    team.update({"week_detail_notify_flag": int(_now)})
                    team['status'] = int(team['status'])
                    team.save()
                    _team = {
                        "name": team['name'],
                        "week_detail_summary_time":team['week_detail_summary_time']
                    }
                    _users = []
                    for member in members:
                        weekDetail = connection.WeekDetail.find_for_notify(team['_id'], member)
                        if weekDetail:
                            if weekDetail['status'] in [0, 1]:
                                key = weekDetail['_id']
                                name = weekDetail['username']
                                email = weekDetail['useremail']
                                _users.append([name, email, str(key)])
                        else:
                            logger.info("find error")

                    _value = {
                        "team": _team
                    }
                    _queue = {"type":"notifyWeek", "value":_value, "users":_users}
                    self.taskQueue.put(_queue)
            elif week_detail_notify_flag == 1:
                return
            else:
                if _now - week_detail_notify_flag >= week_detail_remind_interval * 60 * 2:
                    team.update({"week_detail_notify_flag": 1})
                    team['status'] = int(team['status'])
                    team.save()
                    _team = {
                        "name": team['name'],
                        "week_detail_summary_time":team['week_detail_summary_time']
                    }
                    _users = []
                    for member in members:
                        weekDetail = connection.WeekDetail.find_for_notify(team['_id'], member)
                        if weekDetail:
                            if weekDetail['status'] in [0, 1]:
                                key = weekDetail['_id']
                                name = weekDetail['username']
                                email = weekDetail['useremail']
                                _users.append([name, email, str(key)])
                        else:
                            logger.info("find error")

                    _value = {
                        "team": _team
                    }
                    _queue = {"type":"notifyWeek", "value":_value, "users":_users}
                    self.taskQueue.put(_queue)

    def createWeekDetail(self, team):
        week_detail_create_time = team["week_detail_create_time"]
        week_detail_create_flag = team["week_detail_create_flag"]

        now_week_flag = str(datetime.datetime.now().isocalendar()[2]) + "-" + datetime.datetime.now().strftime('%H:%M')

        if now_week_flag > week_detail_create_time:
            now_flag = get_year_week_str()
            if now_flag > week_detail_create_flag:
                users = connection.WeekDetail.createByUserList(team['_id'], team['members'], team['name'], team['week_detail_summary_time'])
                team.update({"week_detail_create_flag": now_flag})
                team.update({"week_detail_notify_flag": 0})
                team['status'] = int(team['status'])
                team.save()
                _team = {
                    "name": team['name'],
                    "week_detail_summary_time":team['week_detail_summary_time']
                }
                _value = {
                    "team": _team
                }
                _queue = {"type":"createWeek", "value":_value, "users": users}

                self.taskQueue.put(_queue)

    def createDayDetail(self, team):
        if datetime.datetime.now().isocalendar()[2] in [6, 7]:
            pass
        else:
            day_detail_create_time = team["day_detail_create_time"]
            day_detail_create_flag = team["day_detail_create_flag"]

            if datetime.datetime.now().strftime('%H:%M') > day_detail_create_time:
                now_flag = get_year_week_day_str()
                if now_flag > day_detail_create_flag:
                    users = connection.DayDetail.createByUserList(team['_id'], team['members'], team['name'], team['day_detail_summary_time'])
                    team.update({"day_detail_create_flag": now_flag})
                    team.update({"day_detail_notify_flag": 0})
                    team['status'] = int(team['status'])
                    team.save()

                    _team = {
                        "name": team['name'],
                        "day_detail_summary_time":team['day_detail_summary_time']
                    }
                    _value = {
                        "team": _team
                    }
                    _queue = {"type":"createDay", "users":users, "value":_value}

                    self.taskQueue.put(_queue)

    def _run(self):
        try:
            while self.running:
                gevent.sleep(gevent_sleep)
                self.pollingDB()
        except Exception, e:
            s = traceback.format_exc()
            logger.error(s)
