from collections import defaultdict

from shared import get_soundex_form


def soundex_inverted_index(words):
    soundex_iindex = defaultdict(set)
    for word in set(words):
        soundex = get_soundex_form(word)
        soundex_iindex[soundex].add(word)
    return soundex_iindex