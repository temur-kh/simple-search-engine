import os
import shutil

from config import *
from shared import str_to_doc, Document


def get_documents_by_ids(ids):
    docs = []
    print("I'm hereeeeeeeeee")
    for id in ids:
        path = os.path.join(DOCUMENTS_DIR_PATH, str(id))
        if not os.path.exists(path):
            print("AAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            continue
        with open(path, 'r') as f:
            # line = custom_decode_text(f.read())
            line = f.read()
            print(line)
            doc = str_to_doc(line)
            print(doc)
            if doc:
                docs.append(doc)
    return docs


def remove_documents_by_ids(ids):
    for id in ids:
        path = os.path.join(DOCUMENTS_DIR_PATH, str(id))
        if not os.path.exists(path):
            continue
        os.remove(path)


def add_documents(docs: [Document]):
    for doc in docs:
        # print(len(volume.listdir(MAIN_IINDEX_DIR_PATH)), 'add_doc')
        path = os.path.join(DOCUMENTS_DIR_PATH, str(doc.id))
        with open(path, 'w') as f:
            print(doc.__str__())
            f.write(doc.__str__())


def get_word_inverted_index(word: str) -> set:
    if not len(word):
        return set()
    iindex = set()
    path = os.path.join(MAIN_IINDEX_DIR_PATH, word)
    # print(len(volume.listdir(MAIN_IINDEX_DIR_PATH)), 'get_word_ii')
    if os.path.exists(path):
        with open(path, 'r') as f:
            file = f.read()
            # decoded_nums = custom_decode_ids(file)
            # iindex = iindex.union(set(decoded_nums))
            iindex = iindex.union(set(map(int, file.split())))
    path = os.path.join(AUXILIARY_IINDEX_DIR_PATH, word)
    if os.path.exists(path):
        with open(path, 'r') as f:
            file = f.read()
            # decoded_nums = custom_decode_ids(file)
            # iindex = iindex.union(set(decoded_nums))
            iindex = iindex.union(set(map(int, file.split())))
    path = os.path.join(REMOVABLE_IINDEX_DIR_PATH, word)
    if os.path.exists(path):
        with open(path, 'r') as f:
            file = f.read()
            # decoded_nums = custom_decode_ids(file)
            # iindex = iindex.difference(set(decoded_nums))
            iindex = iindex.difference(set(map(int, file.split())))
    return iindex


def need_to_merge_iindexes():
    return len(os.listdir(AUXILIARY_IINDEX_DIR_PATH)) >= AUXILIARY_IINDEX_LIMIT \
           or len(os.listdir(REMOVABLE_IINDEX_DIR_PATH)) >= AUXILIARY_IINDEX_LIMIT


def merge_iindexes():
    for word in os.listdir(AUXILIARY_IINDEX_DIR_PATH):
        main_path = os.path.join(MAIN_IINDEX_DIR_PATH, word)
        aux_path = os.path.join(AUXILIARY_IINDEX_DIR_PATH, word)
        remove_path = os.path.join(REMOVABLE_IINDEX_DIR_PATH, word)
        iindex = get_word_inverted_index(word)
        content = ' '.join([str(doc) for doc in iindex])
        with open(main_path, 'w') as f:
            # print(content)
            f.write(content)
        if os.path.exists(aux_path):
            os.remove(aux_path)
        if os.path.exists(remove_path):
            os.remove(remove_path)


def custom_decode_text(bytes):
    if bytes is not None:
        codes = bytes.decode().split()
        words = [str(x).replace('\x00', '') for x in codes]
        return ' '.join(words)
    else:
        return ''


def custom_decode_ids(bytes):
    if bytes is not None:
        codes = bytes.decode().split()
        str_nums = [str(x).replace('\x00', '') for x in codes]
        int_nums = []
        for num in str_nums:
            if num == '':
                int_nums.append(0)
            else:
                int_nums.append(int(num))
        return int_nums
    else:
        return []


def update_iindex(iindex_collection, dir_path):
    for word in iindex_collection:
        # print(len(volume.listdir(MAIN_IINDEX_DIR_PATH)), 'update_ii')
        path = os.path.join(dir_path, word)
        iindex = iindex_collection[word]
        if os.path.exists(path):
            with open(path, 'r') as f:
                file = f.read()
                # decoded_nums = custom_decode_ids(file)
                # old_iindex = set(decoded_nums)
                old_iindex = set(map(int, file.split()))
            iindex = iindex.union(old_iindex)
        content = ' '.join([str(doc_id) for doc_id in iindex])
        # print(content)
        with open(path, 'w') as f:
            f.write(content)


def remove_iindex(iindex_collection):
    update_iindex(iindex_collection, REMOVABLE_IINDEX_DIR_PATH)


def add_iindex(iindex_collection):
    update_iindex(iindex_collection, AUXILIARY_IINDEX_DIR_PATH)


def init_gluster():
    if os.path.exists(MAIN_IINDEX_DIR_PATH):
        shutil.rmtree(MAIN_IINDEX_DIR_PATH)
    os.mkdir(MAIN_IINDEX_DIR_PATH)
    if os.path.exists(AUXILIARY_IINDEX_DIR_PATH):
        shutil.rmtree(AUXILIARY_IINDEX_DIR_PATH)
    os.mkdir(AUXILIARY_IINDEX_DIR_PATH)
    if os.path.exists(REMOVABLE_IINDEX_DIR_PATH):
        shutil.rmtree(REMOVABLE_IINDEX_DIR_PATH)
    os.mkdir(REMOVABLE_IINDEX_DIR_PATH)
    if os.path.exists(DOCUMENTS_DIR_PATH):
        shutil.rmtree(DOCUMENTS_DIR_PATH)
    os.mkdir(DOCUMENTS_DIR_PATH)
    # print(len(volume.listdir(MAIN_IINDEX_DIR_PATH)), 'start')
