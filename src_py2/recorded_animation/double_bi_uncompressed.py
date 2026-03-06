      
angle_modulator = 1.0
duration_modulator = 1.0
        
joint_names_list = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
                   
# Movement: 1 : up
print("Stage: " + str(1) + ": " + "up")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.015298128128051758], ['HeadPitch', 0.1579599380493164], ['LShoulderPitch', 0.11040592193603516], ['LShoulderRoll', 0.9740481376647949], ['LElbowYaw', -1.5769939422607422], ['LElbowRoll', -1.5232200622558594], ['LWristYaw', -1.4956917762756348], ['LHand', 0.29360002279281616], ['RShoulderPitch', -0.21778607368469238], ['RShoulderRoll', -1.2257080078125], ['RElbowYaw', 1.0967681407928467], ['RElbowRoll', 1.5187020301818848], ['RWristYaw', 1.6612800359725952], ['RHand', 0.2979999780654907]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.8], ['HeadPitch', 0.8], ['LShoulderPitch', 0.8], ['LShoulderRoll', 0.8], ['LElbowYaw', 0.8], ['LElbowRoll', 0.8], ['LWristYaw', 0.8], ['LHand', 0.8], ['RShoulderPitch', 0.8], ['RShoulderRoll', 0.8], ['RElbowYaw', 0.8], ['RElbowRoll', 0.8], ['RWristYaw', 0.8], ['RHand', 0.8]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 2 : hold
print("Stage: " + str(2) + ": " + "hold")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.01683211326599121], ['HeadPitch', 0.1579599380493164], ['LShoulderPitch', 0.11040592193603516], ['LShoulderRoll', 0.9740481376647949], ['LElbowYaw', -1.5769939422607422], ['LElbowRoll', -1.5232200622558594], ['LWristYaw', -1.4956917762756348], ['LHand', 0.29399996995925903], ['RShoulderPitch', -0.21778607368469238], ['RShoulderRoll', -1.2257080078125], ['RElbowYaw', 1.0967681407928467], ['RElbowRoll', 1.5187020301818848], ['RWristYaw', 1.6612800359725952], ['RHand', 0.29839998483657837]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 2.2], ['HeadPitch', 2.2], ['LShoulderPitch', 2.2], ['LShoulderRoll', 2.2], ['LElbowYaw', 2.2], ['LElbowRoll', 2.2], ['LWristYaw', 2.2], ['LHand', 2.2], ['RShoulderPitch', 2.2], ['RShoulderRoll', 2.2], ['RElbowYaw', 2.2], ['RElbowRoll', 2.2], ['RWristYaw', 2.2], ['RHand', 2.2]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 3 : down
print("Stage: " + str(3) + ": " + "down")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.01683211326599121], ['HeadPitch', 0.1579599380493164], ['LShoulderPitch', 0.11040592193603516], ['LShoulderRoll', 0.9740481376647949], ['LElbowYaw', -1.5769939422607422], ['LElbowRoll', -1.5232200622558594], ['LWristYaw', -1.4956917762756348], ['LHand', 0.29360002279281616], ['RShoulderPitch', -0.21778607368469238], ['RShoulderRoll', -1.2257080078125], ['RElbowYaw', 1.0967681407928467], ['RElbowRoll', 1.5187020301818848], ['RWristYaw', 1.6612800359725952], ['RHand', 0.29839998483657837]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 1.0], ['HeadPitch', 1.0], ['LShoulderPitch', 1.0], ['LShoulderRoll', 1.0], ['LElbowYaw', 1.0], ['LElbowRoll', 1.0], ['LWristYaw', 1.0], ['LHand', 1.0], ['RShoulderPitch', 1.0], ['RShoulderRoll', 1.0], ['RElbowYaw', 1.0], ['RElbowRoll', 1.0], ['RWristYaw', 1.0], ['RHand', 1.0]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
            