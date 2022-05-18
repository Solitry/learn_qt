from PySide2.QtCore import QPointF
from PySide2.QtGui import QColor
from .hexagon_graphics_item import HexagonGraphicsItem


class AckGraphicsItem(HexagonGraphicsItem):
    def __init__(self, radius: float, pos: QPointF = QPointF(0, 0), parent=None):
        super().__init__(
            radius=radius,
            status_list=[
                (QColor("#99A020F0"), QColor("#99A020F0"), None),
                (QColor("#999400D3"), QColor("#999400D3"), None),
            ],
            pos=pos,
            init_status=0,
            parent=parent,
        )
