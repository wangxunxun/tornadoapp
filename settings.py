#!/usr/bin/env python
# -*- coding: utf-8 -*-

log = {
    'log_max_bytes': 5 * 1024 * 1024,  # 5M
    'backup_count': 10,
    'level':30,                         # 0: NOTSET; 10: DEBUG; 20:INFO; 30:WARNING; 40: ERROR
    'log_path': 'log/server.log',
    'logformat':{0:"NOTSET", 10:"DEBUG", 20:"INFO", 30:"WARNING", 40:"ERROR"}
}

host_port = 80

From_email = {
    "mail_host" :"smtp.163.com",  #设置服务器
    "mail_user" :"beyondsoft_ams",    #用户名
    "mail_pass" :"vhvargytmhcmjnmf",   #口令 
    "mail_postfix" :"163.com"  #发件箱的后缀 
}

From_email_1 = {
    "mail_host" :"smtp.163.com",  #设置服务器
    "mail_user" :"beyondsoft_wh",    #用户名
    "mail_pass" :"gcjztdfhapgkrofn",   #口令 
    "mail_postfix" :"163.com"  #发件箱的后缀 
}

From_email_2 = {
    "mail_host" :"smtp.163.com",  #设置服务器
    "mail_user" :"ale_ford",    #用户名
    "mail_pass" :"beyondsoft",   #口令 
    "mail_postfix" :"163.com"  #发件箱的后缀 
}

db = {
    'name': "ams"
}

host_ip = "106.185.47.124"

host_url = "http://" + host_ip + ":" + str(host_port)

gevent_sleep = 5  # 秒
