# coding: utf-8

'''
 run all service

'''

__author__='victor'


from gevent import  monkey
from gevent.pywsgi import WSGIServer

monkey.patch_all()

import sys, logging
import json
import time
import datetime
import requests

from logging.handlers import RotatingFileHandler

from config.setting import DD_MSG_QUEUE
from requests.auth import  HTTPBasicAuth
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from multiprocessing import cpu_count, Process
from server import Intranet_Server

from interceptor.request_filter import handle_request
from config.setting import BASIC_AUTH ,LOG_INFO
from worker import _workThreadSMS
from utils  import kafka_client
from utils.log_handle import logger


def workService():

    executor = ThreadPoolExecutor(6)

    def worker(body):

        try:

          msg = json.loads(body)

          if "type" not in msg :

              return

          elif msg["type"] == "SMS" :

              executor.submit(_workThreadSMS, msg)

          else:

              logger.info("UNKNOWN FORMAT : {}".format(body))

        except Exception as e :

            logger.info("UNKNOWN FORMAT : {} , error : {} ".format(body, e))

    for msg in kafka_client.consumer:

        logger.info(
            " PARTITION : {}, TIMESTAMP : {} , OFFSET : {} . VALUE : {}".format(
                msg["partition"],
                msg["timestamp"],
                msg["offset"],
                msg["value"]
        ))
        worker(body=msg['value'])


def mirrorService(xport1) :

    while True :

        time.sleep(8)

        try:

            r1 = requests.post(
                url="http://0.0.0.0:{}/test/jj/col.gif".format(xport1),
                headers={"Content-type":"application/json"},
                json={"event" : "aws_test", "text" : " intranet jj message "},
                auth=HTTPBasicAuth(BASIC_AUTH.get("USER"), BASIC_AUTH.get("PASSWORD")),
                timeout =1
            )

            print('r1.status_code......',r1.status_code)
            if r1.status_code != 200 :

               raise ValueError(
                   "jj message probe status_code error , r1 :{}".format(r1.status_code)
               )

        except Exception as e:

            kafka_client.producer(
                json.dumps(
                    {
                        "type" :  "SMS",
                        "title":  "[WARNING] DATA-API SERVICE SLOW",
                        "context": "TIME:{}, ERROR : {} ".format(
                            datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
                            e
                        )
                    }
                )
            )


def ddService():


    try:
            PATH =LOG_INFO.get("PATH")

            loggerDD = logging.getLogger(
                "dd"
            )

            loggerDD.setLevel(LOG_INFO.get('LEVEL'))

            _logRotatingFileDDHandler = RotatingFileHandler(
                PATH[0:PATH.rfind("/")] + "/dd.log",
                maxBytes= 1024 * 1024,
                backupCount= 10,
                encoding="utf-8"
            )
            _logRotatingFileDDHandler.setFormatter(logging.Formatter('%(message)s'))

            loggerDD.addHandler(_logRotatingFileDDHandler)

            print(' ddService start  finish ......')

    except Exception as e:

           print('ddService Exception ....')

           logger.error('ddService error', str(e))

    while True :

        value = DD_MSG_QUEUE.get(True)

        loggerDD.info(value)







def schedulerIntranetService(xport) :

    try:

        s = Intranet_Server()
        handle_request(s.app)
        multiserver = WSGIServer(('0.0.0.0', xport), s.app, log=None)
        multiserver.start()

        def server_forever():
            multiserver.start_accepting()
            multiserver._stop_event.wait()

        for i in range(cpu_count()):

            p = Process(target=server_forever())

            p.start()

    except Exception as e :

        logger.error("schedulerIntranetService error : {}".format(e))


if __name__ == '__main__':


    if len(sys.argv) == 2 :

        port_num = int(sys.argv[1])

        if port_num >= 65534 or port_num <=0:

               sys.exit(1)
    else:

        port_num = 8889

    with ProcessPoolExecutor(max_workers=4) as executor:

         executor.submit(schedulerIntranetService,port_num)

         executor.submit(mirrorService, port_num)

         executor.submit(workService)

         executor.submit(ddService)








