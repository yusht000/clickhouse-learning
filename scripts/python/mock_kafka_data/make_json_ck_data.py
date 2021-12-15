#!/usr/bin/env python3
# coding: utf-8


import json
import time
from kafka import KafkaProducer



topic = 'topic002'
nums  = 100

def main() :

    producer = KafkaProducer(
        bootstrap_servers=['52.220.214.100:49180','52.220.214.100:49181','52.220.214.100:49182'],
        value_serializer = lambda v: json.dumps(v).encode('utf-8')
    )

    st = time.time()

    cnt = 0

    for _ in range(nums):

        ddtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        data ={
            "ddtime": ddtime,
            "msg": "RTService",
            "platform": "CK-DD",
            "event": "aws_test",
            "data": "123",
            "ddid":_
        }
        time.sleep(1)

        producer.send(topic, value=data)

        cnt += 1

        print(cnt)


    producer.flush()

    et = time.time()

    cost_time = et - st

    print('send nums: {}, cost time: {}, rate: {}/s'.format(nums, cost_time, nums // cost_time))




if __name__ == '__main__':


   main()

   print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
