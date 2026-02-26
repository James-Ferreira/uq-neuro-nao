      
angle_modulator = 1.0
duration_modulator = 1.0
        
joint_names_list = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
                   
# Movement: 1 : up
print("Stage: " + str(1) + ": " + "up")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.0030260086059570312], ['HeadPitch', 0.1748340129852295], ['LShoulderPitch', 0.8651340007781982], ['LShoulderRoll', 0.12267804145812988], ['LElbowYaw', -0.3237159252166748], ['LElbowRoll', -1.366752028465271], ['LWristYaw', -1.3484277725219727], ['LHand', 0.6552000045776367], ['RShoulderPitch', 0.9971418380737305], ['RShoulderRoll', -0.3896780014038086], ['RElbowYaw', 0.4570901393890381], ['RElbowRoll', 1.3146800994873047], ['RWristYaw', -0.24241399765014648], ['RHand', 0.7215999960899353]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.6], ['HeadPitch', 0.6], ['LShoulderPitch', 0.6], ['LShoulderRoll', 0.6], ['LElbowYaw', 0.6], ['LElbowRoll', 0.6], ['LWristYaw', 0.6], ['LHand', 0.6], ['RShoulderPitch', 0.6], ['RShoulderRoll', 0.6], ['RElbowYaw', 0.6], ['RElbowRoll', 0.6], ['RWristYaw', 0.6], ['RHand', 0.6]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 2 : jab
print("Stage: " + str(2) + ": " + "jab")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.0030260086059570312], ['HeadPitch', 0.1748340129852295], ['LShoulderPitch', 0.8329200744628906], ['LShoulderRoll', -0.28229808807373047], ['LElbowYaw', -1.299339771270752], ['LElbowRoll', -1.441918134689331], ['LWristYaw', -1.061570167541504], ['LHand', 0.6552000045776367], ['RShoulderPitch', 0.7731781005859375], ['RShoulderRoll', 0.21011614799499512], ['RElbowYaw', 0.8820080757141113], ['RElbowRoll', 0.23627805709838867], ['RWristYaw', 0.6212279796600342], ['RHand', 0.7215999960899353]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.5], ['HeadPitch', 0.5], ['LShoulderPitch', 0.5], ['LShoulderRoll', 0.5], ['LElbowYaw', 0.5], ['LElbowRoll', 0.5], ['LWristYaw', 0.5], ['LHand', 0.5], ['RShoulderPitch', 0.5], ['RShoulderRoll', 0.5], ['RElbowYaw', 0.5], ['RElbowRoll', 0.5], ['RWristYaw', 0.5], ['RHand', 0.5]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 3 : d
print("Stage: " + str(3) + ": " + "d")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.0030260086059570312], ['HeadPitch', 0.17943596839904785], ['LShoulderPitch', 0.7393460273742676], ['LShoulderRoll', 0.05824995040893555], ['LElbowYaw', -1.0063457489013672], ['LElbowRoll', -1.5293561220169067], ['LWristYaw', -1.02168607711792], ['LHand', 0.6552000045776367], ['RShoulderPitch', 0.9864039421081543], ['RShoulderRoll', -0.1963939666748047], ['RElbowYaw', 0.9602420330047607], ['RElbowRoll', 1.446603775024414], ['RWristYaw', -0.29917192459106445], ['RHand', 0.7215999960899353]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.4], ['HeadPitch', 0.4], ['LShoulderPitch', 0.4], ['LShoulderRoll', 0.4], ['LElbowYaw', 0.4], ['LElbowRoll', 0.4], ['LWristYaw', 0.4], ['LHand', 0.4], ['RShoulderPitch', 0.4], ['RShoulderRoll', 0.4], ['RElbowYaw', 0.4], ['RElbowRoll', 0.4], ['RWristYaw', 0.4], ['RHand', 0.4]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 4 : restore
print("Stage: " + str(4) + ": " + "restore")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.004559993743896484], ['HeadPitch', 0.17943596839904785], ['LShoulderPitch', 0.8820080757141113], ['LShoulderRoll', 0.1548919677734375], ['LElbowYaw', -0.4449019432067871], ['LElbowRoll', -1.0461461544036865], ['LWristYaw', -1.319282054901123], ['LHand', 0.6552000045776367], ['RShoulderPitch', 0.9511218070983887], ['RShoulderRoll', -0.3145120143890381], ['RElbowYaw', 0.4340801239013672], ['RElbowRoll', 1.2364459037780762], ['RWristYaw', 0.3282339572906494], ['RHand', 0.7215999960899353]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.8], ['HeadPitch', 0.8], ['LShoulderPitch', 0.8], ['LShoulderRoll', 0.8], ['LElbowYaw', 0.8], ['LElbowRoll', 0.8], ['LWristYaw', 0.8], ['LHand', 0.8], ['RShoulderPitch', 0.8], ['RShoulderRoll', 0.8], ['RElbowYaw', 0.8], ['RElbowRoll', 0.8], ['RWristYaw', 0.8], ['RHand', 0.8]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
            