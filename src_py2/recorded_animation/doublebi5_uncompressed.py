      
angle_modulator = 1.0
duration_modulator = 1.0
        
joint_names_list = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
                   
# Movement: 1 : up
print("Stage: " + str(1) + ": " + "up")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', -0.04912996292114258], ['HeadPitch', -0.04452800750732422], ['LShoulderPitch', 0.91115403175354], ['LShoulderRoll', 0.2622721195220947], ['LElbowYaw', -0.4295620918273926], ['LElbowRoll', -1.1842060089111328], ['LWristYaw', 0.010695934295654297], ['LHand', 0.29399996995925903], ['RShoulderPitch', 0.9434518814086914], ['RShoulderRoll', -0.2853660583496094], ['RElbowYaw', 0.5107800960540771], ['RElbowRoll', 1.1796879768371582], ['RWristYaw', 0.007627964019775391], ['RHand', 0.29839998483657837]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 1.1], ['HeadPitch', 1.1], ['LShoulderPitch', 1.1], ['LShoulderRoll', 1.1], ['LElbowYaw', 1.1], ['LElbowRoll', 1.1], ['LWristYaw', 1.1], ['LHand', 1.1], ['RShoulderPitch', 1.1], ['RShoulderRoll', 1.1], ['RElbowYaw', 1.1], ['RElbowRoll', 1.1], ['RWristYaw', 1.1], ['RHand', 1.1]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 2 : hold
print("Stage: " + str(2) + ": " + "hold")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', -0.05066394805908203], ['HeadPitch', -0.04452800750732422], ['LShoulderPitch', 0.038308143615722656], ['LShoulderRoll', 0.9019501209259033], ['LElbowYaw', -1.529439926147461], ['LElbowRoll', -1.514016032218933], ['LWristYaw', -1.2870678901672363], ['LHand', 0.29360002279281616], ['RShoulderPitch', -0.16716408729553223], ['RShoulderRoll', -1.2103681564331055], ['RElbowYaw', 1.363684058189392], ['RElbowRoll', 1.5371098518371582], ['RWristYaw', 0.01683211326599121], ['RHand', 0.29839998483657837]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 3.0], ['HeadPitch', 3.0], ['LShoulderPitch', 3.0], ['LShoulderRoll', 3.0], ['LElbowYaw', 3.0], ['LElbowRoll', 3.0], ['LWristYaw', 3.0], ['LHand', 3.0], ['RShoulderPitch', 3.0], ['RShoulderRoll', 3.0], ['RElbowYaw', 3.0], ['RElbowRoll', 3.0], ['RWristYaw', 3.0], ['RHand', 3.0]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 3 : down
print("Stage: " + str(3) + ": " + "down")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', -0.05066394805908203], ['HeadPitch', -0.04452800750732422], ['LShoulderPitch', 0.9402999877929688], ['LShoulderRoll', 0.2730100154876709], ['LElbowYaw', -0.4648439884185791], ['LElbowRoll', -1.1826720237731934], ['LWristYaw', 0.3650500774383545], ['LHand', 0.29360002279281616], ['RShoulderPitch', 1.0769100189208984], ['RShoulderRoll', -0.428027868270874], ['RElbowYaw', 0.5951499938964844], ['RElbowRoll', 1.3484277725219727], ['RWristYaw', -0.6811380386352539], ['RHand', 0.29839998483657837]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 1.0], ['HeadPitch', 1.0], ['LShoulderPitch', 1.0], ['LShoulderRoll', 1.0], ['LElbowYaw', 1.0], ['LElbowRoll', 1.0], ['LWristYaw', 1.0], ['LHand', 1.0], ['RShoulderPitch', 1.0], ['RShoulderRoll', 1.0], ['RElbowYaw', 1.0], ['RElbowRoll', 1.0], ['RWristYaw', 1.0], ['RHand', 1.0]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 4 : hold down
print("Stage: " + str(4) + ": " + "hold down")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', -0.05066394805908203], ['HeadPitch', -0.04452800750732422], ['LShoulderPitch', 0.9387660026550293], ['LShoulderRoll', 0.2730100154876709], ['LElbowYaw', -0.46331000328063965], ['LElbowRoll', -1.1826720237731934], ['LWristYaw', 0.3650500774383545], ['LHand', 0.29399996995925903], ['RShoulderPitch', 1.0769100189208984], ['RShoulderRoll', -0.4295620918273926], ['RElbowYaw', 0.5951499938964844], ['RElbowRoll', 1.3468937873840332], ['RWristYaw', -0.6811380386352539], ['RHand', 0.29839998483657837]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.5], ['HeadPitch', 0.5], ['LShoulderPitch', 0.5], ['LShoulderRoll', 0.5], ['LElbowYaw', 0.5], ['LElbowRoll', 0.5], ['LWristYaw', 0.5], ['LHand', 0.5], ['RShoulderPitch', 0.5], ['RShoulderRoll', 0.5], ['RElbowYaw', 0.5], ['RElbowRoll', 0.5], ['RWristYaw', 0.5], ['RHand', 0.5]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
            