# -*- coding: utf-8 -*-
import time
import json
import settings
from bson import ObjectId
from mongokit import Document
from mongokit import CustomType


class DynamicType(CustomType):
    mongo_type = unicode
    python_type = unicode
    init_type = unicode

    def __init__(self, func, base_type=unicode):
        super(DynamicType, self).__init__()
        self.func = func
        self.mongo_type = base_type
        self.python_type = base_type
        self.init_type = base_type

    def to_bson(self, value):
        """convert type to a mongodb type"""
        return None

    def to_python(self, value):
        """convert type to a python object"""
        return self.func()

    def validate(self, value, path):
        pass


class BaseModel(Document):
    __database__ = settings.db['name']
    use_dot_notation = True

    def by_id(self, id):
        return self.find_one({'_id': ObjectId(id)})

    def update_by_id(self, id, update):
        m = self.by_id(id)
        update.pop('_id', None)
        for k, v in update.iteritems():
            m[k] = v
        m.save()

    def to_json(self):
        json_str = super(BaseModel, self).to_json()
        obj = json.loads(json_str)
        if '$oid' in json_str:
            def strip_oid(obj):
                from collections import Iterable
                if isinstance(obj, dict):
                    for key, value in obj.iteritems():
                        if isinstance(value, Iterable) and '$oid' in value:
                            obj[key] = value['$oid']
                        else:
                            strip_oid(value)
                elif isinstance(obj, list):
                    for item in obj:
                        strip_oid(item)
            strip_oid(obj)
        return json.dumps(obj)
