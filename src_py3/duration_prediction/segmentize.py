from num2words import num2words
import re
from typing import Callable

from src_py3.duration_prediction.duration_predictor import predict_duration

 
class Segmentize():

    def __init__(self, text):
        self.text = text
        self.set_gesture_tags()

    def set_gesture_tags(self):
        # set special gesture tags
        # 1 = single, 2 = cyclical
        self.gesture_tags = {
                            "facepalm": 1,
                            "look upward": 1,
                            "point down": 1,
                            "point forward": 1,
                            "point to self": 1,
                            "point up": 1,
                            "pump fist": 1,
                            "scratch head": 1,
                            "shake fist": 1,
                            "shrug": 1,
                            "spread arms": 1,
                            "wave hand": 1
                        }
        
    ### GENERAL TEXT HANDLING

    def split_text(self):        

        text_claused = self.mark_complete_clauses()

        # Split on given punctuation while preserving punctuation
        segments = re.findall(r'[^.;!?]+[.;!?]', text_claused)

        # remove any leading/trailing whitespace
        segments = [segment.strip() for segment in segments]

        segments = self.merge_short_segments(segments)

        return segments


    def merge_short_segments(self, segments, max_words=5):
        merged = []
        i = 0
        while i < len(segments):
            segment = segments[i]
            word_count = len(segment.split())
            # Merge if 5 words or fewer and not the last segment
            if word_count <= max_words and i < len(segments) - 1:
                # Merge with next segment
                merged_segment = segment + ' ' + segments[i + 1]
                merged.append(merged_segment.strip())
                i += 2  # Skip next segment since it was merged
            else:
                merged.append(segment.strip())
                i += 1
        return merged

    # SPECIFIC TEXT HANDLING

    def has_alphanumeric(self, string):
        """
        Returns True if the string contains at least one alphanumeric character (A–Z, a–z, 0–9).
        Returns False if it contains only punctuation, whitespace, or symbols.
        """
        return bool(re.search(r'[A-Za-z0-9]', string))

    def mark_complete_clauses(self):
        """
        Replace ', and', ', or', ', but' with '; and', '; or', '; but'
        (Python 2.7 compatible)
        """
        # pattern uses a capturing group for the conjunction
        pattern = r",\s+(and|or|but)\b"
        # replace the comma-space with semicolon-space
        replaced = re.sub(pattern, r"; \1", self.text)
        return replaced

    def strip_junk(self, s):
        """Remove "Robot:" and leading punctuation/specials but preserve a leading '[' if present."""

        s2 = re.sub(r'^\s*Robot:\s*', '', s)

        # Strip leading chars that are NOT letters, digits, or '['
        _LEADING_JUNK_EXCEPT_LBRACKET = re.compile(r'^[^A-Za-z0-9\[]+')

        if s2 is None:
            return ""
        return _LEADING_JUNK_EXCEPT_LBRACKET.sub('', s2)

    ### TAGGED GESTURE HANDLING

    def check_for_tags(self, segment):
        """
        Check for gesture tags within a segment.
        Returns (gesture_name, gesture_type) if found, else (None, None).
        """

        seg = segment.lower()
        pattern = r"\[([^\[\]]+)\]"   # capture tag content inside [ ]

        match = re.search(pattern, seg)
        if match:
            tag = match.group(1).strip()  # e.g., "shake head"
            if tag in self.gesture_tags:
                gesture_type = self.gesture_tags[tag]
                return tag, gesture_type
            else:
                return "invalid", "random"
        else:
            return None, "random"

    def remove_tags(self, segment):

        detagged = re.sub(r"\[.*?\]", '', segment)
        detagged_no_extra_space = " ".join(detagged.split())

        return detagged_no_extra_space    

    def split_on_tags(self, tagged_segment):
        """
        Split a text segment into parts before and after a gesture tag
        (marked by square brackets), and extract the tag text.

        Example:
        "I have the right [brings down fist] to a fair trial."
        → (["I have the right ", " to a fair trial."], "brings down fist")
        """

        pattern = r"\[(.*?)\]"  # match text inside [brackets]
        match = re.search(pattern, tagged_segment)

        subsegments = []
        tag_combo = ""
        if match:
            print("match for tag regex")
            start, end = match.span()
            
            before = tagged_segment[:start]
            after = tagged_segment[end:]
            print("before, after: {}, {}".format(before, after))
            if self.has_alphanumeric(before):
                print("added before")
                subsegments += [before]
                tag_combo += "pretag"
            if self.has_alphanumeric(after):
                print("added after")
                subsegments += [after]  
                tag_combo += "posttag"
        else:
            subsegments = [tagged_segment] #that is, the segment is not tagged

        if subsegments == []:
            print("subsegments empty for some reason")
            

        return subsegments, tag_combo

### INTEGRATED SEGMENT HANDLING        

    def process_segments(self):

        """
        Split text, calculate segment durations, assign gestures.
        Outputs list of lists, each of which contains 
        segment, gesture (None or tagged), gesture_type (random, single, cyclical), gesture duration estiamte
        """

        # Divide text into segments.
        segments_raw = self.split_text()
        print("SEGMENTS_raw: {}".format(segments_raw))

        segments_list = []
        for segment_raw in segments_raw:         

            # NAO will pronounce many segment-initial punctuation marks. This leaves only the tag marker [ at the start.
            segment = self.strip_junk(segment_raw)

            # Simply turn segments with multiple tags into untagged segments, for now.
            if len(re.findall(r"\[.*?\]", segment)) > 1:
                segment = self.remove_tags(segment)

            # Identify tag, if present
            tag, gest_type = self.check_for_tags(segment)
            print(f"TAG: {tag}")
            print(f"GEST_TYPE: {gest_type}")

            # in case AI generates an invalid tag
            if tag == "invalid":
                    segment = self.remove_tags(segment)
                    tag == None

            if tag == None:
                #Estimate segment durations
                duration_est = predict_duration(segment)
                # Build list   
                segments_list += [[segment, tag, gest_type, duration_est]]

            else:
                # Isolate pre-/post- segments and tag
                subsegments, tag_combo = self.split_on_tags(segment)
                print(f"SUBSEGMENTS: {subsegments}")

                if tag_combo == "pretag":

                    pretag_segment = self.strip_junk(subsegments[0])
                    pretag_seg_duration_est = predict_duration(pretag_segment)
                    segments_list += [[pretag_segment, "pretag", None, pretag_seg_duration_est]]

                elif tag_combo == "posttag":

                    posttag_segment = self.strip_junk(subsegments[0])
                    posttag_seg_duration_est = predict_duration(posttag_segment) 
                    segments_list += [[posttag_segment, tag, gest_type, posttag_seg_duration_est]]
                
                elif tag_combo == "pretagposttag":

                    pretag_segment = self.strip_junk(subsegments[0])
                    pretag_seg_duration_est = predict_duration(pretag_segment)
                    segments_list += [[pretag_segment, "pretag", None, pretag_seg_duration_est]]

                    posttag_segment = self.strip_junk(subsegments[1])
                    posttag_seg_duration_est = predict_duration(posttag_segment)
                    segments_list += [[posttag_segment, tag, gest_type, posttag_seg_duration_est]]

  
                    

            print("SEGMENTS LIST COMPILED IN SEGMENTIZE")

        return segments_list # [segment, tag, gest_type, duration_estimate]