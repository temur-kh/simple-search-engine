import re

import nltk
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

nltk.download('wordnet')
nltk.download('punkt')
nltk.download('stopwords')


def normalize(text: str) -> str:
    norm_text = re.sub(r'[^\w\s\*]', '', text)  # UPDATE: allow '*' sign
    norm_text = re.sub(r'[^\D]', '', norm_text)
    return ' '.join(norm_text.split()).lower()


def tokenize(text: str) -> [str]:
    return word_tokenize(text)


def lemmatize(tokens: [str]) -> [str]:
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(token) for token in tokens]


def remove_stop_word(tokens: [str]) -> [str]:
    stop_words = stopwords.words('english')
    return [token for token in tokens if token not in stop_words]


def preprocess(text):
    new_text = normalize(text)
    tokens = tokenize(new_text)
    lemmed_words = lemmatize(tokens)
    cleaned_words = remove_stop_word(lemmed_words)
    return cleaned_words
