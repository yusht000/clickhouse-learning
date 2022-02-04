# coding: utf-8

import  datetime

from kafka import KafkaConsumer, KafkaProducer

from kafka.errors import NoBrokersAvailable, KafkaTimeoutError

from config.setting import KAFKA_URI



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

        except Exception as e:

            print("create kafkaProducer is not Available .....", str(e))

        except NoBrokersAvailable :

            print(' create kafkaProducer  is  not Available ...')

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

        except Exception as e :

            print("create kafkaConsume is not Available .....", str(e))


        except NoBrokersAvailable :

            print("create kafkaConsume is not Available .....")

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

        except Exception as e :

            print('', str(e))


    def producer(self,msg):

        if not self._producer_client :

            print("KAFKA-ERROR : producer is not available")

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

                    print("warning  send msg to kafka is more than 60")

                return  True

            except KafkaTimeoutError as e :

                print("KafkaTimeoutError ", msg, str(e))

            except Exception  as e :

                print('exception', str(e))

                return  False


    def on_send_success(self, metadata):

        print(metadata.partition,metadata.timestamp, metadata.offset, metadata.topic,metadata.value)


    def on_send_error(self, error):

        print(error)






if __name__ == '__main__':


    pass










