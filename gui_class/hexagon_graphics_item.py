from PySide2.QtCore import QPointF, Qt
from PySide2.QtWidgets import QGraphicsPolygonItem, QGraphicsTextItem
from PySide2.QtGui import QPolygonF, QPen, QBrush, QColor
import math
from typing import Optional, List, Tuple


class HexagonGraphicsItem(QGraphicsPolygonItem):
    def __init__(self,
                 radius: float,
                 stages: List[Tuple[QColor, QColor, Optional[str]]],
                 pos: QPointF = QPointF(0, 0),
                 init_stage: int = 0,
                 parent=None
                 ):
        super().__init__(parent)

        self.radius = radius
        self.stages = stages

        polygon = QPolygonF()
        for deg in range(0, 360, 60):
            rad = math.radians(deg)
            polygon.append(QPointF(radius * math.cos(rad), radius * math.sin(rad)))

        self.setPolygon(polygon)
        self.setFillRule(Qt.FillRule.WindingFill)

        self.description = None  # type: Optional[QGraphicsTextItem]

        self.stage = init_stage
        self.enter_stage(init_stage)

        self.setPos(pos)

    def get_stage(self) -> int:
        return self.stage

    def enter_stage(self, stage):
        pen = QPen()
        pen.setColor(self.stages[stage][0])
        pen.setStyle(Qt.SolidLine)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        pen.setWidth(1)
        self.setPen(pen)

        brush = QBrush()
        brush.setColor(self.stages[stage][1])
        brush.setStyle(Qt.SolidPattern)
        self.setBrush(brush)

        if self.description is not None:
            self.description.deleteLater()
            self.description = None

        if self.stages[stage][2] is not None:
            self.description = QGraphicsTextItem(self.stages[stage][2], self)
            self.description.setTextWidth(2 * self.radius)
            self.description.setPos(-self.description.boundingRect().center())

        self.stage = stage
