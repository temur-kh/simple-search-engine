from collections import defaultdict

from shared import preprocess
from shared import Document


def make_inverted_index(collection: [Document]):
    inverted_index = defaultdict(set)
    for doc in collection:
        text_tokens = preprocess(doc.full_text())
        for word in set(text_tokens):
            inverted_index[word].add(doc.id)
    return inverted_index
