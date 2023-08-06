
"""
This file defines messages send to the io_window via pipes.

Do not use directly from the outside - use the global functions in basic_io instead.
"""


class IOMessage(object):
    """
    A message to the sub process (or back) with an instruction what to do (msg_type)
    parameters of how to do it (params)
    """
    def __init__(self, msg_type: str, params: dict):
        self.msg_type: str = msg_type
        self.params: dict = params


__all__ = []