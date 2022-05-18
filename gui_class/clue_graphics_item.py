from PySide2.QtCore import Qt, QPointF, QObject, Signal
from PySide2.QtGui import QColor, QPolygonF, QPen, QBrush
from PySide2.QtWidgets import QGraphicsPolygonItem, QGraphicsTextItem, QGraphicsItem, QGraphicsSceneMouseEvent
import math


class ClueSignalDelegate(QObject):
    drop = Signal(QPointF)


class ClueGraphicsItem(QGraphicsPolygonItem):
    def __init__(self, radius: float, pos: QPointF = QPointF(0, 0), parent=None):
        super().__init__(parent)

        polygon = QPolygonF()
        for deg in range(0, 360, 60):
            rad = math.radians(deg)
            polygon.append(QPointF(radius * math.cos(rad), radius * math.sin(rad)))

        self.setPolygon(polygon)
        self.setFillRule(Qt.FillRule.WindingFill)

        pen = QPen()
        pen.setColor(QColor("#FFCC99"))
        pen.setStyle(Qt.SolidLine)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        pen.setWidth(1)
        self.setPen(pen)

        brush = QBrush()
        brush.setColor(QColor("#FFCC99"))
        brush.setStyle(Qt.SolidPattern)
        self.setBrush(brush)

        self.description = QGraphicsTextItem("中文测试这是一个长字符串啊啊啊啊啊啊", self)
        self.description.setTextWidth(2 * radius)
        self.description.setPos(-self.description.boundingRect().center())

        self.setPos(pos)
        self.init_pos = pos

        self.setFlags(QGraphicsItem.ItemIsMovable)
        self.setZValue(4)

        self.delegate = ClueSignalDelegate()

    def set_init_pos(self, pos: QPointF):
        self.setPos(pos)
        self.init_pos = pos

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.setPos(self.init_pos)
            self.delegate.drop.emit(event.scenePos())
        super().mouseReleaseEvent(event)
