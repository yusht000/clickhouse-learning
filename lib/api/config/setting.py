# coding: utf-8

import uuid
from multiprocessing import  Queue
__version__ = "1.0.0"
__number__ = "v3"
__date__ = "20211216"



BASIC_AUTH={
    "USER":"test",
    "PASSWORD":'123'
}

KAFKA_URI = {
    "BOOTSTRAP_SERVERS" : [
        '52.220.214.100:49180',
        '52.220.214.100:49181',
        '52.220.214.100:49182'
    ],
    "TOPIC": "topic002",
    "GROUP_ID": "v1",
    "KEY": "test"
}


LOG_INFO = {
    "LEVEL":"INFO",
    "NAME": "api",
    "PATH": "/Users/bairong/tmp/all.log",
    "ERROR_PATH" : "/Users/bairong/tmp/error.log"
}

DD_EVENT_WHITE=[
    "test" ,'aws_test'
]

SNOWFLAKE_URI = {
    "DATA_CENTER": uuid.getnode(),
}


DD_MSG_QUEUE=Queue(10240)