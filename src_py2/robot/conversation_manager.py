# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from src_py2.robot.nao_robot import NAORobot
from src_py2.robot.motion_library import motions


import random
import re
import time
import unittest

#td strip quotation marks

class ConversationManager(object):

    def __init__(self, robot):
        self.robot = robot
        self.set_syll_duration_vars()
        self.set_rand_duration_vars()
        self.set_rand_joint_vars()
        self.set_gesture_tags()

    def set_syll_duration_vars(self):        
        # Pause and syllable durations
        #self.character_duration = 0.075
        self.short_pause_duration = 0.05
        self.long_pause_duration = 0.1
        self.short_weight = 0.15
        self.long_weight = 0.2
    
    def set_rand_duration_vars(self):

        self.gest_duration_arm = 1.2
        self.gest_duration_hand = 0.8
        self.gest_duration_head = 0.5
        self.sleep_duration = 0.2 

    def set_rand_joint_vars(self):

        # sets of joints
        self.joints_arms =[
                                    'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 
                                    'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll'
                            ]
        self.joints_rhand = ['RWristYaw', 'RHand']
        self.joints_lhand = ['LWristYaw', 'LHand']
        self.joints_head = ['HeadYaw', 'HeadPitch']
        self.joints_headarms = [
                                        'HeadYaw', 'HeadPitch', 
                                        'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 
                                        'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll'                                                                      
                                      ]

        # sets of angles
        self.rand_angles_other_hand = [[0], [0.4]]         
        self.rand_angles_dict = {
                        'left_out': [[angle] for  _, angle in [['LShoulderPitch', 0.9556400775909424], ['LShoulderRoll', 0.45095396041870117], ['LElbowYaw', -2.074009895324707], ['LElbowRoll', -1.178070068359375], ['RShoulderPitch', 0.9357819557189941], ['RShoulderRoll', -0.2945699691772461], ['RElbowYaw', 0.4524879455566406], ['RElbowRoll', 1.1674160957336426]]],
                        'left_up': [[angle] for  _, angle in [['LShoulderPitch', 0.8129780292510986], ['LShoulderRoll', 0.14108610153198242], ['LElbowYaw', -1.4420018196105957], ['LElbowRoll', -1.3222661018371582], ['RShoulderPitch', 0.9342479705810547], ['RShoulderRoll', -0.29610395431518555], ['RElbowYaw', 0.4524879455566406], ['RElbowRoll', 1.1612801551818848]]],
                        'left_over': [[angle] for  _, angle in [['LShoulderPitch', 0.760822057723999], ['LShoulderRoll', -0.0061779022216796875], ['LElbowYaw', -0.6121079921722412], ['LElbowRoll', -1.2056820392608643], ['RShoulderPitch', 0.9357819557189941], ['RShoulderRoll', -0.29917192459106445], ['RElbowYaw', 0.4540219306945801], ['RElbowRoll', 1.1873579025268555]]],
                        'right_out': [[angle] for  _, angle in [['LShoulderPitch', 0.9080860614776611], ['LShoulderRoll', 0.2438640594482422], ['LElbowYaw', -0.4556400775909424], ['LElbowRoll', -1.0752921104431152], ['RShoulderPitch', 0.6243798732757568], ['RShoulderRoll', -0.09208202362060547], ['RElbowYaw', 2.0248379707336426], ['RElbowRoll', 1.1704840660095215]]],
                        'right_over': [[angle] for  _, angle in [['LShoulderPitch', 0.9080860614776611], ['LShoulderRoll', 0.24539804458618164], ['LElbowYaw', -0.4556400775909424], ['LElbowRoll', -1.0768260955810547], ['RShoulderPitch', 0.5737578868865967], ['RShoulderRoll', -0.033789873123168945], ['RElbowYaw', 0.3282339572906494], ['RElbowRoll', 1.415924072265625]]],
                        'right_up':  [[angle] for  _, angle in [['LShoulderPitch', 0.9080860614776611], ['LShoulderRoll', 0.23926210403442383], ['LElbowYaw', -0.45717406272888184], ['LElbowRoll', -1.0722241401672363], ['RShoulderPitch', 0.8007900714874268], ['RShoulderRoll', 0.06592011451721191], ['RElbowYaw', 1.366752028465271], ['RElbowRoll', 1.4803519248962402]]]
                        }
        
        # sets of time points
        self.rand_timepoints_other_hand = [[0.75], [1.5]]

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
    
    ###  TEXT HANDLING

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

    def split_text(self, text):        

        # Split on periods or commas while preserving punctuation
        segments = re.findall(r'[^.;!?]+[.;!?]', text)

        # remove any leading/trailing whitespace
        segments = [segment.strip() for segment in segments]

        segments = self.merge_short_segments(segments)

        return segments 


    ### DURATION HANDLING   

    def estimate_duration_old(self, text):
        length = len(text)
        duration_est = round(length * self.character_duration, 2)

        return duration_est    
    
    def is_vowel(self, char):
        return char.lower() in 'aeiouy'

    def classify_syllable(self, syl):
        if syl and not self.is_vowel(syl[-1]):
            return 'long'
        else:
            return 'short'

    def split_into_syllables(self,segment):
        segment = segment.lower()
        vowels_pat = '[aeiou]'
        cons_pat = '[bcdfghjklmnpqrstvwxyz]'
        
        # Insert hyphen after each vowel
        segment = re.sub('({})'.format(vowels_pat), r'\1-', segment)
        
        # Remove trailing hyphen
        segment = re.sub(r'-$', '', segment)
        
        # Remove hyphen before final consonant
        segment = re.sub('-({})$'.format(cons_pat), r'\1', segment)
        
        # Fix certain consonant clusters (e.g., -nt to n-t)
        segment = re.sub(r'-(n|r|st)(t|n|d|f)', r'\1-\2', segment)
        
        # Fix s-clusters after vowels (e.g., as-t to as-t)
        segment = re.sub('({})-s([tpnml])'.format(vowels_pat), r'\1s-\2', segment)
        
        # Split into initial syllables
        syllables = segment.split('-')
        
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

    def analyze_segment(self, segment):
        syls = self.split_into_syllables(segment)
        types = [self.classify_syllable(s) for s in syls]
        return list(zip(syls, types))

    # To estimate duration for a segment (example weights; refine via testing)
    def estimate_duration(self, segment):

        """
        Use variable weights for puases 1
        """

        # Estimate total pause duration
        if segment == "":
            total_duration = 0
            return total_duration
        else:
            short_pauses = segment.count(" ")
            long_pauses = len(re.findall(r"[,:]", segment)) 
            total_pause_duration = self.short_pause_duration * short_pauses + self.long_pause_duration * long_pauses

            # Estimate total word duration
            analysis = self.analyze_segment(segment)
            total_word_duration = 0.0
            for _, typ in analysis:
                total_word_duration += self.short_weight if typ == 'short' else self.long_weight
            total_duration = total_pause_duration + total_word_duration
            return total_duration
    
    def estimate_durations(self, segments):

        """
        Apply the duration estimate to each text segment in a list.
        """

        durations_est = []
        for segment in segments:
            durations_est += [self.estimate_duration(segment)]
        durations_total_est = sum(durations_est)

        return durations_est, durations_total_est

    ### INTEGRATED SEGMENT HANDLING        

    def lstrip_punct_keep_bracket(self, s):
        """Remove leading punctuation/specials but preserve a leading '[' if present."""

        # Strip leading chars that are NOT letters, digits, or '['
        _LEADING_JUNK_EXCEPT_LBRACKET = re.compile(r'^[^A-Za-z0-9\[]+')

        if s is None:
            return ""
        return _LEADING_JUNK_EXCEPT_LBRACKET.sub('', s)

    def preprocess_segments(self, text):

        """
        Split text, calculate segment durations, assign gestures.
        Outputs list of lists, each of which contains 
        segment, gesture (None or tagged), gesture_type (random, single, cyclical), gesture duration estiamte
        """

        # Divide text into segments.
        segments_raw = self.split_text(text)
        print("segments: {}".format(segments_raw))

        segments_list = []
        for segment_raw in segments_raw:            

            # NAO will pronounce many segment-initial punctuation marks. This leaves only the tag marker [ at the start.
            segment = self.lstrip_punct_keep_bracket(segment_raw)

            # Simply turn segments with multiple tags into untagged segments, for now.
            if len(re.findall(r"\[.*?\]", segment)) > 1:
                segment = self.remove_tags(segment)

            # Identify tag, if present
            tag, gest_type = self.check_for_tags(segment)
            print("TAG: {}, gest_type: {}".format(tag, gest_type)) #666

            if tag == None:
                #Estimate segment durations
                duration_est = self.estimate_duration(segment)
                # Build list   
                segments_list += [[segment, tag, gest_type, duration_est]]
            else:
                # Isolate pre-/post- segments and tag
                subsegments = self.split_on_tags(segment)
                pretag_segment = subsegments[0]
                posttag_segment = subsegments[1]
                # Estimate segment durations
                pretag_seg_duration_est = self.estimate_duration(pretag_segment)
                posttag_seg_duration_est = self.estimate_duration(posttag_segment)
                # Build list
                segments_list += [[pretag_segment, "pretag", None, pretag_seg_duration_est]]
                segments_list += [[posttag_segment, tag, gest_type, posttag_seg_duration_est]]

        return segments_list

  
    ### TAGGED GESTURE HANDLING


    def check_for_tags(self, segment):
        """
        Check for gesture tags within a segment.
        Returns (gesture_name, gesture_type) if found, else (None, None).
        """

        text = segment.lower()
        pattern = r"\[([^\[\]]+)\]"   # capture tag content inside [ ]

        match = re.search(pattern, text)
        if match:
            tag = match.group(1).strip()  # e.g., "shake head"
            if tag in self.gesture_tags:
                gesture_type = self.gesture_tags[tag]
                return tag, gesture_type
            else:
                return None, "random"
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

        if match:
            tag = match.group(1).strip()
            start, end = match.span()
            before = tagged_segment[:start]
            after = tagged_segment[end:]
            subsegments = [before, after]
        else:
            tag = None
            subsegments = [tagged_segment]

        return subsegments

    def get_cumulative_multiple(self, list, multiple):

        """Multiply a list ensuring continuity of cumulative values."""
        
        cumulative_long_list = []

        for i in range(multiple):
            for j in range(len(list)):
                if i == 0:
                    cumulative_long_list.append(list[j])
                else:
                    cumulative_long_list.append(cumulative_long_list[-1] + list[j])

        return cumulative_long_list
    
    # def set_tagged_gest_cyclical(self, tag, posttag_seg_duration):

    #     # this is for cyclical gestures!!!
    #     # probably cycles should go to 3 no matter what and this function should be removed.

    #     joints = self.joints_dict[tag]
        
    #     timepoints_min = self.timepoints_dict[tag]
    #     timepoints_max = []
    #     print("timepoints_min: {}".format(timepoints_min))
    #     final_timepoint_min = timepoints_min[-1][-1]
    #     reps = int(posttag_seg_duration / final_timepoint_min)

    #     for i in timepoints_min:
    #         maxed = self.get_cumulative_multiple(i, reps)
    #         timepoints_max += [maxed]

    #     print('reps: {}'.format(reps))
    #     print("timepoints: {}".format(timepoints_max))

    #     angles_min = self.rand_angles_dict[tag]
    #     angles_max = []
    #     for i in angles_min:
    #         maxed = i * reps
    #         angles_max += [maxed]
    #     print("angles: {}".format(angles_max))

    #     return joints, angles_max, timepoints_max

    def set_tagged_gest_single(self, tag, duration):

        """
        Set a single tagged gesture
        """      

        # Only load the gesture, if its duration does not exceed the duration of the speech segment estimate by more than 0.5s
        timepoints = motions.get(tag, {}).get("time_points_list", []) # with a default if missing
        timepoint_max = max(max(sublist) for sublist in timepoints) 
        if duration + 0.5 < timepoint_max:
            joints = []
            angles = []
            timepoints = []
        else:
            joints = self.joints_dict[tag] 
            angles = self.rand_angles_dict[tag]

        return joints, angles, timepoints
    
    def execute_pretag_gest(self, segment, duration_est):
        # Sit if there is time, otherwise hold last posture.
        if duration_est > 1.5:
            self.robot.mm.sit_gently(post=True)
        self.robot.tts.say(segment)

    def execute_tagged_gest(self, posttag_segment, tag, gesture_type, duration_est):   

            """
            Split a tagged gesture into before and after.
            Identify its type and run.
            Consider moving the text processing to another function.
            """ 

            posttag_joints, posttag_angles, posttag_timepoints = [], [], []
            if gesture_type == 1:

                self.robot.tts.post.say(posttag_segment)
                self.robot.mm.use_motion_library(tag)
                # # Only load the gesture, if its duration does not exceed the duration of the speech segment estimate by more than 0.5s
                # timepoints = motions.get(tag, {}).get("time_points_list", []) # with a default if missing
                # timepoint_max = max(max(sublist) for sublist in timepoints) 
                # if duration_est + 0.5 > timepoint_max:
                #     # Execute posttag segment with speech
                #     self.robot.mm.use_motion_library(tag, post=True)
                # else:
                #     pass
            elif gesture_type == 2:
                pass
            #     posttag_joints, posttag_angles, posttag_timepoints = self.set_tagged_gest_cyclical(tag, duration_est)
            else:
                print('CUSTOM ERROR: key in gesture dictionary is neither 1 nor 2')
            
            #self.robot.tts.say(posttag_segment)     

    ### RANDOM GESTURE HANDLING
    
    def set_random_hand(self, reps_hand):
        yaws, hands = [], []
        yaw = hand = 0  # initialize to arbitrary values

        for i in range(reps_hand):
            if i % 2 == 1 or i == 0:
                yaw = random.uniform(-0.4, 0.4)
                hand = random.choice([0.1, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.6, 0.65, 0.7, 0.7, 0.8, 0.8, 0.9])

            yaws.append(yaw)
            hands.append(hand)

        return [yaws, hands]

    def set_random_head(self, reps_head):
        yaws, pitches = [], []
        yaw = pitch = 0  # initialize to arbitrary values

        for i in range(reps_head):
            if i % 2 == 1 or i == 0:
                move = random.choice([True, False])
                if move:
                    yaw = random.uniform(-0.2, 0.2)
                    pitch = random.uniform(-0.1, 0.3)

            yaws.append(yaw)
            pitches.append(pitch)

        return [yaws, pitches]    

    def set_reps_hand(self, duration_est):
        reps_hand = round((duration_est - self.gest_duration_arm - 1)*1.25)
        return int(reps_hand)
    
    def set_reps_head(self, duration_est):
        print("delete: duration_est: {}".format(duration_est))
        reps_head = (duration_est - self.gest_duration_arm - 1)*2
        return int(reps_head)
    
    def set_random_arm(self, side):

        gesture_arm = side + random.choice(['up', 'out', 'over'])

        return gesture_arm
    
    def set_random_gest(self, duration):

        # Side
        side = self.set_side()            

        # Arms            
        gesture_arm = self.set_random_arm(side)
        angles_arm = self.rand_angles_dict[gesture_arm]
        timepoints_arm = [[self.gest_duration_arm]] * len(angles_arm)

        # Head
        reps_head = self.set_reps_head(duration)
        angles_head = self.set_random_head(reps_head)
        timepoints_head = [[self.gest_duration_head * (i + 1) for i in range(reps_head)] for _ in range(2)]

        # Hands
        joints_hand, joints_other_hand = self.set_hand_joints(side)
        reps_hand = self.set_reps_hand(duration)
        angles_hand = self.set_random_hand(reps_hand)
        timepoints_hand = [[round(self.gest_duration_hand * (i + 1), 2) for i in range(reps_hand)] for _ in range(2)]

        # Integrate joints, angles and time points into Torso lists

        joints_torso = self.joints_headarms + joints_hand + joints_other_hand
        print("joints_torso: {}".format(joints_torso))
        angles_torso = angles_head + angles_arm + angles_hand + self.rand_angles_other_hand
        print(("angles_torso: {}".format(angles_torso)))           

        print("timepoints arm: {}".format(timepoints_arm))
        print("timepoints head: {}".format(timepoints_head))
        print("timepoints hand: {}".format(timepoints_hand))
        print("timepoints hand: {}".format(timepoints_hand))
        print("timepoints other hand: {}".format(self.rand_timepoints_other_hand))
        print("timepoints other hand: {}".format(self.rand_timepoints_other_hand))

        timepoints_torso = timepoints_head + timepoints_arm + timepoints_hand + self.rand_timepoints_other_hand
        print('timepoints_torso', timepoints_torso)

        return joints_torso, angles_torso, timepoints_torso
    
    def execute_random_gests(self, segment, duration):

            joints, angles, timepoints = self.set_random_gest(duration)

            # Execute posttag segment with speech
            self.robot.motion.post.angleInterpolation(joints, angles, timepoints, True)
            self.robot.tts.say(segment)   
    
    def set_hand_joints(self, side):

        if side == 'left_':
            joints = self.joints_lhand
            other_joints = self.joints_rhand
        elif side == 'right_':
            joints = self.joints_rhand
            other_joints = self.joints_lhand

        return joints, other_joints

    def set_side(self):

        side = random.choice(['left_', 'right_'])

        return side    

    ### MAIN FUNCTIONS ###

    def speak(self, text):
        """
        Speak via NAORobot TTS.
        """
        self.robot.tts.say(text)

    def speak_n_time(self, text):
        """
        Speak via NAORobot TTS, time duration, compare to estimated duration
        """
        # Divide text into sentence segments
        segments = self.split_text(text)
 
        #Estimate segment durations
        durations_est, duration_total_est = self.estimate_durations(segments) 
        print(segments)
        print(durations_est)  

        percentages = []
        for index, segment in enumerate(segments):
            print("index: {}".format(index))
            start = time.time()
            self.robot.tts.say(segment)
            end = time.time()
            duration = end - start
            duration_est = durations_est[index]
            difference = duration - duration_est
            print("Segment: {}".format(segment))
            print("Real Duration: {}".format(duration))
            print("Estimated Duration: {}".format(duration_est))
            print("Difference: {}".format(difference))
            print("Accuracy Percentage: {}".format(duration_est/duration))
            percentages += [duration_est/duration]
        summed = sum(percentages)
        mean_percentage = summed / len(percentages)
        print("MEAN ACCURACY PERCENTAGE: {}".format(mean_percentage))

    def speak_n_gest(self, text):

        """
        Speak via NAORobot TTS and simultaneously gesture.
        """       
        segments_list = self.preprocess_segments(text)

        for segment_list in segments_list:

            # segments list structure: [[segment, tag, gest_type, duration_est], [segment, tag, gest_type, duration_est], ...]
            # Speak and execute the appropriate gestures
            segment = segment_list[0]
            tag = segment_list[1]
            gesture_type = segment_list[2]
            duration_est = segment_list[3]

            print("SEGMENTS LIST: {}".format(segment_list))
            print("SEGMENT: {}".format(segment))
            print("TAG: {}".format(tag))
            print("GESTURE TYPE: {}".format(gesture_type))
            print("DURATION_EST: {}".format(duration_est))

            # Execute gentle sit on prettag segment, if there is time
            if tag == "pretag":
                pass
                self.execute_pretag_gest(segment, duration_est)
            # Execute tagged gesture on posttag segment
            elif tag is not None:
                self.execute_tagged_gest(segment, tag, gesture_type, duration_est)
            # Execute random gestures on full segment
            else:
                self.execute_random_gests(segment, duration_est)

        self.robot.mm.sit_gently()












