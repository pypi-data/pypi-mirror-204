"""Module for ExamScheduleContainer model."""

from dataclasses import dataclass
from typing import Iterable

from eokulapi.Models import from_list
from eokulapi.Models.EokulDictable import EokulDictable
from eokulapi.Models.ExamSchedule import ExamSchedule


def _flatten(lis: Iterable):
    """Flattens a list of lists into a single list.

    Args:
        lis (Iterable): List to be flattened

    Yields:
        Any: Flattened Iterable
    """
    for item in lis:
        if isinstance(item, Iterable) and not isinstance(item, str):
            for x in _flatten(item):
                yield x
        else:
            yield item


@dataclass
class ExamScheduleContainer(EokulDictable):
    """Exam schedule container model."""

    data: list[ExamSchedule]
    """Exam schedule data as list of ExamSchedule objects"""

    @classmethod
    def from_dict(cls, obj: dict):
        """Convert a dict to ExamScheduleContainer object.

        Args:
            obj (dict): Object to be converted

        Returns:
            ExamScheduleContainer: ExamScheduleContainer object that is converted from dict
        """
        schedule_list = from_list(
            ExamSchedule.from_dict, obj.get("SinavTarihleriListesi")
        )
        schedule_list = list(
            filter(lambda item: item is not None, _flatten(schedule_list))
        )

        return cls(schedule_list)

    @classmethod
    def empty(cls):
        """Create an object with empty values.

        Returns:
            ExamScheduleContainer: ExamScheduleContainer object with empty values
        """
        return cls([])
