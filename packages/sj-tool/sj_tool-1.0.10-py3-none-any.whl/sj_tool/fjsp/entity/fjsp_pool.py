from dataclasses import dataclass, field
from typing import Dict, Union

from sj_tool.fjsp.entity.job import BaseJob
from sj_tool.fjsp.entity.machine import BaseMachine
from sj_tool.fjsp.entity.operation import BaseOperation
from sj_tool.fjsp.entity.changeover import BasicOpInfo
from sj_tool.fjsp.entity.product import BaseProduct


@dataclass
class FjspPool:
    # 工单列表
    job_dict: Dict[Union[int, str], BaseJob] = field(default_factory=dict)
    # 所有的工序列表
    op_dict: Dict[Union[int, str], BaseOperation] = field(default_factory=dict)
    # 工序基础信息
    op_info_dict: Dict[Union[int, str], BasicOpInfo] = field(default_factory=dict)
    # 机器列表
    machine_dict: Dict[Union[int, str], BaseMachine] = field(default_factory=dict)
    # 产品列表
    product_dict: Dict[Union[int, str], BaseProduct] = field(default_factory=dict)
