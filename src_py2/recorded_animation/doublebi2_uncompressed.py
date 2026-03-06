      
angle_modulator = 1.0
duration_modulator = 1.0
        
joint_names_list = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
                   
# Movement: 1 : up
print("Stage: " + str(1) + ": " + "up")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', -0.05066394805908203], ['HeadPitch', -0.04452800750732422], ['LShoulderPitch', -0.047595977783203125], ['LShoulderRoll', 0.6350340843200684], ['LElbowYaw', -1.5141000747680664], ['LElbowRoll', -1.5324240922927856], ['LWristYaw', -1.265592098236084], ['LHand', 0.29360002279281616], ['RShoulderPitch', -0.24539804458618164], ['RShoulderRoll', -1.20269775390625], ['RElbowYaw', 1.3038580417633057], ['RElbowRoll', 1.552450180053711], ['RWristYaw', 0.63043212890625], ['RHand', 0.29839998483657837]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 1.0], ['HeadPitch', 1.0], ['LShoulderPitch', 1.0], ['LShoulderRoll', 1.0], ['LElbowYaw', 1.0], ['LElbowRoll', 1.0], ['LWristYaw', 1.0], ['LHand', 1.0], ['RShoulderPitch', 1.0], ['RShoulderRoll', 1.0], ['RElbowYaw', 1.0], ['RElbowRoll', 1.0], ['RWristYaw', 1.0], ['RHand', 1.0]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 2 : hold
print("Stage: " + str(2) + ": " + "hold")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', -0.05066394805908203], ['HeadPitch', -0.04452800750732422], ['LShoulderPitch', -0.047595977783203125], ['LShoulderRoll', 0.6350340843200684], ['LElbowYaw', -1.5141000747680664], ['LElbowRoll', -1.5324240922927856], ['LWristYaw', -1.265592098236084], ['LHand', 0.29399996995925903], ['RShoulderPitch', -0.24539804458618164], ['RShoulderRoll', -1.205766201019287], ['RElbowYaw', 1.3038580417633057], ['RElbowRoll', 1.552450180053711], ['RWristYaw', 0.63043212890625], ['RHand', 0.29839998483657837]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 2.1], ['HeadPitch', 2.1], ['LShoulderPitch', 2.1], ['LShoulderRoll', 2.1], ['LElbowYaw', 2.1], ['LElbowRoll', 2.1], ['LWristYaw', 2.1], ['LHand', 2.1], ['RShoulderPitch', 2.1], ['RShoulderRoll', 2.1], ['RElbowYaw', 2.1], ['RElbowRoll', 2.1], ['RWristYaw', 2.1], ['RHand', 2.1]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 3 : down
print("Stage: " + str(3) + ": " + "down")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', -0.05066394805908203], ['HeadPitch', -0.04452800750732422], ['LShoulderPitch', 0.8620660305023193], ['LShoulderRoll', 0.18864011764526367], ['LElbowYaw', -0.41728997230529785], ['LElbowRoll', -0.98785400390625], ['LWristYaw', -1.0999197959899902], ['LHand', 0.29360002279281616], ['RShoulderPitch', 0.9434518814086914], ['RShoulderRoll', -0.21326804161071777], ['RElbowYaw', 0.6856560707092285], ['RElbowRoll', 1.035491943359375], ['RWristYaw', 0.2638061046600342], ['RHand', 0.29839998483657837]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 1.0], ['HeadPitch', 1.0], ['LShoulderPitch', 1.0], ['LShoulderRoll', 1.0], ['LElbowYaw', 1.0], ['LElbowRoll', 1.0], ['LWristYaw', 1.0], ['LHand', 1.0], ['RShoulderPitch', 1.0], ['RShoulderRoll', 1.0], ['RElbowYaw', 1.0], ['RElbowRoll', 1.0], ['RWristYaw', 1.0], ['RHand', 1.0]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 4 : hold down
print("Stage: " + str(4) + ": " + "hold down")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', -0.05066394805908203], ['HeadPitch', -0.04452800750732422], ['LShoulderPitch', 0.8620660305023193], ['LShoulderRoll', 0.18864011764526367], ['LElbowYaw', -0.41728997230529785], ['LElbowRoll', -0.98785400390625], ['LWristYaw', -1.1014537811279297], ['LHand', 0.29360002279281616], ['RShoulderPitch', 0.9449858665466309], ['RShoulderRoll', -0.21480202674865723], ['RElbowYaw', 0.6856560707092285], ['RElbowRoll', 1.0339579582214355], ['RWristYaw', 0.2638061046600342], ['RHand', 0.29839998483657837]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.2], ['HeadPitch', 0.2], ['LShoulderPitch', 0.2], ['LShoulderRoll', 0.2], ['LElbowYaw', 0.2], ['LElbowRoll', 0.2], ['LWristYaw', 0.2], ['LHand', 0.2], ['RShoulderPitch', 0.2], ['RShoulderRoll', 0.2], ['RElbowYaw', 0.2], ['RElbowRoll', 0.2], ['RWristYaw', 0.2], ['RHand', 0.2]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
            