from PySide2.QtCore import Signal, QRectF, QPointF
from PySide2.QtWidgets import QWidget, QHBoxLayout, QGraphicsScene, QGraphicsRectItem, QGraphicsItem
from PySide2.QtGui import QPen, QBrush, QColor

from typing import List, Union, Tuple

from gui_class.fixed_graphics_view import FixedGraphicsView
from gui_class.reason_graphics_item import ReasonGraphicsItem
from gui_class.clue_graphics_item import ClueGraphicsItem
from gui_class.assume_graphics_item import AssumeGraphicsItem

from data_class.text_stage import TextStage
from data_class.infer_stage import InferStage
from data_class.records import TextMemo, InferMemo


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


class InferWidget(QWidget):
    go_next = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.main_scene = QGraphicsScene(self)
        self.main_scene.setSceneRect(QRectF(QPointF(-1000, -1000), QPointF(1000, 1000)))

        self.main_canvas = FixedGraphicsView(self)
        self.main_canvas.setScene(self.main_scene)

        layout = QHBoxLayout(self)
        layout.addWidget(self.main_canvas, 1)

        self.chess_board = ChessBoard()
        self.main_scene.addItem(self.chess_board)

        # self.tiles = {}
        # self.clues = {}

        self.chess_board.add_tile(ReasonGraphicsItem(radius=40, pos=QPointF(100, 100)))
        self.chess_board.add_tile(AssumeGraphicsItem(radius=40, pos=QPointF(-100, -100)))

        self.clues = [
            ClueGraphicsItem(radius=40, pos=QPointF(200, 200)),
        ]

        self.add_clue(self.clues[0])

    def add_clue(self, clue: ClueGraphicsItem):
        self.main_scene.addItem(clue)
        clue.delegate.drop.connect(self.clue_drop)

    def clue_drop(self, scene_pos: QPointF):
        for item in self.main_scene.items(scene_pos):
            if isinstance(item, ReasonGraphicsItem):
                item.enter_status(1)

    def reload(self, stage_info_list: List[Union[Tuple[TextStage, TextMemo], Tuple[InferStage, InferMemo]]]):
        self._clear_tiles()
        self._clear_clues()

    def _clear_tiles(self):
        pass

    def _clear_clues(self):
        pass

    def _load_tiles(self, infer_stage: InferStage, infer_memo: InferMemo):
        pass

    def _load_clues(self):
        pass
