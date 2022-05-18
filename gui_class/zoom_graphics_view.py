from PySide2.QtCore import QEvent, Qt
from PySide2.QtGui import QPainter, QTransform, QWheelEvent, QMouseEvent
from PySide2.QtWidgets import QGraphicsView, QSizePolicy, QGraphicsSceneDragDropEvent


class ZoomGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(self.Sunken | self.StyledPanel)
        self.setRenderHint(QPainter.Antialiasing, True)
        self.setInteractive(True)
        self.setOptimizationFlag(QGraphicsView.DontSavePainterState)
        self.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.verticalScrollBar().hide()
        self.horizontalScrollBar().hide()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.setDragMode(QGraphicsView.RubberBandDrag)

        # self.setAcceptDrops(True)

        self.zoom_value = 100
        self.setup_matrix()

    def get_scale(self):
        return 2. ** ((self.zoom_value - 100.) / 50.)

    def setup_matrix(self):
        scale = self.get_scale()

        matrix = QTransform()
        matrix.scale(scale, scale)

        self.setTransform(matrix)

    def wheelEvent(self, e: QWheelEvent) -> None:
        if e.angleDelta().y() > 0:
            self.zoom_value += 6
        else:
            self.zoom_value -= 6
        self.setup_matrix()
        e.accept()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MiddleButton:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            press_event = QMouseEvent(QEvent.GraphicsSceneMousePress,
                                      event.pos(), Qt.LeftButton,
                                      Qt.LeftButton, Qt.NoModifier)
            press_event.setModifiers(Qt.AltModifier)
            super().mousePressEvent(press_event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MiddleButton:
            self.setDragMode(QGraphicsView.NoDrag)
            release_event = QMouseEvent(QEvent.GraphicsSceneMouseRelease,
                                        event.pos(), Qt.LeftButton,
                                        Qt.LeftButton, Qt.NoModifier)
            self.setCursor(Qt.ArrowCursor)
            super().mouseReleaseEvent(release_event)
            self.setDragMode(QGraphicsView.RubberBandDrag)
        else:
            super().mouseReleaseEvent(event)
