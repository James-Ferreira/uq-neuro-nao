import re

gesture_tags = {
                    "[point forward]": 1, 
                    "point to self": 1,
                    "[point up]": 1,
                    "[point down]": 1, 
                    "[shake head no]": 1, 
                    "[nod yes]": 1, 
                    "[lower head]": 1, 
                    "[shake lowered head]": 1, 
                    "[pump fist]": 1, 
                    "[wave fist]": 1, 
                    "[wave hand]": 1,
                    "[spread arms]": 1, 
                    "[shrug]": 1,
                    }


# Python 2
import re

# Strip leading chars that are NOT letters, digits, or '['
_LEADING_JUNK_EXCEPT_LBRACKET = re.compile(r'^[^A-Za-z0-9\[]+')

def lstrip_punct_keep_bracket(s):
    """Remove leading punctuation/specials but preserve a leading '[' if present."""
    if s is None:
        return ""
    return _LEADING_JUNK_EXCEPT_LBRACKET.sub('', s)

    
if __name__ == "__main__":
    
    segment = "[!point to self] if you ask me, the mafia are a big part of the deep state."
    print(segment) 
    segment = lstrip_punct_keep_bracket(segment)
    print(segment)


