class WikiPage:

    def __init__(self, name: str = '') -> object:
        self.name = name
        self.tags = []
        self.links = []

    def __str__(self):
        links_str = str(self.links).replace('\'', '\"')
        tags_str = str(self.tags).replace('\'', '\"')
        return '"{0}": { "links": {1}, "tags": {2} }'.format(self.name, links_str, tags_str)

    def add_link(self, link):
        if link not in self.links:
            self.links.append(link)

    def add_tag(self, tag):
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_link(self, link):
        if link in self.links:
            self.links.remove(link)

    def remove_tag(self, tag):
        if tag in self.tags:
            self.tags.remove(tag)

    def rename(self, new_name):
        if new_name == self.name:
            return
        self.name = new_name

    def replace_link(self, old, new):
        if old in self.links:
            self.links.remove(old)
            self.links.append(new)

    def replace_tag(self, old, new):
        if old in self.tags:
            self.tags.remove(old)
            self.tags.append(new)

    def set_links(self, links):
        self.links = links

    def set_tags(self, tags):
        self.tags = tags

    def to_dict(self):
        return {'links': self.links, 'tags': self.tags}
