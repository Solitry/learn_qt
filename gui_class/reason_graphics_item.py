from PySide2.QtCore import QPointF, Qt
from PySide2.QtWidgets import QGraphicsSceneMouseEvent
from PySide2.QtGui import QColor

from .hexagon_graphics_item import HexagonGraphicsItem


class ReasonGraphicsItem(HexagonGraphicsItem):
    def __init__(self, radius: float, pos: QPointF = QPointF(0, 0), parent=None):
        super().__init__(
            radius=radius,
            status_list=[
                (QColor("#FFE5CC"), QColor("#FFE5CC"), None),
                (QColor("#FF9933"), QColor("#FFCC99"), "test"),
            ],
            pos=pos,
            init_status=0,
            parent=parent,
        )

        self.setAcceptedMouseButtons(Qt.RightButton)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if event.button() == Qt.RightButton:
            event.accept()
        super().mouseReleaseEvent(event)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if event.button() == Qt.RightButton:
            if self.get_status() == 1:
                self.enter_status(0)
            else:
                self.enter_status(1)
        super().mouseReleaseEvent(event)
