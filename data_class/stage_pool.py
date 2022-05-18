import os

from .text_stage import TextStage
from .infer_stage import InferStage


class StagePool(object):
    def __init__(self):
        self.stages = {}

    def load_from_file(self, path):
        for item in os.listdir(path):
            base, ext = os.path.splitext(item)
            if ext == ".md":
                text_stage = TextStage(base)
                text_stage.load_from_file(os.path.join(path, item))
                self.stages[base] = text_stage
            elif ext == ".toml":
                infer_stage = InferStage(base)
                infer_stage.load_from_file(os.path.join(path, item))
                self.stages[base] = infer_stage
            else:
                assert "Not support ext"
