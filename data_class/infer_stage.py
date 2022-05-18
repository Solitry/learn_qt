from dataclasses import dataclass, field
from typing import List, Dict, Optional
import toml


@dataclass
class Pos:
    a: int = 0
    b: int = 0


@dataclass
class Tile:
    name: Optional[str] = None
    pos: Pos = field(default_factory=Pos)


# @dataclass
# class AsmTile(Tile):
#     text: Optional[str] = None
#     explain: Optional[str] = None
#     show_rely: List["AsmTile"] = field(default_factory=list)  # show when ANY light-up
#     light_rely: List["ReasonTile"] = field(default_factory=list)  # light-up when ALL light-up
#
#
# @dataclass
# class AckTile(Tile):
#     next_stage: Optional[str] = None
#     show_rely: List[AsmTile] = field(default_factory=list)  # show when ANY light-up
#
#
# @dataclass
# class ReasonTile(Tile):
#     clue: Optional[str] = None  # light-up when clue accepted
#     show_rely: List[AsmTile] = field(default_factory=list)  # show when ANY show
#
#
# @dataclass
# class ConnTile(Tile):
#     show_rely: List[AsmTile] = field(default_factory=list)  # show when ANY light-up


@dataclass
class AsmTile(Tile):
    text: Optional[str] = None
    explain: Optional[str] = None
    show_rely: List[str] = field(default_factory=list)  # show when ANY AsmTile light-up
    light_rely: List[str] = field(default_factory=list)  # light-up when ALL ReasonTile light-up


@dataclass
class AckTile(Tile):
    next_stage: Optional[str] = None
    show_rely: List[str] = field(default_factory=list)  # show when ANY AsmTile light-up


@dataclass
class ReasonTile(Tile):
    clue: Optional[str] = None  # light-up when clue accepted
    show_rely: List[str] = field(default_factory=list)  # show when ANY AsmTile show


@dataclass
class ConnTile(Tile):
    show_rely: List[str] = field(default_factory=list)  # show when ANY AsmTile light-up


@dataclass
class InferStage:
    name: str
    tiles: Dict[str, Tile] = field(default_factory=dict)

    def load_from_file(self, path: str) -> None:
        with open(path, "r", encoding='utf8') as f:
            data = toml.load(f)

        for item in data["AsmTile"]:
            tile = AsmTile()
            tile.name = item["name"]
            tile.pos.a = item["pos"][0]
            tile.pos.b = item["pos"][1]
            tile.text = item["text"]
            tile.explain = item["explain"]
            tile.show_rely = sorted(item["show_rely"])
            tile.light_rely = sorted(item["light_rely"])
            self.tiles[tile.name] = tile

        for item in data["AckTile"]:
            tile = AckTile()
            tile.name = item["name"]
            tile.pos.a = item["pos"][0]
            tile.pos.b = item["pos"][1]
            tile.next_stage = item["next_stage"]
            tile.show_rely = sorted(item["show_rely"])
            self.tiles[tile.name] = tile

        for item in data["ReasonTile"]:
            tile = ReasonTile()
            tile.name = item["name"]
            tile.pos.a = item["pos"][0]
            tile.pos.b = item["pos"][1]
            tile.clue = item["clue"]
            tile.show_rely = sorted(item["show_rely"])
            self.tiles[tile.name] = tile

        for item in data["ConnTile"]:
            tile = ConnTile()
            tile.name = item["name"]
            tile.pos.a = item["pos"][0]
            tile.pos.b = item["pos"][1]
            tile.show_rely = sorted(item["show_rely"])
            self.tiles[tile.name] = tile


if __name__ == '__main__':
    infer_stage = InferStage("test_infer_state")
    infer_stage.load_from_file("../resources/1-4.toml")
    print(infer_stage)
