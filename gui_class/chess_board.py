from PySide2.QtCore import QRectF, QPointF
from PySide2.QtWidgets import QGraphicsRectItem, QGraphicsItem
from PySide2.QtGui import QPen, QBrush, QColor


class ChessBoard(QGraphicsRectItem):
    def __init__(self, parent=None):
        super().__init__(QRectF(QPointF(-1000, -1000), QPointF(1000, 1000)), parent)

        self.setFlags(QGraphicsItem.ItemIsMovable)
        self.setZValue(0)

        self.setPen(QPen(QColor("#00000000")))
        self.setBrush(QBrush(QColor("#00000000")))

    def add_tile(self, item: QGraphicsItem):
        item.setParentItem(self)
        item.setZValue(1)
