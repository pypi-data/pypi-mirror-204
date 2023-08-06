"""Module for EokulDictable model."""


class EokulDictable:
    """EokulDictable model.

    Provides a method to convert a dict to object and another method to create object with empty values
    """

    @classmethod
    def from_dict(cls, obj: dict):
        """Convert a dict to object.

        Args:
            obj (dict): Object to be converted

        Returns:
            object: Object that is converted from dict
        """
        return cls(**obj)

    @classmethod
    def empty(cls):
        """Create an object with empty values.

        Returns:
            object: Object with empty values
        """
        return cls()
