import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow

from qutewiki.hightlighter import SyntaxHighlighter
from qutewiki.ui.qutewiki_ui import Ui_MainWindow


class QuteWiki(QMainWindow):

    def __init__(self):
        qt_app = QApplication(sys.argv)

        super(QuteWiki, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        _ = SyntaxHighlighter(self.ui.textEdit)

        self.show()
        sys.exit(qt_app.exec_())
