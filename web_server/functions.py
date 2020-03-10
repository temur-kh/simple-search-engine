from shared import get_soundex_form, levinstein_distance, get_bigrams, preprocess
from databases import get_word_inverted_index, word_exists, get_soundex_iindex, get_bigram_iindex, get_documents_by_ids


def find_closest_words(query_word, soundex_iindex):
    soundex = get_soundex_form(query_word)
    # find the reduced number of candidates
    similars = [(word, levinstein_distance(query_word, word)) for word in soundex_iindex[soundex]]
    similars = sorted(similars, key=lambda x: x[1])
    if not len(similars):
        return []
    # find the closest candidates by the Levinstein distance
    min_dist = similars[0][1]
    closest_words = [word for word, dist in similars if dist == min_dist]
    return closest_words


def wildcards_process(query_word, bigram_iindex):
    query_bigrams = get_bigrams(query_word)
    # find similar words by bigrams
    similars = None
    for bigram in query_bigrams:
        if similars is None:
            similars = bigram_iindex[bigram]
        else:
            similars = similars.intersection(bigram_iindex[bigram])
    # post-filter these words from extra terms
    true_similars = set()
    star_pos = query_word.find('*')
    start_part = query_word[0:star_pos]
    end_part = query_word[star_pos + 1:len(query_word)]
    for word in similars:
        if (start_part == '' or word.startswith(start_part)) and (end_part == '' or word.endswith(end_part)):
            true_similars.add(word)
    return true_similars


def query_results(query):
    # construct a list-based logical query
    results = []
    query_tokens = preprocess(query)
    for token in query_tokens:
        if word_exists(token):
            results.append(token)
        elif '*' in token:
            words = wildcards_process(token, get_bigram_iindex())
            results.append(list(words))
        else:
            words = find_closest_words(token, get_soundex_iindex())
            results.append(list(words))
    return results


def search_docs_ids(query):
    # search for all relevant documents using a logical query
    results = query_results(query)
    doc_ids = None
    for res in results:
        if isinstance(res, list):
            inner_doc_ids = set()
            for word in res:
                inner_doc_ids = inner_doc_ids.union(get_word_inverted_index(word))
        else:
            inner_doc_ids = get_word_inverted_index(res)
        if doc_ids is None:
            doc_ids = inner_doc_ids
        else:
            doc_ids = doc_ids.intersection(inner_doc_ids)
    return list(doc_ids)


def find_docs(ids):
    docs = get_documents_by_ids(ids)
    # formatted = [{'title':doc.title, 'text':doc.text, 'id':doc.id} for doc in docs]
    return docs
