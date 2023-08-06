"""
This is a simple qt helper file.

Do not use directly from the outside
"""

from typing import Optional

from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QMouseEvent


class MyLabel(QLabel):
    def __init__(self, parent: Optional[QWidget]):
        super().__init__(parent)
        self.mouse_x: int = 0
        self.mouse_y: int = 0

    def mouseMoveEvent(self, ev: QMouseEvent) -> None:
        super().mouseMoveEvent(ev)
        if ev.isAccepted():
            return
        self.mouse_x = ev.x()
        self.mouse_y = ev.y()

        ev.setAccepted(True)


__all__ = []