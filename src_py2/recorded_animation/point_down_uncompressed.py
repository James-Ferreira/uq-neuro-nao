      
angle_modulator = 1.0
duration_modulator = 1.0
        
joint_names_list = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
                   
# Movement: 1 : d
print("Stage: " + str(1) + ": " + "d")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.09966802597045898], ['HeadPitch', 0.5828781127929688], ['LShoulderPitch', 0.46476006507873535], ['LShoulderRoll', -0.19485998153686523], ['LElbowYaw', 0.8743381500244141], ['LElbowRoll', -0.47396397590637207], ['LWristYaw', -1.8546481132507324], ['LHand', 0.7663999795913696], ['RShoulderPitch', 0.9143061637878418], ['RShoulderRoll', -0.23627805709838867], ['RElbowYaw', 0.5061781406402588], ['RElbowRoll', 1.0769100189208984], ['RWristYaw', 0.11961007118225098], ['RHand', 0.4611999988555908]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 1.0], ['HeadPitch', 1.0], ['LShoulderPitch', 1.0], ['LShoulderRoll', 1.0], ['LElbowYaw', 1.0], ['LElbowRoll', 1.0], ['LWristYaw', 1.0], ['LHand', 1.0], ['RShoulderPitch', 1.0], ['RShoulderRoll', 1.0], ['RElbowYaw', 1.0], ['RElbowRoll', 1.0], ['RWristYaw', 1.0], ['RHand', 1.0]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 2 : h
print("Stage: " + str(2) + ": " + "h")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.09966802597045898], ['HeadPitch', 0.5828781127929688], ['LShoulderPitch', 0.4632260799407959], ['LShoulderRoll', -0.19025802612304688], ['LElbowYaw', 0.8743381500244141], ['LElbowRoll', -0.47396397590637207], ['LWristYaw', -1.853114128112793], ['LHand', 0.7663999795913696], ['RShoulderPitch', 0.9143061637878418], ['RShoulderRoll', -0.23627805709838867], ['RElbowYaw', 0.5061781406402588], ['RElbowRoll', 1.0769100189208984], ['RWristYaw', 0.11961007118225098], ['RHand', 0.4611999988555908]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 1.0], ['HeadPitch', 1.0], ['LShoulderPitch', 1.0], ['LShoulderRoll', 1.0], ['LElbowYaw', 1.0], ['LElbowRoll', 1.0], ['LWristYaw', 1.0], ['LHand', 1.0], ['RShoulderPitch', 1.0], ['RShoulderRoll', 1.0], ['RElbowYaw', 1.0], ['RElbowRoll', 1.0], ['RWristYaw', 1.0], ['RHand', 1.0]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 3 : u
print("Stage: " + str(3) + ": " + "u")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.13648414611816406], ['HeadPitch', 0.20551395416259766], ['LShoulderPitch', 0.7577540874481201], ['LShoulderRoll', 0.19170808792114258], ['LElbowYaw', -0.1764519214630127], ['LElbowRoll', -0.9126880168914795], ['LWristYaw', -1.172018051147461], ['LHand', 0.7663999795913696], ['RShoulderPitch', 0.9296460151672363], ['RShoulderRoll', -0.27922987937927246], ['RElbowYaw', 0.48470211029052734], ['RElbowRoll', 1.145939826965332], ['RWristYaw', 0.12114405632019043], ['RHand', 0.4611999988555908]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.6], ['HeadPitch', 0.6], ['LShoulderPitch', 0.6], ['LShoulderRoll', 0.6], ['LElbowYaw', 0.6], ['LElbowRoll', 0.6], ['LWristYaw', 0.6], ['LHand', 0.6], ['RShoulderPitch', 0.6], ['RShoulderRoll', 0.6], ['RElbowYaw', 0.6], ['RElbowRoll', 0.6], ['RWristYaw', 0.6], ['RHand', 0.6]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
            