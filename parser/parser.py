from bs4 import BeautifulSoup

"""
In Crawl++, GenericParser is the base of all parsers. There are many parsers built in as well.
To create your own parser, just extend your CustomParser class to GenericParser and implement parse function.
We use BeautifulSoup to do all the heavy lifting.
"""
class GenericParser:   
    def __init__(self, group):
        self.is_parsing = False
        self.data = None
        self.group = group

    def parse(self, chunk):
        raise NotImplementedError("Parse method should be implemented and must return data")

    def start_parsing(self, chunk):
        if self.is_parsing:
            return None
        self.is_parsing = True
        self.data = data = self.parse(chunk)
        if self.data is None:
            raise NotImplementedError("Improper implementation of parse method. Must return data.")
        self.is_parsing = False
        self.data = None
        return data

    def save_data(self):
        # TODO: save self.data in db

"""
TitleParser can return the title of the HTML page
"""
class TitleParser(GenericParser):
    def __init__(self, group):
        super().__init__(group)

    def parse(self, chunk):
        soup = BeautifulSoup(chunk, 'html.parser')
        return soup.title.text

"""
H2Parser returns the text from all H2 elements
"""
class H2Parser(GenericParser):
    def __init__(self, group):
        super().__init__(group)

    def parse(self, chunk):
        soup = BeautifulSoup(chunk, 'html.parser')
        h2s = []
        for h2 in soup.find_all('h2'):
            h2s.append(h2.text)
        return h2s

"""
LinkParser returns all the HREFs from the links
"""
class LinkParser(GenericParser):
    def __init__(self, group):
        super().__init__(group)

    def parse(self, chunk):
        soup = BeautifulSoup(chunk, 'html.parser')
        links = []
        for link in soup.find_all('a'):
            links.append(link.get('href'))
        return links