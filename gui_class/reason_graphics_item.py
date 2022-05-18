from PySide2.QtCore import QPointF, Qt
from PySide2.QtWidgets import QGraphicsSceneMouseEvent
from PySide2.QtGui import QColor

from .hexagon_graphics_item import HexagonGraphicsItem


class ReasonGraphicsItem(HexagonGraphicsItem):
    def __init__(self, radius: float, pos: QPointF = QPointF(0, 0), parent=None):
        super().__init__(
            radius=radius,
            stages=[
                (QColor("#FFE5CC"), QColor("#FFE5CC"), None),
                (QColor("#FF9933"), QColor("#FFCC99"), "test"),
            ],
            pos=pos,
            init_stage=0,
            parent=parent,
        )

        self.setAcceptedMouseButtons(Qt.RightButton)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if event.button() == Qt.RightButton:
            event.accept()
        super().mouseReleaseEvent(event)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if event.button() == Qt.RightButton:
            if self.get_stage() == 1:
                self.enter_stage(0)
            else:
                self.enter_stage(1)
        super().mouseReleaseEvent(event)
