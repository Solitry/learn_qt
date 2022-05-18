from PySide2.QtWidgets import QWidget, QStackedLayout

from text_widget import TextWidget
from infer_widget import InferWidget

from data_class.text_stage import TextStage
from data_class.infer_stage import InferStage
from data_class.stage_pool import StagePool
from data_class.records import Records, TextMemo, InferMemo


class ScreenWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.text_widget = TextWidget(self)
        self.text_widget.go_prev.connect(self.switch_previous_stage)
        self.text_widget.go_next.connect(self.switch_stage)

        self.infer_widget = InferWidget(self)
        self.infer_widget.go_next.connect(self.switch_stage)

        self.layout = QStackedLayout(self)
        self.layout.addWidget(self.text_widget)
        self.layout.addWidget(self.infer_widget)

        self.stage_pool = StagePool()
        self.stage_pool.load_from_file("./resources")

        self.records = Records()
        self.switch_stage("1-1")

        # # if load from stored records
        # current_stage = self.records.history_stages.pop()
        # self.switch_stage(current_stage)

        # TODO: for debug
        self.layout.setCurrentWidget(self.infer_widget)

    def switch_stage(self, stage_name):
        stage = self.stage_pool.stages[stage_name]
        self.records.history_stages.append(stage_name)

        if isinstance(stage, TextStage):
            if stage_name not in self.records:
                self.records.memo[stage_name] = TextMemo()
            self.text_widget.reload(text_stage=stage, has_history=len(self.records.history_stages) > 1)
            self.layout.setCurrentWidget(self.text_widget)
        elif isinstance(stage, InferStage):
            if stage_name not in self.records:
                self.records.memo[stage_name] = InferMemo()
            # TODO: load
            self.layout.setCurrentWidget(self.infer_widget)
        else:
            raise NotImplementedError("Unknown stage type")

    def switch_previous_stage(self):
        self.records.history_stages.pop()
        prev_stage = self.records.history_stages.pop()
        self.switch_stage(prev_stage)
