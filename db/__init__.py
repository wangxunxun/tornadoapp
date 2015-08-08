# -*- coding: utf-8 -*-
from model import connection

def disconnect_all_db():
    connection.User.collection.update({}, {'$set': {'status': u'disconnected'}}, multi=True)
