import os

from gluster import gfapi

from config import *
from shared import str_to_doc, Document

_VOLUME = None


def _get_volume():
    global _VOLUME
    if _VOLUME is None:
        volume = gfapi.Volume(GLUSTERFS_MASTER_IP_ADDRESS, ENGINE_DATE_VOLUME)
        volume.mount()
        _VOLUME = volume
    return _VOLUME


volume = _get_volume()


def get_documents_by_ids(ids):
    docs = []
    for id in ids:
        path = os.path.join(DOCUMENTS_DIR_PATH, str(id))
        if not volume.exists(path):
            continue
        with volume.fopen(path, 'r') as f:
            line = f.read(1).strip()
            doc = str_to_doc(line)
            if doc:
                docs.append(doc)
    return docs


def remove_documents_by_ids(ids):
    for id in ids:
        path = os.path.join(DOCUMENTS_DIR_PATH, str(id))
        if not volume.exists(path):
            continue
        volume.remove(path)


def add_documents(docs: [Document]):
    for doc in docs:
        path = os.path.join(DOCUMENTS_DIR_PATH, str(doc.id))
        with volume.fopen(path, 'w') as f:
            f.write(doc.__str__())


def get_word_inverted_index(word: str) -> set:
    if not len(word):
        return set()
    iindex = set()
    path = os.path.join(MAIN_IINDEX_DIR_PATH, word)
    if volume.exists(path):
        with volume.fopen(path, 'r') as f:
            iindex = iindex.union(set(map(int, f.read().split())))
    path = os.path.join(AUXILIARY_IINDEX_DIR_PATH, word)
    if volume.exists(path):
        with volume.fopen(path, 'r') as f:
            iindex = iindex.union(set(map(int, f.read().split())))
    path = os.path.join(AUXILIARY_IINDEX_DIR_PATH, word)
    if volume.exists(path):
        with volume.fopen(path, 'r') as f:
            iindex = iindex.difference(set(map(int, f.read().split())))
    return iindex


def need_to_merge_iindexes():
    return len(volume.listdir(AUXILIARY_IINDEX_DIR_PATH)) >= AUXILIARY_IINDEX_LIMIT \
           or len(volume.listdir(REMOVABLE_IINDEX_DIR_PATH)) >= AUXILIARY_IINDEX_LIMIT


def merge_iindexes():
    for word in volume.listdir(AUXILIARY_IINDEX_DIR_PATH):
        main_path = os.path.join(MAIN_IINDEX_DIR_PATH, word)
        aux_path = os.path.join(AUXILIARY_IINDEX_DIR_PATH, word)
        remove_path = os.path.join(REMOVABLE_IINDEX_DIR_PATH, word)
        iindex = get_word_inverted_index(word)
        content = ' '.join([str(doc for doc in iindex)])
        with volume.fopen(main_path, 'w') as f:
            f.write(content)
        if volume.exists(aux_path):
            volume.remove(aux_path)
        if volume.exists(remove_path):
            volume.remove(remove_path)


def update_iindex(iindex_collection, dir_path):
    for word in iindex_collection:
        path = os.path.join(dir_path, word)
        iindex = iindex_collection[word]
        if volume.exists(path):
            with volume.fopen(path, 'r') as f:
                old_iindex = set(map(int, f.read().split()))
            iindex = iindex.union(old_iindex)
        content = ' '.join([str(doc_id) for doc_id in iindex])
        with volume.fopen(path, 'w') as f:
            f.write(content)


def remove_iindex(iindex_collection):
    update_iindex(iindex_collection, REMOVABLE_IINDEX_DIR_PATH)


def add_iindex(iindex_collection):
    update_iindex(iindex_collection, AUXILIARY_IINDEX_DIR_PATH)

def init_gluster():
    volume.mkdir(MAIN_IINDEX_DIR_PATH)
    volume.mkdir(AUXILIARY_IINDEX_DIR_PATH)
    volume.mkdir(REMOVABLE_IINDEX_DIR_PATH)
    volume.mkdir(DOCUMENTS_DIR_PATH)
