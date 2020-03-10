import nltk

from databases import *
from engine.indexers import *

def remove_docs(docs):
    remove_documents_by_ids([doc.id for doc in docs])
    iindex = make_inverted_index(docs)
    remove_iindex(iindex)


def add_docs(docs):
    print('Adding docs... Amount:', len(docs))
    add_documents(docs)
    iindex = make_inverted_index(docs)
    add_iindex(iindex)
    bigram_index, bigram_iindex = bigram_inverted_index(docs)
    words_set = bigram_index.keys()
    add_bigram_iindex(bigram_iindex)
    update_words_set(words_set)
    soundex_iindex = soundex_inverted_index(words_set)
    add_soundex_iindex(soundex_iindex)
    print('Finished adding docs')


def merge_iindexes_if_needed():
    if need_to_merge_iindexes():
        force_merge_iindexes()


def force_merge_iindexes():
    merge_iindexes()


def init_databases():
    nltk.download('wordnet')
    nltk.download('punkt')
    nltk.download('stopwords')
    init_gluster()
    init_redis()
