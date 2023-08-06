from typing import Union

import pandas as pd


class BaseJob(object):
    def __init__(
        self, job_id: Union[int, str], product_code: str, arrival_time: str, ots_time: str, demand: Union[int, float]
    ):
        """

        :param job_id:
        :param product_code: 产品编码
        :param arrival_time: job到达时间，即最早可开始时间
        :param ots_time: 截止时间
        :param demand: 需求量
        """
        self.id = job_id
        self.product_code = product_code
        self.arrival_time = pd.to_datetime(arrival_time)
        self.ots_time = pd.to_datetime(ots_time)
        self.demand = demand
        self.start_operations = []
        self.operations = []
