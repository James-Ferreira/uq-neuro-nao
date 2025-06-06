from naoqi import ALModule, ALBroker
import random
import time
from enum import Enum
import threading

# confirmation_path = "/tmp/confirmation.txt"

class TouchMode(Enum):
    HEAD_BASIC = "TouchModuleHead"
    SEE_TARGET = "TouchModuleSeeTarget"
    SHAKE_HAND_CLAS = "TouchModuleShakeHand_clas"
    SHAKE_HAND_META = "TouchModuleShakeHand_meta"
    FOOT_COMPLETE = "TouchModuleFoot"
    CONFIRMATION = "TouchModuleConfirm"
    HANKIE = "TouchModuleHankie"
    HEAD_SMASH = "TouchModuleHeadSmash"
    LEFT_HAND_LAUGH = "TouchModuleLaugh"
    RIGHT_FOOT_SCREAM = "TouchModuleScream"

class TouchModule(ALModule):
    def __init__(self, robot, module_name):
        ALModule.__init__(self, module_name)

        import __main__
        __main__.__dict__[module_name] = self

        self.robot = robot
        self.processing_touch = False

        self.robot.memory.subscribeToEvent("TouchChanged", module_name, "onTouchChanged")

        # ------- helpers for confirmation -------
        self._lock_confirm = threading.Lock()
        self._awaiting_confirm = False
        self._confirm_event = threading.Event()
        self._confirm_result = None

        self._lock_activate = threading.Lock()
        self._awaiting_activate = False
        self._activate_event = threading.Event()
        self._activate_result = None


    def onTouchChanged(self, strVarName, value):
        # print("onTouchChanged")

        if self.processing_touch or not value:
            return
        
        self.processing_touch = True
        
        if len(value) > 1 and isinstance(value[1], list) and len(value[1]) > 0:
            specific_touch = value[1][0]
        else:
            specific_touch = value[0][0] 

        if self._awaiting_confirm:
                with self._lock_confirm:
                    if "Foot" in specific_touch:
                        self._confirm_result = False
                        self._confirm_event.set()

                    if "Hand" in specific_touch:
                        self._confirm_result = True
                        self._confirm_event.set()

        if self._awaiting_activate:
            with self._lock_activate:
                    if "Head" in specific_touch:
                        self._activate_result = True
                        self._activate_event.set()


	    # print(specific_touch)
        # self.robot.tts.say("You touched my {}".format(specific_touch))
        
        # if "Head" in specific_touch:           
            
        #     # if TouchMode.HEAD_BASIC in self.modes:
        #     self.robot.leds.fadeRGB('AllLeds', 0x0000FF, 1)
        #     self.robot.leds.fadeRGB('AllLeds', 0xFFFFFF, 1)

            # if TouchMode.SEE_TARGET in self.modes:
            #     self.search_target(self.touch_count)
            #     self.touch_count +=1

            # if TouchMode.CONFIRMATION in self.modes:
            #     print("Todo: Saving {} to {}".format("reject", confirmation_path))

            # if TouchMode.HEAD_SMASH in self.modes:
            #     self.head_smash()

        # if "RHand" in specific_touch:           

        #     if TouchMode.SHAKE_HAND_CLAS in self.modes:
        #         self.right_hand_shake_clas()

        #     if TouchMode.SHAKE_HAND_META in self.modes:
        #         self.right_hand_shake_meta()

        #     if TouchMode.HANKIE in self.modes:
        #         self.hankie()

        #     if TouchMode.CONFIRMATION in self.modes:
        #         print("Todo: Saving {} to {}".format("yes", confirmation_path))

        # if "Foot" in specific_touch:      
        #     if TouchMode.FOOT_COMPLETE in self.modes:
        #         print("Todo: Saving {} to {}".format("complete", "start_game_path?"))

        #     if TouchMode.CONFIRMATION in self.modes:
        #         print("Todo: Saving {} to {}".format("no", confirmation_path))

        # if "LHand" in specific_touch:
        #     if TouchMode.LEFT_HAND_LAUGH in self.modes:
        #         self.left_hand_laugh()

        # if "RFoot" in specific_touch:
        #     if TouchMode.RIGHT_FOOT_SCREAM in self.modes:
        #         self.right_foot_scream()

        self.processing_touch = False

    def wait_for_touch_activate(self):
        print("waiting for head touch activate")
        with self._lock_activate:
            self._awaiting_activate = True
            self._activate_result   = None
            self._activate_event.clear()

        signalled = self._activate_event.wait()

        with self._lock_activate:
            self._awaiting_activate = False
            return self._activate_result if signalled else None

    def wait_for_touch_confirm(self, timeout=5.0):
        with self._lock_confirm:
            self._awaiting_confirm = True
            self._confirm_result   = None
            self._confirm_event.clear()

        signalled = self._confirm_event.wait(timeout)

        with self._lock_confirm:
            self._awaiting_confirm = False
            return self._confirm_result if signalled else None


    def search_target(self, see_slash_check):
        # EXPERIMENTER touches head and asks, "Can you see the target word?"

        search_duration = random.uniform(6, 12)
        head_movement_count = int(math.floor(search_duration) - 2)
        print(head_movement_count)
        per_head_movement_duration = search_duration / head_movement_count

        head_joints = ['HeadPitch', 'HeadYaw']
        head_time_points = [[],[]]
        head_angles = [[],[]]
        for count in range(head_movement_count):

            # Assign a random duration to each head movement and a random sleep duration to each interval between head movements.
            head_movement_duration = random.uniform(0.5,1)
            sleep_duration = per_head_movement_duration - head_movement_duration
            head_movement_duration_cumulative = head_movement_duration + per_head_movement_duration * count
            sleep_duration_cumulative = sleep_duration + head_movement_duration_cumulative
            head_time_points[0] += [head_movement_duration_cumulative, sleep_duration_cumulative]
            head_time_points[1] += [head_movement_duration_cumulative, sleep_duration_cumulative]

            # Assign random head movements
            head_pitch = random.uniform(0, 0.4)
            head_yaw = random.uniform(-0.3, 0.3)
            head_angles[0] += [head_pitch, head_pitch]
            head_angles[1] += [head_yaw, head_yaw]

        #print(head_joints)
        #print(head_angles)
        #print(head_time_points)

        self.motion.angleInterpolation(head_joints, head_angles, head_time_points, True) 

        # Set conditions so that the same method can be called twice with different output speech
        if see_slash_check == 1:
        
            self.tts.post.say("\\rspd=90\\ I see the target word.") 

        else:
        
            target_number = random.randint(1,4)
            self.tts.post.say("\\rspd=80\\ The number of the target word is: {}".format(target_number))

    def right_hand_shake_clas(self):
        # SHAKE_HAND
        # Set up a timer to unsubscribe after 20 seconds
        """clas.unsubscribe_timer = threading.Timer(30, clas.unsubscribe_and_shutdown)
        clas.unsubscribe_timer.start()  # Start the timer
        print("Subscribed to TouchChanged event with automatic unsubscribe in 30 seconds.")"""
        
        
        punchline_array= [
                                "\\rspd=88\\ Gosh I love shaking hands. Shake. Shake.  Shake.  You just shake and then your friends.  Its so human.",
                                ]
        
        # clas.tts.post.say("Its an honor.  I assure you.")
        
        times_multiple = 0.35
                
        # Stage: 1 : 
        print("Stage: " + str(1) + ": " + "")
        
        joint_names = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll', 'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
        joint_angles_labeled = [['HeadYaw', 0.06592011451721191], ['HeadPitch', 0.3328361511230469], ['LShoulderPitch', 0.970980167388916], ['LShoulderRoll', 0.30675792694091797], ['LElbowYaw', -0.5047280788421631], ['LElbowRoll', -1.201080083847046], ['LWristYaw', -0.8560140132904053], ['LHand', 0.7495999932289124], ['LHipYawPitch', -0.5997519493103027], ['LHipRoll', 0.27002596855163574], ['LHipPitch', -1.5385600328445435], ['LKneePitch', 1.3974320888519287], ['LAnklePitch', 0.8482601642608643], ['LAnkleRoll', -0.010695934295654297], ['RHipYawPitch', -0.5997519493103027], ['RHipRoll', -0.2592041492462158], ['RHipPitch', -1.5355758666992188], ['RKneePitch', 1.4051861763000488], ['RAnklePitch', 0.8406739234924316], ['RAnkleRoll', 0.019984006881713867], ['RShoulderPitch', 0.5538160800933838], ['RShoulderRoll', 0.2208540439605713], ['RElbowYaw', 1.3590821027755737], ['RElbowRoll', 0.38507604598999023], ['RWristYaw', -0.027653932571411133], ['RHand', 0.7947999835014343]]
        times = [motion_time * times_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
        joint_angles_updated = [angle for _, angle in joint_angles_labeled]
            
        self.robot.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)
        
                    
        # Stage: 2 : 
        print("Stage: " + str(2) + ": " + "")
        
        joint_names = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll', 'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
        joint_angles_labeled = [['HeadYaw', 0.06592011451721191], ['HeadPitch', 0.3328361511230469], ['LShoulderPitch', 0.970980167388916], ['LShoulderRoll', 0.30368995666503906], ['LElbowYaw', -0.5031938552856445], ['LElbowRoll', -1.181138038635254], ['LWristYaw', -0.8575479984283447], ['LHand', 0.7495999932289124], ['LHipYawPitch', -0.5982179641723633], ['LHipRoll', 0.2715599536895752], ['LHipPitch', -1.533958077430725], ['LKneePitch', 1.3958981037139893], ['LAnklePitch', 0.8482601642608643], ['LAnkleRoll', -0.010695934295654297], ['RHipYawPitch', -0.5982179641723633], ['RHipRoll', -0.2592041492462158], ['RHipPitch', -1.526371955871582], ['RKneePitch', 1.4036521911621094], ['RAnklePitch', 0.8406739234924316], ['RAnkleRoll', 0.019984006881713867], ['RShoulderPitch', 0.29917192459106445], ['RShoulderRoll', 0.17176604270935059], ['RElbowYaw', 1.4143060445785522], ['RElbowRoll', 0.5185339450836182], ['RWristYaw', -0.12276196479797363], ['RHand', 0.795199990272522]]
        times = [motion_time * times_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
        joint_angles_updated = [angle for _, angle in joint_angles_labeled]
            
        self.robot.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)
        
                    
        # Stage: 3 : 
        print("Stage: " + str(3) + ": " + "")
        
        joint_names = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll', 'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
        joint_angles_labeled = [['HeadYaw', 0.06592011451721191], ['HeadPitch', 0.3328361511230469], ['LShoulderPitch', 0.970980167388916], ['LShoulderRoll', 0.3052239418029785], ['LElbowYaw', -0.5062620639801025], ['LElbowRoll', -1.1995460987091064], ['LWristYaw', -0.8560140132904053], ['LHand', 0.7495999932289124], ['LHipYawPitch', -0.5982179641723633], ['LHipRoll', 0.27002596855163574], ['LHipPitch', -1.5385600328445435], ['LKneePitch', 1.3974320888519287], ['LAnklePitch', 0.8482601642608643], ['LAnkleRoll', -0.010695934295654297], ['RHipYawPitch', -0.5982179641723633], ['RHipRoll', -0.2592041492462158], ['RHipPitch', -1.5371098518371582], ['RKneePitch', 1.4036521911621094], ['RAnklePitch', 0.8406739234924316], ['RAnkleRoll', 0.019984006881713867], ['RShoulderPitch', 0.7470998764038086], ['RShoulderRoll', 0.16102814674377441], ['RElbowYaw', 1.4173741340637207], ['RElbowRoll', 0.4356980323791504], ['RWristYaw', -0.14270401000976562], ['RHand', 0.7947999835014343]]
        times = [motion_time * times_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
        joint_angles_updated = [angle for _, angle in joint_angles_labeled]
            
        self.robot.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)
        
                    
        # Stage: 4 : 
        print("Stage: " + str(4) + ": " + "")
        
        joint_names = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll', 'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
        joint_angles_labeled = [['HeadYaw', 0.06592011451721191], ['HeadPitch', 0.3328361511230469], ['LShoulderPitch', 0.970980167388916], ['LShoulderRoll', 0.3052239418029785], ['LElbowYaw', -0.5062620639801025], ['LElbowRoll', -1.198012113571167], ['LWristYaw', -0.8560140132904053], ['LHand', 0.7495999932289124], ['LHipYawPitch', -0.5997519493103027], ['LHipRoll', 0.27002596855163574], ['LHipPitch', -1.5385600328445435], ['LKneePitch', 1.3974320888519287], ['LAnklePitch', 0.8482601642608643], ['LAnkleRoll', -0.010695934295654297], ['RHipYawPitch', -0.5997519493103027], ['RHipRoll', -0.2592041492462158], ['RHipPitch', -1.5340418815612793], ['RKneePitch', 1.4036521911621094], ['RAnklePitch', 0.8406739234924316], ['RAnkleRoll', 0.019984006881713867], ['RShoulderPitch', 0.18565607070922852], ['RShoulderRoll', 0.19017410278320312], ['RElbowYaw', 1.4189081192016602], ['RElbowRoll', 0.43109607696533203], ['RWristYaw', -0.14883995056152344], ['RHand', 0.7947999835014343]]
        times = [motion_time * times_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
        joint_angles_updated = [angle for _, angle in joint_angles_labeled]
            
        self.robot.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)
        
                    
        # Stage: 5 : 
        print("Stage: " + str(5) + ": " + "")
        
        joint_names = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll', 'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
        joint_angles_labeled = [['HeadYaw', 0.06592011451721191], ['HeadPitch', 0.3328361511230469], ['LShoulderPitch', 0.970980167388916], ['LShoulderRoll', 0.3052239418029785], ['LElbowYaw', -0.5062620639801025], ['LElbowRoll', -1.2026140689849854], ['LWristYaw', -0.8560140132904053], ['LHand', 0.7495999932289124], ['LHipYawPitch', -0.5997519493103027], ['LHipRoll', 0.2715599536895752], ['LHipPitch', -1.5385600328445435], ['LKneePitch', 1.3989660739898682], ['LAnklePitch', 0.8482601642608643], ['LAnkleRoll', -0.010695934295654297], ['RHipYawPitch', -0.5997519493103027], ['RHipRoll', -0.2592041492462158], ['RHipPitch', -1.5355758666992188], ['RKneePitch', 1.4036521911621094], ['RAnklePitch', 0.8406739234924316], ['RAnkleRoll', 0.019984006881713867], ['RShoulderPitch', 0.6504578590393066], ['RShoulderRoll', 0.2070479393005371], ['RElbowYaw', 1.4158400297164917], ['RElbowRoll', 0.35132789611816406], ['RWristYaw', -0.18719005584716797], ['RHand', 0.7947999835014343]]
        times = [motion_time * times_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
        joint_angles_updated = [angle for _, angle in joint_angles_labeled]
            
        self.robot.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)
        
                    
        # Stage: 6 : 
        print("Stage: " + str(6) + ": " + "")
        
        joint_names = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll', 'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
        joint_angles_labeled = [['HeadYaw', 0.06592011451721191], ['HeadPitch', 0.3328361511230469], ['LShoulderPitch', 0.970980167388916], ['LShoulderRoll', 0.30675792694091797], ['LElbowYaw', -0.5062620639801025], ['LElbowRoll', -1.2041480541229248], ['LWristYaw', -0.8560140132904053], ['LHand', 0.7495999932289124], ['LHipYawPitch', -0.5997519493103027], ['LHipRoll', 0.27002596855163574], ['LHipPitch', -1.5385600328445435], ['LKneePitch', 1.3974320888519287], ['LAnklePitch', 0.8482601642608643], ['LAnkleRoll', -0.010695934295654297], ['RHipYawPitch', -0.5997519493103027], ['RHipRoll', -0.2592041492462158], ['RHipPitch', -1.5325078964233398], ['RKneePitch', 1.4036521911621094], ['RAnklePitch', 0.8406739234924316], ['RAnkleRoll', 0.019984006881713867], ['RShoulderPitch', 0.14117002487182617], ['RShoulderRoll', 0.23312616348266602], ['RElbowYaw', 1.4311801195144653], ['RElbowRoll', 0.3436579704284668], ['RWristYaw', -0.18565607070922852], ['RHand', 0.7947999835014343]]
        times = [motion_time * times_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
        joint_angles_updated = [angle for _, angle in joint_angles_labeled]
            
        self.robot.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)
        
                    
        # Stage: 7 : 
        print("Stage: " + str(7) + ": " + "")
        
        joint_names = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll', 'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
        joint_angles_labeled = [['HeadYaw', 0.06592011451721191], ['HeadPitch', 0.3328361511230469], ['LShoulderPitch', 0.9694461822509766], ['LShoulderRoll', 0.3052239418029785], ['LElbowYaw', -0.5062620639801025], ['LElbowRoll', -1.2026140689849854], ['LWristYaw', -0.8560140132904053], ['LHand', 0.7495999932289124], ['LHipYawPitch', -0.5997519493103027], ['LHipRoll', 0.27002596855163574], ['LHipPitch', -1.5385600328445435], ['LKneePitch', 1.3989660739898682], ['LAnklePitch', 0.8482601642608643], ['LAnkleRoll', -0.010695934295654297], ['RHipYawPitch', -0.5997519493103027], ['RHipRoll', -0.2592041492462158], ['RHipPitch', -1.5340418815612793], ['RKneePitch', 1.4036521911621094], ['RAnklePitch', 0.8406739234924316], ['RAnkleRoll', 0.019984006881713867], ['RShoulderPitch', 0.6228458881378174], ['RShoulderRoll', 0.24846601486206055], ['RElbowYaw', 1.4311801195144653], ['RElbowRoll', 0.3083760738372803], ['RWristYaw', -0.18565607070922852], ['RHand', 0.7947999835014343]]
        times = [motion_time * times_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
        joint_angles_updated = [angle for _, angle in joint_angles_labeled]
            
        self.robot.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)
        
                    
        # Stage: 8 : 
        print("Stage: " + str(8) + ": " + "")
        
        joint_names = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll', 'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
        joint_angles_labeled = [['HeadYaw', 0.06592011451721191], ['HeadPitch', 0.3328361511230469], ['LShoulderPitch', 0.970980167388916], ['LShoulderRoll', 0.30675792694091797], ['LElbowYaw', -0.5062620639801025], ['LElbowRoll', -1.201080083847046], ['LWristYaw', -0.8560140132904053], ['LHand', 0.7495999932289124], ['LHipYawPitch', -0.5997519493103027], ['LHipRoll', 0.27002596855163574], ['LHipPitch', -1.5385600328445435], ['LKneePitch', 1.3974320888519287], ['LAnklePitch', 0.8482601642608643], ['LAnkleRoll', -0.01222991943359375], ['RHipYawPitch', -0.5997519493103027], ['RHipRoll', -0.2592041492462158], ['RHipPitch', -1.5325078964233398], ['RKneePitch', 1.4036521911621094], ['RAnklePitch', 0.8406739234924316], ['RAnkleRoll', 0.019984006881713867], ['RShoulderPitch', 0.14730596542358398], ['RShoulderRoll', 0.2561359405517578], ['RElbowYaw', 1.440384030342102], ['RElbowRoll', 0.3298518657684326], ['RWristYaw', -0.12582993507385254], ['RHand', 0.7947999835014343]]
        times = [motion_time * times_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
        joint_angles_updated = [angle for _, angle in joint_angles_labeled]
            
        self.robot.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)
        
                    
        # Stage: 9 : 
        print("Stage: " + str(9) + ": " + "")
        
        joint_names = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll', 'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
        joint_angles_labeled = [['HeadYaw', 0.06592011451721191], ['HeadPitch', 0.3328361511230469], ['LShoulderPitch', 0.970980167388916], ['LShoulderRoll', 0.30675792694091797], ['LElbowYaw', -0.5062620639801025], ['LElbowRoll', -1.201080083847046], ['LWristYaw', -0.8560140132904053], ['LHand', 0.7495999932289124], ['LHipYawPitch', -0.5997519493103027], ['LHipRoll', 0.27002596855163574], ['LHipPitch', -1.5385600328445435], ['LKneePitch', 1.3974320888519287], ['LAnklePitch', 0.8482601642608643], ['LAnkleRoll', -0.010695934295654297], ['RHipYawPitch', -0.5997519493103027], ['RHipRoll', -0.2592041492462158], ['RHipPitch', -1.5325078964233398], ['RKneePitch', 1.4036521911621094], ['RAnklePitch', 0.8406739234924316], ['RAnkleRoll', 0.019984006881713867], ['RShoulderPitch', 0.5568840503692627], ['RShoulderRoll', 0.2469320297241211], ['RElbowYaw', 1.440384030342102], ['RElbowRoll', 0.3099100589752197], ['RWristYaw', -0.12276196479797363], ['RHand', 0.7947999835014343]]
        times = [motion_time * times_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
        joint_angles_updated = [angle for _, angle in joint_angles_labeled]
            
        self.robot.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)
        
                    
        # Stage: 10 : 
        print("Stage: " + str(10) + ": " + "")
        
        joint_names = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll', 'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
        joint_angles_labeled = [['HeadYaw', 0.06592011451721191], ['HeadPitch', 0.3328361511230469], ['LShoulderPitch', 0.970980167388916], ['LShoulderRoll', 0.3052239418029785], ['LElbowYaw', -0.5031938552856445], ['LElbowRoll', -1.1765360832214355], ['LWristYaw', -0.8560140132904053], ['LHand', 0.7495999932289124], ['LHipYawPitch', -0.5982179641723633], ['LHipRoll', 0.2715599536895752], ['LHipPitch', -1.5324240922927856], ['LKneePitch', 1.3958981037139893], ['LAnklePitch', 0.8482601642608643], ['LAnkleRoll', -0.010695934295654297], ['RHipYawPitch', -0.5982179641723633], ['RHipRoll', -0.2592041492462158], ['RHipPitch', -1.5248379707336426], ['RKneePitch', 1.4036521911621094], ['RAnklePitch', 0.8406739234924316], ['RAnkleRoll', 0.019984006881713867], ['RShoulderPitch', 0.46944594383239746], ['RShoulderRoll', -0.6750020980834961], ['RElbowYaw', 1.4388500452041626], ['RElbowRoll', 0.3958139419555664], ['RWristYaw', -0.11816000938415527], ['RHand', 0.7947999835014343]]
        times = [motion_time * 0.6 for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
        joint_angles_updated = [angle for _, angle in joint_angles_labeled]
            
        self.robot.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)
        
                    
        # Stage: 11 : 
        print("Stage: " + str(11) + ": " + "")
        
        joint_names = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll', 'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
        joint_angles_labeled = [['HeadYaw', 0.06592011451721191], ['HeadPitch', 0.3328361511230469], ['LShoulderPitch', 0.9725141525268555], ['LShoulderRoll', 0.3052239418029785], ['LElbowYaw', -0.5047280788421631], ['LElbowRoll', -1.1872740983963013], ['LWristYaw', -0.8560140132904053], ['LHand', 0.7495999932289124], ['LHipYawPitch', -0.5997519493103027], ['LHipRoll', 0.2715599536895752], ['LHipPitch', -1.537026047706604], ['LKneePitch', 1.3974320888519287], ['LAnklePitch', 0.8482601642608643], ['LAnkleRoll', -0.010695934295654297], ['RHipYawPitch', -0.5997519493103027], ['RHipRoll', -0.25766992568969727], ['RHipPitch', -1.5325078964233398], ['RKneePitch', 1.4051861763000488], ['RAnklePitch', 0.8406739234924316], ['RAnkleRoll', 0.019984006881713867], ['RShoulderPitch', 0.9219760894775391], ['RShoulderRoll', -0.24088001251220703], ['RElbowYaw', 0.4693620204925537], ['RElbowRoll', 1.0845799446105957], ['RWristYaw', 0.1978440284729004], ['RHand', 0.7947999835014343]]
        times = [motion_time * 1 for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
        joint_angles_updated = [angle for _, angle in joint_angles_labeled]
            
        self.robot.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)
        
        time.sleep(3.5)
        
        self.robot.tts.post.say(random.choice(punchline_array))  

        time.sleep(1)

    def right_hand_shake_meta(self):
        times_multiple = 1
        shake_multiple = 0.35             
        stand = False
        if stand:                      

            joint_names = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll', 'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
            
            # Stage: 2 : up
            joint_angles_labeled = [['HeadYaw', 0.02603602409362793], ['HeadPitch', 0.2], ['LShoulderPitch', 1.4327141046524048], ['LShoulderRoll', 0.08125996589660645], ['LElbowYaw', -1.3346219062805176], ['LElbowRoll', -0.1748340129852295], ['LWristYaw', -0.06447005271911621], ['LHand', 0.2964000105857849], ['LHipYawPitch', -0.16869807243347168], ['LHipRoll', 0.12122797966003418], ['LHipPitch', 0.13196587562561035], ['LKneePitch', -0.09054803848266602], ['LAnklePitch', 0.09199810028076172], ['LAnkleRoll', -0.11500811576843262], ['RHipYawPitch', -0.16869807243347168], ['RHipRoll', -0.12114405632019043], ['RHipPitch', 0.1288139820098877], ['RKneePitch', -0.09506607055664062], ['RAnklePitch', 0.09054803848266602], ['RAnkleRoll', 0.11355805397033691], ['RShoulderPitch', 0.19792795181274414], ['RShoulderRoll', 0.11194014549255371], ['RElbowYaw', 1.274712085723877], ['RElbowRoll', 0.6013698577880859], ['RWristYaw', 0.004559993743896484], ['RHand', 0.3108000159263611]]
            times = [motion_time * shake_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
            joint_angles_updated = [angle for _, angle in joint_angles_labeled]    
            self.robot.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)        
                            
            # Stage: 3 : down
            joint_angles_labeled = [['HeadYaw', 0.024502038955688477], ['HeadPitch', -0.2], ['LShoulderPitch', 1.4327141046524048], ['LShoulderRoll', 0.08125996589660645], ['LElbowYaw', -1.3346219062805176], ['LElbowRoll', -0.1748340129852295], ['LWristYaw', -0.06447005271911621], ['LHand', 0.29600000381469727], ['LHipYawPitch', -0.17023205757141113], ['LHipRoll', 0.11969399452209473], ['LHipPitch', 0.13196587562561035], ['LKneePitch', -0.09054803848266602], ['LAnklePitch', 0.09046411514282227], ['LAnkleRoll', -0.11347413063049316], ['RHipYawPitch', -0.17023205757141113], ['RHipRoll', -0.12114405632019043], ['RHipPitch', 0.12727999687194824], ['RKneePitch', -0.09506607055664062], ['RAnklePitch', 0.09054803848266602], ['RAnkleRoll', 0.11355805397033691], ['RShoulderPitch', 0.8606162071228027], ['RShoulderRoll', 0.13341593742370605], ['RElbowYaw', 1.274712085723877], ['RElbowRoll', 0.2853660583496094], ['RWristYaw', 0.0060939788818359375], ['RHand', 0.3108000159263611]]
            times = [motion_time * shake_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
            joint_angles_updated = [angle for _, angle in joint_angles_labeled]    
            self.robot.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)        
                            
            # Stage: 4 : up
            joint_angles_labeled = [['HeadYaw', 0.02603602409362793], ['HeadPitch', 0.2], ['LShoulderPitch', 1.4327141046524048], ['LShoulderRoll', 0.08125996589660645], ['LElbowYaw', -1.3346219062805176], ['LElbowRoll', -0.17636799812316895], ['LWristYaw', -0.06447005271911621], ['LHand', 0.2964000105857849], ['LHipYawPitch', -0.16869807243347168], ['LHipRoll', 0.12122797966003418], ['LHipPitch', 0.13196587562561035], ['LKneePitch', -0.09208202362060547], ['LAnklePitch', 0.09199810028076172], ['LAnkleRoll', -0.11347413063049316], ['RHipYawPitch', -0.16869807243347168], ['RHipRoll', -0.11961007118225098], ['RHipPitch', 0.13034796714782715], ['RKneePitch', -0.09353208541870117], ['RAnklePitch', 0.09054803848266602], ['RAnkleRoll', 0.11355805397033691], ['RShoulderPitch', 0.1334998607635498], ['RShoulderRoll', 0.19017410278320312], ['RElbowYaw', 1.3069260120391846], ['RElbowRoll', 0.42342591285705566], ['RWristYaw', 0.029103994369506836], ['RHand', 0.3108000159263611]]
            times = [motion_time * shake_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
            joint_angles_updated = [angle for _, angle in joint_angles_labeled]    
            self.robot.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)        
                            
            # Stage: 5 : down
            joint_angles_labeled = [['HeadYaw', 0.024502038955688477], ['HeadPitch', -0.2], ['LShoulderPitch', 1.4327141046524048], ['LShoulderRoll', 0.08125996589660645], ['LElbowYaw', -1.3346219062805176], ['LElbowRoll', -0.1748340129852295], ['LWristYaw', -0.06447005271911621], ['LHand', 0.2964000105857849], ['LHipYawPitch', -0.16869807243347168], ['LHipRoll', 0.12122797966003418], ['LHipPitch', 0.13196587562561035], ['LKneePitch', -0.09208202362060547], ['LAnklePitch', 0.09199810028076172], ['LAnkleRoll', -0.11347413063049316], ['RHipYawPitch', -0.16869807243347168], ['RHipRoll', -0.12114405632019043], ['RHipPitch', 0.1288139820098877], ['RKneePitch', -0.09506607055664062], ['RAnklePitch', 0.09054803848266602], ['RAnkleRoll', 0.11355805397033691], ['RShoulderPitch', 0.9511218070983887], ['RShoulderRoll', 0.1088719367980957], ['RElbowYaw', 1.3069260120391846], ['RElbowRoll', 0.3467259407043457], ['RWristYaw', 0.03063797950744629], ['RHand', 0.3108000159263611]]
            times = [motion_time * shake_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
            joint_angles_updated = [angle for _, angle in joint_angles_labeled]    
            self.robot.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)

            # Stage: 5.25 : up
            joint_angles_labeled = [['HeadYaw', 0.02603602409362793], ['HeadPitch', 0.2], ['LShoulderPitch', 1.4327141046524048], ['LShoulderRoll', 0.08125996589660645], ['LElbowYaw', -1.3346219062805176], ['LElbowRoll', -0.17636799812316895], ['LWristYaw', -0.06447005271911621], ['LHand', 0.2964000105857849], ['LHipYawPitch', -0.16869807243347168], ['LHipRoll', 0.12122797966003418], ['LHipPitch', 0.13196587562561035], ['LKneePitch', -0.09208202362060547], ['LAnklePitch', 0.09199810028076172], ['LAnkleRoll', -0.11347413063049316], ['RHipYawPitch', -0.16869807243347168], ['RHipRoll', -0.11961007118225098], ['RHipPitch', 0.13034796714782715], ['RKneePitch', -0.09353208541870117], ['RAnklePitch', 0.09054803848266602], ['RAnkleRoll', 0.11355805397033691], ['RShoulderPitch', 0.1334998607635498], ['RShoulderRoll', 0.19017410278320312], ['RElbowYaw', 1.3069260120391846], ['RElbowRoll', 0.42342591285705566], ['RWristYaw', 0.029103994369506836], ['RHand', 0.3108000159263611]]
            times = [motion_time * shake_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
            joint_angles_updated = [angle for _, angle in joint_angles_labeled]    
            self.robot.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)        
                            
            # Stage: 5.75 : down
            joint_angles_labeled = [['HeadYaw', 0.024502038955688477], ['HeadPitch', -0.2], ['LShoulderPitch', 1.4327141046524048], ['LShoulderRoll', 0.08125996589660645], ['LElbowYaw', -1.3346219062805176], ['LElbowRoll', -0.1748340129852295], ['LWristYaw', -0.06447005271911621], ['LHand', 0.2964000105857849], ['LHipYawPitch', -0.16869807243347168], ['LHipRoll', 0.12122797966003418], ['LHipPitch', 0.13196587562561035], ['LKneePitch', -0.09208202362060547], ['LAnklePitch', 0.09199810028076172], ['LAnkleRoll', -0.11347413063049316], ['RHipYawPitch', -0.16869807243347168], ['RHipRoll', -0.12114405632019043], ['RHipPitch', 0.1288139820098877], ['RKneePitch', -0.09506607055664062], ['RAnklePitch', 0.09054803848266602], ['RAnkleRoll', 0.11355805397033691], ['RShoulderPitch', 0.9511218070983887], ['RShoulderRoll', 0.1088719367980957], ['RElbowYaw', 1.3069260120391846], ['RElbowRoll', 0.3467259407043457], ['RWristYaw', 0.03063797950744629], ['RHand', 0.3108000159263611]]
            times = [motion_time * shake_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
            joint_angles_updated = [angle for _, angle in joint_angles_labeled]    
            self.robot.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)          
                            
            # Stage: 6 : up
            joint_angles_labeled = [['HeadYaw', 0.02603602409362793], ['HeadPitch', 0.2], ['LShoulderPitch', 1.4327141046524048], ['LShoulderRoll', 0.08125996589660645], ['LElbowYaw', -1.3346219062805176], ['LElbowRoll', -0.1748340129852295], ['LWristYaw', -0.06447005271911621], ['LHand', 0.2964000105857849], ['LHipYawPitch', -0.16869807243347168], ['LHipRoll', 0.12122797966003418], ['LHipPitch', 0.13196587562561035], ['LKneePitch', -0.09208202362060547], ['LAnklePitch', 0.09199810028076172], ['LAnkleRoll', -0.11347413063049316], ['RHipYawPitch', -0.16869807243347168], ['RHipRoll', -0.12114405632019043], ['RHipPitch', 0.13034796714782715], ['RKneePitch', -0.09353208541870117], ['RAnklePitch', 0.09054803848266602], ['RAnkleRoll', 0.11355805397033691], ['RShoulderPitch', 0.03072190284729004], ['RShoulderRoll', 0.11807608604431152], ['RElbowYaw', 1.3069260120391846], ['RElbowRoll', 0.4755818843841553], ['RWristYaw', 0.02603602409362793], ['RHand', 0.3108000159263611]]
            times = [motion_time * shake_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
            joint_angles_updated = [angle for _, angle in joint_angles_labeled]    
            self.robot.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)        
            
            # Stage: 7 : down
            joint_angles_labeled = [['HeadYaw', 0.02603602409362793], ['HeadPitch', -0.03], ['LShoulderPitch', 1.4327141046524048], ['LShoulderRoll', 0.0827939510345459], ['LElbowYaw', -1.3346219062805176], ['LElbowRoll', -0.1748340129852295], ['LWristYaw', -0.06447005271911621], ['LHand', 0.2964000105857849], ['LHipYawPitch', -0.17023205757141113], ['LHipRoll', 0.12122797966003418], ['LHipPitch', 0.13196587562561035], ['LKneePitch', -0.09361600875854492], ['LAnklePitch', 0.09046411514282227], ['LAnkleRoll', -0.11500811576843262], ['RHipYawPitch', -0.17023205757141113], ['RHipRoll', -0.12114405632019043], ['RHipPitch', 0.1288139820098877], ['RKneePitch', -0.09506607055664062], ['RAnklePitch', 0.08901405334472656], ['RAnkleRoll', 0.11355805397033691], ['RShoulderPitch', 0.8636841773986816], ['RShoulderRoll', 0.12114405632019043], ['RElbowYaw', 1.3069260120391846], ['RElbowRoll', 0.38507604598999023], ['RWristYaw', 0.027570009231567383], ['RHand', 0.3108000159263611]]
            times = [motion_time * shake_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
            joint_angles_updated = [angle for _, angle in joint_angles_labeled]    
            self.robot.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)        
                            
            # Stage: 8 : out
            joint_angles_labeled = [['HeadYaw', 0.02603602409362793], ['HeadPitch', -0.03072190284729004], ['LShoulderPitch', 1.4327141046524048], ['LShoulderRoll', 0.07972598075866699], ['LElbowYaw', -1.3346219062805176], ['LElbowRoll', -0.1748340129852295], ['LWristYaw', -0.06447005271911621], ['LHand', 0.2964000105857849], ['LHipYawPitch', -0.16716408729553223], ['LHipRoll', 0.12122797966003418], ['LHipPitch', 0.13196587562561035], ['LKneePitch', -0.09208202362060547], ['LAnklePitch', 0.09353208541870117], ['LAnkleRoll', -0.11500811576843262], ['RHipYawPitch', -0.16716408729553223], ['RHipRoll', -0.12114405632019043], ['RHipPitch', 0.13034796714782715], ['RKneePitch', -0.09353208541870117], ['RAnklePitch', 0.09208202362060547], ['RAnkleRoll', 0.11355805397033691], ['RShoulderPitch', 0.5430779457092285], ['RShoulderRoll', -0.3436579704284668], ['RElbowYaw', 1.294654130935669], ['RElbowRoll', 0.4249598979949951], ['RWristYaw', -0.6857399940490723], ['RHand', 0.3108000159263611]]
            times = [motion_time * shake_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
            joint_angles_updated = [angle for _, angle in joint_angles_labeled]    
            self.robot.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)        
                
            # Stage: 9 : in
            joint_angles_labeled = [['HeadYaw', 0.14415407180786133], ['HeadPitch', -0.03072190284729004], ['LShoulderPitch', 1.4327141046524048], ['LShoulderRoll', 0.07819199562072754], ['LElbowYaw', -1.3346219062805176], ['LElbowRoll', -0.1748340129852295], ['LWristYaw', -0.06447005271911621], ['LHand', 0.2964000105857849], ['LHipYawPitch', -0.16716408729553223], ['LHipRoll', 0.12122797966003418], ['LHipPitch', 0.13196587562561035], ['LKneePitch', -0.09054803848266602], ['LAnklePitch', 0.09353208541870117], ['LAnkleRoll', -0.11347413063049316], ['RHipYawPitch', -0.16716408729553223], ['RHipRoll', -0.12114405632019043], ['RHipPitch', 0.13034796714782715], ['RKneePitch', -0.09199810028076172], ['RAnklePitch', 0.09361600875854492], ['RAnkleRoll', 0.11355805397033691], ['RShoulderPitch', 1.392913818359375], ['RShoulderRoll', 0.042910099029541016], ['RElbowYaw', 1.2961881160736084], ['RElbowRoll', 0.31297802925109863], ['RWristYaw', -0.1365680694580078], ['RHand', 0.3108000159263611]]
            times = [motion_time * times_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
            joint_angles_updated = [angle for _, angle in joint_angles_labeled]    
            self.robot.motion.angleInterpolation(joint_names, joint_angles_updated, times, True) 
            
            time.sleep(1)
        
            self.robot.tts.post.say("I am looking forward to playing with you.")
            joint_names_list = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
            joint_angles = [angles_compressed for _, angles_compressed in [['HeadYaw', [-0.010779857635498047, -0.010779857635498047, -0.010779857635498047, -0.010779857635498047]], ['HeadPitch', [-0.16418004035949707, -0.16418004035949707, -0.16418004035949707, -0.16571402549743652]], ['LShoulderPitch', [1.3268680572509766, 1.3268680572509766, 1.3943641185760498, 1.3023240566253662]], ['LShoulderRoll', [-0.08901405334472656, -0.09054803848266602, -0.0844118595123291, -0.013848066329956055]], ['LElbowYaw', [-0.7593719959259033, -0.7593719959259033, -0.8943638801574707, -1.0140161514282227]], ['LElbowRoll', [-1.52168607711792, -1.5170841217041016, -1.2869840860366821, -0.07359004020690918]], ['LWristYaw', [-0.21326804161071777, -0.21173405647277832, -0.7854499816894531, -0.4019498825073242]], ['LHand', [0.2943999767303467, 0.2947999835014343, 0.2947999835014343, 0.2943999767303467]], ['RShoulderPitch', [0.9664621353149414, 0.9679961204528809, 1.0247540473937988, 1.322350025177002]], ['RShoulderRoll', [0.1318819522857666, 0.1349501609802246, 0.1487560272216797, 0.05364799499511719]], ['RElbowYaw', [1.2823820114135742, 1.2823820114135742, 1.2977221012115479, 1.3207321166992188]], ['RElbowRoll', [1.0201520919799805, 1.0201520919799805, 1.0815119743347168, 0.047595977783203125]], ['RWristYaw', [0.2208540439605713, 0.22238802909851074, 1.0906319618225098, 0.28374814987182617]], ['RHand', [0.30720001459121704, 0.30720001459121704, 0.30720001459121704, 0.30720001459121704]]]]
            time_points = [time_points_compressed for _, time_points_compressed in [['HeadYaw', [0.77, 1.37, 1.9700000000000002, 2.5700000000000003]], ['HeadPitch', [0.77, 1.37, 1.9700000000000002, 2.5700000000000003]], ['LShoulderPitch', [0.77, 1.37, 1.9700000000000002, 2.5700000000000003]], ['LShoulderRoll', [0.77, 1.37, 1.9700000000000002, 2.5700000000000003]], ['LElbowYaw', [0.77, 1.37, 1.9700000000000002, 2.5700000000000003]], ['LElbowRoll', [0.77, 1.37, 1.9700000000000002, 2.5700000000000003]], ['LWristYaw', [0.77, 1.37, 1.9700000000000002, 2.5700000000000003]], ['LHand', [0.77, 1.37, 1.9700000000000002, 2.5700000000000003]], ['RShoulderPitch', [0.77, 1.37, 1.9700000000000002, 2.5700000000000003]], ['RShoulderRoll', [0.77, 1.37, 1.9700000000000002, 2.5700000000000003]], ['RElbowYaw', [0.77, 1.37, 1.9700000000000002, 2.5700000000000003]], ['RElbowRoll', [0.77, 1.37, 1.9700000000000002, 2.5700000000000003]], ['RWristYaw', [0.77, 1.37, 1.9700000000000002, 2.5700000000000003]], ['RHand', [0.77, 1.37, 1.9700000000000002, 2.5700000000000003]]]]
            self.robot.motion.angleInterpolation(joint_names_list, joint_angles, time_points, True)

        else:
                            
            angle_modulator = 1.0
            duration_modulator = 1.0
                    
            joint_names_list = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
                        
            # Movement: 1 : down
            print("Stage: " + str(1) + ": " + "down")
            joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.09660005569458008], ['HeadPitch', 0.33743810653686523], ['LShoulderPitch', 0.9556400775909424], ['LShoulderRoll', 0.3220980167388916], ['LElbowYaw', -0.4648439884185791], ['LElbowRoll', -1.2118180990219116], ['LWristYaw', 0.03523993492126465], ['LHand', 0.30479997396469116], ['RShoulderPitch', 0.5691559314727783], ['RShoulderRoll', 0.24846601486206055], ['RElbowYaw', 0.7562201023101807], ['RElbowRoll', 0.2654240131378174], ['RWristYaw', -0.09361600875854492], ['RHand', 0.1]]]
            action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.35], ['HeadPitch', 0.35], ['LShoulderPitch', 0.35], ['LShoulderRoll', 0.35], ['LElbowYaw', 0.35], ['LElbowRoll', 0.35], ['LWristYaw', 0.35], ['LHand', 0.35], ['RShoulderPitch', 0.35], ['RShoulderRoll', 0.35], ['RElbowYaw', 0.35], ['RElbowRoll', 0.35], ['RWristYaw', 0.35], ['RHand', 0.35]]]
            self.robot.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
                
            # Movement: 2 : up
            print("Stage: " + str(2) + ": " + "up")
            joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.09660005569458008], ['HeadPitch', 0.1840381622314453], ['LShoulderPitch', 0.9571740627288818], ['LShoulderRoll', 0.32056403160095215], ['LElbowYaw', -0.4709799289703369], ['LElbowRoll', -1.2118180990219116], ['LWristYaw', 0.0367741584777832], ['LHand', 0.30479997396469116], ['RShoulderPitch', 0.027653932571411133], ['RShoulderRoll', 0.27761197090148926], ['RElbowYaw', 0.7838320732116699], ['RElbowRoll', 0.2853660583496094], ['RWristYaw', 0.6089560985565186], ['RHand', 0.1]]]
            action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.35], ['HeadPitch', 0.35], ['LShoulderPitch', 0.35], ['LShoulderRoll', 0.35], ['LElbowYaw', 0.35], ['LElbowRoll', 0.35], ['LWristYaw', 0.35], ['LHand', 0.35], ['RShoulderPitch', 0.35], ['RShoulderRoll', 0.35], ['RElbowYaw', 0.35], ['RElbowRoll', 0.35], ['RWristYaw', 0.35], ['RHand', 0.35]]]
            self.robot.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
                
            # Movement: 3 : d
            print("Stage: " + str(3) + ": " + "d")
            joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.1318819522857666], ['HeadPitch', 0.3803901672363281], ['LShoulderPitch', 0.9587080478668213], ['LShoulderRoll', 0.3190300464630127], ['LElbowYaw', -0.4786500930786133], ['LElbowRoll', -1.2087500095367432], ['LWristYaw', 0.04137611389160156], ['LHand', 0.3051999807357788], ['RShoulderPitch', 0.5430779457092285], ['RShoulderRoll', 0.24846601486206055], ['RElbowYaw', 0.8543961048126221], ['RElbowRoll', 0.03072190284729004], ['RWristYaw', 0.5521979331970215], ['RHand', 0.1]]]
            action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.35], ['HeadPitch', 0.35], ['LShoulderPitch', 0.35], ['LShoulderRoll', 0.35], ['LElbowYaw', 0.35], ['LElbowRoll', 0.35], ['LWristYaw', 0.35], ['LHand', 0.35], ['RShoulderPitch', 0.35], ['RShoulderRoll', 0.35], ['RElbowYaw', 0.35], ['RElbowRoll', 0.35], ['RWristYaw', 0.35], ['RHand', 0.35]]]
            self.robot.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
                
            # Movement: 4 : u
            print("Stage: " + str(4) + ": " + "u")
            joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.1318819522857666], ['HeadPitch', 0.3803901672363281], ['LShoulderPitch', 0.9587080478668213], ['LShoulderRoll', 0.31749606132507324], ['LElbowYaw', -0.4847860336303711], ['LElbowRoll', -1.2118180990219116], ['LWristYaw', 0.042910099029541016], ['LHand', 0.30479997396469116], ['RShoulderPitch', -0.14262008666992188], ['RShoulderRoll', 0.11961007118225098], ['RElbowYaw', 0.8758721351623535], ['RElbowRoll', 0.029187917709350586], ['RWristYaw', 0.6457719802856445], ['RHand', 0.1]]]
            action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.35], ['HeadPitch', 0.35], ['LShoulderPitch', 0.35], ['LShoulderRoll', 0.35], ['LElbowYaw', 0.35], ['LElbowRoll', 0.35], ['LWristYaw', 0.35], ['LHand', 0.35], ['RShoulderPitch', 0.35], ['RShoulderRoll', 0.35], ['RElbowYaw', 0.35], ['RElbowRoll', 0.35], ['RWristYaw', 0.35], ['RHand', 0.35]]]
            self.robot.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)

            # Movement: 2 : up
            print("Stage: " + str(2) + ": " + "up")
            joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.09660005569458008], ['HeadPitch', 0.1840381622314453], ['LShoulderPitch', 0.9571740627288818], ['LShoulderRoll', 0.32056403160095215], ['LElbowYaw', -0.4709799289703369], ['LElbowRoll', -1.2118180990219116], ['LWristYaw', 0.0367741584777832], ['LHand', 0.30479997396469116], ['RShoulderPitch', 0.027653932571411133], ['RShoulderRoll', 0.27761197090148926], ['RElbowYaw', 0.7838320732116699], ['RElbowRoll', 0.2853660583496094], ['RWristYaw', 0.6089560985565186], ['RHand', 0.1]]]
            action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.35], ['HeadPitch', 0.35], ['LShoulderPitch', 0.35], ['LShoulderRoll', 0.35], ['LElbowYaw', 0.35], ['LElbowRoll', 0.35], ['LWristYaw', 0.35], ['LHand', 0.35], ['RShoulderPitch', 0.35], ['RShoulderRoll', 0.35], ['RElbowYaw', 0.35], ['RElbowRoll', 0.35], ['RWristYaw', 0.35], ['RHand', 0.35]]]
            self.robot.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
                
            # Movement: 3 : d
            print("Stage: " + str(3) + ": " + "d")
            joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.1318819522857666], ['HeadPitch', 0.3803901672363281], ['LShoulderPitch', 0.9587080478668213], ['LShoulderRoll', 0.3190300464630127], ['LElbowYaw', -0.4786500930786133], ['LElbowRoll', -1.2087500095367432], ['LWristYaw', 0.04137611389160156], ['LHand', 0.3051999807357788], ['RShoulderPitch', 0.5430779457092285], ['RShoulderRoll', 0.24846601486206055], ['RElbowYaw', 0.8543961048126221], ['RElbowRoll', 0.03072190284729004], ['RWristYaw', 0.5521979331970215], ['RHand', 0.1]]]
            action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.35], ['HeadPitch', 0.35], ['LShoulderPitch', 0.35], ['LShoulderRoll', 0.35], ['LElbowYaw', 0.35], ['LElbowRoll', 0.35], ['LWristYaw', 0.35], ['LHand', 0.35], ['RShoulderPitch', 0.35], ['RShoulderRoll', 0.35], ['RElbowYaw', 0.35], ['RElbowRoll', 0.35], ['RWristYaw', 0.35], ['RHand', 0.35]]]
            self.robot.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
                
            # Movement: 5 : out
            print("Stage: " + str(5) + ": " + "out")
            joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.1288139820098877], ['HeadPitch', 0.19017410278320312], ['LShoulderPitch', 0.9663779735565186], ['LShoulderRoll', 0.3190300464630127], ['LElbowYaw', -0.49245595932006836], ['LElbowRoll', -1.213352084159851], ['LWristYaw', 0.038308143615722656], ['LHand', 0.3051999807357788], ['RShoulderPitch', -0.7393460273742676], ['RShoulderRoll', -0.6105740070343018], ['RElbowYaw', 0.9280281066894531], ['RElbowRoll', 0.6059720516204834], ['RWristYaw', 0.4540219306945801], ['RHand', 0.1]]]
            action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.6], ['HeadPitch', 0.6], ['LShoulderPitch', 0.6], ['LShoulderRoll', 0.6], ['LElbowYaw', 0.6], ['LElbowRoll', 0.6], ['LWristYaw', 0.6], ['LHand', 0.6], ['RShoulderPitch', 0.6], ['RShoulderRoll', 0.6], ['RElbowYaw', 0.6], ['RElbowRoll', 0.6], ['RWristYaw', 0.6], ['RHand', 0.6]]]
            self.robot.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
                
            # Movement: 6 : down
            print("Stage: " + str(6) + ": " + "down")
            joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.1288139820098877], ['HeadPitch', 0.19017410278320312], ['LShoulderPitch', 0.967911958694458], ['LShoulderRoll', 0.32056403160095215], ['LElbowYaw', -0.49552392959594727], ['LElbowRoll', -1.2179540395736694], ['LWristYaw', 0.0367741584777832], ['LHand', 0.30479997396469116], ['RShoulderPitch', 0.748633861541748], ['RShoulderRoll', -0.24701595306396484], ['RElbowYaw', 0.11654210090637207], ['RElbowRoll', 1.1167941093444824], ['RWristYaw', -0.07827591896057129], ['RHand', 0.1]]]
            action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 1.5], ['HeadPitch', 1.5], ['LShoulderPitch', 1.5], ['LShoulderRoll', 1.5], ['LElbowYaw', 1.5], ['LElbowRoll', 1.5], ['LWristYaw', 1.5], ['LHand', 1.5], ['RShoulderPitch', 1.5], ['RShoulderRoll', 1.5], ['RElbowYaw', 1.5], ['RElbowRoll', 1.5], ['RWristYaw', 1.5], ['RHand', 1.5]]]
            self.robot.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)                

            time.sleep(1)

        files.save_file(config_pw.handshook_path_meta, "shook")

    def hankie(self):
        times_multiple = 1.0
        wipe_multiple = .5
        bin_multiple = .3
        
        #stage_1
        joint_names = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll', 'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
        joint_angles_labeled = [['HeadYaw', -0.015382051467895508], ['HeadPitch', 0.25], ['LShoulderPitch', 0.9264941215515137], ['LShoulderRoll', 0.2607381343841553], ['LElbowYaw', -0.4356980323791504], ['LElbowRoll', -1.1489241123199463], ['LWristYaw', 0.01222991943359375], ['LHand', 0.2943999767303467], ['LHipYawPitch', -0.5966839790344238], ['LHipRoll', 0.27002596855163574], ['LHipPitch', -1.5308901071548462], ['LKneePitch', 1.3958981037139893], ['LAnklePitch', 0.8329200744628906], ['LAnkleRoll', -0.015298128128051758], ['RHipYawPitch', -0.5966839790344238], ['RHipRoll', -0.2622721195220947], ['RHipPitch', -1.5202360153198242], ['RKneePitch', 1.4067201614379883], ['RAnklePitch', 0.8406739234924316], ['RAnkleRoll', 0.019984006881713867], ['RShoulderPitch', 0.6903419494628906], ['RShoulderRoll', 0.09966802597045898], ['RElbowYaw', 1.5615700483322144], ['RElbowRoll', 0.7424979209899902], ['RWristYaw', 0.22238802909851074], ['RHand', 0]]
        times = [motion_time * times_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
        joint_angles_updated = [angle for _, angle in joint_angles_labeled]
            
        self.robot.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)
            
        #stage_2
        joint_names = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll', 'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
        joint_angles_labeled = [['HeadYaw', -0.015382051467895508], ['HeadPitch', 0.25], ['LShoulderPitch', 0.9280281066894531], ['LShoulderRoll', 0.2592041492462158], ['LElbowYaw', -0.4387660026550293], ['LElbowRoll', -1.1305160522460938], ['LWristYaw', 0.01222991943359375], ['LHand', 0.2943999767303467], ['LHipYawPitch', -0.5966839790344238], ['LHipRoll', 0.27002596855163574], ['LHipPitch', -1.5324240922927856], ['LKneePitch', 1.3958981037139893], ['LAnklePitch', 0.8329200744628906], ['LAnkleRoll', -0.015298128128051758], ['RHipYawPitch', -0.5966839790344238], ['RHipRoll', -0.2622721195220947], ['RHipPitch', -1.5202360153198242], ['RKneePitch', 1.4082541465759277], ['RAnklePitch', 0.8406739234924316], ['RAnkleRoll', 0.019984006881713867], ['RShoulderPitch', -0.19631004333496094], ['RShoulderRoll', 0.0827939510345459], ['RElbowYaw', 1.3805580139160156], ['RElbowRoll', 1.5478482246398926], ['RWristYaw', 0.31749606132507324], ['RHand', 0]]
        times = [motion_time * times_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
        joint_angles_updated = [angle for _, angle in joint_angles_labeled]
            
        self.robot.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)
            
        #stage_3
        joint_names = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll', 'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
        joint_angles_labeled = [['HeadYaw', 0.013764142990112305], ['HeadPitch', 0.23159193992614746], ['LShoulderPitch', 0.9341640472412109], ['LShoulderRoll', 0.2592041492462158], ['LElbowYaw', -0.45717406272888184], ['LElbowRoll', -1.1121079921722412], ['LWristYaw', 0.01222991943359375], ['LHand', 0.29399996995925903], ['LHipYawPitch', -0.5966839790344238], ['LHipRoll', 0.27002596855163574], ['LHipPitch', -1.5308901071548462], ['LKneePitch', 1.3943641185760498], ['LAnklePitch', 0.8329200744628906], ['LAnkleRoll', -0.015298128128051758], ['RHipYawPitch', -0.5966839790344238], ['RHipRoll', -0.2622721195220947], ['RHipPitch', -1.5202360153198242], ['RKneePitch', 1.4067201614379883], ['RAnklePitch', 0.8406739234924316], ['RAnkleRoll', 0.019984006881713867], ['RShoulderPitch', -0.9663779735565186], ['RShoulderRoll', -0.3068418502807617], ['RElbowYaw', 0.9402999877929688], ['RElbowRoll', 1.5555181503295898], ['RWristYaw', 0.6917920112609863], ['RHand', 0]]
        times = [motion_time * wipe_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
        joint_angles_updated = [angle for _, angle in joint_angles_labeled]
            
        self.robot.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)
            
        #stage_4
        joint_names = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll', 'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
        joint_angles_labeled = [['HeadYaw', -0.2684919834136963], ['HeadPitch', 0.5844120979309082], ['LShoulderPitch', 0.9326300621032715], ['LShoulderRoll', 0.2592041492462158], ['LElbowYaw', -0.46637797355651855], ['LElbowRoll', -1.1090400218963623], ['LWristYaw', 0.01222991943359375], ['LHand', 0.29399996995925903], ['LHipYawPitch', -0.5966839790344238], ['LHipRoll', 0.27002596855163574], ['LHipPitch', -1.5324240922927856], ['LKneePitch', 1.3928301334381104], ['LAnklePitch', 0.8329200744628906], ['LAnkleRoll', -0.015298128128051758], ['RHipYawPitch', -0.5966839790344238], ['RHipRoll', -0.2622721195220947], ['RHipPitch', -1.5187020301818848], ['RKneePitch', 1.4005842208862305], ['RAnklePitch', 0.8406739234924316], ['RAnkleRoll', 0.019984006881713867], ['RShoulderPitch', -0.12421202659606934], ['RShoulderRoll', -0.3988819122314453], ['RElbowYaw', 0.9157559871673584], ['RElbowRoll', 1.5539841651916504], ['RWristYaw', 0.6994619369506836], ['RHand', 0]]
        times = [motion_time * wipe_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
        joint_angles_updated = [angle for _, angle in joint_angles_labeled]
            
        self.robot.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)
            
        #stage_5
        joint_names = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll', 'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
        joint_angles_labeled = [['HeadYaw', -0.27002596855163574], ['HeadPitch', 0.5844120979309082], ['LShoulderPitch', 0.9372320175170898], ['LShoulderRoll', 0.2607381343841553], ['LElbowYaw', -0.46331000328063965], ['LElbowRoll', -1.1029040813446045], ['LWristYaw', 0.01222991943359375], ['LHand', 0.29399996995925903], ['LHipYawPitch', -0.5951499938964844], ['LHipRoll', 0.27002596855163574], ['LHipPitch', -1.5324240922927856], ['LKneePitch', 1.3943641185760498], ['LAnklePitch', 0.8329200744628906], ['LAnkleRoll', -0.015298128128051758], ['RHipYawPitch', -0.5951499938964844], ['RHipRoll', -0.2622721195220947], ['RHipPitch', -1.5202360153198242], ['RKneePitch', 1.4113221168518066], ['RAnklePitch', 0.8406739234924316], ['RAnkleRoll', 0.019984006881713867], ['RShoulderPitch', -0.8114440441131592], ['RShoulderRoll', -0.3988819122314453], ['RElbowYaw', 0.9387660026550293], ['RElbowRoll', 1.5555181503295898], ['RWristYaw', 0.5828781127929688], ['RHand', 0]]
        times = [motion_time * wipe_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
        joint_angles_updated = [angle for _, angle in joint_angles_labeled]
            
        self.robot.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)
            
        #stage_6
        joint_names = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll', 'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
        joint_angles_labeled = [['HeadYaw', -0.27002596855163574], ['HeadPitch', 0.5844120979309082], ['LShoulderPitch', 0.9356980323791504], ['LShoulderRoll', 0.2607381343841553], ['LElbowYaw', -0.46637797355651855], ['LElbowRoll', -1.0998361110687256], ['LWristYaw', 0.01222991943359375], ['LHand', 0.29399996995925903], ['LHipYawPitch', -0.5966839790344238], ['LHipRoll', 0.27002596855163574], ['LHipPitch', -1.5308901071548462], ['LKneePitch', 1.3928301334381104], ['LAnklePitch', 0.8329200744628906], ['LAnkleRoll', -0.015298128128051758], ['RHipYawPitch', -0.5966839790344238], ['RHipRoll', -0.2622721195220947], ['RHipPitch', -1.5171680450439453], ['RKneePitch', 1.40211820602417], ['RAnklePitch', 0.8406739234924316], ['RAnkleRoll', 0.019984006881713867], ['RShoulderPitch', -0.047512054443359375], ['RShoulderRoll', -0.41115403175354004], ['RElbowYaw', 0.9004161357879639], ['RElbowRoll', 1.5555181503295898], ['RWristYaw', 1.2118180990219116], ['RHand', 0]]
        times = [motion_time * wipe_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
        joint_angles_updated = [angle for _, angle in joint_angles_labeled]
            
        self.robot.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)
            
        #stage_7
        joint_names = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll', 'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
        joint_angles_labeled = [['HeadYaw', -0.2684919834136963], ['HeadPitch', 0.5844120979309082], ['LShoulderPitch', 0.9372320175170898], ['LShoulderRoll', 0.2607381343841553], ['LElbowYaw', -0.46331000328063965], ['LElbowRoll', -1.1075060367584229], ['LWristYaw', 0.01222991943359375], ['LHand', 0.29399996995925903], ['LHipYawPitch', -0.5966839790344238], ['LHipRoll', 0.27002596855163574], ['LHipPitch', -1.533958077430725], ['LKneePitch', 1.3943641185760498], ['LAnklePitch', 0.8344540596008301], ['LAnkleRoll', -0.01683211326599121], ['RHipYawPitch', -0.5966839790344238], ['RHipRoll', -0.2607381343841553], ['RHipPitch', -1.5248379707336426], ['RKneePitch', 1.4082541465759277], ['RAnklePitch', 0.8406739234924316], ['RAnkleRoll', 0.019984006881713867], ['RShoulderPitch', -0.8390560150146484], ['RShoulderRoll', -0.4126880168914795], ['RElbowYaw', 0.9280281066894531], ['RElbowRoll', 1.5570521354675293], ['RWristYaw', 0.400331974029541], ['RHand', 0]]
        times = [motion_time * wipe_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
        joint_angles_updated = [angle for _, angle in joint_angles_labeled]
            
        self.robot.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)
            
        #stage_8
        joint_names = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll', 'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
        joint_angles_labeled = [['HeadYaw', -0.2684919834136963], ['HeadPitch', 0.5844120979309082], ['LShoulderPitch', 0.9356980323791504], ['LShoulderRoll', 0.2592041492462158], ['LElbowYaw', -0.467911958694458], ['LElbowRoll', -1.101370096206665], ['LWristYaw', 0.013764142990112305], ['LHand', 0.29399996995925903], ['LHipYawPitch', -0.5966839790344238], ['LHipRoll', 0.27002596855163574], ['LHipPitch', -1.5308901071548462], ['LKneePitch', 1.3943641185760498], ['LAnklePitch', 0.8329200744628906], ['LAnkleRoll', -0.01683211326599121], ['RHipYawPitch', -0.5966839790344238], ['RHipRoll', -0.2622721195220947], ['RHipPitch', -1.5202360153198242], ['RKneePitch', 1.40211820602417], ['RAnklePitch', 0.8406739234924316], ['RAnkleRoll', 0.019984006881713867], ['RShoulderPitch', -0.16716408729553223], ['RShoulderRoll', -0.48632001876831055], ['RElbowYaw', 0.7347440719604492], ['RElbowRoll', 1.5555181503295898], ['RWristYaw', 1.2670420408248901], ['RHand', 0]]
        times = [motion_time * wipe_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
        joint_angles_updated = [angle for _, angle in joint_angles_labeled]
            
        self.robot.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)
            
        #stage_9
        joint_names = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll', 'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
        joint_angles_labeled = [['HeadYaw', -0.2684919834136963], ['HeadPitch', 0.5844120979309082], ['LShoulderPitch', 0.9372320175170898], ['LShoulderRoll', 0.2592041492462158], ['LElbowYaw', -0.467911958694458], ['LElbowRoll', -1.0937001705169678], ['LWristYaw', -0.004643917083740234], ['LHand', 0.29399996995925903], ['LHipYawPitch', -0.5966839790344238], ['LHipRoll', 0.27002596855163574], ['LHipPitch', -1.5308901071548462], ['LKneePitch', 1.3943641185760498], ['LAnklePitch', 0.8329200744628906], ['LAnkleRoll', -0.013764142990112305], ['RHipYawPitch', -0.5966839790344238], ['RHipRoll', -0.2622721195220947], ['RHipPitch', -1.5202360153198242], ['RKneePitch', 1.4097881317138672], ['RAnklePitch', 0.8406739234924316], ['RAnkleRoll', 0.019984006881713867], ['RShoulderPitch', -0.8053081035614014], ['RShoulderRoll', -0.3866100311279297], ['RElbowYaw', 0.8820080757141113], ['RElbowRoll', 1.5555181503295898], ['RWristYaw', 0.6657140254974365], ['RHand', 0]]
        times = [motion_time * wipe_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
        joint_angles_updated = [angle for _, angle in joint_angles_labeled]
            
        self.robot.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)
            
        #stage_10
        joint_names = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll', 'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
        joint_angles_labeled = [['HeadYaw', -0.27002596855163574], ['HeadPitch', 0.5844120979309082], ['LShoulderPitch', 0.9372320175170898], ['LShoulderRoll', 0.2592041492462158], ['LElbowYaw', -0.46944594383239746], ['LElbowRoll', -1.0952341556549072], ['LWristYaw', -0.004643917083740234], ['LHand', 0.29399996995925903], ['LHipYawPitch', -0.5951499938964844], ['LHipRoll', 0.27002596855163574], ['LHipPitch', -1.5308901071548462], ['LKneePitch', 1.3943641185760498], ['LAnklePitch', 0.8329200744628906], ['LAnkleRoll', -0.01683211326599121], ['RHipYawPitch', -0.5951499938964844], ['RHipRoll', -0.2622721195220947], ['RHipPitch', -1.5141000747680664], ['RKneePitch', 1.40211820602417], ['RAnklePitch', 0.8406739234924316], ['RAnkleRoll', 0.019984006881713867], ['RShoulderPitch', -0.21318411827087402], ['RShoulderRoll', -1.282465934753418], ['RElbowYaw', 0.8083760738372803], ['RElbowRoll', 0.6397199630737305], ['RWristYaw', 0.8559300899505615], ['RHand', 0]]
        times = [motion_time * times_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
        joint_angles_updated = [angle for _, angle in joint_angles_labeled]
            
        self.robot.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)
            
        #stage_11
        joint_names = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll', 'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
        joint_angles_labeled = [['HeadYaw', -0.27002596855163574], ['HeadPitch', 0.5844120979309082], ['LShoulderPitch', 0.9356980323791504], ['LShoulderRoll', 0.2592041492462158], ['LElbowYaw', -0.46944594383239746], ['LElbowRoll', -1.101370096206665], ['LWristYaw', -0.004643917083740234], ['LHand', 0.29399996995925903], ['LHipYawPitch', -0.5966839790344238], ['LHipRoll', 0.27002596855163574], ['LHipPitch', -1.5324240922927856], ['LKneePitch', 1.3943641185760498], ['LAnklePitch', 0.8329200744628906], ['LAnkleRoll', -0.015298128128051758], ['RHipYawPitch', -0.5966839790344238], ['RHipRoll', -0.2622721195220947], ['RHipPitch', -1.5202360153198242], ['RKneePitch', 1.4067201614379883], ['RAnklePitch', 0.8406739234924316], ['RAnkleRoll', 0.019984006881713867], ['RShoulderPitch', -0.2070479393005371], ['RShoulderRoll', -1.2502517700195312], ['RElbowYaw', 0.6058881282806396], ['RElbowRoll', 0.4449019432067871], ['RWristYaw', -1.1781539916992188], ['RHand', 0]]
        times = [motion_time * times_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
        joint_angles_updated = [angle for _, angle in joint_angles_labeled]
            
        self.robot.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)
        
        self.robot.tts.say("Bin:  now.")
            
        #stage_12
        joint_names = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll', 'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
        joint_angles_labeled = [['HeadYaw', -0.27002596855163574], ['HeadPitch', 0.5844120979309082], ['LShoulderPitch', 0.9356980323791504], ['LShoulderRoll', 0.2592041492462158], ['LElbowYaw', -0.46944594383239746], ['LElbowRoll', -1.101370096206665], ['LWristYaw', -0.004643917083740234], ['LHand', 0.29399996995925903], ['LHipYawPitch', -0.5966839790344238], ['LHipRoll', 0.27002596855163574], ['LHipPitch', -1.5324240922927856], ['LKneePitch', 1.3943641185760498], ['LAnklePitch', 0.8329200744628906], ['LAnkleRoll', -0.01683211326599121], ['RHipYawPitch', -0.5966839790344238], ['RHipRoll', -0.2622721195220947], ['RHipPitch', -1.5217700004577637], ['RKneePitch', 1.4051861763000488], ['RAnklePitch', 0.8391399383544922], ['RAnkleRoll', 0.019984006881713867], ['RShoulderPitch', -0.2070479393005371], ['RShoulderRoll', -1.1950278282165527], ['RElbowYaw', 0.6012859344482422], ['RElbowRoll', 0.3758718967437744], ['RWristYaw', -0.35132789611816406], ['RHand', 1]]
        times = [motion_time * times_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
        joint_angles_updated = [angle for _, angle in joint_angles_labeled]
            
        self.robot.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)
        
        #stage_1
        joint_names = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll', 'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
        joint_angles_labeled = [['HeadYaw', 0.015298128128051758], ['HeadPitch', 0.19937801361083984], ['LShoulderPitch', 0.9341640472412109], ['LShoulderRoll', 0.2607381343841553], ['LElbowYaw', -0.46637797355651855], ['LElbowRoll', -1.0983021259307861], ['LWristYaw', 0.0014920234680175781], ['LHand', 0.2943999767303467], ['LHipYawPitch', -0.5966839790344238], ['LHipRoll', 0.27002596855163574], ['LHipPitch', -1.5324240922927856], ['LKneePitch', 1.3943641185760498], ['LAnklePitch', 0.8329200744628906], ['LAnkleRoll', -0.015298128128051758], ['RHipYawPitch', -0.5966839790344238], ['RHipRoll', -0.2622721195220947], ['RHipPitch', -1.5202360153198242], ['RKneePitch', 1.4097881317138672], ['RAnklePitch', 0.8391399383544922], ['RAnkleRoll', 0.02151799201965332], ['RShoulderPitch', -0.2607381343841553], ['RShoulderRoll', -0.8974318504333496], ['RElbowYaw', 0.5614020824432373], ['RElbowRoll', 0.7424979209899902], ['RWristYaw', -1.3085441589355469], ['RHand', 1]]
        times = [motion_time * bin_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
        joint_angles_updated = [angle for _, angle in joint_angles_labeled]
            
        self.robot.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)
            
        #stage_2
        joint_names = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll', 'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
        joint_angles_labeled = [['HeadYaw', 0.015298128128051758], ['HeadPitch', 0.19937801361083984], ['LShoulderPitch', 0.9341640472412109], ['LShoulderRoll', 0.2592041492462158], ['LElbowYaw', -0.46637797355651855], ['LElbowRoll', -1.0983021259307861], ['LWristYaw', 0.0014920234680175781], ['LHand', 0.29399996995925903], ['LHipYawPitch', -0.5966839790344238], ['LHipRoll', 0.27002596855163574], ['LHipPitch', -1.5324240922927856], ['LKneePitch', 1.3943641185760498], ['LAnklePitch', 0.8329200744628906], ['LAnkleRoll', -0.015298128128051758], ['RHipYawPitch', -0.5966839790344238], ['RHipRoll', -0.2622721195220947], ['RHipPitch', -1.5202360153198242], ['RKneePitch', 1.4067201614379883], ['RAnklePitch', 0.8406739234924316], ['RAnkleRoll', 0.019984006881713867], ['RShoulderPitch', -0.31749606132507324], ['RShoulderRoll', -0.9127721786499023], ['RElbowYaw', 0.6810541152954102], ['RElbowRoll', 0.024585962295532227], ['RWristYaw', 0.18710613250732422], ['RHand',1]]
        times = [motion_time * bin_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
        joint_angles_updated = [angle for _, angle in joint_angles_labeled]
            
        self.robot.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)
            
        #stage_3
        joint_names = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll', 'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
        joint_angles_labeled = [['HeadYaw', 0.015298128128051758], ['HeadPitch', 0.19937801361083984], ['LShoulderPitch', 0.9341640472412109], ['LShoulderRoll', 0.2592041492462158], ['LElbowYaw', -0.46637797355651855], ['LElbowRoll', -1.0983021259307861], ['LWristYaw', 0.0014920234680175781], ['LHand', 0.29399996995925903], ['LHipYawPitch', -0.5966839790344238], ['LHipRoll', 0.27002596855163574], ['LHipPitch', -1.5324240922927856], ['LKneePitch', 1.3928301334381104], ['LAnklePitch', 0.8329200744628906], ['LAnkleRoll', -0.015298128128051758], ['RHipYawPitch', -0.5966839790344238], ['RHipRoll', -0.2607381343841553], ['RHipPitch', -1.5202360153198242], ['RKneePitch', 1.4067201614379883], ['RAnklePitch', 0.8391399383544922], ['RAnkleRoll', 0.019984006881713867], ['RShoulderPitch', -0.49697399139404297], ['RShoulderRoll', -0.8130619525909424], ['RElbowYaw', 0.05518198013305664], ['RElbowRoll', 0.29917192459106445], ['RWristYaw', -0.7977218627929688], ['RHand', 1]]
        times = [motion_time * bin_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
        joint_angles_updated = [angle for _, angle in joint_angles_labeled]
            
        self.robot.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)
            
        #stage_4
        joint_names = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll', 'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
        joint_angles_labeled = [['HeadYaw', 0.015298128128051758], ['HeadPitch', 0.19937801361083984], ['LShoulderPitch', 0.9341640472412109], ['LShoulderRoll', 0.2592041492462158], ['LElbowYaw', -0.467911958694458], ['LElbowRoll', -1.0983021259307861], ['LWristYaw', 0.0014920234680175781], ['LHand', 0.29399996995925903], ['LHipYawPitch', -0.5966839790344238], ['LHipRoll', 0.27002596855163574], ['LHipPitch', -1.5324240922927856], ['LKneePitch', 1.3928301334381104], ['LAnklePitch', 0.8329200744628906], ['LAnkleRoll', -0.01683211326599121], ['RHipYawPitch', -0.5966839790344238], ['RHipRoll', -0.2622721195220947], ['RHipPitch', -1.5202360153198242], ['RKneePitch', 1.4067201614379883], ['RAnklePitch', 0.8391399383544922], ['RAnkleRoll', 0.019984006881713867], ['RShoulderPitch', -0.47089600563049316], ['RShoulderRoll', -0.6857399940490723], ['RElbowYaw', 0.018366098403930664], ['RElbowRoll', 0.07827591896057129], ['RWristYaw', 0.7117340564727783], ['RHand', 1]]
        times = [motion_time * bin_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
        joint_angles_updated = [angle for _, angle in joint_angles_labeled]
            
        self.robot.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)
            
        #stage_5
        joint_names = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll', 'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
        joint_angles_labeled = [['HeadYaw', 0.015298128128051758], ['HeadPitch', 0.19937801361083984], ['LShoulderPitch', 0.9341640472412109], ['LShoulderRoll', 0.2592041492462158], ['LElbowYaw', -0.467911958694458], ['LElbowRoll', -1.0983021259307861], ['LWristYaw', 0.0014920234680175781], ['LHand', 0.2943999767303467], ['LHipYawPitch', -0.5966839790344238], ['LHipRoll', 0.27002596855163574], ['LHipPitch', -1.5324240922927856], ['LKneePitch', 1.3943641185760498], ['LAnklePitch', 0.8329200744628906], ['LAnkleRoll', -0.015298128128051758], ['RHipYawPitch', -0.5966839790344238], ['RHipRoll', -0.2622721195220947], ['RHipPitch', -1.5202360153198242], ['RKneePitch', 1.4036521911621094], ['RAnklePitch', 0.8391399383544922], ['RAnkleRoll', 0.019984006881713867], ['RShoulderPitch', -0.06898808479309082], ['RShoulderRoll', -0.9097042083740234], ['RElbowYaw', 0.05824995040893555], ['RElbowRoll', 0.34519195556640625], ['RWristYaw', -0.14883995056152344], ['RHand', 1]]
        times = [motion_time * bin_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
        joint_angles_updated = [angle for _, angle in joint_angles_labeled]
            
        self.robot.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)
            
        #stage_13
        joint_names = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll', 'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
        joint_angles_labeled = [['HeadYaw', -0.27002596855163574], ['HeadPitch', 0.5844120979309082], ['LShoulderPitch', 0.9372320175170898], ['LShoulderRoll', 0.2592041492462158], ['LElbowYaw', -0.46944594383239746], ['LElbowRoll', -1.104438066482544], ['LWristYaw', -0.004643917083740234], ['LHand', 0.2943999767303467], ['LHipYawPitch', -0.5966839790344238], ['LHipRoll', 0.27002596855163574], ['LHipPitch', -1.5324240922927856], ['LKneePitch', 1.3943641185760498], ['LAnklePitch', 0.8329200744628906], ['LAnkleRoll', -0.01683211326599121], ['RHipYawPitch', -0.5966839790344238], ['RHipRoll', -0.2622721195220947], ['RHipPitch', -1.5217700004577637], ['RKneePitch', 1.4067201614379883], ['RAnklePitch', 0.8406739234924316], ['RAnkleRoll', 0.019984006881713867], ['RShoulderPitch', -0.2039799690246582], ['RShoulderRoll', -0.9633941650390625], ['RElbowYaw', 0.4954400062561035], ['RElbowRoll', 0.33598804473876953], ['RWristYaw', -0.3497939109802246], ['RHand', 1]]
        times = [motion_time * times_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
        joint_angles_updated = [angle for _, angle in joint_angles_labeled]
            
        self.robot.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)
            
        #stage_14
        joint_names = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll', 'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
        joint_angles_labeled = [['HeadYaw', -0.27002596855163574], ['HeadPitch', 0.5828781127929688], ['LShoulderPitch', 0.9372320175170898], ['LShoulderRoll', 0.2592041492462158], ['LElbowYaw', -0.467911958694458], ['LElbowRoll', -1.0998361110687256], ['LWristYaw', -0.004643917083740234], ['LHand', 0.29399996995925903], ['LHipYawPitch', -0.5966839790344238], ['LHipRoll', 0.27002596855163574], ['LHipPitch', -1.5324240922927856], ['LKneePitch', 1.3943641185760498], ['LAnklePitch', 0.8329200744628906], ['LAnkleRoll', -0.015298128128051758], ['RHipYawPitch', -0.5966839790344238], ['RHipRoll', -0.2622721195220947], ['RHipPitch', -1.5187020301818848], ['RKneePitch', 1.4082541465759277], ['RAnklePitch', 0.8406739234924316], ['RAnkleRoll', 0.019984006881713867], ['RShoulderPitch', 0.5798940658569336], ['RShoulderRoll', -0.29303598403930664], ['RElbowYaw', 0.23772811889648438], ['RElbowRoll', 1.3484277725219727], ['RWristYaw', 0.6058881282806396], ['RHand', 1]]
        times = [motion_time * times_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
        joint_angles_updated = [angle for _, angle in joint_angles_labeled]
            
        self.robot.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)
            
        #stage_15
        joint_names = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll', 'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
        joint_angles_labeled = [['HeadYaw', -0.015382051467895508], ['HeadPitch', 0.3251659870147705], ['LShoulderPitch', 0.9372320175170898], ['LShoulderRoll', 0.2607381343841553], ['LElbowYaw', -0.46944594383239746], ['LElbowRoll', -1.104438066482544], ['LWristYaw', -0.004643917083740234], ['LHand', 0.29399996995925903], ['LHipYawPitch', -0.5966839790344238], ['LHipRoll', 0.27002596855163574], ['LHipPitch', -1.533958077430725], ['LKneePitch', 1.3928301334381104], ['LAnklePitch', 0.8329200744628906], ['LAnkleRoll', -0.015298128128051758], ['RHipYawPitch', -0.5966839790344238], ['RHipRoll', -0.2622721195220947], ['RHipPitch', -1.5187020301818848], ['RKneePitch', 1.4051861763000488], ['RAnklePitch', 0.8391399383544922], ['RAnkleRoll', 0.02151799201965332], ['RShoulderPitch', 0.774712085723877], ['RShoulderRoll', -0.3298518657684326], ['RElbowYaw', 0.14722204208374023], ['RElbowRoll', 1.1597461700439453], ['RWristYaw', 0.6074221134185791], ['RHand', 0.49320000410079956]]
        times = [motion_time * times_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
        joint_angles_updated = [angle for _, angle in joint_angles_labeled]
            
        self.robot.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)
            
        #stage_16
        joint_names = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll', 'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
        joint_angles_labeled = [['HeadYaw', -0.015382051467895508], ['HeadPitch', 0.3251659870147705], ['LShoulderPitch', 0.9372320175170898], ['LShoulderRoll', 0.2622721195220947], ['LElbowYaw', -0.46944594383239746], ['LElbowRoll', -1.1059720516204834], ['LWristYaw', -0.004643917083740234], ['LHand', 0.2943999767303467], ['LHipYawPitch', -0.5966839790344238], ['LHipRoll', 0.27002596855163574], ['LHipPitch', -1.533958077430725], ['LKneePitch', 1.3928301334381104], ['LAnklePitch', 0.8329200744628906], ['LAnkleRoll', -0.015298128128051758], ['RHipYawPitch', -0.5966839790344238], ['RHipRoll', -0.2622721195220947], ['RHipPitch', -1.5202360153198242], ['RKneePitch', 1.4051861763000488], ['RAnklePitch', 0.8406739234924316], ['RAnkleRoll', 0.02151799201965332], ['RShoulderPitch', 0.774712085723877], ['RShoulderRoll', -0.3298518657684326], ['RElbowYaw', 0.1487560272216797], ['RElbowRoll', 1.1597461700439453], ['RWristYaw', 0.6074221134185791], ['RHand', 0.49320000410079956]]
        times = [motion_time * times_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
        joint_angles_updated = [angle for _, angle in joint_angles_labeled]
            
        self.robot.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)

    def head_smash(self):
        self.tts.say("Ooga.")
        self.animation.run('animations/Sit/Waiting/KnockEye_1')

    def left_hand_laugh(self):
        responses = ["Sorry, my left hand is very ticklish.", "Like I said, that really tickles.",
            "Please don't do that again!", "Gosh darnit. Are you a sadist?", "I beg you, stop. I can't take any more!", 
            "I want my daddy", "Thats it. I'm dead."]

        laugh_file = "/home/nao/AUDIO/laugh{}.mp3".format(self.laugh_count)
        # print(laugh_file)
        self.leds.fadeRGB("ChestLeds", 'magenta', 0.1)
        self.motion.post.angleInterpolationWithSpeed("HeadPitch", -0.5, 0.5)
        self.audio_player.playFile(laugh_file)
        self.motion.post.angleInterpolationWithSpeed("HeadPitch", 0.5, 0.5)
        self.leds.fadeRGB("ChestLeds", 0xFFFFFF, 0.1)
        self.tts.say(responses[self.laugh_count])
        self.laugh_count += 1
        if self.laugh_count == 8:
            self.laugh_count = 0

    def right_foot_scream(self):
        responses = [
            "Sorry, my right foot is very sensitive.", "Like I said, that really hurts.",
			"Please don't do that again!", "Gosh darnit. Are you a sadist?", "Please, no more!", 
			"I want my mommy", "", "Thats it.  I'm dead."
            ]
        scream_file = "/home/nao/AUDIO/scream{}.mp3".format(self.scream_count)
        # print(scream_file)
        self.leds.post.fadeRGB("RightFootLeds", 0xFF0000, 0.2)
        self.leds.post.fadeRGB("ChestLeds", 0xFF0000, 0.1)
        self.leds.post.fadeRGB("FaceLeds", 0xFF0000, 0.1)
        self.motion.post.angleInterpolationWithSpeed("HeadPitch", -0.5, 0.5)
        self.audio_player.playFile(scream_file)
        self.motion.post.angleInterpolationWithSpeed("HeadPitch", 0.5, 0.5)
        self.leds.post.off("RightFootLeds")
        self.leds.post.fadeRGB("ChestLeds", 0xFFFFFF, 0.1)
        self.leds.post.fadeRGB("FaceLeds", 0xFFFFFF, 0.1)
        self.tts.say(responses[self.scream_count])
        self.scream_count += 1
        if self.scream_count == 8:
            self.scream_count = 0