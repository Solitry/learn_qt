from PySide2.QtCore import Qt, Signal, QRectF, QPointF
from PySide2.QtWidgets import QWidget, QHBoxLayout, QGraphicsScene, QGraphicsRectItem, QGraphicsItem, QGraphicsTextItem
from PySide2.QtGui import QBrush, QColor

from typing import List, Union, Tuple, Optional, Any, Dict, cast
from dataclasses import dataclass, field
import math
import collections

from gui_class.fixed_graphics_view import FixedGraphicsView
from gui_class.arrow_graphics_item import ArrowGraphicsItem

from gui_class.ack_graphics_item import AckGraphicsItem
from gui_class.assume_graphics_item import AssumeGraphicsItem
from gui_class.connect_graphics_item import ConnectGraphicsItem
from gui_class.reason_graphics_item import ReasonGraphicsItem

from gui_class.clue_graphics_item import ClueGraphicsItem

from data_class.text_stage import TextStage, Clue
from data_class.infer_stage import InferStage, Tile, AsmTile, AckTile, ReasonTile, ConnTile
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


class TextStageBriefBoard(QGraphicsRectItem):
    def __init__(self, parent=None):
        super().__init__(QRectF(QPointF(300, -250), QPointF(550, -50)), parent)

        self.setZValue(4)

        self.setPen(Qt.NoPen)
        self.setBrush(QBrush(QColor("#FFFFFF")))

        self.text_area = QGraphicsTextItem("", self)
    
    def set_background_color(self, color: QColor):
        self.setBrush(QBrush(color))
    
    def set_text(self, text: str):
        self.text_area.setPlainText(text)
        self.text_area.setTextWidth(200)
        self.text_area.setPos(self.boundingRect().center() - self.text_area.boundingRect().center())


@dataclass
class ClueData:
    clue: Clue
    belong_stage: str
    used: bool = False
    graphics_item: Optional[ClueGraphicsItem] = None


AllTilesGraphicsItem = Union[AckGraphicsItem, AssumeGraphicsItem, ConnectGraphicsItem, ReasonGraphicsItem]


@dataclass
class TileData:
    tile: Tile
    show: bool = False
    light: bool = False
    graphics_item: Optional[AllTilesGraphicsItem] = None
    link_tiles: List[str] = field(default_factory=list)
    extra: Dict[str, Any] = field(default_factory=dict)


class InferWidget(QWidget):
    go_next = Signal(str)

    Origin = QPointF(-300, 0)
    TileAxisA = QPointF(0, -math.sqrt(3))
    TileAxisB = QPointF(1.5, -0.5 * math.sqrt(3))

    CluePos = [
        QPointF(332.000000, 21.000000),
        QPointF(451.000000, 15.000000),
        QPointF(549.000000, 20.000000),
        QPointF(325.000000, 106.000000),
        QPointF(459.000000, 117.000000),
        QPointF(561.000000, 113.000000),
        QPointF(311.000000, 217.000000),
        QPointF(429.000000, 211.000000),
        QPointF(568.000000, 215.000000),

        QPointF(513.000000, 271.000000),
    ]

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

        self.text_stage_brief_board = TextStageBriefBoard()
        self.main_scene.addItem(self.text_stage_brief_board)

        self.left_arrow = ArrowGraphicsItem(20, 180, QPointF(270, -150))
        self.left_arrow.delegate.clicked.connect(lambda: self.switch_text_stage(-1))
        self.main_scene.addItem(self.left_arrow)

        self.right_arrow = ArrowGraphicsItem(20, 0, QPointF(580, -150))
        self.right_arrow.delegate.clicked.connect(lambda: self.switch_text_stage(1))
        self.main_scene.addItem(self.right_arrow)

        # data
        self.tiles = {}  # type: Dict[str, TileData]
        self.clues = {}  # type: Dict[str, ClueData]

        self.current_infer_stage = None  # type: Optional[InferStage]
        self.current_memo = None  # type: Optional[InferMemo]

        self.text_stages = []  # type: List[Tuple[TextStage, TextMemo]]
        self.text_stage_idx = None

        # debug
        # self.chess_board.add_tile(ReasonGraphicsItem(radius=40, pos=QPointF(100, 100)))
        # self.chess_board.add_tile(AssumeGraphicsItem(radius=40, pos=QPointF(-100, -100)))
        
        # self.clues2 = [ClueGraphicsItem(radius=40, pos=QPointF(100, 200))]
        # self.add_clue(self.clues2[0])

    def add_clue(self, clue: ClueGraphicsItem):
        self.main_scene.addItem(clue)
        clue.delegate.drop.connect(self.clue_drop)

    def clue_drop(self, name: str, scene_pos: QPointF):
        # print(scene_pos)
        for item in self.main_scene.items(scene_pos):
            if isinstance(item, ReasonGraphicsItem):
                item.enter_status(1)
        # TODO: drop clue on reason

    def reason_cancel_clue(self, reason_name: str):
        # TODO: cancel clue on reason
        pass

    def switch_text_stage(self, delta: int):
        self.switch_to_target_text_stage(self.text_stage_idx + delta)

    def switch_to_target_text_stage(self, idx: int):
        if idx < 0 or idx >= len(self.text_stages):
            return
        
        if idx == 0:
            self.left_arrow.hide()
        else:
            self.left_arrow.show()
        
        if idx + 1 == len(self.text_stages):
            self.right_arrow.hide()
        else:
            self.right_arrow.show()
        
        stage, memo = self.text_stages[idx]

        # show brief
        self.text_stage_brief_board.set_background_color(QColor(stage.config["background_color"]))
        self.text_stage_brief_board.set_text(stage.brief)

        # hide old clues
        if self.text_stage_idx is not None:
            old_stage, _ = self.text_stages[self.text_stage_idx]
            for clue in old_stage.clues:
                clue_data = self.clues[clue.name]
                clue_data.graphics_item.hide()

        # show clues
        for clue in stage.clues:
            clue_data = self.clues[clue.name]
            if not clue_data.used:
                clue_data.graphics_item.show()

        self.text_stage_idx = idx

    def reload(self, stage_info_list: List[Union[Tuple[TextStage, TextMemo], Tuple[InferStage, InferMemo]]]):
        # clear tiles
        for key, item in self.tiles.items():
            self.main_scene.removeItem(item.graphics_item)
        self.tiles.clear()

        # clear clues
        for key, item in self.clues.items():
            self.main_scene.removeItem(item.graphics_item)
        self.clues.clear()

        # current stage
        self.current_infer_stage, self.current_memo = stage_info_list[-1]  # type: InferStage, InferMemo

        # load clues & text stages
        self.text_stages = []

        for stage, memo in stage_info_list:
            if isinstance(stage, TextStage):
                if stage.name not in self.current_infer_stage.rel_stages:
                    continue
                # clues
                for idx, clue in enumerate(stage.clues):
                    if idx >= 9:
                        raise IndexError("Not support more than 9 clues in 1 stage")
                    clue_data = ClueData(clue, belong_stage=stage.name)
                    clue_data.graphics_item = \
                        ClueGraphicsItem(name=clue.name, radius=self.radius, pos=self.CluePos[idx], text=clue.text)
                    clue_data.graphics_item.hide()
                    self.add_clue(clue_data.graphics_item)
                    self.clues[clue.name] = clue_data
                # text stages
                self.text_stages.append((stage, memo))

        # load tiles
        for name, tile in self.current_infer_stage.tiles.items():
            tile_data = TileData(tile)
            pos = self._get_hexagon_pos(tile.pos.a, tile.pos.b)

            if isinstance(tile, AsmTile):
                tile_data.graphics_item = AssumeGraphicsItem(name=name, radius=self.radius, pos=pos, text=tile.text)

            elif isinstance(tile, AckTile):
                tile_data.graphics_item = AckGraphicsItem(name=name, radius=self.radius, pos=pos)

            elif isinstance(tile, ReasonTile):
                clue = self.clues[tile.clue].clue
                tile_data.graphics_item = ReasonGraphicsItem(name=name, radius=self.radius, pos=pos, text=clue.text)
                tile_data.graphics_item.delegate.right_clicked.connect(self.reason_cancel_clue)

            elif isinstance(tile, ConnTile):
                tile_data.graphics_item = ConnectGraphicsItem(name=name, radius=self.radius, pos=pos)

            else:
                raise NotImplementedError("Not support tile type")

            self.chess_board.add_tile(tile_data.graphics_item)
            self.tiles[name] = tile_data
        
        # set used flag to the clues of the previous infer stages
        for stage, memo in stage_info_list[:-1]:
            if isinstance(stage, InferStage):
                for light_up_reason in memo.light_up_reasons:
                    reason_tile = cast(ReasonTile, stage.tiles[light_up_reason])
                    self.clues[reason_tile.clue].used = True

        # release essential clues in the current stage
        for name, tile in self.current_infer_stage.tiles.items():
            if isinstance(tile, ReasonTile):
                self.clues[tile.clue].used = False

        # set used flag to the clues of the current infer stages
        for light_up_reason in self.current_memo.light_up_reasons:
            reason_tile = cast(ReasonTile, self.current_infer_stage.tiles[light_up_reason])
            self.clues[reason_tile.clue].used = True

        # maintain link tiles
        for name, tile_data in self.tiles.items():
            for sr in tile_data.tile.show_rely:
                self.tiles[sr].link_tiles.append(name)
            if isinstance(tile_data.tile, AsmTile):
                for lr in tile_data.tile.light_rely:
                    self.tiles[lr].link_tiles.append(name)

        # for name, tile_data in self.tiles.items():
        #     print(name, ":")
        #     for link in tile_data.link_tiles:
        #         print("  ", link)

        # light-up reasons & update all tiles status
        for light_up_reason in self.current_memo.light_up_reasons:
            self.tiles[light_up_reason].light = True
        self.update_tiles_status(list(self.tiles))

        # prepare dashboard
        self.switch_to_target_text_stage(len(self.text_stages) - 1)

    def _get_hexagon_pos(self, a, b) -> QPointF:
        return self.Origin + self.TileAxisA * (self.radius * a) + self.TileAxisB * (self.radius * b)

    def update_tiles_status(self, changed_tiles):
        q = collections.deque(changed_tiles)

        while len(q) > 0:
            tile_data = self.tiles[q[0]]
            # print(tile_data.tile.name, ":", tile_data.show, tile_data.light)

            if isinstance(tile_data.tile, AsmTile):
                modified = self._update_asm_tile_status(tile_data)
            elif isinstance(tile_data.tile, AckTile):
                modified = self._update_ack_tile_status(tile_data)
            elif isinstance(tile_data.tile, ReasonTile):
                modified = self._update_reason_tile_status(tile_data)
            elif isinstance(tile_data.tile, ConnTile):
                modified = self._update_conn_tile_status(tile_data)
            else:
                raise NotImplementedError("Not support tile type")

            if modified:
                # print(" modify", tile_data.show, tile_data.light)
                for link_tile in tile_data.link_tiles:
                    if q.count(link_tile) == 0:
                        q.append(link_tile)

                # update graphics
                if tile_data.show:
                    tile_data.graphics_item.show()
                else:
                    tile_data.graphics_item.hide()

                if tile_data.light:
                    tile_data.graphics_item.enter_status(1)
                else:
                    tile_data.graphics_item.enter_status(0)

            q.popleft()

    def _update_asm_tile_status(self, tile_data: TileData) -> bool:
        tile = cast(AsmTile, tile_data.tile)
        new_show = len(tile.show_rely) == 0 or any([self.tiles[sr].light for sr in tile.show_rely])
        new_light = all([self.tiles[lr].light for lr in tile.light_rely])

        modified = new_show != tile_data.show or new_light != tile_data.light

        tile_data.show = new_show
        tile_data.light = new_light

        return modified

    def _update_ack_tile_status(self, tile_data: TileData) -> bool:
        tile = cast(AckTile, tile_data.tile)
        new_show = len(tile.show_rely) == 0 or any([self.tiles[sr].light for sr in tile.show_rely])

        modified = new_show != tile_data.show

        tile_data.show = new_show

        return modified

    def _update_reason_tile_status(self, tile_data: TileData) -> bool:
        tile = cast(ReasonTile, tile_data.tile)
        new_show = len(tile.show_rely) == 0 or any([self.tiles[sr].show for sr in tile.show_rely])

        modified = new_show != tile_data.show

        tile_data.show = new_show

        return modified

    def _update_conn_tile_status(self, tile_data: TileData) -> bool:
        tile = cast(ConnTile, tile_data.tile)
        new_show = len(tile.show_rely) == 0 or any([self.tiles[sr].light for sr in tile.show_rely])

        modified = new_show != tile_data.show

        tile_data.show = new_show

        return modified
