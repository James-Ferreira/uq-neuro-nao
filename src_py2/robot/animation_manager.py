# -*- coding: utf-8 -*-
from __future__ import absolute_import
from src_py2.robot.nao_robot import NAORobot

# Regex for removing print statements (may cause spacing issues): print\("Stage: " \+ str\((\d+)\) \+ ": " \+ "([a-zA-Z_]+)"\)
import json
import os
import re
import runpy 
import sys
import time

###########################################
### CREATE COMPRESSED AND UNCOMPRESSED ANIMATIONS FOR PURE ACTIONS AND DIALOGUE ACTIONS
### ALSO OPTIONALLY CREATE DICTIONARIES FOR DIALOGUE ACTIONS
###########################################

class AnimationManager(object):    

    def __init__(self, robot):

        self.robot = robot
        self.set_weights()
        self.set_empty_vars()

    def set_weights(self):
        
        self.pitch = 1 # or 0.85        
        self.angle_modulator = 1.0 # For multiplying with angles.
        self.duration_modulator = 1.0 # For multiplying with durations.
        self.talk_speed = 79
        self.volume = 70

    def set_empty_vars(self):
        self.animation_name = ""
        self.joint_names_list = []
        self.joint_angles = []
        self.joint_angles_dict = {}
        self.time_points = []
        self.script_contents_uncompressed = """"""
        self.script_contents_compressed = """"""

    def select_list(self):  

        """Select a list of self."""

        joints_group = int(raw_input("Choose a group of joints: (1) head, (2) torso except for hands, (3) torso, (4) legs, (5) whole body.\n !!!WARNING: robot will loosen when you press <ENTER>!!!\n: "))

        if joints_group ==  1:

            message_prefix = 'Head'
            selected_joints = ['HeadYaw', 'HeadPitch']

        elif joints_group == 2:

            message_prefix = 'Head and arms but NOT hands'
            selected_joints = ['HeadYaw', 'HeadPitch', 
                        'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 
                        'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw'
                        ]

        elif joints_group == 3:

            message_prefix = 'Head and arms and hands'
            selected_joints = ['HeadYaw', 'HeadPitch', 
                        'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 
                        'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand'
                        ]

        elif joints_group == 4:

            message_prefix = 'Legs'
            selected_joints = ['LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll', 
                        'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll'
                        ]

        elif joints_group == 5:

            message_prefix = 'Full body'
            selected_joints = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll', 'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
            
        else:
            print("Invalid input: enter a digit from 1 to 5")

        print(message_prefix + " selected.")
        return selected_joints

    # Call and input number of desired parts combination
    def select_list_arg(self, joints_group):  

        """Choose a group of joints: (1) head, (2) torso except for hands, (3) torso, (4) legs, (5) whole body."""

        if joints_group ==  1:

            message_prefix = 'Head'
            selected_joints = ['HeadYaw', 'HeadPitch']

        elif joints_group == 2:

            message_prefix = 'Head and arms but NOT hands'
            selected_joints = ['HeadYaw', 'HeadPitch', 
                        'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 
                        'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw'
                        ]

        elif joints_group == 3:

            message_prefix = 'Head and arms and hands'
            selected_joints = ['HeadYaw', 'HeadPitch', 
                        'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 
                        'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand'
                        ]

        elif joints_group == 4:

            message_prefix = 'Legs'
            selected_joints = ['LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll', 
                        'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll'
                        ]

        elif joints_group == 5:

            message_prefix = 'Full body'
            selected_joints = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll', 'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
            
        else:
            print("Invalid input: enter a digit from 1 to 5")

        print(message_prefix + " selected.")
        return selected_joints

    def loosen_list(self):
        
        """Loosen the joint in the joints_list argument"""

        for joint in self.joint_names_list:
            self.robot.motion.setStiffnesses(joint, 0.0)

    def stiffen_list(self):
        
        """Stiffen the joint in the joints_list argument"""

        for joint in self.joint_names_list:
            self.robot.motion.setStiffnesses(joint, 1.0)    

    def after_angles_recorded(self, action_duration):

        """
        Create time and angle lists for compressed and uncompressed actions.
        """

        # Assign the action_duration just specified to all the self.
        action_durations = [action_duration] * len(self.joint_names_list)
        # Create a list comprehension that outputs a basic action duration list from a labeled action duration list that makes the final script readable and fine-tunable.
        action_durations_labeled = [[name, duration] for name, duration in zip(self.joint_names_list, action_durations)]       
        # Add the action duration just specified to the list of cumulative action durations.
        # Note that this list will be identical for every action, so it needs to be created only once and then repeated for every joint in the compressed animation.
        if self.time_points == []:
            # Make the initial time point that initial action duration.
            self.time_points += [action_duration]
        else:
            # Make susequent time points cumulative.
            self.time_points += [self.time_points[-1] + action_duration]
    
        # Create a list comprehension that outputs a basic joint angle list from a labeled joint angle list that makes the final script readable and fine-tunable.
        joint_angles_labeled = [[joint, angle] for joint, angle in zip(self.joint_names_list, self.joint_angles)] 
        # Assign the lists of joint angles to the appropriate keys in a joints dictionary
        for joint, angle in zip(self.joint_names_list, self.joint_angles):
            self.joint_angles_dict[joint] += [angle]
        
        return action_durations_labeled, joint_angles_labeled
    
    # Create a snippet of compressed actions.
    def compress(self, dialogue=0):
            
        # Create the list of joint angle lists.
        joint_angles_compressed = []
        for joint_name in self.joint_names_list:
            joint_angles_compressed += [self.joint_angles_dict[joint_name]]
        joint_angles_compressed_labeled = [[joint, angles] for joint, angles in zip(self.joint_names_list, joint_angles_compressed)] 

        # Create the redundant list of time point lists
        self.time_points_compressed = []
        for _ in self.joint_names_list:
            self.time_points_compressed += [self.time_points]
        self.time_points_compressed_labeled = [[joint, self.time_points] for joint, self.time_points in zip(self.joint_names_list, self.time_points_compressed)] 

        ### COMPRESSED SCRIPT CONTENTS ###    

        compressed_snippet = ""
        compressed_snippet += """   
joint_angles = [angles_compressed for _, angles_compressed in {}]
time_points = [time_points_compressed for _, time_points_compressed in {}]
{}.motion.angleInterpolation(joint_names_list, joint_angles, time_points, True)
        """.format(joint_angles_compressed_labeled, self.time_points_compressed_labeled, self.robot.name[0:4])

        # The additional compressed lists are used for the self.dictionarize() function, which only applies to dialogue at present.
        if dialogue == 0:
            return compressed_snippet
        else:
            return compressed_snippet, joint_angles_compressed, self.time_points_compressed        

    
    def clean_joint_angles_dict(self):

        """
        Create empty joint angles dictionary.
        """
        
        # Create a dictionary in which the keys are the joint names and the values are empty lists.
        # This will be used for compression in ANIMATE JUST ACTIONS
        joint_angles_dict = {}
        for joint in self.joint_names_list:
            joint_angles_dict[joint] = []
        
        return joint_angles_dict

    def import_list_variable(self, file_path):

        # Execute the file and capture its globals.
        module_globals = runpy.run_path(file_path)

        # Get the lines_timed variable from the globals.
        lines_timed = module_globals.get("lines_timed")

        if lines_timed is None:
            print("Error: 'lines_timed' variable not found in the file.")
        else:
            print("Dialogue loaded successfully:")
            # for line in lines_timed:
            #     print(line)

        return lines_timed
        
    def setup_vars(self):

        """
        These are the basic variables.  Some are empty and will be filled later.
        """
        # Decide on animation name.
        self.animation_name = raw_input('Animation name: ')
    
        # Get the joints names only for the joints to be loosened and animated.
        self.joint_names_list = self.select_list()

        # Create empty cumulative action durations list of lists for compression.
        self.time_points = []
        # Joint angles dictionary with joint names as keys and empty lists as values.
        self.joint_angles_dict = self.clean_joint_angles_dict()

        # Insert constants into all scripts to be generated.
        script_preface ="""      
angle_modulator = {}
duration_modulator = {}
        
joint_names_list = {}
                """.format(self.angle_modulator, self.duration_modulator, self.joint_names_list)
        
        # Set up for uncompressed and compressed scripts.
        self.script_contents_compressed, self.script_contents_uncompressed = script_preface, script_preface

    ### RAW INPUT HANDLING ###

    def float_check(self, string):

        """Ensure that raw string input is floatable"""
        try:
            float(string)
            return True
        except (TypeError, ValueError):
            return False
        
    def get_action_label(self):

        """
        In case of inadvertent entry of a number for action label, repeat instead of breaking script
        """

        repeat = True
        while repeat:

            # Specify the label for the action to be recorded.
            # Note that raw_input() is a custom module method.
            action_label = raw_input("Type ACTION LABEL: ")

            is_float = self.float_check(action_label)  

            if is_float:
                print("       !!!input a STRING, dammit!")
                repeat = True                    
            else:
                repeat = False                           

        return action_label    

    def get_action_duration(self):

        """
        In case of inadvertent entry of a string for action duration, repeat instead of breaking script
        """

        repeat = True
        while repeat:
            # Assign a duration to the action just recorded.
            # Note that raw_input is a custom module method.
            action_duration_raw = raw_input("TYPE ACTION DURATION: ") 

            is_float = self.float_check(action_duration_raw)  

            if is_float:
                action_duration = float(action_duration_raw)
                repeat = False   
            else:
                print("         !!!input a FLOAT or INTEGER, dammit!!!")

        return action_duration 


    ### ANIMATION VARIANTS    
    def silent_animation(self, action_count):     

                # Default movement count is 100.
                for stage in range(action_count):
                    
                    # raw input for action label
                    action_label = self.get_action_label()

                    # Check if action_label is 'quit' and break out of the loop if true to save the animation.
                    if action_label.lower() == 'quit':
                        print("Exiting early because 'quit' was entered.")
                        break                             

                    # Record the final joint angles of the action just labeled. ACTION RECORDED AFTER ACTION LABEL, NOT AFTER TIME
                    self.joint_angles = self.robot.motion.getAngles(self.joint_names_list, True)    

                    # Input the action duration
                    action_duration = self.get_action_duration()  

                    # Custom method at top of this script for creating time and angle lists for compressed and uncompressed actions.
                    action_durations_labeled, joint_angles_labeled = self.after_angles_recorded(action_duration)

                    ### UNCOMPRESSED SCRIPT CONTENTS ###    
                    
                    self.script_contents_uncompressed += """   
# Movement: {} : {}
print("Stage: " + str({}) + ": " + "{}")
joint_angles = [angle_modulator * angle for  _, angle in {}]
action_durations = [duration_modulator * duration for _, duration in {}]
{}.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
            """.format(stage+1, action_label, stage+1, action_label, joint_angles_labeled, action_durations_labeled, self.robot.name[0:4])
                                
                    print("Movement " + str(stage+1) + ": " + action_label)

                # Using the custom self.compress() method at the top of this script with default dialogue=0.
                self.script_contents_compressed += self.compress() 
    
    def save_animation(self):

            uncompressed_name = self.animation_name + "_uncompressed.py"
            compressed_name = self.animation_name + "_compressed.py"

            # Calculate the path relative to THIS script's location
            script_dir = os.path.dirname(os.path.abspath(__file__))
            recorded_dir = os.path.join(script_dir, '..', 'recorded_animation')

            # Make output paths
            output_path_uc = os.path.join(recorded_dir, uncompressed_name)
            output_path_c = os.path.join(recorded_dir, compressed_name)

            # Ensure directory exists
            if not os.path.exists(recorded_dir):
                os.makedirs(recorded_dir)

            with open(output_path_uc, 'w') as f:
                f.write(self.script_contents_uncompressed)
            print('Uncompressed animation created.')

            with open(output_path_c, 'w') as f:
                f.write(self.script_contents_compressed)
            print('Compressed animation created.') 

    def animate(self, dialogue_script=0, action_count=100):  

        # Setup variables needed to get started.
        self.setup_vars()
        
        # Loosen the selected joints.
        self.loosen_list()

        if dialogue_script == 0: 
            self.silent_animation(action_count)
        elif dialogue_script == 1:
            

            #         def dialogue_animations(self.joint_names_list, joint_angles_dict, self.time_points):

            #             self.tts.setParameter("pitchShift", self.pitch)

            #         ### IMPORT AND PREPROCESS DIALOGUE SCRIPT ###

            #         # Add the directory containing your dialogue files to sys.path.
            #         sys.path.append('MEASURE/DIALOGUE_TIMED')
            #         sys.path.append('MEASURE/DIALOGUE_UNTIMED')
                    
            #         measure_or_not = raw_input("int", "(1) Measure dialogue line durations OR (2) Load pre-timed dialogue file in MEASURE/DIALOGUE_TIMED/: ")
                
            #         # Run through the lines of dialogue and determine the duration of each.
            #         if measure_or_not == 1:
                        
            #             dialogue_untimed = raw_input("str", "Enter the name of the dialogue file in MEASURE/DIALOGUE_UNTIMED without '.py': ")
                        
            #             # Path to the import file
            #             file_path_import = 'MEASURE/DIALOGUE_UNTIMED/{}.py'.format(dialogue_untimed)
            #             print("file_path_import: " + file_path_import)

            #             # Path to the export file
            #             file_path_export = 'MEASURE/DIALOGUE_TIMED/{}_timed.py'.format(dialogue_untimed)
            #             dialogue_file = dialogue_untimed + "_timed"                
                        
            #             # Initialize the list
            #             lines_imported = []
                        
            #             with open(file_path_import, 'r') as file:
            #                 for line in file:
            #                     # Strip leading/trailing whitespace and newlines
            #                     stripped_line = line.strip()
            #                     if stripped_line:  # Ensure the line is not empty
            #                         lines_imported.append(stripped_line)
                        
            #             print("LINES IMPORTED\n")
            #             print(lines_imported)    
                        
            #             lines_to_measure = []
            #             line_words = ""
            #             line_words_pattern = r'\((.*?)\)'
            #             line_words_pattern_format = r'say\((.*)\)$' #pick out any dialogue lines with .format() method
                        
            #             for line in lines_imported:
            #                 line_words = ""  # Reset line_words for each new line
                            
            #                 if "time.sleep(" in line:
            #                     lines_to_measure.append(['', line])
            #                     continue  # Skip further processing for this line
                            
            #                 if ".say(" in line:
            #                     if ".format(" in line:
            #                         match = re.search(line_words_pattern_format, line)
            #                         if match:
            #                             # Evaluate the formatted string, so that the robot does not say "dot format parenthesis" etc.
            #                             line_words = eval(match.group(1))
            #                     else:
            #                         match = re.search(line_words_pattern, line)
            #                         if match:
            #                             # Append the matched content to the list
            #                             line_words = match.group(1)
            #                     lines_to_measure.append([line[0:4], line_words])
            #                     continue  # Skip further processing for this line
                            
            #                 if ".playFile(" in line:
            #                     match = re.search(line_words_pattern, line)
            #                     if match:
            #                             # Append the matched content to the list
            #                             line_words = match.group(1)
            #                     lines_to_measure.append([line[0:4], line_words])
            #                     continue  # Skip further processing for this line
                        
            #             print("LINES TO MEASURE\n")
            #             print(lines_to_measure)
                        
            #             # Set variables
            #             temp_volume = 30
                                    
            #             self.tts.setParameter('pitchShift', self.pitch)
            #             self.audio_device.setOutputVolume(temp_volume)          
            #             self.tts.setParameter('speed', self.talk_speed)
                        
            #             lines_timed = []
            #             duration_total = 0
                        
            #             ### RUN THROUGH ALL LINES IN THE DIALOGUE SCRIPT, PLAY, MEASURE DURATIONS, RECORD. ###
            #             for line in lines_to_measure:
            #                 if "#KEY:" in line[1]: 
                            
            #                     # Add the extract dictionary key phrase.
            #                     key = line[1][6:]
            #                     duration = 0
            #                     # Record key phrase in updated lines_timed list.
            #                     lines_timed += [["key", line[0], key, duration]]
                            
            #                 elif "time.sleep" in line[1]:
                                
            #                     # Use regex to extract the number inside the parentheses
            #                     match = re.search(r"time\.sleep\((\d+(\.\d{1,2})?)\)", line[1])
            #                     if match:
            #                         duration = float(match.group(1))  # Convert the matched number to a float
            #                         #print("Extracted sleep time: {}".format(sleep_time))
                                    
            #                         # Add labeled to lines_timed list
            #                         lines_timed += [["sleep", line[0], line[1], duration]]
                            
            #                 elif ".audio_player." in line[1]:
                                
            #                     # Record the start time
            #                     start_time = time.time()
                                
            #                     # Play the file
            #                     self.audio_player.playFile(line[1])
                                
            #                     # Record the end time
            #                     end_time = time.time()
                                
            #                     # Calculate and print the duration
            #                     duration = round(end_time - start_time, 2)
                                
            #                     # Add label to lines_timed list
            #                     lines_timed += [["play", line[0], line[1], duration]]
                                
            #                 else:
                        
            #                     # Record the start time
            #                     start_time = time.time()
                                
            #                     # Trigger the robot to say the string.
            #                     self.tts.say(line[1])
                                
            #                     # Record the end time
            #                     end_time = time.time()
                                
            #                     # Calculate and print the duration
            #                     duration = round(end_time - start_time, 2)
                            
            #                     # Add labeled to lines_timed list
            #                     lines_timed += [["talk", line[0], line[1], duration]]
                            
            #                 duration_total += duration
                        
            #             print("\nTOTAL DURATION: {}".format(duration_total))

            #             # SAMPLE lines_timed: 
            #             # ["talk", "meta", "speaky speaky", 1.5]
            #             # ["sleep", "meta", "", 0.8]
            #             # ["play", "clas", "/audio/file.mp3", 2.0]
            #             print (lines_timed)
                        
            #             script_contents_uncompressed = """
            # # Exported lines_timed list
            # lines_timed = [        
            # """
            #             for item in lines_timed:
            #                 script_contents_uncompressed += (str(item) + ",\n")
                        
            #             script_contents_uncompressed += "]" 
                        
            #             # Ensure the folder exists.
            #             try:
                        
            #                 # Write the list to a Python file.
            #                 with open(file_path_export, 'w') as f:
            #                                 f.write(script_contents_uncompressed)
            #                 print("File saved to:", file_path_export)            
            #             except IOError as e:
            #                     print("An IOError occurred:", e)
            #                     print("Check file and folder permissions.")
                            
            #         # If dialogue lines with durations list already exists in the correct output directory MEASURE/DIALOGUE_TIMED/.
            #         elif measure_or_not == 2: 
                    
            #             dialogue_file = raw_input("Enter the name of the dialogue file without '_timed.py': ")
            #             dialogue_file += "_timed"
            #             print("Dialogue file to load: " + dialogue_file)
            #         else:
            #             print("INVALID INPUT: ENTER 1 OR 2.")

            #         timed_dialogue_file_path = "MEASURE/DIALOGUE_TIMED/" + dialogue_file + ".py"
            #         dialogue = self.import_list_variable(timed_dialogue_file_path)

            #         # Dynamically import the dialogue list with action durations recorded.
            #         # Note that this file was saved just now, if you measured dialogue, or already existed, if you did not measure dialogue.

            #         #####################################
            #         ### SET UP DIALOGUE ACTION SCRIPT ###
            #         #####################################

            #         current_index = 0
            #         dialogue_in = 0
            #         duration_remaining = 0
            #         duration_filled = 0
            #         action_number = 1
                    
            #         script_contents_uncompressed = """
            # # Regex pattern to remove action print statements: r'^print\("motion.*?"\)$'

            # # Invariant joint names
            # joint_names_list = {}

            # angle_modulator = {}
            # duration_modulator = {}

            # talk_speed = {}
            # clas.tts.setParameter('speed', talk_speed)
            # meta.tts.setParameter('speed', talk_speed)
            #     """.format(joint_names_list, self.angle_modulator, self.duration_modulator, self.talk_speed) 
                    
            #         #####################################
            #         ### ANIMATE DIALOGUE ###
            #         #####################################
            #         key = 'NOKEY'
            #         while current_index < len(dialogue):
                        
            #             # Take a line from the dialogue script for processing.
            #             line = dialogue[current_index]
                        
            #             # Identify the next line in the dialogue script.
            #             if (current_index + 1) == len(dialogue):
            #                 line_next = ["none", "none (current line is final)", "none", "none"]
            #             else:        
            #                 line_next = dialogue[current_index+1]

            #             # The dialogue list             
            #             duration_line = line[3]
            #             duration_remaining = duration_line - duration_filled
                        
            #             # Pick out the sleep duration from sleep calls.
            #             print("if line[0] == 'key'")
            #             if line[0] == "key":
            #                 key = line[2]
            #                 print("KEY:")
            #                 print(key)

            #             else:

            #                 if line[0] == "sleep":
                            
            #                     robot_assigned = raw_input("Sleep: choose a robot: (1) m or (2) c: ")
                                
            #                     if robot_assigned == "m":
            #                         line[1] = "meta"
            #                     else:
            #                         line[1] = "clas"
                            
            #                 print("[[[Next Line: {}: {}: {}]]]".format(line_next[1], line_next[2], line_next[3]))

            #                 # Assign label to action.
            #                 # Note that raw_input is a custom module method.
            #                 action_label = raw_input(str(action_number) + ": " + str(duration_remaining) + "/" + str(line[3]) + ": " + line[1] + ": " + line[2] + "\n Action Label:")
                            
            #                 # Assign a duration to the action just recorded.
            #                 # Note that raw_input is a custom module method.
            #                 action_duration = raw_input("Duration remaining: {}: TYPE ACTION DURATION:".format(duration_remaining))

            #                 # Record angles.
            #                 joint_angles = self.motion.getAngles(joint_names_list, True)

            #                 # Custom method at top of this script for creating time and angle lists for compressed and uncompressed actions.
            #                 action_durations_labeled, self.time_points, joint_angles_labeled, joint_angles_dict = self.after_angles_recorded(action_duration, self.time_points, joint_names_list, joint_angles, joint_angles_dict)

            #                 # This conditional inserts the dialogue line into the script        
            #                 if dialogue_in == 0:
                                
            #                     if line[0] == 'talk':
                                    
            #                         script_contents_uncompressed += "\n\n{}.tts.post.say('{}')\n\n".format(line[1], line[2])

            #                     elif line[0] == 'play':
            #                         post_playFile = line[2].replace("_player.", "_player.post.")
            #                         script_contents_uncompressed += "\n{}{}\n".format(line[1], post_playFile)
                                        
            #                     dialogue_in = 1
                                
            #                 else:
            #                     pass
                        
            #                 script_contents_uncompressed += """
            # # Action {}: {}; Action Duration: {} 
            # # Line: {}: {}; Line Duration: {}
            # print("Action {}: {}; Action Duration: {}")

            # joint_angles = [angle_modulator * angle for  _, angle in {}]
            # action_durations = [duration_modulator * duration for _, duration in {}]
            # {}.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)      
            #         """.format(action_number, action_label, action_duration, line[1], line[2], line[3], action_number, action_label, action_duration, joint_angles_labeled, action_durations_labeled, self.name[0:4])

            #                 action_number += 1
            #                 duration_filled += action_duration
                            
            #             # If dialogue duration has been used up, compress and dictionarize the actions for that line of dialogue.  
            #             # Otherwise, add another action to the same line of dialogue.                

            #             if (duration_line - duration_filled) < 0.1:
            #                 dialogue_in = 0
            #                 duration_filled = 0
            #                 current_index += 1

            #                 # Because duration is 0 for 'key' lines.
            #                 if duration_line > 0:
            #                     # Input the line of dialogue before the compressed action.
            #                     script_contents_compressed += """\n{}.tts.post.say('{}')\n""".format(self.name[0:4], line[2])  
            #                     # Using the custom self.compress() method at the top of this script compress the action and output compressed lists for diciontarize().
            #                     compressed_snippet, joint_angles_compressed, self.time_points_compressed = self.compress(joint_names_list, joint_angles_dict, self.time_points, dialogue=1)
            #                     script_contents_compressed += compressed_snippet
                                
            #                     if do_dictionarize == 1:
                                        
            #                             # Put the compressed action into dialogue action dictionary format.
            #                             self.dictionarize(animation_name, key, line[2], joint_names_list, joint_angles_compressed, self.time_points_compressed)

            #                 self.time_points = []
            #                 joint_angles_dict = self.clean_joint_angles_dict(joint_names_list)              

            #             print("\n")        

            pass

        ### SAVE THE THE GENERATED SCRIPT, REGARDLESS OF WHETHER IT IS A PLAIN ACTION SCRIPT OR A DIALOGUE ACTION SCRIPT ###
        self.save_animation()

        # Restore default volume and stiffness
        self.robot.audio_device.setOutputVolume(self.volume)
        self.robot.mm.stiff()












