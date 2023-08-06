"""Module for LessonSchedule model."""

from dataclasses import dataclass

from eokulapi.Models import from_list
from eokulapi.Models.EokulDictable import EokulDictable
from eokulapi.Models.LessonDay import LessonDay


@dataclass
class LessonSchedule(EokulDictable):
    """Lesson schedule model."""

    data: list[LessonDay]
    """Lesson schedule data as list of LessonDay objects"""

    @classmethod
    def from_dict(cls, obj: dict):
        """Convert a dict to LessonSchedule object.

        Args:
            obj (dict): Object to be converted

        Returns:
            LessonSchedule: LessonSchedule object that is converted from dict
        """
        liste = from_list(LessonDay.from_dict, obj.get("DersProgramiListesi"))
        return cls(liste)

    @classmethod
    def empty(cls):
        """Create an object with empty values.

        Returns:
            LessonSchedule: LessonSchedule object with empty values
        """
        return cls([])
