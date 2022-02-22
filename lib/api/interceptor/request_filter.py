# coding: utf-8

import  json
import  datetime
from flask import  request
from config.setting import DD_EVENT_WHITE, DD_MSG_QUEUE
from utils import UID

def handle_request(app):


    @app.after_request
    def say_goodbye(response):

        if "/test/jj" in request.full_path and response.status_code == 200 :

            if request.is_json  and request.json.get("event") in DD_EVENT_WHITE :

                 DD_MSG_QUEUE.put(json.dumps({**request.json, "ddtime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ,'ddid': UID.id }))

                 print(' starting handle_request put queue before  response...')

        return response










