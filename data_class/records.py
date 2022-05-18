from dataclasses import dataclass, field
from typing import List, Dict, Union


@dataclass
class TextMemo:
    def to_pure_obj(self) -> dict:
        return {
            "type": self.__class__.__name__,
        }

    @staticmethod
    def from_pure_obj(val: dict) -> "TextMemo":
        return TextMemo()


@dataclass
class InferMemo:
    light_up_reasons: List[str] = field(default_factory=list)

    def to_pure_obj(self) -> dict:
        return {
            "type": self.__class__.__name__,
            "light_up_reasons": self.light_up_reasons,
        }

    @staticmethod
    def from_pure_obj(val: dict) -> "InferMemo":
        ret = InferMemo()
        ret.light_up_reasons = val["light_up_reasons"]
        return ret


@dataclass
class Records:
    history_stages: List[str] = field(default_factory=list)
    memo: Dict[str, Union[TextMemo, InferMemo]] = field(default_factory=dict)

    def to_pure_obj(self) -> dict:
        return {
            "history_stages": self.history_stages,
            "memo": {
                key: item.to_pure_obj()
                for key, item in self.memo.items()
            },
        }

    @staticmethod
    def from_pure_obj(val: dict) -> "Records":
        ret = Records()
        ret.history_stages = val["history_stages"]
        ret.memo = {}
        for key, val in val["memo"].items():
            item = TextMemo.from_pure_obj(val) if val["type"] == TextMemo.__name__ else InferMemo.from_pure_obj(val)
            ret.memo[key] = item
        return ret


if __name__ == '__main__':
    records = Records()

    records.history_stages.append("1-1")
    records.history_stages.append("1-2")
    records.history_stages.append("1-3")
    records.history_stages.append("1-4")

    records.memo["1-1"] = TextMemo()
    records.memo["1-2"] = TextMemo()
    records.memo["1-3"] = TextMemo()

    records.memo["1-4"] = InferMemo()
    records.memo["1-4"].light_up_reasons.append("1-1:1")

    dump_obj = records.to_pure_obj()
    print(dump_obj)
    load_record = Records.from_pure_obj(dump_obj)
    print(load_record)
