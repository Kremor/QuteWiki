import codecs
import json
import os

from qutewiki.filesaver import FileSaver
from qutewiki.wikipage import WikiPage
from qutewiki.wikitag import WikiTag


class WikiManager:

    def __init__(self, path: str):
        self.pages = {}
        self.tags = {}
        self.path = path
        self.dir = path.replace('wiki.json', '')

        file = codecs.open(path, 'r', 'utf-8')
        lines = file.readlines()
        data = ''
        for line in lines:
            data += line
        file.close()

        wiki_dict = json.loads(data)

        pages = wiki_dict['pages']

        for key in pages:
            page = WikiPage(key)
            page.set_links(pages[key]['links'])
            page.set_tags(pages[key]['tags'])
            self.pages[key] = page

    def add_page(self, name):
        page = WikiPage(name)
        self.pages[name] = page
        return page

    def add_tag(self):
        pass

    def get_page(self, name):
        if name in self.pages:
            return self.pages[name]
        return None

    def get_pages(self):
        pages = []
        for key in self.pages:
            pages.append(key)
        return pages

    def get_tag(self, name):
        pass

    def get_tags(self):
        tags = []
        for key in self.tags:
            tags.append(key)
        return tags

    def is_page(self, name):
        return name in self.pages

    def is_tag(self, name):
        return name in self.tags

    def name_repeats(self, current, new):
        if current != new and self.is_page(new):
            return True
        return False

    def remove_page(self):
        pass

    def remove_tag(self):
        pass

    def rename_page(self, old, new):
        page = self.pages[old]
        page.rename(new)
        del self.pages[old]
        self.pages[new] = page
        if os.path.isfile(self.dir + old + '.md'):
            os.rename(self.dir + old + '.md', self.dir + new + '.md')
        #TODO change name in links

    def rename_tag(self):
        pass

    def tag_repeats(self, current, new):
        if current != new and self.is_tag(new):
            return True
        return False

    def to_json(self):
        pages = {}
        for key in self.pages:
            pages[key] = self.pages[key].to_dict()

        return json.dumps({'pages': pages, 'tags': {}}, ensure_ascii=False)
