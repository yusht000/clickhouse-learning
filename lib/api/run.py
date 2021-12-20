# coding: utf-8

'''
 run all service

'''

__author__='victor'

import sys
import json

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

from worker import _workThreadSMS



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













if __name__ == '__main__':


    if len(sys.argv) == 2 :

        port_num = int(sys.argv[1])

        if port_num >= 65534 or port_num <=0:

               print('port error ...')

               sys.exit(1)
    else:

        port_num = 8889


    with ProcessPoolExecutor(max_workers=1) as executor:

         executor.submit(workService())







