# coding: utf-8

import  datetime

from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import NoBrokersAvailable, KafkaTimeoutError
from config.setting import KAFKA_URI
from utils.log_handle import logger



class kafkaClient(object):

    def __init__(self):
        self._producer_client = self._createProducer
        self._consumer_client = self._createConsumer


    @property
    def _createProducer(self):

        try:
            return  KafkaProducer(
                bootstrap_servers = KAFKA_URI["BOOTSTRAP_SERVERS"],
                retries = 3,
            )
        except NoBrokersAvailable :

            logger.error("KAFKA ERROR : kafka brokers not available in producer , {}".format(
                KAFKA_URI["BOOTSTRAP_SERVERS"]
            ))


    @property
    def _createConsumer(self):

        try:

            return KafkaConsumer(
                KAFKA_URI["TOPIC"],
                group_id = KAFKA_URI["GROUP_ID"],
                bootstrap_servers = KAFKA_URI["BOOTSTRAP_SERVERS"],
                auto_offset_reset = "latest",
                enable_auto_commit = True,
                auto_commit_interval_ms = 5000
            )

        except NoBrokersAvailable :

              logger.error("KAFKA ERROR : kafka brokers not available in consumer  , {}". format(
                  KAFKA_URI["BOOTSTRAP_SERVERS"]
              ))


    @property
    def consumer(self):

        try :

            for x in self._consumer_client:

                yield{
                    "partition": x.partition,
                    "timestamp": x.timestamp,
                    "offset": x.offset,
                    "value":x.value.decode()
                }

        except NoBrokersAvailable as e :

              logger.error(
                  "KAFKA-ERROR : kafka broker is not available in consumer , {} ".format(
                      KAFKA_URI["BOOTSTRAP_SERVERS"]
                  )
              )


    def producer(self,msg):

        if not self._producer_client :
            logger.error(
                 "KAFKA ERROR : producer is not available , {}".format(
                     datetime.datetime.now().strptime('%Y-%m-%d %H:%M')
                 )
             )
            return  False

        else:

            try:

                pre = datetime.datetime.now()

                future= self._producer_client.send(
                    topic=KAFKA_URI["TOPIC"],
                    key = KAFKA_URI["KEY"].encode(),
                    value=msg.encode()
                )

                future.add_callback(self.on_send_success).add_errback(self.on_send_error)

                next= datetime.datetime.now()

                if (next - pre).seconds > 60:

                    logger.warning("KAFKA-WARNING : send msg to kafka is more than 60s")

                return  True

            except KafkaTimeoutError as e :

                logger.error(
                    "KAFKA-ERROR: send msg timeout, content :{} . exception : () ".format(
                        msg,
                        e
                    )
                )

            except Exception  as e :

                logger.error(
                    "KAFKA-ERROR: send msg timeout, content :{} . exception : () ".format(
                        msg,
                        e
                    )
                )

                return  False


    def on_send_success(self, metadata):

        logger.info(
            "KAFKA-INFO : partition : {}, timestamp :{}, offset : {} ,topic: {}, value:{} ".format(
                metadata.partition,
                metadata.timestamp,
                metadata.offset,
                metadata.topic,
                metadata.value
            )
        )

    def on_send_error(self, except_error):

        logger.error(
            "KAFKA-ERROR : send msg error ",
            exc_info = except_error
        )


if __name__ == '__main__':


    pass










