"""
This module defines a common exception type.
"""


class BasicIOError(RuntimeError):
    """
    Exceptions raised by this module are all of this type.
    """
    pass


__all__ = ['BasicIOError']