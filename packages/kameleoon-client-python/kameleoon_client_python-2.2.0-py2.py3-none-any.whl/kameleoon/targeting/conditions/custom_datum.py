"""CustomData condition"""
import re
import json
import logging
from typing import Any, Union, Dict, Optional

from kameleoon.data import CustomData
from kameleoon.helpers.logger import get_logger
from kameleoon.exceptions import NotFoundError, KameleoonException
from kameleoon.targeting.condition import Condition
from kameleoon.targeting.conditions.constants import Operator, DataType

__all__ = [
    "CustomDatum",
]


class CustomDatum(Condition):
    """CustomDatum represents a Custom Data condition from back-office"""

    def __init__(self, json_condition: Dict[str, Union[str, Any]]):
        super().__init__(json_condition)
        if (
            "customDataIndex" not in json_condition
            or json_condition["customDataIndex"] is None
        ):
            raise NotFoundError("customDataIndex")
        self.index = json_condition["customDataIndex"]
        if (
            "valueMatchType" not in json_condition
            or json_condition["valueMatchType"] is None
        ):
            raise NotFoundError("valueMatchType")
        self.operator = json_condition["valueMatchType"]
        if "value" in json_condition and json_condition["value"] is not None:
            self.value = json_condition["value"]
        self.__logger_instance: Optional[logging.Logger] = None

    @property
    def __logger(self) -> logging.Logger:
        if self.__logger_instance is None:
            self.__logger_instance = get_logger()
        return self.__logger_instance

    # pylint: disable=R0912,R0915
    def check(self, datas) -> bool:  # noqa: C901
        is_targeted = False
        custom_data = self.__get_last_custom_data(datas)
        if not custom_data:
            is_targeted = self.operator == Operator["UNDEFINED"]
        else:
            if self.operator == Operator["MATCH"]:
                try:
                    pattern = re.compile(self.value)
                    is_targeted = any(re.match(pattern, val) is not None for val in custom_data.values)
                except re.error as err:
                    self.__logger.error(err)
            elif self.operator == Operator["CONTAINS"]:
                is_targeted = any(self.value in val for val in custom_data.values)
            elif self.operator == Operator["EXACT"]:
                is_targeted = self.value in custom_data.values
            elif self.operator == Operator["EQUAL"]:
                try:
                    value = float(self.value)
                    is_targeted = any(float(val) == value for val in custom_data.values)
                except ValueError as err:
                    self.__logger.error(err)
            elif self.operator == Operator["GREATER"]:
                try:
                    value = float(self.value)
                    is_targeted = any(float(val) > value for val in custom_data.values)
                except ValueError as err:
                    self.__logger.error(err)
            elif self.operator == Operator["LOWER"]:
                try:
                    value = float(self.value)
                    is_targeted = any(float(val) < value for val in custom_data.values)
                except ValueError as err:
                    self.__logger.error(err)
            elif self.operator == Operator["IS_TRUE"]:
                is_targeted = "true" in custom_data.values
            elif self.operator == Operator["IS_FALSE"]:
                is_targeted = "false" in custom_data.values
            elif self.operator == Operator["AMONG_VALUES"]:
                try:
                    # Possible issues with float values.
                    all_matches = json.loads(self.value)
                    parse_dict = {False: "false", True: "true"}
                    condtition_values = {parse_dict.get(m, str(m)) for m in all_matches}
                    is_targeted = any(val in condtition_values for val in custom_data.values)
                except json.JSONDecodeError as err:
                    self.__logger.error(err)
            elif self.operator != Operator["UNDEFINED"]:
                raise KameleoonException(f"Undefined operator {self.operator}")
        return is_targeted

    def __get_last_custom_data(self, datas) -> Optional[CustomData]:
        data_type = DataType["CUSTOM"]
        data_iter = iter(x for x in reversed(datas) if (x.instance == data_type) and (x.id == self.index))
        return next(data_iter, None)
