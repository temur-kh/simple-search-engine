def get_bigrams(word: str) -> [str]:
    bigrams = []
    for i in range(len(word)):
        if word[i] == '*':
            continue
        elif i == 0:
            bi = '$' + word[i]
            bigrams.append(bi)
            continue
        if word[i-1] != '*':
            bi = word[i-1:i+1]
            bigrams.append(bi)
        if i == len(word)-1:
            bi = word[i] + '$'
            bigrams.append(bi)
    return bigrams
