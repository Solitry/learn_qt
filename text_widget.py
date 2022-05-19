from PySide2.QtCore import Signal
from PySide2.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QHBoxLayout, QPushButton, QLayout
from PySide2.QtGui import QColor, QPalette

from data_class.text_stage import TextStage


def clear_layout(layout: QLayout):
    while layout.count():
        item = layout.itemAt(0)
        if item.widget() is not None:
            item.widget().deleteLater()
        if item.layout() is not None:
            clear_layout(item.layout())
        layout.removeItem(item)


class TextWidget(QWidget):
    go_prev = Signal()
    go_next = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.show_text = QTextEdit(self)
        self.show_text.setReadOnly(True)

        self.btn_layout = QHBoxLayout()

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.show_text, 1)
        self.main_layout.addLayout(self.btn_layout, 0)

    def reload(self, text_stage: TextStage, can_back: bool) -> None:
        self.show_text.setMarkdown(text_stage.text or "")

        p = QPalette()
        p.setColor(QPalette.Base, QColor(text_stage.config["background_color"]))
        self.show_text.setPalette(p)

        clear_layout(self.btn_layout)

        self.btn_layout.addSpacing(20)

        prev_btn = QPushButton("<-", self)
        prev_btn.clicked.connect(lambda: self.go_prev.emit())
        if not can_back:
            prev_btn.hide()
        self.btn_layout.addWidget(prev_btn, 0)

        self.btn_layout.addSpacing(20)
        self.btn_layout.addStretch(1)

        for name, go_where in text_stage.nexts:
            def gen(val):
                def func():
                    self.go_next.emit(val)
                return func

            btn = QPushButton(name, self)
            btn.clicked.connect(gen(go_where))
            self.btn_layout.addWidget(btn, 0)
            self.btn_layout.addSpacing(10)

        self.btn_layout.addSpacing(10)
