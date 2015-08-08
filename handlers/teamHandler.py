#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import time
import datetime

import tornado.web

from log import logger

from db import connection
from bson import ObjectId

from baseHandler import BaseHandler

from utils import get_week_str
from utils import get_year_month_day_str_ch
from utils import get_hour_minute_str
from utils import get_hour_minute_second_str
from utils import get_year_week_day_str
from utils import get_year_month_day_str
from utils import get_year_week_str
from utils import get_year_week_day_str_ch
from utils import get_year_week_day_str_ch_from_format_str


class TeamIndexHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        email = self.get_secure_cookie("user")
        user = connection.User.get_user_by_email(email)
        if user:
            username = user['name']
            email = user['email']
        else:
            username = email

        team = connection.Team.find_one({'ownerID': user['_id']})
        if team:
            teamid = str(team['_id'])
            self.redirect('/team/detail/' + teamid)
        else:
            self.redirect('/team/noteam')


class TeamActionHandler(BaseHandler):

    @tornado.web.authenticated
    def put(self, teamID=None):
        teamID = teamID
        day_detail_create_time =  self.get_argument("day_detail_create_time", "")
        day_detail_summary_time = self.get_argument("day_detail_summary_time", "")

        member_task_summary_time = self.get_argument("member_task_summary_time", "")
        team_task_summary_time = self.get_argument("team_task_summary_time", "")

        week_detail_create_time = self.get_argument("week_detail_create_time", "")
        week_detail_summary_time = self.get_argument("week_detail_summary_time", "")

        day_detail_remind_interval = self.get_argument("day_detail_remind_interval", "")
        week_detail_remind_interval = self.get_argument("week_detail_remind_interval", "")

        day_or_week = int(self.get_argument("day_or_week", "0"))

        members = self.get_argument("members", "")

        updateData = {}
        updateData['day_or_week'] = day_or_week
        if day_detail_create_time:
            updateData['day_detail_create_time'] = day_detail_create_time
        if day_detail_summary_time:
            updateData['day_detail_summary_time'] = day_detail_summary_time
        if member_task_summary_time:
            updateData['member_task_summary_time'] = member_task_summary_time
        if team_task_summary_time:
            updateData['team_task_summary_time'] = team_task_summary_time
        if week_detail_create_time:
            updateData['week_detail_create_time'] = week_detail_create_time
        if week_detail_summary_time:
            updateData['week_detail_summary_time'] = week_detail_summary_time
        if day_detail_remind_interval:
            updateData['day_detail_remind_interval'] = int(day_detail_remind_interval)
        if week_detail_remind_interval:
            updateData['week_detail_remind_interval'] = int(week_detail_remind_interval)

        team = connection.Team.find_one({"_id": ObjectId(teamID)})
        if team:
            team.update(updateData)
            team.save()
        self.write("Success")

    @tornado.web.authenticated
    def post(self):
        name = self.get_argument("name")
        day_detail_create_time =  self.get_argument("day_detail_create_time")
        day_detail_summary_time = self.get_argument("day_detail_summary_time")

        member_task_summary_time = self.get_argument("member_task_summary_time")
        team_task_summary_time = self.get_argument("team_task_summary_time")

        week_detail_create_time = self.get_argument("week_detail_create_time")
        week_detail_summary_time = self.get_argument("week_detail_summary_time")

        day_detail_remind_interval = self.get_argument("day_detail_remind_interval")
        week_detail_remind_interval = self.get_argument("week_detail_remind_interval")

        day_or_week = int(self.get_argument("day_or_week", "0"))

        members = self.get_argument("members", "{}")

        date = {
            "name": name,
            "day_detail_create_time": day_detail_create_time,
            "day_detail_summary_time": day_detail_summary_time,

            "member_task_summary_time": member_task_summary_time,
            "team_task_summary_time": team_task_summary_time,

            "week_detail_create_time": week_detail_create_time,
            "week_detail_summary_time": week_detail_summary_time,

            "day_detail_remind_interval": int(day_detail_remind_interval),
            "week_detail_remind_interval": int(week_detail_remind_interval),
            "day_or_week": day_or_week,
        }

        members = json.loads(members)
        email = self.get_secure_cookie("user")
        flag = True

        user = connection.User.get_user_by_email(email)

        for m in members:
            if email == m["email"]:
                flag = False
                m["role"] = int(m["role"]) + 3
            else:
                m["role"] = int(m["role"])
        if flag:
            members.append({"email": email, "name":user['name'], "role":2})

        date['ownerID'] = user['_id']
        date['ownername'] = user['name']
        date['owneremail'] = user['email']
        date['members'] = members

        flag, msg = connection.Team.createTeam(date)
        if flag:
            self.write("Success")
        else:
            self.write(msg)

    @tornado.web.authenticated
    def delete(self, teamID=""):
        teamID = self.get_argument("teamID", teamID)
        if teamID:
            team = connection.Team.find_one({"_id": ObjectId(teamID)})
            team.delete()
            self.write("Success")
        else:
            self.write("Error")

    @tornado.web.authenticated
    def patch(self, teamID=""):
        teamID = self.get_argument("teamID", teamID)
        status = int(self.get_argument("status", "0"))
        teamname = self.get_argument("name", "teamname")
        if len(teamID) == 24:
            team = connection.Team.find_one({"_id": ObjectId(teamID)})
            if team:
                if status == 2:
                    team.deep_delete()
                    self.write("Success")
                elif status == 0:
                    team['status'] = status
                    team['name'] = teamname
                    team.save()
                    self.write("Success")
                elif status == 1:
                    team['status'] = status
                    team['name'] = teamname
                    team.save()
                    self.write("Success")
                else:
                    self.write("Error")
            else:
                self.write("Error")
        else:
            self.write("Error")
        


class TeamNoteamHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        email = self.get_secure_cookie("user")
        user = connection.User.get_user_by_email(email)
        if user:
            username = user['name']
            email = user['email']
        else:
            username = email

        self.render("team_noteam.html", username=username)

    @tornado.web.authenticated
    def post(self, teamID):
        pass

    @tornado.web.authenticated
    def put(self, teamID):
        pass

    @tornado.web.authenticated
    def delete(self, teamID):
        pass


class TeamSummaryDayHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, teamID):

        def get_year_week_day_list():
            _ = []
            now_flag_year_week = "-".join([str(i) for i in datetime.datetime.now().isocalendar()[:2]])
            now_day = datetime.datetime.now().isocalendar()[2]
            for d in xrange(1, now_day+1):
                if d in [1,2,3,4,5]:
                    _.append(now_flag_year_week + "-" + str(d))

            return _

        def get_week_str(i):
            s = i.split("-")[2]
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


        email = self.get_secure_cookie("user")
        user = connection.User.get_user_by_email(email)
        if user:
            username = user['name']
            email = user['email']
        else:
            username = email
        userID = user['_id']
        teamID = ObjectId(teamID)

        _d = datetime.datetime.now()
        date_str = str(_d.year) + u"年" + str(_d.month) + u"月" + str(_d.day) + u"日"

        team = connection.Team.find_one({"_id": teamID})
        members = team['members']

        details = []

        for m in members:
            user_daydetails = []
            _username = m['name']
            for ywd in get_year_week_day_list():
                detail = connection.DayDetail.find_one({"teamID": teamID, "useremail": m['email'], "year_week_day": ywd})
                if detail:
                    user_daydetails.append([detail, get_week_str(ywd)])

            if len(user_daydetails) > 0:
                details.append([_username, user_daydetails])


        self.render("summary_report_day.html", owner=username, date=date_str, details=details)


class TeamSummaryWeekHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, teamID):

        email = self.get_secure_cookie("user")
        user = connection.User.get_user_by_email(email)
        if user:
            username = user['name']
            email = user['email']
        else:
            username = email
        userID = user['_id']
        teamID = ObjectId(teamID)

        _d = datetime.datetime.now()
        date_str = str(_d.year) + u"年" + str(_d.month) + u"月" + str(_d.day) + u"日"

        team = connection.Team.find_one({"_id": teamID})
        members = team['members']

        details = []

        year_week_str = "-".join([str(i) for i in datetime.datetime.now().isocalendar()[:2]])

        for m in members:
            _username = m['name']
            detail = connection.WeekDetail.find_one({"teamID":teamID, "useremail":m['email'], "year_week":year_week_str})
            if detail:
                details.append([_username, detail])

        self.render("summary_report_week.html", owner=username, date=date_str, details=details)


class TeamTaskHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, teamID=None):
        if len(teamID) == 24:
            thisteam = connection.Team.find_one({'_id': ObjectId(teamID)})
            if not thisteam:
                self.redirect("/404")
        else:
            self.redirect("/404")
        email = self.get_secure_cookie("user")
        user = connection.User.get_user_by_email(email)
        if user:
            username = user['name']
            email = user['email']
        else:
            username = email

        teams_dbobj = connection.Team.find({'ownerID': user['_id']})
        teams = []
        index_num = 0;
        i = 0
        for t in teams_dbobj:
            team = {}
            _teamID = str(t['_id'])
            team['teamID'] = _teamID
            team['name'] = t['name']
            team['status'] = t['status']
            team['day_or_week'] = t['day_or_week']
            teams.append(team)
            if teamID == _teamID:
                index_num = i
            i += 1
        members = thisteam['members']

        tasks_0 = self._get_tasks_by_status(thisteam, 0)
        tasks_1 = self._get_tasks_by_status(thisteam, 1)
        tasks_2 = self._get_tasks_by_status(thisteam, 2)
        tasks_3 = self._get_tasks_by_status(thisteam, 3)

        main = [tasks_0, tasks_1, tasks_2, tasks_3]

        import json
        mains = json.dumps(main, indent=4)

        self.render("team_task.html", teams=teams, thisteam=thisteam, type="task", username=username, main=main, mains=mains, index_num=index_num, members=members)

    def _get_tasks_by_status(self, thisteam, status):
        members = thisteam['members']

        u_t_l = []

        for m in members:
            u_t = {}
            username = m['name']
            email = m['email']
            tasks_db = connection.Task.find({"teamID":thisteam['_id'], "status":status, "useremail": email})
            tasks = []
            for t in tasks_db:
                task = {}
                task['username'] = username
                task['useremail'] = t['useremail']
                task['status'] = t['status']
                task['name'] = t['name']
                task['pubusername'] = t["pubusername"]
                task['explain'] = t['explain']
                task['remarks'] = t['remarks']
                task['priority'] = t['priority']
                task['done_100'] = t['done_100']
                task['weight'] = t['weight']
                task['score'] = t['score']
                task['dead_line_time'] = [get_year_month_day_str_ch(t['dead_line_time']), get_hour_minute_str(t['dead_line_time'])]
                task['start_time'] = [get_year_month_day_str_ch(t['start_time']), get_hour_minute_str(t['start_time'])]
                task['done_time'] = [get_year_month_day_str_ch(t['done_time']), get_hour_minute_str(t['done_time'])]
                task['id'] = str(t['_id'])
                tasks.append(task)
            if status == 2:
                tasks_db = connection.Task.find({"teamID":thisteam['_id'], "status":4, "useremail": email})
                for t in tasks_db:
                    task = {}
                    task['username'] = username
                    task['useremail'] = t['useremail']
                    task['status'] = t['status']
                    task['name'] = t['name']
                    task['pubusername'] = t["pubusername"]
                    task['explain'] = t['explain']
                    task['remarks'] = t['remarks']
                    task['priority'] = t['priority']
                    task['done_100'] = t['done_100']
                    task['weight'] = t['weight']
                    task['score'] = t['score']
                    task['dead_line_time'] = [get_year_month_day_str_ch(t['dead_line_time']), get_hour_minute_str(t['dead_line_time'])]
                    task['start_time'] = [get_year_month_day_str_ch(t['start_time']), get_hour_minute_str(t['start_time'])]
                    task['done_time'] = [get_year_month_day_str_ch(t['done_time']), get_hour_minute_str(t['done_time'])]
                    task['id'] = str(t['_id'])
                    tasks.append(task)

            if len(tasks) == 0:
                continue

            u_t['username'] = username
            u_t['email'] = email
            u_t['id'] = email
            u_t['tasks'] = tasks

            u_t_l.append(u_t)

        return u_t_l


    @tornado.web.authenticated
    def post(self, teamID):
        name = self.get_argument("name", "")
        explain = self.get_argument("explain", "")
        priority = int(self.get_argument("priority", "0"))
        dead_line_time = self.get_argument("dead_line_time", "")
        usermail = self.get_argument("usermail", "")
        weight = self.get_argument("weight", "1")

        print weight

        dead_line_time = ",".join(dead_line_time.split(" "))

        dead_line_time = eval("datetime.datetime(" + dead_line_time + ")")
        now = datetime.datetime.now()

        if (now - dead_line_time).total_seconds() > 0:
            self.write(u"不要这么难为人嘛，人生没有后悔药，所以你也不能安排人家在已经消逝的时间里面完成未来的事情。")
        else:
            team = connection.Team.find_one({"_id": ObjectId(teamID)})
            if team:
                members = team['members']
                for m in members:
                    if m['role'] > 1:
                        createuseremail = m['email']
                        createusername = m['name']

                        pubuseremail = m['email']
                        pubusername = m['name']

                    if m['email'] == usermail:
                        useremail = m['email']
                        username = m['name']
                    teamname = team['name']
                connection.Task.newTask(ObjectId(teamID), teamname, username, useremail, createusername, createuseremail, pubusername, pubuseremail, name, explain, priority, dead_line_time, weight)
                self.write("Success")
            else:
                self.write("Team Error.")

    @tornado.web.authenticated
    def put(self, teamID):
        member_task_summary_time = self.get_argument("member_task_summary_time", "")
        team_task_summary_time = self.get_argument("team_task_summary_time", "")
        team = connection.Team.find_one({'_id': ObjectId(teamID)})

        if team:
            team["member_task_summary_time"] = member_task_summary_time
            team["team_task_summary_time"] = team_task_summary_time
            team.save()
            self.write("Success")
        else:
            self.write("Error")

    @tornado.web.authenticated
    def patch(self, teamID):
        def _priority2str(priority):
            if priority == 0:
                return u"紧急"
            elif priority == 1:
                return u"高"
            elif priority == 2:
                return u"中"
            elif priority == 3:
                return u"低"
            else:
                return u"随你便"
    
        def _datetime2str(d):
            return str(d.year) + "年" + str(d.month) + "月" + str(d.day) + "日 " + str(d.hour) + ":" + str(d.minute)

        taskid = self.get_argument("taskid", "")
        name = self.get_argument("name", "")
        explain = self.get_argument("explain", "")
        priority = int(self.get_argument("priority", "0"))
        dead_line_time = self.get_argument("dead_line_time", "")
        useremail = self.get_argument("useremail", "")
        username = self.get_argument("username", "")
        remarks = self.get_argument("remarks", "")
        status = int(self.get_argument("status", "0"))
        done_100 = int(self.get_argument("done_100", "0"))
        weight = int(self.get_argument("weight", "1"))
        score = float(self.get_argument("score", "1.0"))
        real_time = self.get_argument("real_time", "")

        task = connection.Task.find_one({"_id": ObjectId(taskid)})
        if task:
            dead_line_time = ",".join(dead_line_time.split(" "))
            dead_line_time = eval("datetime.datetime(" + dead_line_time + ")")

            real_time = ",".join(real_time.split(" "))
            real_time = eval("datetime.datetime(" + real_time + ")")

            now = datetime.datetime.now()

            if (now - dead_line_time).total_seconds() > 0:
                self.write(u"不要这么难为人嘛，人生没有后悔药，所以你也不能安排人家在已经消逝的时间里面完成未来的事情。")
            else:
                if status == 2 and real_time > dead_line_time:
                    status = 4
                task['status'] = status
                task['name'] = name
                task['priority'] = priority
                task['explain'] = explain
                task['done_100'] = done_100
                task['remarks'] = remarks
                task['username'] = username
                task['dead_line_time'] = dead_line_time
                task['update_time'] = datetime.datetime.now()
                task['weight'] = int(weight)
                task['score'] = float(score)
                if status == 1:
                    task['start_time'] = real_time
                elif status in [2, 4]:
                    task['done_time'] = real_time
                else:
                    pass

                if task['useremail'] == useremail:
                    task['useremail'] = useremail
                else:
                    thisuseremail = self.get_secure_cookie("user")
                    thisuser = connection.User.find_one({"email":thisuseremail})
                    thisusername = thisuser['name']
                    task['pubusername'] = thisusername
                    task['pubuseremail'] = thisuseremail

                    pubTaskEmail = {}
    
                    pubTaskEmail["teamname"] = task["teamname"]
                    pubTaskEmail["username"] = username
                    pubTaskEmail['pubusername'] = thisusername
                    pubTaskEmail["name"] = task['name']
                    pubTaskEmail["dead_line_time"] = _datetime2str(task["dead_line_time"])
                    pubTaskEmail["priority"] = _priority2str(task["priority"])
                    pubTaskEmail["explain"] = task["explain"]
                    pubTaskEmail["now"] = _datetime2str(datetime.datetime.now())
                    pubTaskEmail['email'] = useremail
                    
                    from settings import host_url
                    pubTaskEmail['url'] = host_url + "/edit/task/" + str(task['_id'])

                    from db.cache import taskQueue
                    _queue = {"type": "pubTask", "data":pubTaskEmail}
                    taskQueue.put(_queue)

                task.save()
                self.write("Success")
        else:
            self.write("No Task")

    @tornado.web.authenticated
    def delete(self, teamID):
        taskid = self.get_argument("taskid", "")
        task = connection.Task.find_one({"_id": ObjectId(taskid)})
        if task:
            task.delete()
            self.write("Success")
        else:
            self.write("No Task")


class TeamDetailHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, teamID=None):
        if len(teamID) == 24:
            thisteam = connection.Team.find_one({'_id': ObjectId(teamID)})
            if not thisteam:
                self.redirect("/404")
        else:
            self.redirect("/404")
        email = self.get_secure_cookie("user")
        user = connection.User.get_user_by_email(email)
        if user:
            username = user['name']
            email = user['email']
        else:
            username = email

        teams_dbobj = connection.Team.find({'ownerID': user['_id']})
        teams = []
        index_num = 0;
        i = 0
        for t in teams_dbobj:
            team = {}
            _teamID = str(t['_id'])
            team['teamID'] = _teamID
            team['name'] = t['name']
            team['status'] = t['status']
            team['day_or_week'] = t['day_or_week']
            teams.append(team)
            if teamID == _teamID:
                index_num = i
            i += 1

        week_now_create = str(datetime.datetime.now().isocalendar()[2]) + "-" + datetime.datetime.now().strftime('%H:%M')
        day_now_create = datetime.datetime.now().strftime('%H:%M')

        day_now_flag = "-".join([str(i) for i in datetime.datetime.now().isocalendar()])
        week_now_flag = "-".join([str(i) for i in datetime.datetime.now().isocalendar()[:2]])
        day_detail_summary_flag = thisteam['day_detail_summary_flag']
        week_detail_summary_flag = thisteam['week_detail_summary_flag']

        day_detail_create_time = thisteam['day_detail_create_time']
        week_detail_create_time = thisteam['week_detail_create_time']

        today_create = day_now_flag > day_detail_create_time
        week_create = week_now_flag > week_detail_create_time

        today_summary = day_now_flag == day_detail_summary_flag
        this_week_summary = week_now_flag == week_detail_summary_flag

        day_int = datetime.datetime.now().isocalendar()[2]

        week_historys = {}
        day_historys = []

        if thisteam['day_or_week'] == 0:
            for d in xrange(day_int):
                year_week_day = "-".join([str(i) for i in (datetime.datetime.now().isocalendar()[:2])]) + "-" + str(d+1)
                details_db = connection.DayDetail.find({"teamID": ObjectId(teamID), "year_week_day":year_week_day})
                if details_db:
                    details = []
                    for d in details_db:
                        detail = {}
                        detail['submit_list'] = d['submit_list']
                        detail['status'] = d['status']
                        detail['id'] = d['_id']
                        detail['username'] = d['username']
                        details.append(detail)
                    if details:
                        day_historys.append({"date": year_week_day, "details": details})
            day_historys.reverse()
        else:
            year_week = "-".join([str(i) for i in (datetime.datetime.now().isocalendar()[:2])])

            details_db = connection.WeekDetail.find({"teamID": ObjectId(teamID), "year_week":year_week})
            if details_db:
                details = []
                for d in details_db:
                    detail = {}
                    detail['submit_list'] = d['submit_list']
                    detail['status'] = d['status']
                    detail['id'] = d['_id']
                    detail['username'] = d['username']
                    details.append(detail)

            week_historys = {"date": year_week, 'details':details}

        values = {
            "today_create":today_create,
            "week_create":week_create,
            "today_summary":today_summary,
            "this_week_summary":this_week_summary,
            "day_historys":day_historys,
            "week_historys":week_historys
        }
        self.render("team_detail.html", teams=teams, thisteam=thisteam, type="detail", username=username, main=values, index_num=index_num)

    @tornado.web.authenticated
    def post(self):
        pass

    @tornado.web.authenticated
    def put(self):
        pass


class TeamMemberHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, teamID=None):
        if len(teamID) == 24:
            thisteam = connection.Team.find_one({'_id': ObjectId(teamID)})
            if not thisteam:
                self.redirect("/404")
        else:
            self.redirect("/404")
        email = self.get_secure_cookie("user")
        user = connection.User.get_user_by_email(email)
        if user:
            username = user['name']
            email = user['email']
        else:
            username = email

        teams_dbobj = connection.Team.find({'ownerID': user['_id']})
        teams = []
        index_num = 0;
        i = 0
        for t in teams_dbobj:
            team = {}
            _teamID = str(t['_id'])
            team['teamID'] = _teamID
            team['name'] = t['name']
            team['status'] = t['status']
            team['day_or_week'] = t['day_or_week']
            teams.append(team)
            if teamID == _teamID:
                index_num = i
            i += 1

        self.render("team_member.html", teams=teams, thisteam=thisteam, type="member", username=username, index_num=index_num)

    @tornado.web.authenticated
    def post(self):
        pass

    @tornado.web.authenticated
    def put(self, teamID):
        members = self.get_argument("members", "[]")
        team = connection.Team.find_one({'_id': ObjectId(teamID)})

        if members and team:
            members = json.loads(members)
            _ul = []
            _el = []
            _rl = []

            for m in team['members']:
                _ul.append(m["name"])
                _el.append(m['email'])
                _rl.append(m['role'])

            for m in members:
                m['role'] = int(m['role'])
                if m['email'] in _el:
                    i = _el.index(m['email'])
                    team['members'][i]['name'] = m['name']
                    tr = team['members'][i]['role']
                    if tr > 1:
                        if int(m['role']) == 0:
                            tr = int(m['role']) + 3
                        else:
                            tr = 2
                    else:
                        tr = int(m['role'])
                    team['members'][i]['role'] = tr
                else:
                    team['members'].append(m)
            team["day_detail_create_flag"] = "1970-1-1"
            team["week_detail_create_flag"] = "1970-1"
            team.save()
            self.write("Success")
        else:
            self.write("Error")

    @tornado.web.authenticated
    def delete(self, teamID):
        email = self.get_secure_cookie("user")
        useremail = self.get_argument("useremail", "")
        team = connection.Team.find_one({'_id': ObjectId(teamID)})

        if team and useremail:
            user_ids = []
            i = 0
            for u in team['members']:
                if str(useremail) == str(u['email']):
                    if str(u['email']) != email:
                        team['members'].pop(i)
                    else:
                        team['members'][i]['role'] = 2
                    break
                i += 1
            team.save()
            self.write("Success")
        else:
            self.write("Error")
