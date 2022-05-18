from PySide2.QtCore import Qt, Signal, QRectF, QPointF
from PySide2.QtWidgets import QWidget, QHBoxLayout, QGraphicsScene, QGraphicsRectItem, QGraphicsItem
from PySide2.QtGui import QPen, QBrush, QColor

from typing import List, Union, Tuple, Optional, Any, Dict
from dataclasses import dataclass, field
import math

from gui_class.fixed_graphics_view import FixedGraphicsView

from gui_class.ack_graphics_item import AckGraphicsItem
from gui_class.assume_graphics_item import AssumeGraphicsItem
from gui_class.connect_graphics_item import ConnectGraphicsItem
from gui_class.reason_graphics_item import ReasonGraphicsItem

from gui_class.clue_graphics_item import ClueGraphicsItem

from data_class.text_stage import TextStage
from data_class.infer_stage import InferStage, AsmTile, AckTile, ReasonTile, ConnTile
from data_class.records import TextMemo, InferMemo


class ChessBoard(QGraphicsRectItem):
    def __init__(self, parent=None):
        super().__init__(QRectF(QPointF(-1000, -1000), QPointF(1000, 1000)), parent)

        self.setFlags(QGraphicsItem.ItemIsMovable)
        self.setZValue(0)

        self.setPen(Qt.NoPen)  # transparent
        self.setBrush(Qt.NoBrush)  # transparent

    def add_tile(self, item: QGraphicsItem):
        item.setParentItem(self)


class DashMask(QGraphicsRectItem):
    def __init__(self, parent=None):
        super().__init__(QRectF(QPointF(200, -1000), QPointF(1000, 1000)), parent)

        self.setZValue(3)

        self.setPen(Qt.NoPen)
        self.setBrush(QBrush(QColor("#0F000000")))


@dataclass
class ClueData:
    name: str
    used: bool = False
    graphics_item: Optional[ClueGraphicsItem] = None


AllTilesGraphicsItem = Union[AckGraphicsItem, AssumeGraphicsItem, ConnectGraphicsItem, ReasonGraphicsItem]


@dataclass
class TileData:
    name: str
    show: bool = False
    light: bool = False
    graphics_item: Optional[AllTilesGraphicsItem] = None
    extra: Dict[str, Any] = field(default_factory=dict)


class InferWidget(QWidget):
    go_next = Signal(str)

    Origin = QPointF(-300, 0)
    TileAxisA = QPointF(0, -math.sqrt(3))
    TileAxisB = QPointF(1.5, -0.5 * math.sqrt(3))

    def __init__(self, parent=None):
        super().__init__(parent)

        self.radius = 40

        # UI
        self.main_scene = QGraphicsScene(self)
        self.main_scene.setSceneRect(QRectF(QPointF(-1000, -1000), QPointF(1000, 1000)))

        self.main_canvas = FixedGraphicsView(self)
        self.main_canvas.setScene(self.main_scene)

        layout = QHBoxLayout(self)
        layout.addWidget(self.main_canvas, 1)

        self.chess_board = ChessBoard()
        self.main_scene.addItem(self.chess_board)

        dash_mask = DashMask()
        self.main_scene.addItem(dash_mask)

        # data
        self.tiles = {}  # type: Dict[str, TileData]
        self.clues = {}  # type: Dict[str, ClueData]

        self.current_memo = None  # type: Optional[InferMemo]

        # debug
        # self.chess_board.add_tile(ReasonGraphicsItem(radius=40, pos=QPointF(100, 100)))
        # self.chess_board.add_tile(AssumeGraphicsItem(radius=40, pos=QPointF(-100, -100)))
        
        self.clues2 = [
            ClueGraphicsItem(radius=40, pos=QPointF(200, 200)),
        ]
        
        self.add_clue(self.clues2[0])

    def add_clue(self, clue: ClueGraphicsItem):
        self.main_scene.addItem(clue)
        clue.delegate.drop.connect(self.clue_drop)

    def clue_drop(self, scene_pos: QPointF):
        for item in self.main_scene.items(scene_pos):
            if isinstance(item, ReasonGraphicsItem):
                item.enter_status(1)

    def reload(self, stage_info_list: List[Union[Tuple[TextStage, TextMemo], Tuple[InferStage, InferMemo]]]):
        # clear tiles
        for key, item in self.tiles.items():
            self.main_scene.removeItem(item.graphics_item)
        self.tiles.clear()

        # clear clues
        for key, item in self.clues.items():
            self.main_scene.removeItem(item.graphics_item)
        self.clues.clear()

        # load tiles
        current_infer_stage, self.current_memo = stage_info_list[-1]  # type: InferStage, InferMemo

        for name, tile in current_infer_stage.tiles.items():
            tile_data = TileData(name)
            pos = self._get_hexagon_pos(tile.pos.a, tile.pos.b)
            if isinstance(tile, AsmTile):
                tile_data.graphics_item = AssumeGraphicsItem(radius=self.radius, pos=pos)
            elif isinstance(tile, AckTile):
                tile_data.graphics_item = AckGraphicsItem(radius=self.radius, pos=pos)
            elif isinstance(tile, ReasonTile):
                tile_data.graphics_item = ReasonGraphicsItem(radius=self.radius, pos=pos)
            elif isinstance(tile, ConnTile):
                tile_data.graphics_item = ConnectGraphicsItem(radius=self.radius, pos=pos)
            else:
                raise NotImplementedError("Not support tile type")
            self.chess_board.add_tile(tile_data.graphics_item)

    def _get_hexagon_pos(self, a, b) -> QPointF:
        return self.Origin + self.TileAxisA * (self.radius * a) + self.TileAxisB * (self.radius * b)

    def _load_clues(self):
        pass
