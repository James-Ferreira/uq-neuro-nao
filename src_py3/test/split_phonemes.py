from phonemizer import phonemize
from phonemizer.separator import Separator

# Phonemize a single sentence (English, espeak backend, IPA output)
text = "Hello, world!"
phones = phonemize(
    text,
    language='en-us',
    backend='espeak',
    strip=True,  # Remove trailing whitespace
    preserve_punctuation=True
)
print(phones)  # Output: "həloʊ wɜːld"

# Batch process a list of sentences with custom separators
texts = ["This is a test.", "Phonemizer rocks!"]
phones_list = phonemize(
    texts,
    language='en-us',
    backend='espeak',
    separator=Separator(phone=' ', word='|', syllable='#'),  # Space phones, | for words, # for syllables
    with_stress=True  # Add stress marks like ˈ
)
for ph in phones_list:
    print(ph)  # e.g., "ðˈɪs ɪz ə tˈɛst ."

# Using Festival backend (English only)
phones_fest = phonemize(texts, language='en-us', backend='festival')