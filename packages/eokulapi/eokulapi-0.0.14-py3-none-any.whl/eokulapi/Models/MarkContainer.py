"""Module for MarkContainer model."""

from dataclasses import dataclass

from eokulapi.Models import from_list
from eokulapi.Models.EokulDictable import EokulDictable
from eokulapi.Models.MarkLesson import MarkLesson


@dataclass
class MarkContainer(EokulDictable):
    """Mark container model."""

    avg: dict[int, float]
    """Average mark of the student.

    Key is the semester number and value is the average mark of the semester."""

    data: list[MarkLesson]
    """Mark data as list of MarkLesson objects"""

    @classmethod
    def from_dict(cls, obj: dict):
        """Convert a dict to MarkContainer object.

        Args:
            obj (dict): Object to be converted

        Returns:
            MarkContainer: MarkContainer object that is converted from dict
        """
        from itertools import groupby

        liste = from_list(MarkLesson.from_dict, obj.get("notListesi"))

        by_term = groupby(liste, lambda x: x.term)

        ort = {}

        for term, lessons in by_term:
            lessons = list(lessons)
            ort[term] = sum(
                [lesson.lesson_weekly_period * lesson.score for lesson in lessons]
            ) / sum([lesson.lesson_weekly_period for lesson in lessons])

        return cls(ort, liste)

    @classmethod
    def empty(cls):
        """Create an object with empty values.

        Returns:
            MarkContainer: MarkContainer object with empty values
        """
        return cls(None, [])
