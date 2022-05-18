from PySide2.QtCore import Signal, QRectF
from PySide2.QtGui import QPainter, QWheelEvent, QResizeEvent
from PySide2.QtWidgets import QGraphicsView, QSizePolicy


class FixedGraphicsView(QGraphicsView):
    # view_changed = Signal(QRectF)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(self.Sunken | self.StyledPanel)
        self.setRenderHint(QPainter.Antialiasing, True)
        self.setInteractive(True)
        self.verticalScrollBar().hide()
        self.horizontalScrollBar().hide()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def wheelEvent(self, e: QWheelEvent) -> None:
        e.accept()

    def get_scene_rect(self) -> QRectF:
        view_rect = self.viewport().rect()
        scene_rect = QRectF(self.mapToScene(view_rect.topLeft()), self.mapToScene(view_rect.bottomRight()))
        return scene_rect

    # def resizeEvent(self, event: QResizeEvent) -> None:
    #     scene_rect = self.get_scene_rect()
    #     self.view_changed.emit(scene_rect)
    #     super().resizeEvent(event)
