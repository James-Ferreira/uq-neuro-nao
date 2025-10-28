      
angle_modulator = 1.0
duration_modulator = 1.0
        
joint_names_list = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
                   
# Movement: 1 : up
print("Stage: " + str(1) + ": " + "up")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.2009119987487793], ['HeadPitch', -0.04912996292114258], ['LShoulderPitch', 0.03217196464538574], ['LShoulderRoll', 0.18710613250732422], ['LElbowYaw', -1.4113221168518066], ['LElbowRoll', -1.4572581052780151], ['LWristYaw', -0.36820197105407715], ['LHand', 0.3044000267982483], ['RShoulderPitch', 0.9434518814086914], ['RShoulderRoll', -0.31911396980285645], ['RElbowYaw', 0.4754979610443115], ['RElbowRoll', 1.205766201019287], ['RWristYaw', -0.05986785888671875], ['RHand', 0.30879998207092285]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 1.0], ['HeadPitch', 1.0], ['LShoulderPitch', 1.0], ['LShoulderRoll', 1.0], ['LElbowYaw', 1.0], ['LElbowRoll', 1.0], ['LWristYaw', 1.0], ['LHand', 1.0], ['RShoulderPitch', 1.0], ['RShoulderRoll', 1.0], ['RElbowYaw', 1.0], ['RElbowRoll', 1.0], ['RWristYaw', 1.0], ['RHand', 1.0]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 2 : shaked
print("Stage: " + str(2) + ": " + "shaked")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.2009119987487793], ['HeadPitch', -0.047595977783203125], ['LShoulderPitch', 0.09046411514282227], ['LShoulderRoll', 0.20858192443847656], ['LElbowYaw', -0.902033805847168], ['LElbowRoll', -0.5000419616699219], ['LWristYaw', -0.3728039264678955], ['LHand', 0.3044000267982483], ['RShoulderPitch', 0.9434518814086914], ['RShoulderRoll', -0.31911396980285645], ['RElbowYaw', 0.4754979610443115], ['RElbowRoll', 1.205766201019287], ['RWristYaw', -0.05986785888671875], ['RHand', 0.30879998207092285]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.4], ['HeadPitch', 0.4], ['LShoulderPitch', 0.4], ['LShoulderRoll', 0.4], ['LElbowYaw', 0.4], ['LElbowRoll', 0.4], ['LWristYaw', 0.4], ['LHand', 0.4], ['RShoulderPitch', 0.4], ['RShoulderRoll', 0.4], ['RElbowYaw', 0.4], ['RElbowRoll', 0.4], ['RWristYaw', 0.4], ['RHand', 0.4]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 3 : up
print("Stage: " + str(3) + ": " + "up")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.2009119987487793], ['HeadPitch', -0.04912996292114258], ['LShoulderPitch', -0.0813438892364502], ['LShoulderRoll', 0.2070479393005371], ['LElbowYaw', -1.2257080078125], ['LElbowRoll', -1.463394045829773], ['LWristYaw', -0.3528618812561035], ['LHand', 0.3044000267982483], ['RShoulderPitch', 0.9434518814086914], ['RShoulderRoll', -0.317579984664917], ['RElbowYaw', 0.4754979610443115], ['RElbowRoll', 1.205766201019287], ['RWristYaw', -0.0583338737487793], ['RHand', 0.30879998207092285]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.4], ['HeadPitch', 0.4], ['LShoulderPitch', 0.4], ['LShoulderRoll', 0.4], ['LElbowYaw', 0.4], ['LElbowRoll', 0.4], ['LWristYaw', 0.4], ['LHand', 0.4], ['RShoulderPitch', 0.4], ['RShoulderRoll', 0.4], ['RElbowYaw', 0.4], ['RElbowRoll', 0.4], ['RWristYaw', 0.4], ['RHand', 0.4]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 4 : d
print("Stage: " + str(4) + ": " + "d")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.2009119987487793], ['HeadPitch', -0.04912996292114258], ['LShoulderPitch', 0.07512402534484863], ['LShoulderRoll', 0.25], ['LElbowYaw', -1.0094141960144043], ['LElbowRoll', -0.5107800960540771], ['LWristYaw', -0.357464075088501], ['LHand', 0.3044000267982483], ['RShoulderPitch', 0.9434518814086914], ['RShoulderRoll', -0.317579984664917], ['RElbowYaw', 0.4754979610443115], ['RElbowRoll', 1.205766201019287], ['RWristYaw', -0.05986785888671875], ['RHand', 0.30879998207092285]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.4], ['HeadPitch', 0.4], ['LShoulderPitch', 0.4], ['LShoulderRoll', 0.4], ['LElbowYaw', 0.4], ['LElbowRoll', 0.4], ['LWristYaw', 0.4], ['LHand', 0.4], ['RShoulderPitch', 0.4], ['RShoulderRoll', 0.4], ['RElbowYaw', 0.4], ['RElbowRoll', 0.4], ['RWristYaw', 0.4], ['RHand', 0.4]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 5 : up
print("Stage: " + str(5) + ": " + "up")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.2009119987487793], ['HeadPitch', -0.04912996292114258], ['LShoulderPitch', -0.16111207008361816], ['LShoulderRoll', 0.21778607368469238], ['LElbowYaw', -1.302408218383789], ['LElbowRoll', -1.4894720315933228], ['LWristYaw', -0.34212398529052734], ['LHand', 0.3044000267982483], ['RShoulderPitch', 0.9434518814086914], ['RShoulderRoll', -0.31911396980285645], ['RElbowYaw', 0.4754979610443115], ['RElbowRoll', 1.20269775390625], ['RWristYaw', -0.0583338737487793], ['RHand', 0.30879998207092285]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.4], ['HeadPitch', 0.4], ['LShoulderPitch', 0.4], ['LShoulderRoll', 0.4], ['LElbowYaw', 0.4], ['LElbowRoll', 0.4], ['LWristYaw', 0.4], ['LHand', 0.4], ['RShoulderPitch', 0.4], ['RShoulderRoll', 0.4], ['RElbowYaw', 0.4], ['RElbowRoll', 0.4], ['RWristYaw', 0.4], ['RHand', 0.4]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 6 : down
print("Stage: " + str(6) + ": " + "down")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.2009119987487793], ['HeadPitch', -0.047595977783203125], ['LShoulderPitch', 0.8114440441131592], ['LShoulderRoll', 0.42180800437927246], ['LElbowYaw', -0.17491793632507324], ['LElbowRoll', -1.2762460708618164], ['LWristYaw', -0.24701595306396484], ['LHand', 0.3044000267982483], ['RShoulderPitch', 0.9434518814086914], ['RShoulderRoll', -0.31911396980285645], ['RElbowYaw', 0.4754979610443115], ['RElbowRoll', 1.20269775390625], ['RWristYaw', -0.0583338737487793], ['RHand', 0.30879998207092285]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 1.0], ['HeadPitch', 1.0], ['LShoulderPitch', 1.0], ['LShoulderRoll', 1.0], ['LElbowYaw', 1.0], ['LElbowRoll', 1.0], ['LWristYaw', 1.0], ['LHand', 1.0], ['RShoulderPitch', 1.0], ['RShoulderRoll', 1.0], ['RElbowYaw', 1.0], ['RElbowRoll', 1.0], ['RWristYaw', 1.0], ['RHand', 1.0]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
            