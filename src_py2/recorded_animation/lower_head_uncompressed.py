      
angle_modulator = 1.0
duration_modulator = 1.0
        
joint_names_list = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
                   
# Movement: 1 : u
print("Stage: " + str(1) + ": " + "u")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.06898808479309082], ['HeadPitch', 0.019900083541870117], ['LShoulderPitch', 0.9648439884185791], ['LShoulderRoll', 0.31749606132507324], ['LElbowYaw', -0.5016598701477051], ['LElbowRoll', -1.2271580696105957], ['LWristYaw', -0.9480538368225098], ['LHand', 0.38520002365112305], ['RShoulderPitch', 1.1091241836547852], ['RShoulderRoll', -0.4771158695220947], ['RElbowYaw', 0.6258301734924316], ['RElbowRoll', 1.455808162689209], ['RWristYaw', 0.9019501209259033], ['RHand', 0.30879998207092285]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.4], ['HeadPitch', 0.4], ['LShoulderPitch', 0.4], ['LShoulderRoll', 0.4], ['LElbowYaw', 0.4], ['LElbowRoll', 0.4], ['LWristYaw', 0.4], ['LHand', 0.4], ['RShoulderPitch', 0.4], ['RShoulderRoll', 0.4], ['RElbowYaw', 0.4], ['RElbowRoll', 0.4], ['RWristYaw', 0.4], ['RHand', 0.4]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 2 : d
print("Stage: " + str(2) + ": " + "d")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.07819199562072754], ['HeadPitch', 0.5874800682067871], ['LShoulderPitch', 0.9648439884185791], ['LShoulderRoll', 0.3159620761871338], ['LElbowYaw', -0.49859189987182617], ['LElbowRoll', -1.21642005443573], ['LWristYaw', -0.2224719524383545], ['LHand', 0.38520002365112305], ['RShoulderPitch', 1.0769100189208984], ['RShoulderRoll', -0.4449019432067871], ['RElbowYaw', 0.5936160087585449], ['RElbowRoll', 1.4113221168518066], ['RWristYaw', 0.23926210403442383], ['RHand', 0.30879998207092285]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 1.0], ['HeadPitch', 1.0], ['LShoulderPitch', 1.0], ['LShoulderRoll', 1.0], ['LElbowYaw', 1.0], ['LElbowRoll', 1.0], ['LWristYaw', 1.0], ['LHand', 1.0], ['RShoulderPitch', 1.0], ['RShoulderRoll', 1.0], ['RElbowYaw', 1.0], ['RElbowRoll', 1.0], ['RWristYaw', 1.0], ['RHand', 1.0]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
            