import re

from PyQt5.Qt import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QTextEdit


class Editor(QTextEdit):

    link_clicked = pyqtSignal(str)
    title_changed = pyqtSignal(str)

    bullet_list = re.compile('[*] .*')
    list_pattern = re.compile('\d+[.] .*|[*] .*')
    numbered_list = re.compile('\d+[.] .*')

    def __init__(self, parent=None):
        super(Editor, self).__init__(parent)
        self.setTabStopWidth(30)
        self.cursorPositionChanged.connect(self.on_cursor_pos_changed)
        self.textChanged.connect(self.on_text_changed)
        self.editing_title = False

    def mouseMoveEvent(self, event: QMouseEvent):
        super().mouseMoveEvent(event)

        cursor = self.cursorForPosition(event.pos())

    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)

        if event.button() == Qt.LeftButton:
            text_cursor = self.cursorForPosition(event.pos())
            text_cursor.select(QTextCursor.WordUnderCursor)
            word = text_cursor.selectedText()

    def on_cursor_pos_changed(self):
        if self.textCursor().blockNumber() != 0 and self.editing_title:
            title = self.document().findBlockByNumber(0).text().strip()
            self.title_changed.emit(title)
            self.editing_title = False

    def on_text_changed(self):
        if self.document().isModified():
            cursor = self.textCursor()
            block = cursor.block()
            pos = block.blockNumber()
            text = block.text()

            if pos == 0:
                self.editing_title = True

            if Editor.is_list(text):
                match = Editor.list_pattern.search(text)

                start = match.start()
                end = match.end()
                tabs = '\t'

                if pos > 0:
                    if Editor.is_list(self.document().findBlockByNumber(pos - 1).text()):
                        prev_text = self.document().findBlockByNumber(pos - 1).text()
                        prev_match = Editor.list_pattern.search(prev_text)
                        prev_text = prev_text[0:prev_match.start()]
                        num_tabs = prev_text.count('\t')
                        if num_tabs < text[0:start].count('\t'):
                            num_tabs += 1
                        tabs = tabs * num_tabs

                text = '\n' + tabs + text[start:end]

                edit_cursor = QTextCursor(block)

                self.blockSignals(True)

                edit_cursor.beginEditBlock()
                edit_cursor.select(QTextCursor.BlockUnderCursor)
                edit_cursor.removeSelectedText()
                edit_cursor.insertText(text)
                edit_cursor.endEditBlock()

                self.blockSignals(False)

    @staticmethod
    def is_list(text: str):
        match = Editor.list_pattern.search(text)
        if match:
            return True
        return False
