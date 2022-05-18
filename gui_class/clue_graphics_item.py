from PySide2.QtCore import Qt, QPointF, QObject, Signal
from PySide2.QtGui import QColor, QPolygonF, QPen, QBrush
from PySide2.QtWidgets import QGraphicsPolygonItem, QGraphicsTextItem, QGraphicsItem, QGraphicsSceneMouseEvent
from typing import Optional
import math

from .hexagon_graphics_item import HexagonGraphicsItem


class ClueSignalDelegate(QObject):
    drop = Signal(QPointF)


class ClueGraphicsItem(HexagonGraphicsItem):
    def __init__(self, radius: float, pos: QPointF = QPointF(0, 0), text: Optional[str] = None, parent=None):
        super().__init__(
            radius=radius,
            status_list=[
                (QColor("#EEFFCC99"), QColor("#EEFFCC99"), text),
                (QColor("#EEFFCC99"), QColor("#99FFCC99"), text),
            ],
            pos=pos,
            init_status=0,
            parent=parent,
        )

        self.init_pos = pos

        self.setFlags(QGraphicsItem.ItemIsMovable)
        self.setZValue(4)

        self.delegate = ClueSignalDelegate()

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
