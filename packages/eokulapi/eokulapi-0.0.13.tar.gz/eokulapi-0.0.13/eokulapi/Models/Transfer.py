"""Module for Transfer model."""

from dataclasses import dataclass

from eokulapi.Models.EokulDictable import EokulDictable


@dataclass
class Transfer(EokulDictable):
    """not implemented Transfer model."""

    pass

    @classmethod
    def from_dict(cls, obj: dict):
        """Not implemented method to convert a dict to Transfer object."""
        return cls()

    @classmethod
    def empty(cls):
        """Not implemented method to create Transfer object with empty values."""
        return cls()
