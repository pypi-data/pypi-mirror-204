"""Base class for all conditions"""

from typing import Any, Union, Dict


class Condition:
    """Condition is a base class for all SDK conditions"""

    def __init__(self, json_condition: Dict[str, Union[str, Any]]):
        self.type_ = json_condition.get("targetingType")
        self.include = json_condition.get("include", True)

    def check(self, datas):
        """Check the condition for targeting"""
        raise NotImplementedError
