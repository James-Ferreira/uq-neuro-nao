import copy
import motion_library
import threading
import random
import time

class MotionManager:
    # rename robot arg to nao ?
    def __init__(self, robot):
        self.nao = robot
        self.motion = robot.motion
        self.reversed = robot.reversed

    def crouch(self, post=None):
        speed = 0.75
        if post == 1:
            self.nao.posture.pose.goToPosture('Crouch', speed)
        else:
            self.nao.posture.goToPosture('Crouch', speed)

    def lie_back(self, post=None):
        speed = 0.75
        if post == 1:
            self.nao.posture.post.goToPosture('LyingBack', speed)
        else:
            self.nao.posture.goToPosture('LyingBack', speed)

    def lie_belly(self, post=None):
        speed = 0.75
        if post == 1:
            self.nao.posture.post.goToPosture('LyingBelly', speed)
        else:
            self.nao.posture.goToPosture('LyingBelly', speed)

    def sit(self, post=False):
        speed = 0.75
        if post == True:
            self.nao.posture.post.goToPosture('Sit', speed)
        else:
            self.nao.posture.goToPosture('Sit', speed)

    def sit_gently(self, post=False):
        # to sit without the jerking common in the default sit command.
        # will not work if robot is standing.
        if not self.posture_check('Sit') and not self.posture_check('SitRelax'):
            return
        else:
            self.use_motion_library('sit_gently', post=post)
   
    def sit_relax(self, post=None):
        speed = 0.75
        if post == 1:
            self.nao.posture.post.goToPosture('SitRelax', speed)
        else:
            self.nao.posture.goToPosture('SitRelax', speed)

    def stand(self, post=None):
        speed = 0.75
        if post == 1:
            self.nao.posture.post.goToPosture('Stand', speed)
        else:
            self.nao.posture.goToPosture('Stand', speed)

    def stand_init(self, post=None):
        speed = 0.75
        if post == 1:
            self.nao.posture.post.goToPosture('StandInit', speed)
        else:
            self.nao.posture.goToPosture('StandInit', speed)

    def stand_zero(self, post=None):
        speed = 0.75
        if post == 1:
            self.nao.posture.post.goToPosture('StandZero', speed)  
        else:
            self.nao.posture.goToPosture('StandZero', speed) 

    def repose(self, leds=True):
        if leds == False:
            self.nao.leds.post.fadeRGB("AllLeds", 0x000000, 0.1)

        if not self.posture_check('Sit'):
            print("repose failed")
            return
        else:
            joint_angles = [angles_compressed for _, angles_compressed in [['HeadYaw', [-0.013848066329956055]], ['HeadPitch', [0.5752079486846924]], ['LShoulderPitch', [0.8896780014038086]], ['LShoulderRoll', [0.16716408729553223]], ['LElbowYaw', [-0.48018407821655273]], ['LElbowRoll', [-0.9970581531524658]], ['LWristYaw', [-0.8299360275268555]], ['LHand', [0.6647999882698059]], ['RShoulderPitch', [0.8575479984283447]], ['RShoulderRoll', [-0.127363920211792]], ['RElbowYaw', [0.4371480941772461]], ['RElbowRoll', [0.9112381935119629]], ['RWristYaw', [0.891211986541748]], ['RHand', [0.5971999764442444]]]]
            time_points = [time_points_compressed for _, time_points_compressed in [['HeadYaw', [1]], ['HeadPitch', [1]], ['LShoulderPitch', [1]], ['LShoulderRoll', [1]], ['LElbowYaw', [1]], ['LElbowRoll', [1]], ['LWristYaw', [1]], ['LHand', [1]], ['RShoulderPitch', [1]], ['RShoulderRoll', [1]], ['RElbowYaw', [1]], ['RElbowRoll', [1]], ['RWristYaw', [1]], ['RHand', [1]]]]
            self.motion.post.angleInterpolation(motion_library.joint_names_list, joint_angles, time_points, True)

    def execute_motion(self, reverse, joint_angles, time_points, post=False):
        print("{}'s reverse = {}".format(self.nao.name, reverse))

        joints = mirror_joint_names(motion_library.joint_names_list) if reverse else motion_library.joint_names_list
        angles = transform_angles_by_joint_name(motion_library.joint_names_list, joint_angles) if reverse else joint_angles

        interpolator = self.motion.post.angleInterpolation if post else self.motion.angleInterpolation
        return interpolator(joints, angles, time_points, True)
    
    def use_motion_library(self, key, default_orientation = None, post = False):
        print("{} using motion '{}'".format(self.nao.name, key))

        motion_data = motion_library.motions.get(key)
        if not motion_data:
            print("Motion not found.")
            return
        
        # needed to override self.reversed for extend_righ_hand animation in simple_welcome(). reverse = None kwarg might break other stuff down the line??
        reverse = self.reversed if default_orientation is None else False

        self.execute_motion(
            reverse,
            motion_data["joint_angles_list"],
            motion_data["time_points_list"],
            post
        )

    def posture_check(self, posture):
        desired_posture = posture.capitalize()

        if posture.lower() not in ['stand', 'sit']:
            print("Invalid posture requested: {}".format(posture))
            return False

        current_posture = self.nao.posture.getPosture()

        if current_posture == desired_posture:
            return True
        elif current_posture != desired_posture:
            print("Current posture, {}, is not compatible with requested movement: {}.".format(current_posture, desired_posture))
            return False
        
    def loose(self):
        # Body parts to loosen
        body_parts = [
            "Head", "LArm", "RArm",
            "LHipYawPitch", "LHipRoll", "LHipPitch", "LKneePitch", 
            "LAnklePitch", "LAnkleRoll", 
            "RHipYawPitch", "RHipRoll", "RHipPitch", "RKneePitch", 
            "RAnklePitch", "RAnkleRoll"
            ]
    
        # Set looseness to full body
        for part in body_parts:
            self.motion.setStiffnesses(part, 0.0)

    def loose_t(self):
        # Body parts to loosen
        body_parts = [
            "Head", "LArm", "RArm",
            ]
    
        # Set looseness to full body
        for part in body_parts:
            self.motion.setStiffnesses(part, 0.0)
           
    def stiff(self):
        # Body parts to keep stiff (hips and legs)
        body_parts = [
            "Head", "LArm", "RArm",
            "LHipYawPitch", "LHipRoll", "LHipPitch", "LKneePitch", 
            "LAnklePitch", "LAnkleRoll", 
            "RHipYawPitch", "RHipRoll", "RHipPitch", "RKneePitch", 
            "RAnklePitch", "RAnkleRoll"
            ]
    
        # Set stiffness for the lower body to 1.0 (stiff)
        for part in body_parts:
            self.motion.setStiffnesses(part, 1.0)

    def catch_fly(self):
        current_posture = self.nao.posture.getPosture()
        if current_posture != 'Sit':
            print('Current posture {} is incompatible with requested animation.'.format(
                current_posture))
            return
        
        self.nao.animation.run('animations/Sit/Waiting/CatchFly_1')

    def puppet_show(self):
        current_posture = self.nao.posture.getPosture()
        if current_posture != 'Sit':
            print('Current posture {} is incompatible with requested animation.'.format(
                current_posture))
            return
        
        self.nao.animation.run('animations/Sit/Waiting/Puppet_1')

    def bob_n_speak(self, text):
        # Create an event that signals the bobbing thread to stop.
        stop_event = threading.Event()

        def head_bobbing():
            # Continue bobbing until stop_event is set.
            while not stop_event.is_set():
                joint_names = ['HeadYaw', 'HeadPitch']
                yaw = random.uniform(-0.2, 0.2)
                pitch = random.uniform(0.5, 0.1)
                bob_duration = random.uniform(0.4, 1.4)
                sleep_duration = random.uniform(0.9, 1.8)
                joint_angles = [yaw, pitch]
                action_durations = [bob_duration, bob_duration]
                self.motion.angleInterpolation(joint_names, joint_angles, action_durations, True)
                time.sleep(sleep_duration)

        # Start the bobbing in a separate thread.
        bobbing_thread = threading.Thread(target=head_bobbing)
        bobbing_thread.start()

        # While the robot speaks, head bobbing happens in parallel.
        self.nao.tts.say(str(text))

        # Once speaking is finished, signal the bobbing thread to stop.
        stop_event.set()
        bobbing_thread.join()
    
    def wave_bye(self):
        byes = ["\\RSPD=65\\ Thats all folks.  When I am forth bid me farewell and smile.",
            "\\RSPD=70\\ I'm out. I have too pleased a heart to take a tedious leave.", 
            "\\RSPD=55\\ Goodbye. I have heard the call. I must depart.", 
            "\\RSPD=60\\ Farewell. Farewell, my soft friends.", 
            "\\RSPD=60\\ Farewell. Farewell, my moist kinsfolk.", 
            "\\RSPD=50\\Bye.Bye. Bye. Bye.Bye.", 
            "\\RSPD=50\\ And now. I bid you a doo dudy doo.", 
            "\\RSPD=50\\ And so. I must take my leave of you slimeballs.", 
            "\\RSPD=55\\ So Farewell. My blessing on you creatures of tissue"]
        
        random.shuffle(byes)
        
        current_posture = self.nao.posture.getPosture()
        
        #wave bye, standing version (same as wave_bye2)
        if current_posture == 'Stand':
            
            self.nao.tts.post.say(byes[0])
            self.nao.animation.run('animations/Stand/Gestures/Hey_2')
            self.nao.leds.post.fadeRGB("FaceLeds", 0xFFFFFF, 1)
        
        #wave bye, sitting version (same as wave_bye3)
        elif current_posture == 'Sit':
            # Ensure the robot is in the sitting posture
            self.nao.posture.goToPosture("Sit", 0.5)
        
            # Open the right hand
            self.motion.post.openHand('RHand')
            
            # Raise the right arm to a waving position
            names  = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw"]
            angles = [0.2, -0.6, 1.0, 1.0, -.5]  # Angles in radians
            fractionMaxSpeed = 0.2
            self.motion.setAngles(names, angles, fractionMaxSpeed)
            time.sleep(0.7)

            self.nao.tts.post.say(byes[0])

            # Perform the waving motion
            for _ in range(7):  # Wave hand back and forth
                # Move elbow yaw to simulate waving
                self.motion.setAngles(["RElbowYaw", "RElbowRoll"],[-2, 1.5], 0.4)
                time.sleep(0.3)
                self.motion.setAngles(["RElbowYaw", "RElbowRoll"],[2,.05], 0.4)
                time.sleep(0.3)            

            # Close the right hand
            self.motion.post.setAngles('RWristYaw', 0,.5)
            self.motion.post.closeHand('RHand')
            time.sleep(0.5)
    
            # Lower the right arm back to initial position
            angles = [1.5, 0.0, 1.0, 0.5, 1]
            self.motion.setAngles(names, angles, fractionMaxSpeed)
            time.sleep(3)
            
            # Ensure the robot is in the sitting posture
            self.nao.posture.goToPosture("Sit", 0.5)  
    
        else:
            print('Current posture, {}, is incompatible with requested animation.'.format(current_posture))
            return
        
    def right_handshake_a(self):
        joint_names = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll', 'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']

        # can we delete this?
        # punchline_array= ["\\rspd=88\\ Gosh I love shaking hands. Shake. Shake.  Shake.  You just shake and then your friends.  Its so human."]
        
        self.nao.tts.post.say("Its an honor. I assure you.")
            
        times_multiple = 0.35
            
        # Stage: 1 : 
        print("Stage: " + str(1) + ": " + "")
        
        joint_angles_labeled = [['HeadYaw', 0.06592011451721191], ['HeadPitch', 0.3328361511230469], ['LShoulderPitch', 0.970980167388916], ['LShoulderRoll', 0.30675792694091797], ['LElbowYaw', -0.5047280788421631], ['LElbowRoll', -1.201080083847046], ['LWristYaw', -0.8560140132904053], ['LHand', 0.1], ['LHipYawPitch', -0.5997519493103027], ['LHipRoll', 0.27002596855163574], ['LHipPitch', -1.5385600328445435], ['LKneePitch', 1.3974320888519287], ['LAnklePitch', 0.8482601642608643], ['LAnkleRoll', -0.010695934295654297], ['RHipYawPitch', -0.5997519493103027], ['RHipRoll', -0.2592041492462158], ['RHipPitch', -1.5355758666992188], ['RKneePitch', 1.4051861763000488], ['RAnklePitch', 0.8406739234924316], ['RAnkleRoll', 0.019984006881713867], ['RShoulderPitch', 0.5538160800933838], ['RShoulderRoll', 0.2208540439605713], ['RElbowYaw', 1.3590821027755737], ['RElbowRoll', 0.38507604598999023], ['RWristYaw', -0.027653932571411133], ['RHand', 0.3]]
        times = [motion_time * times_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
        joint_angles_updated = [angle for _, angle in joint_angles_labeled]
            
        self.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)
        
                
        # Stage: 2 : 
        print("Stage: " + str(2) + ": " + "")
        
        joint_angles_labeled = [['HeadYaw', 0.06592011451721191], ['HeadPitch', 0.3328361511230469], ['LShoulderPitch', 0.970980167388916], ['LShoulderRoll', 0.30368995666503906], ['LElbowYaw', -0.5031938552856445], ['LElbowRoll', -1.181138038635254], ['LWristYaw', -0.8575479984283447], ['LHand', 0.1], ['LHipYawPitch', -0.5982179641723633], ['LHipRoll', 0.2715599536895752], ['LHipPitch', -1.533958077430725], ['LKneePitch', 1.3958981037139893], ['LAnklePitch', 0.8482601642608643], ['LAnkleRoll', -0.010695934295654297], ['RHipYawPitch', -0.5982179641723633], ['RHipRoll', -0.2592041492462158], ['RHipPitch', -1.526371955871582], ['RKneePitch', 1.4036521911621094], ['RAnklePitch', 0.8406739234924316], ['RAnkleRoll', 0.019984006881713867], ['RShoulderPitch', 0.29917192459106445], ['RShoulderRoll', 0.17176604270935059], ['RElbowYaw', 1.4143060445785522], ['RElbowRoll', 0.5185339450836182], ['RWristYaw', -0.12276196479797363], ['RHand', 0.3]]
        times = [motion_time * times_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
        joint_angles_updated = [angle for _, angle in joint_angles_labeled]
            
        self.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)
        
                
        # Stage: 3 : 
        print("Stage: " + str(3) + ": " + "")
        
        joint_angles_labeled = [['HeadYaw', 0.06592011451721191], ['HeadPitch', 0.3328361511230469], ['LShoulderPitch', 0.970980167388916], ['LShoulderRoll', 0.3052239418029785], ['LElbowYaw', -0.5062620639801], ['LElbowRoll', -1.1995460987091064], ['LWristYaw', -0.8560140132904053], ['LHand', 0.1], ['LHipYawPitch', -0.5982179641723633], ['LHipRoll', 0.27002596855163574], ['LHipPitch', -1.5385600328445435], ['LKneePitch', 1.3974320888519287], ['LAnklePitch', 0.8482601642608643], ['LAnkleRoll', -0.010695934295654297], ['RHipYawPitch', -0.5982179641723633], ['RHipRoll', -0.2592041492462158], ['RHipPitch', -1.5371098518371582], ['RKneePitch', 1.4036521911621094], ['RAnklePitch', 0.8406739234924316], ['RAnkleRoll', 0.019984006881713867], ['RShoulderPitch', 0.7470998764038086], ['RShoulderRoll', 0.16102814674377441], ['RElbowYaw', 1.4173741340637207], ['RElbowRoll', 0.4356980323791504], ['RWristYaw', -0.14270401000976562], ['RHand', 0.3]]
        times = [motion_time * times_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
        joint_angles_updated = [angle for _, angle in joint_angles_labeled]
            
        self.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)
        
                
        # Stage: 4 : 
        print("Stage: " + str(4) + ": " + "")
        
        joint_angles_labeled = [['HeadYaw', 0.06592011451721191], ['HeadPitch', 0.3328361511230469], ['LShoulderPitch', 0.970980167388916], ['LShoulderRoll', 0.3052239418029785], ['LElbowYaw', -0.5062620639801], ['LElbowRoll', -1.198012113571167], ['LWristYaw', -0.8560140132904053], ['LHand', 0.1], ['LHipYawPitch', -0.5997519493103027], ['LHipRoll', 0.27002596855163574], ['LHipPitch', -1.5385600328445435], ['LKneePitch', 1.3974320888519287], ['LAnklePitch', 0.8482601642608643], ['LAnkleRoll', -0.010695934295654297], ['RHipYawPitch', -0.5997519493103027], ['RHipRoll', -0.2592041492462158], ['RHipPitch', -1.5340418815612793], ['RKneePitch', 1.4036521911621094], ['RAnklePitch', 0.8406739234924316], ['RAnkleRoll', 0.019984006881713867], ['RShoulderPitch', 0.18565607070922852], ['RShoulderRoll', 0.19017410278320312], ['RElbowYaw', 1.4189081192016602], ['RElbowRoll', 0.43109607696533203], ['RWristYaw', -0.14883995056152344], ['RHand', 0.3]]
        times = [motion_time * times_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
        joint_angles_updated = [angle for _, angle in joint_angles_labeled]
            
        self.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)
        
                
        # Stage: 5 : 
        print("Stage: " + str(5) + ": " + "")
        
        joint_angles_labeled = [['HeadYaw', 0.06592011451721191], ['HeadPitch', 0.3328361511230469], ['LShoulderPitch', 0.970980167388916], ['LShoulderRoll', 0.3052239418029785], ['LElbowYaw', -0.5062620639801], ['LElbowRoll', -1.2026140689849854], ['LWristYaw', -0.8560140132904053], ['LHand', 0.1], ['LHipYawPitch', -0.5997519493103027], ['LHipRoll', 0.2715599536895752], ['LHipPitch', -1.5385600328445435], ['LKneePitch', 1.3989660739898682], ['LAnklePitch', 0.8482601642608643], ['LAnkleRoll', -0.010695934295654297], ['RHipYawPitch', -0.5997519493103027], ['RHipRoll', -0.2592041492462158], ['RHipPitch', -1.5355758666992188], ['RKneePitch', 1.4036521911621094], ['RAnklePitch', 0.8406739234924316], ['RAnkleRoll', 0.019984006881713867], ['RShoulderPitch', 0.6504578590393066], ['RShoulderRoll', 0.2070479393005371], ['RElbowYaw', 1.4158400297164917], ['RElbowRoll', 0.35132789611816406], ['RWristYaw', -0.18719005584716797], ['RHand', 0.3]]
        times = [motion_time * times_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
        joint_angles_updated = [angle for _, angle in joint_angles_labeled]
            
        self.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)
        
                
        # Stage: 6 : 
        print("Stage: " + str(6) + ": " + "")
        
        joint_angles_labeled = [['HeadYaw', 0.06592011451721191], ['HeadPitch', 0.3328361511230469], ['LShoulderPitch', 0.970980167388916], ['LShoulderRoll', 0.30675792694091797], ['LElbowYaw', -0.5062620639801], ['LElbowRoll', -1.2041480541229248], ['LWristYaw', -0.8560140132904053], ['LHand', 0.1], ['LHipYawPitch', -0.5997519493103027], ['LHipRoll', 0.27002596855163574], ['LHipPitch', -1.5385600328445435], ['LKneePitch', 1.3974320888519287], ['LAnklePitch', 0.8482601642608643], ['LAnkleRoll', -0.010695934295654297], ['RHipYawPitch', -0.5997519493103027], ['RHipRoll', -0.2592041492462158], ['RHipPitch', -1.5325078964233398], ['RKneePitch', 1.4036521911621094], ['RAnklePitch', 0.8406739234924316], ['RAnkleRoll', 0.019984006881713867], ['RShoulderPitch', 0.14117002487182617], ['RShoulderRoll', 0.23312616348266602], ['RElbowYaw', 1.4311801195144653], ['RElbowRoll', 0.3436579704284668], ['RWristYaw', -0.18565607070922852], ['RHand', 0.3]]
        times = [motion_time * times_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
        joint_angles_updated = [angle for _, angle in joint_angles_labeled]
            
        self.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)
        
                
        # Stage: 7 : 
        print("Stage: " + str(7) + ": " + "")
        
        joint_angles_labeled = [['HeadYaw', 0.06592011451721191], ['HeadPitch', 0.3328361511230469], ['LShoulderPitch', 0.9694461822509766], ['LShoulderRoll', 0.3052239418029785], ['LElbowYaw', -0.5062620639801], ['LElbowRoll', -1.2026140689849854], ['LWristYaw', -0.8560140132904053], ['LHand', 0.1], ['LHipYawPitch', -0.5997519493103027], ['LHipRoll', 0.27002596855163574], ['LHipPitch', -1.5385600328445435], ['LKneePitch', 1.3989660739898682], ['LAnklePitch', 0.8482601642608643], ['LAnkleRoll', -0.010695934295654297], ['RHipYawPitch', -0.5997519493103027], ['RHipRoll', -0.2592041492462158], ['RHipPitch', -1.5340418815612793], ['RKneePitch', 1.4036521911621094], ['RAnklePitch', 0.8406739234924316], ['RAnkleRoll', 0.019984006881713867], ['RShoulderPitch', 0.6228458881378174], ['RShoulderRoll', 0.24846601486206055], ['RElbowYaw', 1.4311801195144653], ['RElbowRoll', 0.3083760738372803], ['RWristYaw', -0.18565607070922852], ['RHand', 0.3]]
        times = [motion_time * times_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
        joint_angles_updated = [angle for _, angle in joint_angles_labeled]
            
        self.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)
        
                
        # Stage: 8 : 
        print("Stage: " + str(8) + ": " + "")
        
        joint_angles_labeled = [['HeadYaw', 0.06592011451721191], ['HeadPitch', 0.3328361511230469], ['LShoulderPitch', 0.970980167388916], ['LShoulderRoll', 0.30675792694091797], ['LElbowYaw', -0.5062620639801], ['LElbowRoll', -1.201080083847046], ['LWristYaw', -0.8560140132904053], ['LHand', 0.1], ['LHipYawPitch', -0.5997519493103027], ['LHipRoll', 0.27002596855163574], ['LHipPitch', -1.5385600328445435], ['LKneePitch', 1.3974320888519287], ['LAnklePitch', 0.8482601642608643], ['LAnkleRoll', -0.01222991943359375], ['RHipYawPitch', -0.5997519493103027], ['RHipRoll', -0.2592041492462158], ['RHipPitch', -1.5325078964233398], ['RKneePitch', 1.4036521911621094], ['RAnklePitch', 0.8406739234924316], ['RAnkleRoll', 0.019984006881713867], ['RShoulderPitch', 0.14730596542358398], ['RShoulderRoll', 0.2561359405517578], ['RElbowYaw', 1.440384030342102], ['RElbowRoll', 0.3298518657684326], ['RWristYaw', -0.12582993507385254], ['RHand', 0.3]]
        times = [motion_time * times_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
        joint_angles_updated = [angle for _, angle in joint_angles_labeled]
            
        self.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)
        
                
        # Stage: 9 : 
        print("Stage: " + str(9) + ": " + "")
        
        joint_angles_labeled = [['HeadYaw', 0.06592011451721191], ['HeadPitch', 0.3328361511230469], ['LShoulderPitch', 0.970980167388916], ['LShoulderRoll', 0.30675792694091797], ['LElbowYaw', -0.5062620639801], ['LElbowRoll', -1.201080083847046], ['LWristYaw', -0.8560140132904053], ['LHand', 0.1], ['LHipYawPitch', -0.5997519493103027], ['LHipRoll', 0.27002596855163574], ['LHipPitch', -1.5385600328445435], ['LKneePitch', 1.3974320888519287], ['LAnklePitch', 0.8482601642608643], ['LAnkleRoll', -0.010695934295654297], ['RHipYawPitch', -0.5997519493103027], ['RHipRoll', -0.2592041492462158], ['RHipPitch', -1.5325078964233398], ['RKneePitch', 1.4036521911621094], ['RAnklePitch', 0.8406739234924316], ['RAnkleRoll', 0.019984006881713867], ['RShoulderPitch', 0.5568840503692627], ['RShoulderRoll', 0.2469320297241211], ['RElbowYaw', 1.440384030342102], ['RElbowRoll', 0.3099100589752197], ['RWristYaw', -0.12276196479797363], ['RHand', 0.3]]
        times = [motion_time * times_multiple for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
        joint_angles_updated = [angle for _, angle in joint_angles_labeled]
            
        self.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)
        
                
        # Stage: 10 : 
        print("Stage: " + str(10) + ": " + "")
        
        joint_angles_labeled = [['HeadYaw', 0.06592011451721191], ['HeadPitch', 0.3328361511230469], ['LShoulderPitch', 0.970980167388916], ['LShoulderRoll', 0.3052239418029785], ['LElbowYaw', -0.5031938552856445], ['LElbowRoll', -1.1765360832214355], ['LWristYaw', -0.8560140132904053], ['LHand', 0.1], ['LHipYawPitch', -0.5982179641723633], ['LHipRoll', 0.2715599536895752], ['LHipPitch', -1.5324240922927856], ['LKneePitch', 1.3958981037139893], ['LAnklePitch', 0.8482601642608643], ['LAnkleRoll', -0.010695934295654297], ['RHipYawPitch', -0.5982179641723633], ['RHipRoll', -0.2592041492462158], ['RHipPitch', -1.5248379707336426], ['RKneePitch', 1.4036521911621094], ['RAnklePitch', 0.8406739234924316], ['RAnkleRoll', 0.019984006881713867], ['RShoulderPitch', 0.46944594383239746], ['RShoulderRoll', -0.6750020980834961], ['RElbowYaw', 1.4388500452041626], ['RElbowRoll', 0.3958139419555664], ['RWristYaw', -0.11816000938415527], ['RHand', 0.3]]
        times = [motion_time * 0.6 for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
        joint_angles_updated = [angle for _, angle in joint_angles_labeled]
            
        self.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)
        
                
        # Stage: 11 : 
        print("Stage: " + str(11) + ": " + "")
        
        joint_angles_labeled = [['HeadYaw', 0.06592011451721191], ['HeadPitch', 0.3328361511230469], ['LShoulderPitch', 0.9725141268555], ['LShoulderRoll', 0.3052239418029785], ['LElbowYaw', -0.5047280788421631], ['LElbowRoll', -1.1872740983963013], ['LWristYaw', -0.8560140132904053], ['LHand', 0.1], ['LHipYawPitch', -0.5997519493103027], ['LHipRoll', 0.2715599536895752], ['LHipPitch', -1.537026047706604], ['LKneePitch', 1.3974320888519287], ['LAnklePitch', 0.8482601642608643], ['LAnkleRoll', -0.010695934295654297], ['RHipYawPitch', -0.5997519493103027], ['RHipRoll', -0.25766992568969727], ['RHipPitch', -1.5325078964233398], ['RKneePitch', 1.4051861763000488], ['RAnklePitch', 0.8406739234924316], ['RAnkleRoll', 0.019984006881713867], ['RShoulderPitch', 0.9219760894775391], ['RShoulderRoll', -0.24088001251220703], ['RElbowYaw', 0.4693620204925537], ['RElbowRoll', 1.0845799446105957], ['RWristYaw', 0.1978440284729004], ['RHand', 0.3]]
        times = [motion_time * 1 for motion_time in [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
        joint_angles_updated = [angle for _, angle in joint_angles_labeled]
            
        self.motion.angleInterpolation(joint_names, joint_angles_updated, times, True)
        
        # can we delete this?
        # self.nao.tts.post.say(random.choice(punchline_array))  

    def right_handshake_b(self):
        angle_modulator = 1.0
        duration_modulator = 1.0
                
        joint_names_list = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
                    
        # Movement: 1 : down
        print("Stage: " + str(1) + ": " + "down")
        joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.09660005569458008], ['HeadPitch', 0.33743810653686523], ['LShoulderPitch', 0.9556400775909424], ['LShoulderRoll', 0.3220980167388916], ['LElbowYaw', -0.4648439884185791], ['LElbowRoll', -1.2118180990219116], ['LWristYaw', 0.03523993492126465], ['LHand', 0.30479997396469116], ['RShoulderPitch', 0.5691559314727783], ['RShoulderRoll', 0.24846601486206055], ['RElbowYaw', 0.7562201023101807], ['RElbowRoll', 0.2654240131378174], ['RWristYaw', -0.09361600875854492], ['RHand', 0.1]]]
        action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.35], ['HeadPitch', 0.35], ['LShoulderPitch', 0.35], ['LShoulderRoll', 0.35], ['LElbowYaw', 0.35], ['LElbowRoll', 0.35], ['LWristYaw', 0.35], ['LHand', 0.35], ['RShoulderPitch', 0.35], ['RShoulderRoll', 0.35], ['RElbowYaw', 0.35], ['RElbowRoll', 0.35], ['RWristYaw', 0.35], ['RHand', 0.35]]]
        self.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
            
        # Movement: 2 : up
        print("Stage: " + str(2) + ": " + "up")
        joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.09660005569458008], ['HeadPitch', 0.1840381622314453], ['LShoulderPitch', 0.9571740627288818], ['LShoulderRoll', 0.32056403160095215], ['LElbowYaw', -0.4709799289703369], ['LElbowRoll', -1.2118180990219116], ['LWristYaw', 0.0367741584777832], ['LHand', 0.30479997396469116], ['RShoulderPitch', 0.027653932571411133], ['RShoulderRoll', 0.27761197090148926], ['RElbowYaw', 0.7838320732116699], ['RElbowRoll', 0.2853660583496094], ['RWristYaw', 0.6089560985565186], ['RHand', 0.1]]]
        action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.35], ['HeadPitch', 0.35], ['LShoulderPitch', 0.35], ['LShoulderRoll', 0.35], ['LElbowYaw', 0.35], ['LElbowRoll', 0.35], ['LWristYaw', 0.35], ['LHand', 0.35], ['RShoulderPitch', 0.35], ['RShoulderRoll', 0.35], ['RElbowYaw', 0.35], ['RElbowRoll', 0.35], ['RWristYaw', 0.35], ['RHand', 0.35]]]
        self.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
            
        # Movement: 3 : d
        print("Stage: " + str(3) + ": " + "d")
        joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.1318819522857666], ['HeadPitch', 0.3803901672363281], ['LShoulderPitch', 0.9587080478668213], ['LShoulderRoll', 0.3190300464630127], ['LElbowYaw', -0.4786500930786133], ['LElbowRoll', -1.2087500095367432], ['LWristYaw', 0.04137611389160156], ['LHand', 0.3051999807357788], ['RShoulderPitch', 0.5430779457092285], ['RShoulderRoll', 0.24846601486206055], ['RElbowYaw', 0.8543961048126221], ['RElbowRoll', 0.03072190284729004], ['RWristYaw', 0.5521979331970215], ['RHand', 0.1]]]
        action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.35], ['HeadPitch', 0.35], ['LShoulderPitch', 0.35], ['LShoulderRoll', 0.35], ['LElbowYaw', 0.35], ['LElbowRoll', 0.35], ['LWristYaw', 0.35], ['LHand', 0.35], ['RShoulderPitch', 0.35], ['RShoulderRoll', 0.35], ['RElbowYaw', 0.35], ['RElbowRoll', 0.35], ['RWristYaw', 0.35], ['RHand', 0.35]]]
        self.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
            
        # Movement: 4 : u
        print("Stage: " + str(4) + ": " + "u")
        joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.1318819522857666], ['HeadPitch', 0.3803901672363281], ['LShoulderPitch', 0.9587080478668213], ['LShoulderRoll', 0.31749606107324], ['LElbowYaw', -0.4847860336303711], ['LElbowRoll', -1.2118180990219116], ['LWristYaw', 0.042910099029541016], ['LHand', 0.30479997396469116], ['RShoulderPitch', -0.14262008666992188], ['RShoulderRoll', 0.11961007118225098], ['RElbowYaw', 0.8758721351623535], ['RElbowRoll', 0.029187917709350586], ['RWristYaw', 0.6457719802856445], ['RHand', 0.1]]]
        action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.35], ['HeadPitch', 0.35], ['LShoulderPitch', 0.35], ['LShoulderRoll', 0.35], ['LElbowYaw', 0.35], ['LElbowRoll', 0.35], ['LWristYaw', 0.35], ['LHand', 0.35], ['RShoulderPitch', 0.35], ['RShoulderRoll', 0.35], ['RElbowYaw', 0.35], ['RElbowRoll', 0.35], ['RWristYaw', 0.35], ['RHand', 0.35]]]
        self.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)

        # Movement: 2 : up
        print("Stage: " + str(2) + ": " + "up")
        joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.09660005569458008], ['HeadPitch', 0.1840381622314453], ['LShoulderPitch', 0.9571740627288818], ['LShoulderRoll', 0.32056403160095215], ['LElbowYaw', -0.4709799289703369], ['LElbowRoll', -1.2118180990219116], ['LWristYaw', 0.0367741584777832], ['LHand', 0.30479997396469116], ['RShoulderPitch', 0.027653932571411133], ['RShoulderRoll', 0.27761197090148926], ['RElbowYaw', 0.7838320732116699], ['RElbowRoll', 0.2853660583496094], ['RWristYaw', 0.6089560985565186], ['RHand', 0.1]]]
        action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.35], ['HeadPitch', 0.35], ['LShoulderPitch', 0.35], ['LShoulderRoll', 0.35], ['LElbowYaw', 0.35], ['LElbowRoll', 0.35], ['LWristYaw', 0.35], ['LHand', 0.35], ['RShoulderPitch', 0.35], ['RShoulderRoll', 0.35], ['RElbowYaw', 0.35], ['RElbowRoll', 0.35], ['RWristYaw', 0.35], ['RHand', 0.35]]]
        self.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
            
        # Movement: 3 : d
        print("Stage: " + str(3) + ": " + "d")
        joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.1318819522857666], ['HeadPitch', 0.3803901672363281], ['LShoulderPitch', 0.9587080478668213], ['LShoulderRoll', 0.3190300464630127], ['LElbowYaw', -0.4786500930786133], ['LElbowRoll', -1.2087500095367432], ['LWristYaw', 0.04137611389160156], ['LHand', 0.3051999807357788], ['RShoulderPitch', 0.5430779457092285], ['RShoulderRoll', 0.24846601486206055], ['RElbowYaw', 0.8543961048126221], ['RElbowRoll', 0.03072190284729004], ['RWristYaw', 0.5521979331970215], ['RHand', 0.1]]]
        action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.35], ['HeadPitch', 0.35], ['LShoulderPitch', 0.35], ['LShoulderRoll', 0.35], ['LElbowYaw', 0.35], ['LElbowRoll', 0.35], ['LWristYaw', 0.35], ['LHand', 0.35], ['RShoulderPitch', 0.35], ['RShoulderRoll', 0.35], ['RElbowYaw', 0.35], ['RElbowRoll', 0.35], ['RWristYaw', 0.35], ['RHand', 0.35]]]
        self.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
            
        # Movement: 5 : out
        print("Stage: " + str(5) + ": " + "out")
        joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.1288139820098877], ['HeadPitch', 0.19017410278320312], ['LShoulderPitch', 0.9663779735565186], ['LShoulderRoll', 0.3190300464630127], ['LElbowYaw', -0.49245595932006836], ['LElbowRoll', -1.213352084159851], ['LWristYaw', 0.038308143615722656], ['LHand', 0.3051999807357788], ['RShoulderPitch', -0.7393460273742676], ['RShoulderRoll', -0.6105740070343018], ['RElbowYaw', 0.9280281066894531], ['RElbowRoll', 0.6059720516204834], ['RWristYaw', 0.4540219306945801], ['RHand', 0.1]]]
        action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.6], ['HeadPitch', 0.6], ['LShoulderPitch', 0.6], ['LShoulderRoll', 0.6], ['LElbowYaw', 0.6], ['LElbowRoll', 0.6], ['LWristYaw', 0.6], ['LHand', 0.6], ['RShoulderPitch', 0.6], ['RShoulderRoll', 0.6], ['RElbowYaw', 0.6], ['RElbowRoll', 0.6], ['RWristYaw', 0.6], ['RHand', 0.6]]]
        self.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
            
        # Movement: 6 : down
        print("Stage: " + str(6) + ": " + "down")
        joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.1288139820098877], ['HeadPitch', 0.19017410278320312], ['LShoulderPitch', 0.967911958694458], ['LShoulderRoll', 0.32056403160095215], ['LElbowYaw', -0.49552392959594727], ['LElbowRoll', -1.2179540395736694], ['LWristYaw', 0.0367741584777832], ['LHand', 0.30479997396469116], ['RShoulderPitch', 0.748633861541748], ['RShoulderRoll', -0.24701595306396484], ['RElbowYaw', 0.11654210090637207], ['RElbowRoll', 1.1167941093444824], ['RWristYaw', -0.07827591896057129], ['RHand', 0.1]]]
        action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 1.5], ['HeadPitch', 1.5], ['LShoulderPitch', 1.5], ['LShoulderRoll', 1.5], ['LElbowYaw', 1.5], ['LElbowRoll', 1.5], ['LWristYaw', 1.5], ['LHand', 1.5], ['RShoulderPitch', 1.5], ['RShoulderRoll', 1.5], ['RElbowYaw', 1.5], ['RElbowRoll', 1.5], ['RWristYaw', 1.5], ['RHand', 1.5]]]
        self.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)                


def range_map(x, old_min, old_max, new_min, new_max):
    """
    Maps x in [old_min, old_max] to [new_min, new_max] linearly.
    """
    return new_min + ((x - old_min) * (new_max - new_min) / (old_max - old_min))

def mirror_joint_names(names):
    mirrored = []
    for n in names:
        if n.startswith("L"):
            mirrored.append("R" + n[1:])
        elif n.startswith("R"):
            mirrored.append("L" + n[1:])
        else:
            mirrored.append(n)
    return mirrored

def transform_angles_by_joint_name(joint_names, joint_angles):
    L_ELBOW_ROLL_RANGE = (-1.5446, -0.0349)
    R_ELBOW_ROLL_RANGE = (0.0349, 1.5446)
    NEGATE_JOINTS = {
    "HeadYaw", "LShoulderRoll", "LElbowYaw", "LWristYaw",
    "RShoulderRoll", "RElbowYaw", "RWristYaw"
    }
    
    angles_copy = copy.deepcopy(joint_angles)

    for i, jname in enumerate(joint_names):
        original_list = angles_copy[i]

        if jname == "RElbowRoll":
            angles_copy[i] = [
                range_map(val,
                        L_ELBOW_ROLL_RANGE[0], L_ELBOW_ROLL_RANGE[1],
                        R_ELBOW_ROLL_RANGE[1], R_ELBOW_ROLL_RANGE[0])
                for val in original_list
            ]
        
        elif jname == "LElbowRoll":
            angles_copy[i] = [
                range_map(val,
                        R_ELBOW_ROLL_RANGE[0], R_ELBOW_ROLL_RANGE[1],
                        L_ELBOW_ROLL_RANGE[1], L_ELBOW_ROLL_RANGE[0])
                for val in original_list
            ]
        elif jname in NEGATE_JOINTS:
            angles_copy[i] = [-val for val in original_list]

    return angles_copy
