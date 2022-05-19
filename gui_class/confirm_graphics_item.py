from PySide2.QtCore import Qt, QPointF, QObject, Signal
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QGraphicsItem, QGraphicsSceneMouseEvent
from typing import Optional

from .hexagon_graphics_item import HexagonGraphicsItem


class ConfirmSignalDelegate(QObject):
    drop = Signal(QPointF)


class ConfirmGraphicsItem(HexagonGraphicsItem):
    def __init__(self, name: str, radius: float, pos: QPointF = QPointF(0, 0), text: Optional[str] = None, parent=None):
        super().__init__(
            name=name,
            radius=radius,
            status_list=[
                (QColor("#EE990099"), QColor("#EE990099"), text),
                (QColor("#EE990099"), QColor("#99990099"), text),
            ],
            pos=pos,
            init_status=0,
            parent=parent,
        )

        self.init_pos = pos

        self.setFlags(QGraphicsItem.ItemIsMovable)
        self.setZValue(4)

        self.delegate = ConfirmSignalDelegate()

    def set_init_pos(self, pos: QPointF):
        self.setPos(pos)
        self.init_pos = pos

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.enter_status(1)
            event.accept()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.setPos(self.init_pos)
            self.enter_status(0)
            self.delegate.drop.emit(event.scenePos())
        super().mouseReleaseEvent(event)
