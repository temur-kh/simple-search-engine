import os

from bs4 import BeautifulSoup

from config import EMPTY_CONTENT
from shared import Document


class ReutersStream:
    def __init__(self, dir_path, upper_limit=22):
        self.dir_path = dir_path
        self._index = 0
        self._upper_limit = upper_limit
        self._next_id = 0

    def next(self):
        if self._index == self._upper_limit:
            return None
        filename = 'reut2-{}.sgm'.format(str(self._index).zfill(3))
        path = os.path.join(self.dir_path, filename)
        soup = BeautifulSoup(open(path, 'rb'), 'html.parser')
        collection = []
        for article in soup.find_all('reuters'):
            try:
                title = article.find('title').text
            except:
                title = EMPTY_CONTENT
            try:
                text = article.find('body').text
            except:
                text = EMPTY_CONTENT

            doc = Document(self._next_id, title, text)
            collection.append(doc)
            self._next_id += 1
        self._index += 1
        return collection

    def has_next(self):
        return self._index < self._upper_limit


class ReutersAddStream(ReutersStream):
    def __init__(self, dir_path):
        super().__init__(dir_path)


class ReutersDeleteStream(ReutersStream):
    def __init__(self, dir_path):
        super().__init__(dir_path, 5)
