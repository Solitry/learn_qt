from PySide2.QtCore import QPointF
from PySide2.QtGui import QColor
from .hexagon_graphics_item import HexagonGraphicsItem


class AssumeGraphicsItem(HexagonGraphicsItem):
    def __init__(self, radius: float, pos: QPointF = QPointF(0, 0), parent=None):
        super().__init__(
            radius=radius,
            stages=[
                (QColor("#FF3333"), QColor("#FF9999"), "中文测试这是一个长字符串啊啊啊啊啊啊"),
                (QColor("#FF3333"), QColor("#FF9999"), "中文测试这是一个长字符串啊啊啊啊啊啊"),
            ],
            pos=pos,
            init_stage=0,
            parent=parent,
        )
