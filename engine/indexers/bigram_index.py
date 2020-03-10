from collections import defaultdict

from shared import get_bigrams, normalize, tokenize, remove_stop_word


def bigram_inverted_index(collection):
    bigram_index = defaultdict(set)
    bigram_iindex = defaultdict(set)
    for doc in collection:
        # preprocess without lemmatization
        new_text = normalize(doc.full_text())
        tokens = tokenize(new_text)
        text_tokens = remove_stop_word(tokens)
        for word in set(text_tokens):
            if word in bigram_index:
                continue
            bigrams = get_bigrams(word)
            bigram_index[word] = set(bigrams)
            for bigram in bigrams:
                bigram_iindex[bigram].add(word)
    return bigram_index, bigram_iindex
