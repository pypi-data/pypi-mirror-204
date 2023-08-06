"""Module for AdditionalExam model."""

from dataclasses import dataclass

from eokulapi.Models import from_list, from_str
from eokulapi.Models.EokulDictable import EokulDictable


@dataclass
class AdditionalExam(EokulDictable):
    """Additional exam model."""

    name: str | None
    """Name of the additional exam"""

    appeal: list
    """Appeal state of the additional exam"""

    result: list
    """Result of the additional exam"""
    location: list
    """Location of the additional exam"""

    @classmethod
    def from_dict(cls, obj: dict):
        """Convert a dict to AdditionalExam object.

        Args:
            obj (dict): Object to be converted

        Returns:
            AdditionalExam: AdditionalExam object that is converted from dict
        """
        name = from_str(obj.get("SinavAdi"))
        basv = from_list(list, obj.get("sinavBasvuruListesi"))
        sonuc = from_list(list, obj.get("sinavSonucListesi"))
        yer = from_list(list, obj.get("sinavYeriListesi"))
        return cls(name, basv, sonuc, yer)

    @classmethod
    def empty(cls):
        """Create an object with empty values.

        Returns:
            AdditionalExam: AdditionalExam object with empty values
        """
        return cls(None, [], [], [])
