import codecs

from PyQt5.QtCore import QThread


class FileSaver(QThread):

    def __init__(self, path: str, contents: str):
        super(FileSaver, self).__init__()
        self.path = path
        self.contents = contents
        self.start()

    def run(self):
        file = codecs.open(self.path, 'w', 'utf-8')
        file.write(self.contents)
        file.close()
        print('saved:', self.path)
