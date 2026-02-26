import re

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
            "nod yes": 1,
            "point down": 1,
            "point forward": 1,
            "point to self": 1,
            "point up": 1,
            "pump fist": 1,
            "scratch head": 1,
            "shake head no": 1,
            "shake fist": 1,
            "shrug": 1,
            "spread arms": 1,
            "wave hand": 1,
        }
        # Common LLM spelling variants / aliases -> canonical tags.
        self.gesture_tag_aliases = {
            "nodd yes": "nod yes",
            "nodding yes": "nod yes",
            "nod head yes": "nod yes",
            "shake no": "shake head no",
            "head shake no": "shake head no",
            "shake your head no": "shake head no",
        }

    # GENERAL TEXT HANDLING

    def split_text(self):
        text_claused = self.mark_complete_clauses()

        # Split on punctuation while preserving it, but keep a trailing clause without punctuation.
        segments = re.findall(r'[^.;!?]+(?:[.;!?]|$)', text_claused)

        # remove any leading/trailing whitespace
        segments = [segment.strip() for segment in segments]

        # drop empty / punctuation-only segments
        segments = [s for s in segments if self.has_alphanumeric(s)]

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
        return bool(re.search(r'[A-Za-z0-9]', string or ""))

    def mark_complete_clauses(self):
        """
        Replace ', and', ', or', ', but' with '; and', '; or', '; but'
        (Python 2.7 compatible)
        """
        pattern = r",\s+(and|or|but)\b"
        replaced = re.sub(pattern, r"; \1", self.text)
        return replaced

    def strip_junk(self, s):
        """Remove "Robot:" and leading punctuation/specials but preserve a leading '[' if present."""
        s2 = re.sub(r'^\s*Robot:\s*', '', s or "")

        # Strip leading chars that are NOT letters, digits, or '['
        _LEADING_JUNK_EXCEPT_LBRACKET = re.compile(r'^[^A-Za-z0-9\[]+')
        return _LEADING_JUNK_EXCEPT_LBRACKET.sub('', s2)

    # TAGGED GESTURE HANDLING

    def check_for_tags(self, segment):
        """
        Check for gesture tags within a segment.
        Returns (gesture_name, gesture_type) if found, else (None, "random").
        """
        seg = (segment or "").lower()
        pattern = r"\[([^\[\]]+)\]"  # capture tag content inside [ ]

        match = re.search(pattern, seg)
        if match:
            raw_tag = match.group(1).strip().lower()  # e.g., "shake head"
            tag = self.gesture_tag_aliases.get(raw_tag, raw_tag)
            if tag in self.gesture_tags:
                gesture_type = self.gesture_tags[tag]
                return tag, gesture_type
            else:
                return None, "random"
        else:
            return None, "random"

    def remove_tags(self, segment):
        detagged = re.sub(r"\[.*?\]", '', segment or "")
        detagged_no_extra_space = " ".join(detagged.split())
        return detagged_no_extra_space

    def split_on_tags(self, tagged_segment):
        """
        Split a text segment into parts before and after a gesture tag
        (marked by square brackets), and extract the tag placement pattern.

        Returns (subsegments, tag_combo)
        tag_combo in: "", "pretag", "posttag", "pretagposttag", "tagonly"
        """
        pattern = r"\[(.*?)\]"
        match = re.search(pattern, tagged_segment or "")

        subsegments = []
        tag_combo = ""
        if match:
            start, end = match.span()
            before = (tagged_segment or "")[:start]
            after = (tagged_segment or "")[end:]

            if self.has_alphanumeric(before):
                subsegments += [before]
                tag_combo += "pretag"
            if self.has_alphanumeric(after):
                subsegments += [after]
                tag_combo += "posttag"

            if subsegments == []:
                return [], "tagonly"
        else:
            subsegments = [tagged_segment]

        return subsegments, tag_combo

    def normalize_segment_tags(self, segment):
        """
        Reduce a segment to at most one valid gesture tag.
        Keeps the first valid tag and removes all other tags.
        If no valid tag exists, removes all tags.
        """
        pattern = r"\[([^\[\]]+)\]"
        matches = list(re.finditer(pattern, segment or ""))
        if len(matches) <= 1:
            return segment

        first_valid = None
        for match in matches:
            candidate = match.group(1).strip().lower()
            canonical = self.gesture_tag_aliases.get(candidate, candidate)
            if canonical in self.gesture_tags:
                first_valid = (canonical, match.span())
                break

        if first_valid is None:
            return self.remove_tags(segment)

        valid_tag, (start, end) = first_valid
        before = self.remove_tags((segment or "")[:start]).strip()
        after = self.remove_tags((segment or "")[end:]).strip()
        pieces = [piece for piece in (before, "[{}]".format(valid_tag), after) if piece]
        return " ".join(pieces)

    # INTEGRATED SEGMENT HANDLING

    def process_segments(self):
        """
        Split text, calculate segment durations, assign gestures.

        Outputs list of lists:
        [segment, tag, gest_type, duration_est]
        """

        segments_raw = self.split_text()
        print("SEGMENTS_raw: {}".format(segments_raw))

        segments_list = []
        for segment_raw in segments_raw:

            segment = self.strip_junk(segment_raw)

            # Keep first valid tag when multiple tags appear; drop the rest.
            if len(re.findall(r"\[.*?\]", segment)) > 1:
                segment = self.normalize_segment_tags(segment)

            # Identify tag, if present
            tag, gest_type = self.check_for_tags(segment)
            # in case AI generates an invalid tag
            if tag == "invalid":
                segment = self.remove_tags(segment)
                tag = None
                gest_type = None

            if tag is None and len(re.findall(r"\[.*?\]", segment)) > 0:
                segment = self.remove_tags(segment).strip()
                if not self.has_alphanumeric(segment):
                    continue

            if tag is None:
                duration_est = predict_duration(segment)
                segments_list += [[segment, None, "random", duration_est]]

            else:
                subsegments, tag_combo = self.split_on_tags(segment)
                #print(f"SUBSEGMENTS: {subsegments}")

                if tag_combo == "pretag":
                    pretag_segment = self.strip_junk(subsegments[0])
                    pretag_seg_duration_est = predict_duration(pretag_segment)
                    segments_list += [[pretag_segment, "pretag", "random", pretag_seg_duration_est]]

                elif tag_combo == "posttag":
                    posttag_segment = self.strip_junk(subsegments[0])
                    posttag_seg_duration_est = predict_duration(posttag_segment)
                    segments_list += [[posttag_segment, tag, gest_type, posttag_seg_duration_est]]

                elif tag_combo == "pretagposttag":
                    pretag_segment = self.strip_junk(subsegments[0])
                    pretag_seg_duration_est = predict_duration(pretag_segment)
                    segments_list += [[pretag_segment, "pretag", "random", pretag_seg_duration_est]]

                    posttag_segment = self.strip_junk(subsegments[1])
                    posttag_seg_duration_est = predict_duration(posttag_segment)
                    segments_list += [[posttag_segment, tag, gest_type, posttag_seg_duration_est]]

                elif tag_combo == "tagonly":
                    # No speakable text; drop it explicitly.
                    # If you ever want "gesture-only" actions, you'd need to extend the downstream contract.
                    pass

            #print("SEGMENTS LIST COMPILED IN SEGMENTIZE")

        return segments_list  # [segment, tag, gest_type, duration_estimate]
