import codecs
import os

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox

from qutewiki.filesaver import FileSaver
from qutewiki.hightlighter import SyntaxHighlighter
from qutewiki.wikimanager import WikiManager
from qutewiki.wikipage import  WikiPage
from qutewiki.ui.qutewiki_ui import Ui_MainWindow


class QuteWiki(QMainWindow, Ui_MainWindow):

    def __init__(self):
        import sys

        qt_app = QApplication(sys.argv)

        super(QuteWiki, self).__init__()

        self.allow_saving = False
        self.file_thread = None
        self.wiki_thread = None

        self.wiki_path = ''
        self.wiki_file = ''
        self.wiki = WikiManager()
        self.current_page = WikiPage()
        self.init_folder()

        self.setupUi(self)
        self.highlighter = SyntaxHighlighter(self.textEdit)

        pages = self.wiki.get_pages()
        for i, page in enumerate(pages):
            self.pagesView.insertItem(i, page)
        self.pagesView.itemClicked.connect(self.on_page_selected)

        self.textEdit.title_changed.connect(self.on_title_changed)
        self.textEdit.textChanged.connect(self.on_text_changed)

        self.timer = QTimer(self)
        self.timer.setInterval(30000)
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.save)
        self.timer.start()

        self.addPageButton.pressed.connect(self.add_page)

        self.update_wiki()

        self.show()
        sys.exit(qt_app.exec_())

    def add_page(self):
        title = self.get_title()
        if not self.textEdit.isEnabled():
            self.textEdit.setEnabled(True)
        self.set_text(title + '\n\nDescribe your new note here')
        self.pagesView.insertItem(0, title)
        self.pagesView.setCurrentRow(0)
        self.current_page = self.wiki.add_page(title)
        self.change_title(title)

    def add_tag(self):
        pass

    def change_title(self, page: str):
        self.setWindowTitle('QuteWiki - ' + page)

    def closeEvent(self, event: QCloseEvent):
        self.timer.stop()
        self.save()
        self.wait_for_saving()
        if self.file_thread:
            self.file_thread.wait()
        if self.wiki_thread:
            self.wiki_thread.wait()
        super().closeEvent(event)

    def get_title(self):
        title = 'New Page'
        i = 1
        while self.wiki.is_page(title + ' ' + str(i)):
            i += 1
        return title + ' ' + str(i)

    def init_folder(self, path: str = '~'):
        self.wiki_path = os.path.expanduser(path) + '/.qutewiki'
        self.wiki_file = self.wiki_path + '/wiki.json'

        if not os.path.isdir(self.wiki_path):
            os.makedirs(self.wiki_path)

        if not os.path.isfile(self.wiki_file):
            file = codecs.open(self.wiki_file, 'w', 'utf-8')
            file.write('{ "pages": {}, "tags" : [] }')
            file.close()

        self.wiki.setup(self.wiki_file)

    def open_wiki(self, path: str):
        pass

    def on_page_selected(self, item: QListWidgetItem):
        title = self.textEdit.document().findBlockByNumber(0).text().strip()
        if self.wiki.name_repeats(self.current_page.name, title):
            self.pagesView.setCurrentRow(0)
            self.show_message('The Page <b>{}</b> already exists.'
                              'Change the title of the page before switching.'
                              .format(title))
        else:
            if title != self.current_page.name:
                self.wiki.rename_page(self.current_page.name, title)
                self.pagesView.item(0).setText(title)
            self.save()
            row = self.pagesView.row(item)
            item = self.pagesView.takeItem(row)
            self.pagesView.insertItem(0, item)
            page = item.text()
            file = codecs.open(self.wiki_path + '/' + page + '.md', 'r', 'utf-8')
            content = file.read()
            file.close()
            self.pagesView.setCurrentRow(0)
            self.current_page = self.wiki.get_page(page)
            self.set_text(content)
            self.textEdit.setEnabled(True)
            self.change_title(page)

    def on_text_changed(self):
        self.allow_saving = True

    def on_title_changed(self, title):
        if self.wiki.name_repeats(self.current_page.name, title):
            self.show_message('The Page <b>{}</b> already exists.'
                              'Change the title of the page to another one.'
                              .format(title))
        else:
            self.wiki.rename_page(self.current_page.name, title)
            list_item = self.pagesView.currentItem()
            list_item.setText(title)
            self.update_wiki()
            self.change_title(title)

    def save(self):
        if self.allow_saving and self.current_page.name != '':
            title = self.textEdit.document().findBlockByNumber(0).text().strip()
            if self.wiki.name_repeats(self.current_page.name, title):
                return

            if title != self.current_page.name:
                self.wiki.rename_page(self.current_page.name, title)
                self.pagesView.item(0).setText(title)

            self.wait_for_saving()

            contents = self.textEdit.toPlainText() + '\n'
            path = '{}/{}.md'.format(self.wiki_path, self.current_page.name)
            self.file_thread = FileSaver(path, contents)

            wiki_data = self.wiki.to_json()
            self.wiki_thread = FileSaver(self.wiki_file, wiki_data)

            self.allow_saving = False

    def set_text(self, text: str):
        self.textEdit.blockSignals(True)
        self.textEdit.setText(text)
        self.textEdit.blockSignals(False)

    def show_message(self, msg: str):
        msgbox = QMessageBox(self)
        msgbox.setWindowTitle('QuteWiki')
        msgbox.setText(msg)
        msgbox.setStandardButtons(QMessageBox.Ok)
        msgbox.show()

    def update_wiki(self):
        pages = self.wiki.get_pages()
        self.highlighter.set_pages(pages)

    def wait_for_saving(self):
        if self.file_thread:
            if not self.file_thread.isFinished():
                self.file_thread.wait()
        if self.wiki_thread:
            if not self.wiki_thread.isFinished():
                self.wiki_thread.wait()
