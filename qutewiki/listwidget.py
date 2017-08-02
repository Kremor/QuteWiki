from PyQt5.Qt import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QMenu


class ListWidget(QListWidget):

    remove_item_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(ListWidget, self).__init__(parent)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.RightButton:
            item = self.itemAt(event.pos())
            if item:
                self.show_context_menu(item.text(), event.pos())
        else:
            super().mousePressEvent(event)

    def remove_item_action(self, item_name):
        self.remove_item_signal.emit(item_name)

    def show_context_menu(self, item_name: str, point: QPoint):
        menu = QMenu()
        menu.addAction(
            'Remove {}'.format(item_name),
            lambda: self.remove_item_action(item_name)
        )
        menu.exec(self.mapToGlobal(point))
