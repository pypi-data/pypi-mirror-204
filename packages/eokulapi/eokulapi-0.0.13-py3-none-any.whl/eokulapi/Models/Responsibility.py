"""Module for Responsibility model."""

from dataclasses import dataclass

from eokulapi.Models.EokulDictable import EokulDictable


@dataclass
class Responsibility(EokulDictable):
    """Not implemented Responsibility model."""

    pass

    @classmethod
    def from_dict(cls, obj: dict):
        """Not implemented method to convert a dict to Responsibility object."""
        return cls()

    @classmethod
    def empty(cls):
        """Not implemented method to create Responsibility object with empty values."""
        return cls()
