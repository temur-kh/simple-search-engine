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
        lines = line.split('###')
        if len(lines) == 3:
            id = int(lines[0])
            return Document(id, lines[1], lines[2])
        else:
            print(len(lines))
            print(lines)
            print("NOOOOOOOOOOOOOOOOOOOOO")
            raise Exception
    except:
        print('Document string could not be converted to object: %s' % line)
        return None
