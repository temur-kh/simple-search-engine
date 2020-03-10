def get_soundex_form(word: str) -> str:
    if not word:
        return word
    elif len(word) == 1:
        return word.upper()
    upper = word.upper()
    # step 1 according to lecture slides
    raw_soundex = upper[0]
    # step 2-3
    for ch in upper[1:]:
        if ch in ['A', 'E', 'I', 'O', 'U', 'H', 'W', 'Y']:
            raw_soundex += '0'
        elif ch in ['B', 'F', 'P', 'V']:
            raw_soundex += '1'
        elif ch in ['C', 'G', 'J', 'K', 'Q', 'S', 'X', 'Z']:
            raw_soundex += '2'
        elif ch in ['D', 'T']:
            raw_soundex += '3'
        elif ch == 'L':
            raw_soundex += '4'
        elif ch in ['M', 'N']:
            raw_soundex += '5'
        elif ch == 'R':
            raw_soundex += '6'
        else:
            continue
    filtered_soundex = raw_soundex[:2]
    # step 4
    prev_ch = raw_soundex[1]
    for ch in raw_soundex[2:]:
        if ch != prev_ch:
            filtered_soundex += ch
            prev_ch = ch
    # step 5
    filtered_soundex = filtered_soundex.replace('0', '')
    # step 6
    soundex = (filtered_soundex + '000')[:4]
    return soundex