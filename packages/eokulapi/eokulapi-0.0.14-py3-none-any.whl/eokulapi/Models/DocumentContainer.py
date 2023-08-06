"""Module for DocumentContainer model."""

from dataclasses import dataclass

from eokulapi.Models import from_list
from eokulapi.Models.Document import Document
from eokulapi.Models.EokulDictable import EokulDictable


@dataclass
class DocumentContainer(EokulDictable):
    """Document container model."""

    data: list[Document]
    """Document data as list of Document objects"""

    @classmethod
    def from_dict(cls, obj: dict):
        """Convert a dict to DocumentContainer object.

        Args:
            obj (dict): Object to be converted

        Returns:
            DocumentContainer: DocumentContainer object that is converted from dict
        """
        liste = from_list(Document.from_dict, obj.get("TumBelgeler"))
        return cls(liste)

    @classmethod
    def empty(cls):
        """Create an object with empty values.

        Returns:
            DocumentContainer: DocumentContainer object with empty values
        """
        return cls([])
