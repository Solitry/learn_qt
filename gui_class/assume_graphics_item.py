from PySide2.QtCore import QPointF
from PySide2.QtGui import QColor
from .hexagon_graphics_item import HexagonGraphicsItem
from typing import Optional


class AssumeGraphicsItem(HexagonGraphicsItem):
    def __init__(self, name: str, radius: float, pos: QPointF = QPointF(0, 0), text: Optional[str] = None, parent=None):
        super().__init__(
            name=name,
            radius=radius,
            status_list=[
                (QColor("#99FF3333"), QColor("#99FF9999"), text),
                (QColor("#99FF3333"), QColor("#99FF3333"), text),
            ],
            pos=pos,
            init_status=0,
            parent=parent,
        )
