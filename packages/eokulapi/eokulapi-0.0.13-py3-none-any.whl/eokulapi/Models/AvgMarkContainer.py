"""Module for AvgMarkContainer model."""

from dataclasses import dataclass

from eokulapi.Models import from_list
from eokulapi.Models.AvgMarkLesson import AvgMarkLesson
from eokulapi.Models.EokulDictable import EokulDictable


@dataclass
class AvgMarkContainer(EokulDictable):
    """Average mark container model."""

    data: list[AvgMarkLesson]
    """Average mark data as list of AvgMarkLesson objects"""

    @classmethod
    def from_dict(cls, obj: dict):
        """Convert a dict to AvgMarkContainer object.

        Args:
            obj (dict): Object to be converted

        Returns:
            AvgMarkContainer: AvgMarkContainer object that is converted from dict
        """
        liste = from_list(AvgMarkLesson.from_dict, obj.get("YaziliOrtalamaListesi"))
        return cls(liste)

    @classmethod
    def empty(cls):
        """Create an object with empty values.

        Returns:
            AvgMarkContainer: AvgMarkContainer object with empty values
        """
        return cls([])
