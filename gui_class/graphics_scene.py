from PySide2.QtCore import Signal, QPointF
from PySide2.QtWidgets import QGraphicsScene, QGraphicsSceneMouseEvent


class GraphicsScene(QGraphicsScene):
    mouse_moved_signal = Signal(QPointF)
    mouse_release_signal = Signal()

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        super().mouseMoveEvent(event)
        self.mouse_moved_signal.emit(event.scenePos())

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent):
        super().mouseReleaseEvent(event)
        self.mouse_release_signal.emit()
