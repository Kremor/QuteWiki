import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow


class QuteWiki(QMainWindow):

    def __init__(self):
        qt_app = QApplication(sys.argv)

        super(QuteWiki, self).__init__()

        self.show()
        sys.exit(qt_app.exec_())
