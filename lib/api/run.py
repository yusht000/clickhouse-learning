# coding: utf-8

'''
 run all service

'''

__author__='victor'

import sys
import json
import time
import datetime
import requests

from requests.auth import  HTTPBasicAuth
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

from config.setting import BASIC_AUTH
from worker import _workThreadSMS
from utils  import kafka_client


def workService():

    executor = ThreadPoolExecutor(6)

    def worker(body):

        try:

          msg = json.loads(body)

          if "type" not in msg :

              return

          elif msg["type"] == "SMS" :

              executor.submit(_workThreadSMS(),msg)

        except Exception as e :

            print("workService" , str(e))

    for msg in kafka_client.consumer:

        print(msg['partition'], msg['timestamp'], msg['offset'], msg['value'])

        worker(body=msg['value'])





def mirrorService(xport1) :

    while True :

        time.sleep(60 * 10)

        try:

            r1 = requests.post(
                url="http://0.0.0.0:{}/test/jj/col.gif".format(xport1),
                headers={"Content-type":"application/json"},
                json={"event" : "mm", "text" : " intranet jj message "},
                auth=HTTPBasicAuth(BASIC_AUTH.get("USER"), BASIC_AUTH.get("PASSWORD")),
                timeout =1
            )

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



if __name__ == '__main__':


    if len(sys.argv) == 2 :

        port_num = int(sys.argv[1])

        if port_num >= 65534 or port_num <=0:

               print('port error ...')

               sys.exit(1)
    else:

        port_num = 8889


    with ProcessPoolExecutor(max_workers=2) as executor:

         executor.submit(mirrorService, port_num)
         executor.submit(workService)








