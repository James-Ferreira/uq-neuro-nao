# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from src_py2.robot.nao_robot import NAORobot

import random
import re
import time
import unittest



class Converse(object):
    """
    Usage:
        converser = Converse("meta")      # auto-connect; tries both meta IPs
        converser.say("Hello from NAO!")  # uses the connected NAORobot

        # If you created with connect_on_init=False:
        converser = Converse("clas", connect_on_init=False)
        converser.connect()               # connect later
    """

    def __init__(self, name, connect_on_init=True):
        self.name = name
        self.robot = None       # the NAORobot instance once connected
        self.ip_used = None      # which IP actually worked
        self._ip_pool = self._ips_for(name)
        if connect_on_init:
            self.connect()
        # durations
        self.character_duration = 0.075
        self.gest_duration_arm = 1.2
        self.gest_duration_hand = 0.8
        self.gest_duration_head = 0.5
        self.sleep_duration = 0.2 
        # sets of joints
        self.joints_arms =[
                                    'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 
                                    'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll'
                            ]
        self.joints_rhand = ['RWristYaw', 'RHand']
        self.joints_lhand = ['LWristYaw', 'LHand']
        self.joints_head = ['HeadYaw', 'HeadPitch']
        self.joints_headarms = [
                                    'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 
                                    'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 
                                    'HeadYaw', 'HeadPitch', 
                                      ]
        # sets of angles         
        self.angles_other_hand = [[0], [0.4]]        
        self.angles_dict = {
                                'left_out': [[angle] for  _, angle in [['LShoulderPitch', 0.9556400775909424], ['LShoulderRoll', 0.45095396041870117], ['LElbowYaw', -2.074009895324707], ['LElbowRoll', -1.178070068359375], ['RShoulderPitch', 0.9357819557189941], ['RShoulderRoll', -0.2945699691772461], ['RElbowYaw', 0.4524879455566406], ['RElbowRoll', 1.1674160957336426]]],
                                'left_up': [[angle] for  _, angle in [['LShoulderPitch', 0.8129780292510986], ['LShoulderRoll', 0.14108610153198242], ['LElbowYaw', -1.4420018196105957], ['LElbowRoll', -1.3222661018371582], ['RShoulderPitch', 0.9342479705810547], ['RShoulderRoll', -0.29610395431518555], ['RElbowYaw', 0.4524879455566406], ['RElbowRoll', 1.1612801551818848]]],
                                'left_over': [[angle] for  _, angle in [['LShoulderPitch', 0.760822057723999], ['LShoulderRoll', -0.0061779022216796875], ['LElbowYaw', -0.6121079921722412], ['LElbowRoll', -1.2056820392608643], ['RShoulderPitch', 0.9357819557189941], ['RShoulderRoll', -0.29917192459106445], ['RElbowYaw', 0.4540219306945801], ['RElbowRoll', 1.1873579025268555]]],
                                'right_out': [[angle] for  _, angle in [['LShoulderPitch', 0.9080860614776611], ['LShoulderRoll', 0.2438640594482422], ['LElbowYaw', -0.4556400775909424], ['LElbowRoll', -1.0752921104431152], ['RShoulderPitch', 0.6243798732757568], ['RShoulderRoll', -0.09208202362060547], ['RElbowYaw', 2.0248379707336426], ['RElbowRoll', 1.1704840660095215]]],
                                'right_over': [[angle] for  _, angle in [['LShoulderPitch', 0.9080860614776611], ['LShoulderRoll', 0.24539804458618164], ['LElbowYaw', -0.4556400775909424], ['LElbowRoll', -1.0768260955810547], ['RShoulderPitch', 0.5737578868865967], ['RShoulderRoll', -0.033789873123168945], ['RElbowYaw', 0.3282339572906494], ['RElbowRoll', 1.415924072265625]]],
                                'right_up':  [[angle] for  _, angle in [['LShoulderPitch', 0.9080860614776611], ['LShoulderRoll', 0.23926210403442383], ['LElbowYaw', -0.45717406272888184], ['LElbowRoll', -1.0722241401672363], ['RShoulderPitch', 0.8007900714874268], ['RShoulderRoll', 0.06592011451721191], ['RElbowYaw', 1.366752028465271], ['RElbowRoll', 1.4803519248962402]]],
                            }
        
        # sets of time points
        self.timepoints_other_hand = [[0.75], [1.5]]

    # REAMS OF CHAT-WRITTEN IP-HANDLING    

    def _ips_for(self, name):
        if name == "meta":
            # meta flips between these two
            return ["192.168.0.78", "192.168.0.79"]
        elif name == "clas":
            return ["192.168.0.183"]
        else:
            return []

    def connect(self):
        """
        Try each known IP until one succeeds. Raises if none work.
        """
        if not self._ip_pool:
            raise ValueError("Unknown robot name '{}' (no IPs configured).".format(self.name))

        last_err = None
        for ip in self._ip_pool:
            try:
                self.robot = NAORobot(self.name, ip)
                self.ip_used = ip
                return self.robot
            except Exception as e:
                last_err = e
                print("WARN: Failed to connect to {} @ {}: {}".format(self.name, ip, e))

        # If we got here, all IPs failed
        self.robot = None
        self.ip_used = None
        raise RuntimeError(
            "Could not connect to {} using any known IPs: {}. Last error: {}".format(
                self.name, ", ".join(self._ip_pool), last_err
            )
        )

    @property
    def is_connected(self):
        return self.robot is not None

    def getrobot(self):
        """
        Access the underlying NAORobot (connects on-demand).
        """
        if not self.robot:
            self.connect()
        return self.robot

    def reconnect(self, ip=None):
        """
        Force a reconnect. Optionally prefer a specific IP first.
        """
        if ip is not None:
            # Put the requested IP at the front of the pool if not already there
            self._ip_pool = [ip] + [x for x in self._ip_pool if x != ip]
        return self.connect()

    def __getattr__(self, attr):
        """
        Delegate unknown attributes/methods to the underlying NAORobot,
        so you can do converser.motion, converser.posture, etc.
        """
        robot = self.getrobot()
        return getattr(robot, attr)
    
    # SPEAKING

    def say(self, quote):
        """
        Speak via NAORobot TTS, connecting on-demand if needed.
        """
        if not self.robot:
            self.connect()
        self.robot.tts.say(quote)

    # RANDOM GESTURE HANDLING

    def estimate_duration(self, text):
        length = len(text)
        duration_est = round(length * self.character_duration, 2)

        return duration_est
    
    def estimate_durations(self, text):
        # Split the text into segments based on punctuation
        segments = self.split_text(text)

        # Calculate the estimated duration for each segment
        durations_est = [round(len(segment) * self.character_duration, 2) for segment in segments]

        # Sum the timepoints to get the total estimated duration
        total_duration_est = sum(durations_est)

        return durations_est, total_duration_est   

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
    
    def set_angles_hand(self, reps_hand):
        yaws, hands = [], []
        yaw = hand = 0  # initialize to arbitrary values

        for i in range(reps_hand):
            if i % 2 == 1 or i == 0:
                yaw = random.uniform(-0.4, 0.4)
                hand = random.choice([0.1, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.6, 0.65, 0.7, 0.7, 0.8, 0.8, 0.9])

            yaws.append(yaw)
            hands.append(hand)

        return [yaws, hands]

    def set_angles_head(self, reps_head):
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
        reps_head = round((duration_est - self.gest_duration_arm - 1))*2
        return int(reps_head)
    
    def set_gest_arm(self, side):

        gesture_arm = side + random.choice(['up', 'out', 'over'])

        return gesture_arm
    
    # def set_gest_special(self, keyword, duration):

    #     # this is for cyclical gestures!!!

    #     joints = self.joints_dict[keyword]
        
    #     timepoints_min = self.timepoints_dict[keyword]
    #     timepoints_max = []
    #     print("timepoints_min: {}".format(timepoints_min))
    #     final_timepoint_min = timepoints_min[-1][-1]
    #     reps = int(duration / final_timepoint_min)

    #     for i in timepoints_min:
    #         maxed = self.get_cumulative_multiple(i, reps)
    #         timepoints_max += [maxed]

    #     print('reps: {}'.format(reps))
    #     print("timepoints: {}".format(timepoints_max))

    #     angles_min = self.angles_dict[keyword]
    #     angles_max = []
    #     for i in angles_min:
    #         maxed = i * reps
    #         angles_max += [maxed]
    #     print("angles: {}".format(angles_max))

    #     return joints, angles_max, timepoints_max
    
    def set_gest_standard(self, duration):

        # Side
        side = self.set_side()            

        # Arms            
        gesture_arm = self.set_gest_arm(side)
        angles_arm = self.angles_dict[gesture_arm]
        timepoints_arm = [[self.gest_duration_arm]] * len(angles_arm)

        # Head
        reps_head = self.set_reps_head(duration)
        angles_head = self.set_angles_head(reps_head)
        timepoints_head = [[self.gest_duration_head * (i + 1) for i in range(reps_head)] for _ in range(2)]

        # Hands
        joints_hand, joints_other_hand = self.set_hand_joints(side)
        reps_hand = self.set_reps_hand(duration)
        angles_hand = self.set_angles_hand(reps_hand)
        timepoints_hand = [[round(self.gest_duration_hand * (i + 1), 2) for i in range(reps_hand)] for _ in range(2)]

        # Integrate joints, angles and time points into Torso lists

        joints_torso = self.joints_headarms + joints_hand + joints_other_hand
        print("joints_torso: {}".format(joints_torso))
        angles_torso = angles_arm + angles_head + angles_hand + self.angles_other_hand
        print(("angles_torso: {}".format(angles_torso)))           

        print("timepoints arm: {}".format(timepoints_arm))
        print("timepoints head: {}".format(timepoints_head))
        print("timepoints hand: {}".format(timepoints_hand))
        print("timepoints hand: {}".format(timepoints_hand))
        print("timepoints other hand: {}".format(self.timepoints_other_hand))
        print("timepoints other hand: {}".format(self.timepoints_other_hand))

        timepoints_torso = timepoints_arm + timepoints_head + timepoints_hand + self.timepoints_other_hand
        print('timepoints_torso', timepoints_torso)

        return joints_torso, angles_torso, timepoints_torso
    
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
    
    def split_text(self, text):        

        # Split on periods or commas while preserving punctuation
        segments = re.findall(r'[^.;!?]+[.;!?]', text)

        # remove any leading/trailing whitespace
        segments = [segment.strip() for segment in segments]

        segments = self.merge_short_segments(segments)

        return segments 
    
    ### MAIN GESTURE AND SPEAK FUNCTION ###
    def gns(self, text):

        #Segment text on full stops and semicolons
        segments = self.split_text(text)
        print("segments: {}".format(segments))
        #Estimate segment durations
        durations, duration_total_est = self.estimate_durations(text)   

        start_time = time.time()

        # loop through segments, assign movements, execute simultaneously
        for index, segment in enumerate(segments):

            # Set duration for the current segment
            duration = durations[index] 

            # # Identify keyword, if present
            # keyword = self.check_for_key_words(segment)
            # print("keyword: {}".format(keyword))
        
            # Set joints, angles and timepoints
            joints, angles, timepoints = self.set_gest_standard(duration)

            # Execute
            self.robot.motion.post.angleInterpolation(joints, angles, timepoints, True)
            self.robot.tts.say(segment)            


        end_time = time.time()
        elapsed_time = end_time - start_time
        
        print("Estimated duration: {}".format(duration_total_est))
        print("Actual duration: {}".format(elapsed_time))

        self.robot.mm.sit_gently()












