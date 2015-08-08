# -*- coding: UTF-8 -*-
'''
jack.zh sen mail test.
'''
import thread        
import smtplib
from email.mime.text import MIMEText

from settings import From_email
from settings import From_email_1
from settings import From_email_2

from log import logger


def send_mail(to_list, sub, content):
    me="beyondsoft.ams"+"<"+From_email["mail_user"]+"@"+From_email["mail_postfix"]+">"
    msg = MIMEText(content,_subtype='html',_charset='utf-8')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        server = smtplib.SMTP()
        server.connect(From_email["mail_host"])
        server.login(From_email["mail_user"],From_email["mail_pass"])
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception, e:
        logger.error(str(e))
        send_mail_1(to_list, sub, content)


def send_mail_1(to_list, sub, content):
    me="beyondsoft.ams"+"<"+From_email_1["mail_user"]+"@"+From_email_1["mail_postfix"]+">"
    msg = MIMEText(content,_subtype='html',_charset='utf-8')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        server = smtplib.SMTP()
        server.connect(From_email_1["mail_host"])
        server.login(From_email_1["mail_user"],From_email_1["mail_pass"])
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception, e:
        logger.error(str(e))
        send_mail_2(to_list, sub, content)


def send_mail_2(to_list, sub, content):
    me="beyondsoft.ams"+"<"+From_email_2["mail_user"]+"@"+From_email_2["mail_postfix"]+">"
    msg = MIMEText(content,_subtype='html',_charset='utf-8')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        server = smtplib.SMTP()
        server.connect(From_email_2["mail_host"])
        server.login(From_email_2["mail_user"],From_email_2["mail_pass"])
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception, e:
        logger.error(str(e))
        return False


def send_mail_thread(mailto_list, subject, msg):
    if send_mail(mailto_list, subject, msg):
        logger.info("send mail success.") 
    else:
        logger.error("send mail fail.")
        logger.error(subject)
        logger.error(msg)


def util_send_email(msg, subject, emails):
    thread.start_new_thread(send_mail_thread, (emails, subject, msg))


if __name__ == '__main__':
    fd = open("../templates/mail/week_summary.html", "r")
    s = fd.read()
    fd.close()
    logger.error(s)

    mailto_list=["zzh.coder@qq.com"]
    if send_mail(mailto_list,"hello",s):
        logger.error("yes")
    else:
        logger.error("no")
