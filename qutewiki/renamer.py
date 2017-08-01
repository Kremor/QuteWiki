import codecs
import os
from threading import Thread


class Renamer(Thread):

    def __init__(self, path, old, new, links):
        self.path = path
        self.old = old
        self.new = new
        self.links = links
        self.start()

    def run(self):
        pass
