import json

import redis

from config import *

_REDIS = None


def _get_redis():
    global _REDIS
    if _REDIS is None:
        r_obj = redis.StrictRedis(host=REDIS_MASTER_IP_ADDRESS)
        _REDIS = r_obj
    return _REDIS


r = _get_redis()


def word_exists(word):
    return r.sismember(WORDS_SET, word)


def get_words_set():
    return r.smembers(WORDS_SET)


def update_words_set(words_set):
    for word in words_set:
        r.sadd(WORDS_SET, word)


def get_soundex_iindex():
    return json.loads(r.get(SOUNDEX_IINDEX_DICT))


def add_soundex_iindex(soundex_iindex):
    old_iindex_collection = get_soundex_iindex()
    results = add_redis_iindex(soundex_iindex, old_iindex_collection)
    r.set(SOUNDEX_IINDEX_DICT, json.dumps(results))


def get_bigram_iindex():
    return json.loads(r.get(BIGRAM_IINDEX_DICT))


def add_bigram_iindex(bigram_iindex):
    old_iindex_collection = get_bigram_iindex()
    results = add_redis_iindex(bigram_iindex, old_iindex_collection)
    r.set(BIGRAM_IINDEX_DICT, json.dumps(results))


def add_redis_iindex(iindex_collection, old_iindex_collection):
    for index in iindex_collection:
        new_iindex = iindex_collection[index]
        if index in old_iindex_collection:
            new_iindex = new_iindex.intersection(old_iindex_collection[index])
        old_iindex_collection[index] = new_iindex
    return old_iindex_collection


def init_redis():
    r.sadd(WORDS_SET, {})
    r.set(BIGRAM_IINDEX_DICT, json.dumps({}))
    r.set(SOUNDEX_IINDEX_DICT, json.dumps({}))
