      
angle_modulator = 1.0
duration_modulator = 1.0
        
joint_names_list = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
                   
# Movement: 1 : up
print("Stage: " + str(1) + ": " + "up")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', -0.05066394805908203], ['HeadPitch', -0.04452800750732422], ['LShoulderPitch', 0.41567206382751465], ['LShoulderRoll', 0.8359880447387695], ['LElbowYaw', -1.5325078964233398], ['LElbowRoll', -1.5201520919799805], ['LWristYaw', -1.5064301490783691], ['LHand', 0.29360002279281616], ['RShoulderPitch', 0.3007059097290039], ['RShoulderRoll', -0.9833359718322754], ['RElbowYaw', 1.366752028465271], ['RElbowRoll', 1.5079641342163086], ['RWristYaw', 0.8620660305023193], ['RHand', 0.29839998483657837]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 1.2], ['HeadPitch', 1.2], ['LShoulderPitch', 1.2], ['LShoulderRoll', 1.2], ['LElbowYaw', 1.2], ['LElbowRoll', 1.2], ['LWristYaw', 1.2], ['LHand', 1.2], ['RShoulderPitch', 1.2], ['RShoulderRoll', 1.2], ['RElbowYaw', 1.2], ['RElbowRoll', 1.2], ['RWristYaw', 1.2], ['RHand', 1.2]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 2 : hold
print("Stage: " + str(2) + ": " + "hold")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', -0.05066394805908203], ['HeadPitch', -0.04606199264526367], ['LShoulderPitch', 0.41567206382751465], ['LShoulderRoll', 0.8359880447387695], ['LElbowYaw', -1.5325078964233398], ['LElbowRoll', -1.5201520919799805], ['LWristYaw', -1.5064301490783691], ['LHand', 0.29360002279281616], ['RShoulderPitch', 0.30223989486694336], ['RShoulderRoll', -0.9848699569702148], ['RElbowYaw', 1.366752028465271], ['RElbowRoll', 1.5079641342163086], ['RWristYaw', 0.8620660305023193], ['RHand', 0.29839998483657837]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 3.0], ['HeadPitch', 3.0], ['LShoulderPitch', 3.0], ['LShoulderRoll', 3.0], ['LElbowYaw', 3.0], ['LElbowRoll', 3.0], ['LWristYaw', 3.0], ['LHand', 3.0], ['RShoulderPitch', 3.0], ['RShoulderRoll', 3.0], ['RElbowYaw', 3.0], ['RElbowRoll', 3.0], ['RWristYaw', 3.0], ['RHand', 3.0]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 3 : down
print("Stage: " + str(3) + ": " + "down")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', -0.05066394805908203], ['HeadPitch', -0.04606199264526367], ['LShoulderPitch', 0.41567206382751465], ['LShoulderRoll', 0.837522029876709], ['LElbowYaw', -1.5309739112854004], ['LElbowRoll', -1.5201520919799805], ['LWristYaw', -1.5064301490783691], ['LHand', 0.29399996995925903], ['RShoulderPitch', 0.30223989486694336], ['RShoulderRoll', -0.9833359718322754], ['RElbowYaw', 1.366752028465271], ['RElbowRoll', 1.5079641342163086], ['RWristYaw', 0.8620660305023193], ['RHand', 0.29839998483657837]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 1.0], ['HeadPitch', 1.0], ['LShoulderPitch', 1.0], ['LShoulderRoll', 1.0], ['LElbowYaw', 1.0], ['LElbowRoll', 1.0], ['LWristYaw', 1.0], ['LHand', 1.0], ['RShoulderPitch', 1.0], ['RShoulderRoll', 1.0], ['RElbowYaw', 1.0], ['RElbowRoll', 1.0], ['RWristYaw', 1.0], ['RHand', 1.0]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
            