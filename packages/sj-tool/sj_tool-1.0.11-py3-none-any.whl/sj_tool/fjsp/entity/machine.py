from typing import List


class BaseMachine(object):
    def __init__(self, idx, name, available_ops: List[str] = [], unit_times={}):
        """

        :param machine_id:
        :param available_ops:
        """
        self.id = idx
        self.name = name
        self.available_ops = available_ops
        self.unit_times = unit_times  # {('product_id','operation_type'):单个的节拍 }
