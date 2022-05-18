from PySide2.QtCore import QPointF
from PySide2.QtGui import QColor
from .hexagon_graphics_item import HexagonGraphicsItem


class AssumeGraphicsItem(HexagonGraphicsItem):
    def __init__(self, radius: float, pos: QPointF = QPointF(0, 0), parent=None):
        super().__init__(
            radius=radius,
            status_list=[
                (QColor("#99FF3333"), QColor("#99FF9999"), "中文测试这是一个长字符串啊啊啊啊啊啊"),
                (QColor("#99FF3333"), QColor("#99FF9999"), "中文测试这是一个长字符串啊啊啊啊啊啊"),
            ],
            pos=pos,
            init_status=0,
            parent=parent,
        )
