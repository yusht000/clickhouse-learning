# coding: utf-8


import datetime
import time
import random
import os
from config.setting import SNOWFLAKE_URI

class uniqueID(object):

    def __init__(self):
        self.twepoch = 1288834974657
        self.datacenter_id_bits = 5
        self.worker_id_bits = 5
        self.sequence_id_bits = 12
        self.max_datacenter_id = 1 << self.datacenter_id_bits
        self.max_worker_id = 1 << self.worker_id_bits
        self.max_sequence_id = 1 << self.sequence_id_bits
        self.max_timestamp = 1 << (64 - self.datacenter_id_bits - self.worker_id_bits - self.sequence_id_bits)

    def make_snowflake(self, timestamp_ms, datacenter_id, worker_id, sequence_id):
        sid = ((int(timestamp_ms) - self.twepoch) % self.max_timestamp) << self.datacenter_id_bits << self.worker_id_bits << self.sequence_id_bits
        sid += (datacenter_id % self.max_datacenter_id) << self.worker_id_bits << self.sequence_id_bits
        sid += (worker_id % self.max_worker_id) << self.sequence_id_bits
        sid += sequence_id % self.max_sequence_id

        return sid

    def melt(self, snowflake_id):
        sequence_id = snowflake_id & (self.max_sequence_id - 1)
        worker_id = (snowflake_id >> self.sequence_id_bits) & (self.max_worker_id - 1)
        datacenter_id = (snowflake_id >> self.sequence_id_bits >> self.worker_id_bits) & (self.max_datacenter_id - 1)
        timestamp_ms = snowflake_id >> self.sequence_id_bits >> self.worker_id_bits >> self.datacenter_id_bits
        timestamp_ms += self.twepoch

        return (timestamp_ms, int(datacenter_id), int(worker_id), int(sequence_id))

    def local_datetime(self, timestamp_ms):
        return datetime.datetime.fromtimestamp(timestamp_ms / 1000.)

    @property
    def id(self):
        return self.make_snowflake(
            time.time() * 1000000,
            SNOWFLAKE_URI["DATA_CENTER"],
            os.getpid(),
            random.randint(0, 100)
        )

if __name__ == "__main__":
    pass