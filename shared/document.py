import logging


class Document:
    def __init__(self, id, title, text):
        self.id = id
        if not title:
            self.title = '[empty]'
        else:
            self.title = title
        if not text:
            self.text = '[empty]'
        else:
            self.text = text

    def full_text(self):
        return self.title + '\n' + self.text

    def __str__(self):
        return '###'.join([str(self.id), self.title, self.text])


def str_to_doc(line: str):
    try:
        id, title, text = line.split('###')
        id = int(id)
        return Document(id, title, text)
    except:
        logging.error('Document string could not be converted to object: %s' % line)
        return None
