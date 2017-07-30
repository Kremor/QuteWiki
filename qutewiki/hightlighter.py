import re

from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QSyntaxHighlighter
from PyQt5.QtGui import QTextCharFormat


class SyntaxHighlighter(QSyntaxHighlighter):

    def __init__(self, parent=None):
        super(SyntaxHighlighter, self).__init__(parent)

        self.rules = []

        heading1_rule = QTextCharFormat()
        heading1_rule.setFontPointSize(22)
        self.rules.append((re.compile('# .*'), heading1_rule))

        heading2_rule = QTextCharFormat()
        heading2_rule.setFontPointSize(20)
        self.rules.append((re.compile('## .*'), heading2_rule))

        heading3_rule = QTextCharFormat()
        heading3_rule.setFontPointSize(18)
        self.rules.append((re.compile('### .*'), heading3_rule))

        heading4_rule = QTextCharFormat()
        heading4_rule.setFontPointSize(16)
        self.rules.append((re.compile('#### .*'), heading4_rule))

        heading5_rule = QTextCharFormat()
        heading5_rule.setFontPointSize(14)
        self.rules.append((re.compile('##### .*'), heading5_rule))

        page_rule = QTextCharFormat()
        page_rule.setForeground(QBrush(QColor(0, 50, 200)))
        page_rule.setFontUnderline(True)

        self.pages = []

    def highlightBlock(self, text: str):
        text = text.lower()

        for pattern, char_format in self.rules:
            matches = pattern.finditer(text)
            for match in matches:
                start = match.start()
                end = match.end()
                self.setFormat(start, end - start, char_format)

        for pattern, char_format in self.pages:
            matches = pattern.finditer(text)
            for match in matches:
                start = match.start()
                end = match.end()

                if start > 0:
                    if match.string[start - 1].isalnum():
                        continue
                if end < len(text):
                    if match.string[end].isalnum():
                        continue

                self.setFormat(start, end - start, char_format)

        self.setCurrentBlockState(0)
