from typing import Dict


class BasicOpInfo(object):
    def __init__(self, op_type, name, machine_times: Dict[int, float]):
        self.op_type = op_type
        self.name = name
        self.machine_times = machine_times


class Changeover(object):
    def __init__(self):
        self.info = {}

    def add(self, pre_mtm, pre_op_type, cur_mtm, cur_op_type, processing_time):
        self.info[(pre_op_type, cur_op_type)] = processing_time

    def get(self, pre_mtm, pre_op_type, cur_mtm, cur_op_type):
        return self.info[(pre_op_type, cur_op_type)]
