from PySide2.QtCore import Qt, QPointF, QObject, Signal
from PySide2.QtGui import QColor, QPolygonF, QPen, QBrush
from PySide2.QtWidgets import QGraphicsPolygonItem, QGraphicsTextItem, QGraphicsItem, QGraphicsSceneMouseEvent
import math


class ArrowSignalDelegate(QObject):
    clicked = Signal()


class ArrowGraphicsItem(QGraphicsPolygonItem):
    def __init__(self, radius: float, toward_angle: float, pos: QPointF = QPointF(0, 0), parent=None):
        super().__init__(parent)

        polygon = QPolygonF()
        for deg in range(0, 360, 120):
            rad = math.radians(deg + toward_angle)
            polygon.append(QPointF(radius * math.cos(rad), radius * math.sin(rad)))

        self.setPolygon(polygon)
        self.setFillRule(Qt.FillRule.WindingFill)

        self.setPen(Qt.NoPen)

        brush = QBrush()
        brush.setColor(QColor("#8470FF"))
        brush.setStyle(Qt.SolidPattern)
        self.setBrush(brush)

        self.setPos(pos)

        self.setZValue(4)

        self.delegate = ArrowSignalDelegate()

        self.setAcceptedMouseButtons(Qt.LeftButton)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            event.accept()
        # super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.delegate.clicked.emit()
        super().mouseReleaseEvent(event)
