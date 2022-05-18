from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Dict


@dataclass
class Clue:
    name: str
    text: str


@dataclass
class TextStage:
    name: str
    brief: Optional[str] = None
    text: Optional[str] = None
    clues: List[Clue] = field(default_factory=list)
    nexts: List[Tuple[str, str]] = field(default_factory=list)
    config: Dict[str, str] = field(default_factory=dict)

    def load_from_file(self, path: str) -> None:
        with open(path, "r", encoding='utf8') as f:
            content = f.read()

        parts = content.split("---")
        assert len(parts) == 5

        self.text = parts[0].strip() + "\n"
        self.brief = parts[1].strip() + "\n"
        self._load_clue(parts[2])
        self._load_next(parts[3])
        self._load_config(parts[4])

    def _load_clue(self, raw):
        for raw_line in raw.split("\n"):
            line = raw_line.strip()
            p = line.find(".")
            if p == -1:
                continue
            name = self.name + ":" + line[:p].strip()
            text = line[p + 1:].strip()
            self.clues.append(Clue(name, text))

    def _load_next(self, raw):
        for raw_line in raw.split("\n"):
            line = raw_line.strip()
            p = line.find(":")
            if p == -1:
                continue
            key = line[:p].strip()
            val = line[p + 1:].strip()
            self.nexts.append((key, val))

    def _load_config(self, raw):
        for raw_line in raw.split("\n"):
            line = raw_line.strip()
            p = line.find(":")
            if p == -1:
                continue
            key = line[:p].strip()
            val = line[p + 1:].strip()
            self.config[key] = val


if __name__ == "__main__":
    for name in ["1-1", "1-2", "1-3"]:
        tmp = TextStage(name)
        tmp.load_from_file(f"../resources/{name}.md")
        print(tmp)
