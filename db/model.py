# -*- coding: utf-8 -*-
import time
import settings
from bson import ObjectId
from log import logger
from mongokit import Connection, IS
from ext import DynamicType, BaseModel

import datetime

from utils import get_year_month_day_str_ch
from utils import get_hour_minute_str
from utils import get_hour_minute_second_str
from utils import get_year_week_day_str
from utils import get_year_month_day_str
from utils import get_year_week_str
from utils import get_year_week_day_str_ch
from utils import get_year_week_day_str_ch_from_format_str

connection = Connection()

@connection.register
class FeedBack(BaseModel):
    __collection__ = "FeedBack_Col"

    structure = {
        "message": basestring,
        "username": basestring,
        "email": basestring,

        "status": int, # 0: New   1: OK   2: Do not fix

        "createtime": datetime.datetime,
        "fixtime": datetime.datetime,
        "rfs": dict #reserve fields
    }

    def create(self, message, username, email):
        fb = self()
        fb['createtime'] = datetime.datetime.now()
        fb['message'] = message
        fb['username'] = username
        fb['status'] = 0
        fb['email'] = email
        fb['fixtime'] = datetime.datetime.now()
        fb.save()

    def update_status(self, id, status):
        fb = self.find_one({"_id": id})
        fb.update({"status": int(status)})
        if status == 1:
            fb['fixtime'] = datetime.datetime.now()
        fb.save()

    def get_all(self):
        return connection.FeedBack.find({})


@connection.register
class Bulletin(BaseModel):
    __collection__ = "Bulletin_Col"

    structure = {
        "name": basestring,
        "time": datetime.datetime,
        "type": int, # 0:URL 1:Text
        "teamname": basestring,
        "text": basestring,
        "teamID":ObjectId,
        "username": basestring,
        "useremail": basestring,        
        "rfs": dict #reserve fields
    }

@connection.register
class User(BaseModel):
    __collection__ = "User_Col"

    structure = {
        "name": basestring,
        "email": basestring,
        "addtime": datetime.datetime,
        "password": basestring,
        "role": int, # reserve fields
        "tel_office": basestring,
        "tel_personal":basestring,
        "job_number": basestring,
        "address":basestring,
        "age":int,
        "sex":int,
        "rfs": dict #reserve fields
    }

    default_values = {
        "role": 0,
        "rfs": {}
    }

    def regist(self, email, username, password):
        flag = self.find_by_email(email)
        if flag:
            user = self() # WTF
            user["addtime"] = datetime.datetime.now()
            user['email'] = email
            user['name'] = username
            user['password'] = password

            user.save()
            return True, ""
        else:
            return False, u"此邮箱已注册"

    def find_by_email(self, email):
        user = self.find_one({'email': email})
        if user:
            return False
        else:
            return True

    def get_user_by_email(self, email):
        user = self.find_one({'email': email})
        return user

    def login_action(self, email, password):
        user = self.find_one({'email': email, "password":password})
        if user:
            return True, ""
        else:
            return False, u"邮箱或者密码错误"

    def add_user_by_teamadd_action(self, email, username):
        user = self.get_user_by_email(email)
        if user:
            return user['_id']
        else:
            user = self() # WTF
            user["addtime"] = datetime.datetime.now()
            user["password"] = ""
            user["administrator"] = False

            user['email'] = email
            user['username'] = username
            user['administrator'] = False
            user.save()
            return user['_id']


@connection.register
class Team(BaseModel):
    __collection__ = "Team_Col"

    structure = {
        "name": basestring,
        "create_time": datetime.datetime,
        "status": int,  # 0:nomal 1:archive 2:deleted

        "ownerID": ObjectId,
        "ownername": basestring,
        "owneremail": basestring,

        "day_or_week": int, # 0: day 1:week

        # day_detail
        "day_detail_create_time": basestring,   # 12:15
        "day_detail_remind_interval": int,      # Minute
        "day_detail_summary_time": basestring,
        "day_detail_create_flag": basestring,   # flag create which day ; value: "2015-18-3"
        "day_detail_summary_flag": basestring,   # flag summary which day ; value: "2015-18-3"
        "day_detail_notify_flag": int,

        # week datail
        "week_detail_create_time": basestring,   # 3-12:15
        "week_detail_remind_interval": int,      # Minute
        "week_detail_summary_time": basestring,  # 5-20:00
        "week_detail_create_flag": basestring,   # flag create which week ; value: "2015-18"
        "week_detail_summary_flag": basestring,   # flag summary which week ; value: "2015-18"
        "week_detail_notify_flag": int,

        # task_detail
        "member_task_summary_time":  basestring,
        "team_task_summary_time":  basestring,
        "member_task_summary_flag": basestring,
        "team_task_summary_flag": basestring,

        # member
        # [{?},{?}]
        #   |
        #   v
        # {
        #     "name": "jack", 
        #     "email":"zhangzhihe@beyondsoft.com", 
        #     "role": int, 
        #     "tel_personal":basestring,
        #     "job_number": basestring,
        #     "address":basestring
        # }
        #  role: 0:  码农 1: 关注者 2: 所有者 3:码农&&所有者 4:关注者&&所有者

        "members": list, #[ObjectId], # user list
        "rfs": dict #reserve fields
    }
    required_fields = ["name"]

    default_values = {
        "create_time": datetime.datetime.now(),

        "status": 0,

        # day_detail
        "day_detail_create_time": "09:00",   # 12:15
        # "day_detail_remind_time": "16:00", # 12:30
        "day_detail_remind_interval": 15,      # Minute
        "day_detail_summary_time": "20:00",
        "day_detail_create_flag": "1970-1-1",   # flag create which day ; value: "2015-18-3"
        "day_detail_summary_flag": "1970-1-1",   # flag summary which day ; value: "2015-18-3"
        "day_detail_notify_flag": 0,

        # week datail
        "week_detail_create_time": "5-09:00",
        # "week_detail_remind_time": "5-16:00",
        "week_detail_remind_interval": 15,
        "week_detail_summary_time": "5-20:00",
        "week_detail_create_flag": "1970-1",   # flag create which week ; value: "2015-18"
        "week_detail_summary_flag": "1970-1",   # flag summary which week ; value: "2015-18"
        "week_detail_notify_flag": 0,

        # task_detail
        "member_task_summary_time":  "20:00",
        "team_task_summary_time":  "20:15",
        "day_or_week": 0
    }

    def createTeam(self, date):
        _team = self.find_team_by_name(date['name'])
        if _team:
            return False, u"Team名称'" + date['name'] + u"'已经存在"
        else:
            team = self() # WTF
            team["create_time"] =  datetime.datetime.now()
            team["day_detail_create_flag"] =  "1970-1-1"
            team["day_detail_summary_flag"] =  "1970-1-1"
            team["day_detail_notify_flag"] =  0
            team["week_detail_create_flag"] =  "1970-1"
            team["week_detail_summary_flag"] =  "1970-1"
            team["week_detail_notify_flag"] =  0

            for d in date:
                team[d] = date[d]
            team.save()
            return True, ""

    def find_team_by_name(self, name):
        team = self.find_one({"name":name})
        return team

    def get_summary_week(self, year_week=None):
        year_week = year_week or get_year_week_str()
        teamID = self['_id']
        weeks = connection.WeekDetail.find({"teamID":teamID, "year_week":year_week})
        weeks_detail = []
        for w in weeks:
            _week = {}
            username = w['username']
            _week['username'] = username
            _week['status'] = w['status']
            _week['submit_list'] = w['submit_list']
            _week['rfs'] = w['rfs']
            weeks_detail.append(_week)
        return weeks_detail

    def get_summary_day(self, year_week_day=None):
        year_week_day = year_week_day or get_year_week_day_str()
        teamID = self['_id']
        days = connection.DayDetail.find({"teamID":teamID, "year_week_day":year_week_day})
        days_detail = []
        for d in days:
            _day = {}
            username = d['username']
            _day['username'] = username
            _day['status'] = d['status']
            _day['submit_list'] = d['submit_list']
            _day['rfs'] = d['rfs']
            days_detail.append(_day)
        return days_detail

    def get_users(self):
        users = []
        for m in self.members:
            user = [m["name"], m["email"]]
            users.append(user)
        return users

    def deep_delete(self):
        teamID = self['_id']

        dayDetails = connection.DayDetail.find({"teamID": teamID})
        for i in dayDetails:
            i.delete()

        weekDetails = connection.WeekDetail.find({"teamID": teamID})
        for i in weekDetails:
            i.delete()

        tasks = connection.Task.find({"teamID": teamID})
        for i in tasks:
            i.delete()
    
        taskMemberSummarys = connection.TaskMemberSummary.find({"teamID": teamID})
        for i in taskMemberSummarys:
            i.delete()
 
        taskTeamSummarys = connection.TaskTeamSummary.find({"teamID": teamID})
        for i in taskTeamSummarys:
            i.delete()

        self.delete()


@connection.register
class DayDetail(BaseModel):
    __collection__ = "DayDetail_Col"

    structure = {
        "teamID": ObjectId,
        "useremail": basestring,

        "username": basestring,
        "teamname": basestring,

        "year_week_day": basestring,

        "submit_list": list,
        # submit_list是一个列表，列表里面存储的数据大致如下：
        # [{}]
        #   |
        #   V
        # {
        #    "pre": list,
        #    "next": list,
        #    "problem": list,
        #    "submit_time":datetime.datetime
        # }
        # pre, next 的list如下：
        # [{}]
        #   |
        #   V
        # {
        #    "level": int, # 0:紧急 1:高 2:中 3:低
        #    "type": int, # 0:工作 1:学习 2:拓展 3:其他
        #    "text": basestring
        # }

        # problem 的list如下：
        # [{}]
        #   |
        #   V
        # {
        #    "level": int, # 0:紧急 1:高 2:中 3:低
        #    "type": int, # 0:工作 1:学习 2:拓展 3:其他
        #    "text": basestring
        # }

        "status": IS(
            0,  # 未提交
            1,  # 已提醒
            2,  # 已OK
            3,  # 已请假
            4,  # 失效Detail
            5,  # 延迟提交
            6,  # 保留字段
            7   # 保留字段
        ),
        "create_time": datetime.datetime,
        "submit_time": datetime.datetime,
        "update_time": datetime.datetime,
        "deadline_time": datetime.datetime,
        "expend_time": int,
        "late": int, # 0:NO 1: YES
        "rfs": dict #reserve fields
    }

    default_values  = {
        "status": 0,
        "expend_time": 8,
        "late": 0,
    }

    def find_for_notify(self, teamID, member):
        year_week_day = get_year_week_day_str()
        return self.find_one({
            "teamID":teamID,
            "username":member['name'],
            "useremail":member['email'],
            "year_week_day":year_week_day
            })

    def createByUserList(self, teamID, members, teamname, day_detail_summary_time):
        usersDayDetails = []

        year_week_day = get_year_week_day_str()

        print day_detail_summary_time

        for m in members:
            if m['role'] not in [0, 3]:
                continue
            d = {
                "teamID": teamID,
                "teamname": teamname,
                "username": m["name"],
                "useremail": m["email"],
                "year_week_day": year_week_day
            }
            if connection.DayDetail.find_one(d):
                continue
            detail = []
            dayDetail = self()
            dayDetail["status"] = 0
            dayDetail["create_time"] = datetime.datetime.now()

            dayDetail["teamID"] = teamID
            dayDetail["teamname"] = teamname
            dayDetail["username"] = m["name"]
            dayDetail["useremail"] = m["email"]
            dayDetail["year_week_day"] = year_week_day

            dayDetail["submit_time"] = datetime.datetime.now()
            dayDetail["update_time"] = datetime.datetime.now()
            dayDetail["deadline_time"] = datetime.datetime.now()
            dayDetail["expend_time"] = 8

            dayDetail.save()
            key = dayDetail['_id']
            detail = [m["name"], m["email"], str(key)]
            usersDayDetails.append(detail)
        return usersDayDetails

    def pushDetail(self, idstr, pretext, nexttext, problem_text, expend_time):
        dayDetail = self.find_one({"_id": ObjectId(idstr)})
        submit = {}
        submit['pre'] = [{
            "level": 0, # 0:紧急 1:高 2:中 3:低
            "type": 0, # 0:工作 1:学习 2:拓展 3:其他
            "text": pretext
            }]

        submit['next'] = [{
            "level": 0, # 0:紧急 1:高 2:中 3:低
            "type": 0, # 0:工作 1:学习 2:拓展 3:其他
            "text": nexttext
            }]
        submit['submit_time'] = datetime.datetime.now()
        if problem_text:
            submit['problem'] = [{
                "level": 0, # 0:紧急 1:高 2:中 3:低
                "type": 0, # 0:工作 1:学习 2:拓展 3:其他
                "text": problem_text
                }]
        if dayDetail:
            dayDetail.update({
                "status": 2,
                "update_time": datetime.datetime.now(),
                "submit_time": datetime.datetime.now(),
                "expend_time": int(expend_time)
                })
            dayDetail["submit_list"].append(submit)
            dayDetail.save()
            self._checkDetailSummary(dayDetail['year_week_day'], dayDetail['teamID'])

    def _checkDetailSummary(self, year_week_day, teamID):

        now_year_week_day = get_year_week_day_str()
        team = connection.Team.find_one({"_id":ObjectId(teamID)})
        if team:
            now = datetime.datetime.now()
            _h = now.hour
            _m = now.minute
            if _h < 10:
                _h = "0" + str(_h)
            if _m < 10:
                _m = "0" + str(_m)
            now = str(_h) + ":" + str(_m)
            now = now_year_week_day + now

            team_day_detail_summary_time = team["day_detail_summary_time"]

            s_time = year_week_day + team_day_detail_summary_time

            if now > s_time:
                pass
            else:
                dayDetails = self.find({"teamID": teamID, "year_week_day":year_week_day})
                for detail in dayDetails:
                    if detail['status'] not in [2, 3]:
                        return

            if now_year_week_day == year_week_day:
                team.update({"day_detail_summary_flag":year_week_day})
                team.save()

            from db.cache import taskQueue
            day_summary = team.get_summary_day(year_week_day)
            users = team.get_users()
            _queue = {"type": "summaryDay", "users": users, "value": day_summary, "team": team['name'], "now_flag":year_week_day}
            taskQueue.put(_queue)

    def find_by_id_verbose(self, idstr):
        dayDetail = self.find_one({"_id": ObjectId(idstr)})
        if dayDetail:
            username = dayDetail['username']

            r_day_detail = {}
            r_day_detail["year_week_day"] = dayDetail["year_week_day"]
            r_day_detail["create_time"] = dayDetail["create_time"]
            r_day_detail["status"] = dayDetail["status"]
            r_day_detail["submit_list"] = dayDetail["submit_list"]
            r_day_detail["username"] = username
            r_day_detail["rfs"] = dayDetail["rfs"]
            r_day_detail["expend_time"] = dayDetail["expend_time"]

            return r_day_detail
        else:
            return None


@connection.register
class WeekDetail(BaseModel):
    __collection__ = "WeekDetail_Col"

    structure = {
        "teamID": ObjectId,
        "useremail": basestring,

        "username": basestring,
        "teamname": basestring,

        "year_week": basestring,
        "submit_list": list,

        # submit_list是一个列表，列表里面存储的数据大致如下：
        # [{}]
        #   |
        #   V
        # {
        #    "pre": list,
        #    "next": list,
        #    "problem": list,
        #    "submit_time":datetime.datetime
        # }
        # pre, next 的list如下：
        # [{}]
        #   |
        #   V
        # {
        #    "level": int, # 0:紧急 1:高 2:中 3:低
        #    "type": int, # 0:工作 1:学习 2:拓展 3:其他
        #    "text": basestring
        # }

        # problem 的list如下：
        # [{}]
        #   |
        #   V
        # {
        #    "level": int, # 0:紧急 1:高 2:中 3:低
        #    "type": int, # 0:工作 1:学习 2:拓展 3:其他
        #    "text": basestring
        # }

        "status": IS(
            0,  # 未提交
            1,  # 已提醒
            2,  # 已OK
            3,  # 已请假
            4,  # 失效Detail
            5,  # 保留字段
            6,  # 保留字段
            7   # 保留字段
        ),
        "create_time": datetime.datetime,
        "submit_time": datetime.datetime,
        "update_time": datetime.datetime,
        "deadline_time": datetime.datetime,
        "expend_time": int,
        "late": int, # 0:NO 1: YES
        "rfs": dict #reserve fields
    }

    default_values = {
        "status": 0,
        "expend_time":40
    }

    def find_for_notify(self, teamID, member):
        year_week = get_year_week_str()
        return self.find_one({
            "teamID":teamID,
            "username":member['name'],
            "useremail":member['email'],
            "year_week":year_week
            })

    def createByUserList(self, teamID, members, teamname, week_detail_summary_time):
        weekDetails = []
        year_week = get_year_week_str()

        print week_detail_summary_time

        for m in members:
            if m['role'] not in [0, 3]:
                continue
            d = {
                "teamID": teamID,
                "teamname": teamname,
                "username": m["name"],
                "useremail": m["email"],
                "year_week": year_week
            }
            if connection.DayDetail.find_one(d):
                continue
            detail = []
            weekDetail = self()
            weekDetail["status"] = 0
            weekDetail["create_time"] = datetime.datetime.now()

            weekDetail["teamID"] = teamID
            weekDetail["teamname"] = teamname
            weekDetail["username"] = m["name"]
            weekDetail["useremail"] = m["email"]
            weekDetail["year_week"] = year_week

            weekDetail["submit_time"] = datetime.datetime.now()
            weekDetail["update_time"] = datetime.datetime.now()
            weekDetail["deadline_time"] = datetime.datetime.now()
            weekDetail["expend_time"] = 40

            weekDetail.save()
            key = weekDetail['_id']
            detail = [m["name"], m["email"], str(key)]
            weekDetails.append(detail)
        return weekDetails

    def pushDetail(self, idstr, pretext, nexttext, problem_text, expend_time):
        weekDetail = self.find_one({"_id": ObjectId(idstr)})
        submit = {}
        submit['pre'] = [{
            "level": 0, # 0:紧急 1:高 2:中 3:低
            "type": 0, # 0:工作 1:学习 2:拓展 3:其他
            "text": pretext
            }]

        submit['next'] = [{
            "level": 0, # 0:紧急 1:高 2:中 3:低
            "type": 0, # 0:工作 1:学习 2:拓展 3:其他
            "text": nexttext
            }]
        submit['submit_time'] = datetime.datetime.now()
        if problem_text:
            submit['problem'] = [{
                "level": 0, # 0:紧急 1:高 2:中 3:低
                "type": 0, # 0:工作 1:学习 2:拓展 3:其他
                "text": problem_text
                }]
        if weekDetail:
            weekDetail.update({
                "status": 2,
                "update_time": datetime.datetime.now(),
                "submit_time": datetime.datetime.now(),
                "expend_time": int(expend_time)
                })
            weekDetail["submit_list"].append(submit)
            weekDetail.save()
            self._checkDetailSummary(weekDetail['year_week'], weekDetail['teamID'])


    def _checkDetailSummary(self, year_week, teamID):
        weekDetails = self.find({"teamID": teamID, "year_week":year_week})
        all_ok = True
        for detail in weekDetails:
            if detail['status'] not in [2, 3]:
                all_ok = False

        now_year_week = get_year_week_str()
        team = connection.Team.find_one({"_id":ObjectId(teamID)})
        if team:
            if now_year_week == year_week:
                team.update({"week_detail_summary_flag":year_week})
                team.save()

        now_time_str = str(datetime.datetime.now().isocalendar()[2]) + datetime.datetime.now().strftime('%H:%M')
        team_time_str = team['week_detail_summary_time']

        if not all_ok and now_year_week == year_week and now_time_str <= team_time_str:
            return

        from db.cache import taskQueue

        week_summary = team.get_summary_week(year_week)
        users = team.get_users()
        _queue = {"type": "summaryWeek", "users": users, "value": week_summary, "team": team['name'], "now_flag":year_week}
        taskQueue.put(_queue)

    def find_by_id_verbose(self, idstr):
        weekDetail = self.find_one({"_id": ObjectId(idstr)})
        if weekDetail:
            username = weekDetail['username']
            r_week_detail = {}
            r_week_detail["year_week"] = weekDetail["year_week"]
            r_week_detail["create_time"] = weekDetail["create_time"]
            r_week_detail["status"] = weekDetail["status"]
            r_week_detail["submit_list"] = weekDetail["submit_list"]
            r_week_detail["username"] = username
            r_week_detail["rfs"] = weekDetail["rfs"]
            r_week_detail["expend_time"] = weekDetail["expend_time"]

            return r_week_detail
        else:
            return None


@connection.register
class Task(BaseModel):
    __collection__ = "Task_Col"

    structure = {
        "teamID": ObjectId,
        "useremail": basestring,

        "username": basestring,
        "teamname": basestring,

        "createusername": basestring,
        "pubusername": basestring,

        "createuseremail": basestring,
        "pubuseremail": basestring,

        "name": basestring,
        "dead_line_time": datetime.datetime,
        "explain": basestring, # 说明
        "remarks": basestring, # 备注
        # "remarks": list,
        # list: [{}]
        #         |
        #         V
        # {
        #     "uuid": basestring, # id mark
        #     "username": "jack.zh",
        #     "updatetime":datetime.datetime(),
        #     "text": basestring,
        #     "type": int
        # }
        "priority": IS(
            0,  # 紧急
            1,  # 高
            2,  # 中
            3,  # 低
            4,  # 保留字段
            5,  # 保留字段
            6,  # 保留字段
            7   # 保留字段
        ),
        "status": IS(
            0,  # 未完成
            1,  # 进行中
            2,  # 已完成
            3,  # 延后
            4,  # 延后完成
            5,  # 保留字段
            6,  # 保留字段
            7   # 保留字段
        ),
        "weight": IS(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
        "score":  float,

        "create_time": datetime.datetime,
        "update_time": datetime.datetime,
        "done_time": datetime.datetime,
        "start_time": datetime.datetime,
        "done_100": int,
        "rfs": dict #reserve fields
    }

    default_values = {
        "name": "new task",
        "explain": "",
        "priority": 2,
        "status": 0,
        "remarks": "",
        "done_100": 0,
        "weight": 1,
        "score": 1.0
    }

    def newTask(self, teamID, teamname, username, useremail, createusername, createuseremail, pubusername, pubuseremail, name, explain, priority, dead_line_time, weight):
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

        task = self()
        task["teamID"] = teamID
        task["teamname"] = teamname
        
        task['username'] = username
        task['useremail'] = useremail

        task['createusername'] = createusername
        task['createuseremail'] = createuseremail

        task['pubusername'] = pubusername
        task['pubuseremail'] = pubuseremail

        task["name"] = name
        task["dead_line_time"] = dead_line_time
        task["priority"] = priority
        task["create_time"] = datetime.datetime.now()
        task["update_time"] = datetime.datetime.now()
        task["done_time"] = dead_line_time
        task["start_time"] = datetime.datetime.now()
        task["explain"] = explain
        task['weight'] = int(weight)

        task.save()
        
        createTaskEmail = {}        
    
        createTaskEmail["teamname"] = teamname
        createTaskEmail["username"] = username
        createTaskEmail['createUsername'] = createusername
        createTaskEmail["name"] = name
        createTaskEmail["dead_line_time"] = _datetime2str(dead_line_time)
        createTaskEmail["priority"] = _priority2str(priority)
        createTaskEmail["explain"] = explain
        createTaskEmail["now"] = _datetime2str(datetime.datetime.now())
        createTaskEmail['email'] = useremail
        
        from settings import host_url
        createTaskEmail['url'] = host_url + "/edit/task/" + str(task['_id'])

        from db.cache import taskQueue
        _queue = {"type": "createTask", "data":createTaskEmail}
        taskQueue.put(_queue)

    def find_by_id_verbose(self, key):
        task = self.find_one({"_id": ObjectId(key)})
        if task:
            teamID = task['teamID']

            team = connection.Team.find_one({"_id":teamID})
            if team:
                ms = team['members']
                members = []
                for m in ms:
                    members.append({"username":m['name'], "email":m['email'], "role": m['role']})
            else:
                return None

            status = task['status']

            priority = task['priority']

            remarks = task['remarks']

            name = task['name']

            explain = task['explain']

            dead_line_time = task['dead_line_time']
            dead_line_time = str(dead_line_time.year) + "年" + str(dead_line_time.month) + "月" + str(dead_line_time.day) + "日 " + str(dead_line_time.hour) + ":" + str(dead_line_time.minute)

            createtime = task['create_time']
            createtime = [str(createtime.year) + "年" + str(createtime.month) + "月" + str(createtime.day) + "日 " + str(createtime.hour) + ":" + str(createtime.minute) ,  createtime.weekday()]

            done_100 = task['done_100']

            taskDict = {
                "status": status,
                "dead_line_time": dead_line_time,
                "explain": explain,
                "remarks": remarks,
                "name": name,
                "createtime": createtime,
                "members": members,
                "priority": priority,
                "username": task["username"],
                "createusername": task["createusername"],
                "pubusername": task["pubusername"],
                "email": task["useremail"],
                "done_100": done_100,
                'start_time': [get_year_month_day_str_ch(task['start_time']), get_hour_minute_str(task['start_time'])],
                'done_time': [get_year_month_day_str_ch(task['done_time']), get_hour_minute_str(task['done_time'])],
            }
            return taskDict

        else:
            return None

    def updateByService(self, key, status, pub, pub_text, update_task_remarks, update_task_done_100, real_time):
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

        task = self.find_one({"_id": ObjectId(key)})
        if status == 2 and real_time > task["dead_line_time"]:
            status = 4
        if task:
            if pub == 1:
                if status == 2 and real_time > task["dead_line_time"]:
                    status = 4
                useremail = pub_text.split("(")[1].split(")")[0]
                username = pub_text.split("(")[0]

                pubuseremail = task['useremail']
                pubusername = task['username']

                task['useremail'] = useremail
                task['username'] = username
                task['pubuseremail'] = pubuseremail
                task['pubusername'] = pubusername

                pubTaskEmail = {}
    
                pubTaskEmail["teamname"] = task["teamname"]
                pubTaskEmail["username"] = username
                pubTaskEmail['pubusername'] = pubusername
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

            task['status'] = status
            task['remarks'] = update_task_remarks
            task['done_100'] = update_task_done_100
            task['update_time'] = datetime.datetime.now()

            if status == 1:
                task['start_time'] = real_time
            elif status in [2, 4]:
                task['done_time'] = real_time
            else:
                pass

            if status in [2, 4]:
                task['done_100'] = 100
            if status == 0:
                task['done_100'] = 0
            task.save()
            return "Success"
        else:
            return "No Task"


@connection.register
class TaskMemberSummary(BaseModel):
    __collection__ = "TaskMemberSummary_Col"

    structure = {
        "teamID": ObjectId,
        "useremail": basestring,

        "teamname": basestring,
        "username": basestring,

        "createtime": datetime.datetime,
        "html": basestring,
        "rfs": dict #reserve fields
    }

    default_values = {
        "teamname": "",
        "username": "",
        "createtime": datetime.datetime.now(),
        "html": ""
    }

    def newHtml(self, _db_dict):
        tms = self()
        tms['createtime'] = datetime.datetime.now()
        for _ in _db_dict:
            tms[_] = _db_dict[_]

        tms.save()

        return str(tms['_id'])

@connection.register
class TaskTeamSummary(BaseModel):
    __collection__ = "TaskTeamSummary_Col"

    structure = {
        "teamID": ObjectId,
        "teamname": basestring,

        "createtime": datetime.datetime,
        "html": basestring,
        "rfs": dict #reserve fields
    }

    default_values = {
        "teamname": "",
        "createtime": datetime.datetime.now(),
        "html": ""
    }

    def newHtml(self, _db_dict):
        tts = self()
        tts['createtime'] = datetime.datetime.now()
        for _ in _db_dict:
            tts[_] = _db_dict[_]

        tts.save()
        return str(tts['_id'])