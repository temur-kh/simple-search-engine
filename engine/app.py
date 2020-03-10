import time

from shared import ReutersAddStream, ReutersDeleteStream
from engine.functions import *
from config import RESOURCES_DIR_PATH


def crawler():
    add_stream = ReutersAddStream(RESOURCES_DIR_PATH)
    delete_stream = ReutersDeleteStream(RESOURCES_DIR_PATH)

    index = 0
    while add_stream.has_next():
        if index > 15 and delete_stream.has_next():
            deletable_docs = delete_stream.next()
            remove_docs(deletable_docs)
        addable_docs = add_stream.next()
        add_docs(addable_docs)
        merge_iindexes_if_needed()
    force_merge_iindexes()


def process(*args, **kwargs):
    init_databases()
    crawler()
