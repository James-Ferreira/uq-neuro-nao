import copy
import motion_library
import threading
import random
import time

class MotionManager:
    def __init__(self, robot, reversed):
        self.robot = robot
        self.motion = robot.motion
        self.reversed = reversed

    def crouch(self, post=None):
        speed = 0.75
        if post == 1:
            self.robot.posture.pose.goToPosture('Crouch', speed)
        else:
            self.robot.posture.goToPosture('Crouch', speed)

    def lie_back(self, post=None):
        speed = 0.75
        if post == 1:
            self.robot.posture.post.goToPosture('LyingBack', speed)
        else:
            self.robot.posture.goToPosture('LyingBack', speed)

    def lie_belly(self, post=None):
        speed = 0.75
        if post == 1:
            self.robot.posture.post.goToPosture('LyingBelly', speed)
        else:
            self.robot.posture.goToPosture('LyingBelly', speed)

    def sit(self, post=None):
        speed = 0.75
        if post == 1:
            self.robot.posture.post.goToPosture('Sit', speed)
        else:
            self.robot.posture.goToPosture('Sit', speed)

    def sit_gently(self):
        # to sit without the jerking common in the default sit command.
        # will not work if robot is standing.
        if not self.posture_check('Sit') and not self.posture_check('SitRelax'):
            return
        else:
            joint_names_list = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
            joint_angles = [angles_compressed for _, angles_compressed in [['HeadYaw', [-0.052197933197021484]], ['HeadPitch', [-0.05526590347290039]], ['LShoulderPitch', [0.9050180912017822]], ['LShoulderRoll', [0.25153398513793945]], ['LElbowYaw', [-0.43109607696533203]], ['LElbowRoll', [-1.1826720237731934]], ['LWristYaw', [0.004559993743896484]], ['LHand', [0.29399996995925903]], ['RShoulderPitch', [0.9465198516845703]], ['RShoulderRoll', [-0.3083760738372803]], ['RElbowYaw', [0.5153820514678955]], ['RElbowRoll', [1.1965618133544922]], ['RWristYaw', [0.004559993743896484]], ['RHand', [0.29680001735687256]]]]
            time_points = [time_points_compressed for _, time_points_compressed in [['HeadYaw', [1.25]], ['HeadPitch', [1.25]], ['LShoulderPitch', [1.25]], ['LShoulderRoll', [1.25]], ['LElbowYaw', [1.25]], ['LElbowRoll', [1.25]], ['LWristYaw', [1.25]], ['LHand', [1.25]], ['RShoulderPitch', [1.25]], ['RShoulderRoll', [1.25]], ['RElbowYaw', [1.25]], ['RElbowRoll', [1.25]], ['RWristYaw', [1.25]], ['RHand', [1.25]]]]
            self.motion.post.angleInterpolation(joint_names_list, joint_angles, time_points, True)                
   
    def sit_relax(self, post=None):
        speed = 0.75
        if post == 1:
            self.robot.posture.post.goToPosture('SitRelax', speed)
        else:
            self.robot.posture.goToPosture('SitRelax', speed)

    def stand(self, post=None):
        speed = 0.75
        if post == 1:
            self.robot.posture.post.goToPosture('Stand', speed)
        else:
            self.robot.posture.goToPosture('Stand', speed)

    def stand_init(self, post=None):
        speed = 0.75
        if post == 1:
            self.robot.posture.post.goToPosture('StandInit', speed)
        else:
            self.robot.posture.goToPosture('StandInit', speed)

    def stand_zero(self, post=None):
        speed = 0.75
        if post == 1:
            self.robot.posture.post.goToPosture('StandZero', speed)  
        else:
            self.robot.posture.goToPosture('StandZero', speed) 

    def repose(self, leds=True):
        if leds == False:
            self.robot.leds.post.fadeRGB("AllLeds", 0x000000, 0.1)

        if not self.posture_check('Sit'):
            print("repose failed")
            return
        else:
            joint_names_list = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
            joint_angles = [angles_compressed for _, angles_compressed in [['HeadYaw', [-0.013848066329956055]], ['HeadPitch', [0.5752079486846924]], ['LShoulderPitch', [0.8896780014038086]], ['LShoulderRoll', [0.16716408729553223]], ['LElbowYaw', [-0.48018407821655273]], ['LElbowRoll', [-0.9970581531524658]], ['LWristYaw', [-0.8299360275268555]], ['LHand', [0.6647999882698059]], ['RShoulderPitch', [0.8575479984283447]], ['RShoulderRoll', [-0.127363920211792]], ['RElbowYaw', [0.4371480941772461]], ['RElbowRoll', [0.9112381935119629]], ['RWristYaw', [0.891211986541748]], ['RHand', [0.5971999764442444]]]]
            time_points = [time_points_compressed for _, time_points_compressed in [['HeadYaw', [1.25]], ['HeadPitch', [1.25]], ['LShoulderPitch', [1.25]], ['LShoulderRoll', [1.25]], ['LElbowYaw', [1.25]], ['LElbowRoll', [1.25]], ['LWristYaw', [1.25]], ['LHand', [1.25]], ['RShoulderPitch', [1.25]], ['RShoulderRoll', [1.25]], ['RElbowYaw', [1.25]], ['RElbowRoll', [1.25]], ['RWristYaw', [1.25]], ['RHand', [1.25]]]]
            self.motion.post.angleInterpolation(joint_names_list, joint_angles, time_points, True)

    def execute_motion(self, reverse, joint_angles, time_points, post=False):
        print("executing motion")

        joints = mirror_joint_names(motion_library.joint_names_list) if reverse else motion_library.joint_names_list
        angles = transform_angles_by_joint_name(motion_library.joint_names_list, joint_angles) if reverse else joint_angles

        interpolator = self.motion.post.angleInterpolation if post else self.motion.angleInterpolation
        return interpolator(joints, angles, time_points, True)
    
    def use_motion_library(self, key):
        motion_data = motion_library.motions.get(key)
        if not motion_data:
            print("Motion not found.")
            return

        self.execute_motion(
            self.reversed,
            motion_data["joint_angles_list"],
            motion_data["time_points_list"]
        )

    def posture_check(self, posture):
        desired_posture = posture.capitalize()

        if posture.lower() not in ['stand', 'sit']:
            print("Invalid posture requested: {}".format(posture))
            return False

        current_posture = self.robot.posture.getPosture()

        if current_posture == desired_posture:
            return True
        elif current_posture != desired_posture:
            print("Current posture, {}, is not compatible with requested movement: {}.".format(current_posture, desired_posture))
            return False
        
    def loose(self):
        # Body parts to loosen
        lower_body_parts = [
            "Head", "LArm", "RArm",
            "LHipYawPitch", "LHipRoll", "LHipPitch", "LKneePitch", 
            "LAnklePitch", "LAnkleRoll", 
            "RHipYawPitch", "RHipRoll", "RHipPitch", "RKneePitch", 
            "RAnklePitch", "RAnkleRoll"
            ]
    
        # Set looseness to full body
        for part in lower_body_parts:
            self.motion.setStiffnesses(part, 0.0)
           
    def stiff(self):
        # Body parts to keep stiff (hips and legs)
        lower_body_parts = [
            "Head", "LArm", "RArm",
            "LHipYawPitch", "LHipRoll", "LHipPitch", "LKneePitch", 
            "LAnklePitch", "LAnkleRoll", 
            "RHipYawPitch", "RHipRoll", "RHipPitch", "RKneePitch", 
            "RAnklePitch", "RAnkleRoll"
            ]
    
        # Set stiffness for the lower body to 1.0 (stiff)
        for part in lower_body_parts:
            self.motion.setStiffnesses(part, 1.0)

    def catch_fly(self):
        current_posture = self.robot.posture.getPosture()
        if current_posture != 'Sit':
            print('Current posture {} is incompatible with requested animation.'.format(
                current_posture))
            return
        
        self.robot.animation.run('animations/Sit/Waiting/CatchFly_1')

    def puppet_show(self):
        current_posture = self.robot.posture.getPosture()
        if current_posture != 'Sit':
            print('Current posture {} is incompatible with requested animation.'.format(
                current_posture))
            return
        
        self.robot.animation.run('animations/Sit/Waiting/Puppet_1')

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
        self.robot.tts.say(str(text))

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
        
        current_posture = self.posture.getPosture()
        
        #wave bye, standing version (same as wave_bye2)
        if current_posture == 'Stand':
            
            self.tts.post.say(byes[0])
            self.animation.run('animations/Stand/Gestures/Hey_2')
            self.leds.post.fadeRGB("FaceLeds", 0xFFFFFF, 1)
        
        #wave bye, sitting version (same as wave_bye3)
        elif current_posture == 'Sit':
            # Ensure the robot is in the sitting posture
            self.posture.goToPosture("Sit", 0.5)
        
            # Open the right hand
            self.motion.post.openHand('RHand')
            
            # Raise the right arm to a waving position
            names  = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw"]
            angles = [0.2, -0.6, 1.0, 1.0, -.5]  # Angles in radians
            fractionMaxSpeed = 0.2
            self.motion.setAngles(names, angles, fractionMaxSpeed)
            time.sleep(0.7)

            self.tts.post.say(byes[0])

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
            self.posture.goToPosture("Sit", 0.5)  
    
        else:
            print('Current posture, {}, is incompatible with requested animation.'.format(current_posture))
            return


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
