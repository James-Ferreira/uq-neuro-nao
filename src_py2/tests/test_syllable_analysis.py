import re

def is_vowel(char):
    return char.lower() in 'aeiouy'

def classify_syllable(syl):
    if syl and not is_vowel(syl[-1]):
        return 'long'
    else:
        return 'short'

def split_into_syllables(word):
    word = word.lower()
    vowels_pat = '[aeiou]'
    cons_pat = '[bcdfghjklmnpqrstvwxyz]'
    
    # Insert hyphen after each vowel
    word = re.sub('({})'.format(vowels_pat), r'\1-', word)
    
    # Remove trailing hyphen
    word = re.sub(r'-$', '', word)
    
    # Remove hyphen before final consonant
    word = re.sub('-({})$'.format(cons_pat), r'\1', word)
    
    # Fix certain consonant clusters (e.g., -nt to n-t)
    word = re.sub(r'-(n|r|st)(t|n|d|f)', r'\1-\2', word)
    
    # Fix s-clusters after vowels (e.g., as-t to as-t)
    word = re.sub('({})-s([tpnml])'.format(vowels_pat), r'\1s-\2', word)
    
    # Split into initial syllables
    syllables = word.split('-')
    
    # Merge any vowelless fragments to the previous syllable
    merged = []
    for syl in syllables:
        if syl and re.search(vowels_pat, syl) is None:
            if merged:
                merged[-1] += syl
            else:
                merged.append(syl)
        else:
            merged.append(syl)
    
    return merged

def analyze_word(word):
    syls = split_into_syllables(word)
    types = [classify_syllable(s) for s in syls]
    return list(zip(syls, types))

# Example usage
print(analyze_word('gel to the store of late timebeing there'))     # [('gel', 'long')]
print(analyze_word('jello'))   # [('je', 'short'), ('llo', 'short')]
print(analyze_word('go'))      # [('go', 'short')]
print(analyze_word('going'))   # [('go', 'short'), ('ing', 'long')]

# To estimate duration for a word (example weights; refine via testing)
def estimate_duration(word, short_weight=0.1, long_weight=0.15):
    analysis = analyze_word(word)
    total = 0.0
    for _, typ in analysis:
        total += short_weight if typ == 'short' else long_weight
    return total

print(estimate_duration('going to the store'))  # 0.25 (example)