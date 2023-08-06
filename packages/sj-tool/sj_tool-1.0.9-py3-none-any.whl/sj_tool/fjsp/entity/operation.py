from typing import List, Tuple, Dict, Union


class BaseOperation:
    def __init__(
        self,
        idx: Union[int, str],
        job_id: Union[int, str],
        op_type: Union[int, str],
        machine_times: Dict[int, float] = None,
    ):
        """

        :param idx: 工序id
        :param job_id: 工单id
        :param op_type: 工序类型
        :param machine_times: 操作在不同机器上的所需时间列表，例：{1:2,2:2,3:4},
                其中每个tuple的第一个元素表示机器id，第二个元素表示工序在对应机器上的单个所需时间
        """
        self.id = idx
        self.job_id = job_id
        self.op_type = op_type
        # op ids
        self.pre_ops = []
        self.next_ops = []
        self.machine_times = machine_times
