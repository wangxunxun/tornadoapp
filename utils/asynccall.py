#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import requests
import Queue
import threading
import thread
from log import logger


_task_queue = Queue.Queue()
_callback_queue = Queue.Queue()


def get_ip_address_by_taobao(ip, data):
    payload = {'ip': ip}
    r = requests.get("http://ip.taobao.com/service/getIpInfo.php", params=payload)
    if r.status_code == 200:
        jsonObj = r.json()
        text = r.text
        if jsonObj['code'] == 0:
            backObj = {
                "data": data,
                "code": 0,
                "country": jsonObj['data']['country'],
                "country_id": jsonObj['data']['country_id']
            }
        else:
            backObj = {"code": jsonObj['code']}

        return backObj
    else:
        return {"code": -1}


def async_call(function, callback, *args, **kwargs):
    _task_queue.put({
        'function': function,
        'callback': callback,
        'args': args,
        'kwargs': kwargs
    })


def do_callback(task):
    function = task.get('function')
    callback = task.get('callback')
    args = task.get('args')
    kwargs = task.get('kwargs')
    backObj = function(*args, **kwargs)
    _callback_queue.put([callback, backObj])
    _task_queue.task_done()


def _task_queue_consumer():
    while True:
        try:
            task = _task_queue.get()
            thread.start_new_thread(do_callback, (task, ))
        except Exception as ex:
            logger.error(ex)

def _callback_queue_consumer():
    while True:
        try:
            callback = _callback_queue.get()
            callback[0](callback[1])
        except Exception as ex:
            logger.error(ex)
            import traceback
            logger.error(traceback.format_exc())   


if __name__ == '__main__':
    def handle_result(result):
        print(type(result), result)

    t = threading.Thread(target=_task_queue_consumer)
    t.daemon = True
    t.start()

    async_call(get_ip_address_by_taobao, handle_result, "42.96.155.222")

    while True:
        import time
        time.sleep(2)
