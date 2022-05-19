from PySide2.QtCore import QPointF
from PySide2.QtGui import QColor
from .hexagon_graphics_item import HexagonGraphicsItem


class ConnectGraphicsItem(HexagonGraphicsItem):
    def __init__(self, name: str, radius: float, pos: QPointF = QPointF(0, 0), parent=None):
        super().__init__(
            name=name,
            radius=radius * 0.9,
            status_list=[
                (QColor("#99E0E0E0"), QColor("#99E0E0E0"), None),
            ],
            pos=pos,
            init_status=0,
            parent=parent,
        )
