#!/usr/bin/env python3.8
import sys
import signal
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication
from qasync import QEventLoop

from screen_widget import ScreenWidget


def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    loop = QEventLoop(app, set_running_loop=False)

    widget = ScreenWidget()
    widget.show()

    def handler(signum, frame):
        loop.close()
        exit(1)

    signal.signal(signal.SIGTERM, handler)
    signal.signal(signal.SIGINT, handler)

    loop.run_forever()
    loop.close()


if __name__ == "__main__":
    main()
