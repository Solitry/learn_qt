from PySide2.QtCore import QPointF, Qt
from PySide2.QtWidgets import QGraphicsSceneMouseEvent
from PySide2.QtGui import QColor
from typing import Optional

from .hexagon_graphics_item import HexagonGraphicsItem


class ReasonGraphicsItem(HexagonGraphicsItem):
    def __init__(self, radius: float, pos: QPointF = QPointF(0, 0), text: Optional[str] = None, parent=None):
        super().__init__(
            radius=radius,
            status_list=[
                (QColor("#99FFE5CC"), QColor("#99FFE5CC"), None),
                (QColor("#99FF9933"), QColor("#99FFCC99"), text),
            ],
            pos=pos,
            init_status=0,
            parent=parent,
        )

        self.setAcceptedMouseButtons(Qt.RightButton)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if event.button() == Qt.RightButton:
            event.accept()
        # super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if event.button() == Qt.RightButton:
            if self.get_status() == 1:
                self.enter_status(0)
            else:
                self.enter_status(1)
        super().mouseReleaseEvent(event)
