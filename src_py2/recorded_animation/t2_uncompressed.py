      
angle_modulator = 1.0
duration_modulator = 1.0
        
joint_names_list = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
                   
# Movement: 1 : up
print("Stage: " + str(1) + ": " + "up")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.0060939788818359375], ['HeadPitch', 0.3711860179901123], ['LShoulderPitch', 0.8206479549407959], ['LShoulderRoll', -0.042994022369384766], ['LElbowYaw', -0.6688659191131592], ['LElbowRoll', -0.5460619926452637], ['LWristYaw', -1.0646381378173828], ['LHand', 0.7103999853134155], ['RShoulderPitch', 0.9204421043395996], ['RShoulderRoll', -0.2884340286254883], ['RElbowYaw', 0.4693620204925537], ['RElbowRoll', 1.129065990447998], ['RWristYaw', 1.6658821105957031], ['RHand', 0.29680001735687256]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 1.2], ['HeadPitch', 1.2], ['LShoulderPitch', 1.2], ['LShoulderRoll', 1.2], ['LElbowYaw', 1.2], ['LElbowRoll', 1.2], ['LWristYaw', 1.2], ['LHand', 1.2], ['RShoulderPitch', 1.2], ['RShoulderRoll', 1.2], ['RElbowYaw', 1.2], ['RElbowRoll', 1.2], ['RWristYaw', 1.2], ['RHand', 1.2]]]
meta.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 2 : down
print("Stage: " + str(2) + ": " + "down")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.007627964019775391], ['HeadPitch', 0.3711860179901123], ['LShoulderPitch', 0.9172899723052979], ['LShoulderRoll', 0.25], ['LElbowYaw', -0.46331000328063965], ['LElbowRoll', -1.1688660383224487], ['LWristYaw', -1.1474738121032715], ['LHand', 0.7103999853134155], ['RShoulderPitch', 0.9219760894775391], ['RShoulderRoll', -0.2884340286254883], ['RElbowYaw', 0.47089600563049316], ['RElbowRoll', 1.1275320053100586], ['RWristYaw', 1.6658821105957031], ['RHand', 0.29680001735687256]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 1.0], ['HeadPitch', 1.0], ['LShoulderPitch', 1.0], ['LShoulderRoll', 1.0], ['LElbowYaw', 1.0], ['LElbowRoll', 1.0], ['LWristYaw', 1.0], ['LHand', 1.0], ['RShoulderPitch', 1.0], ['RShoulderRoll', 1.0], ['RElbowYaw', 1.0], ['RElbowRoll', 1.0], ['RWristYaw', 1.0], ['RHand', 1.0]]]
meta.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 3 : head up
print("Stage: " + str(3) + ": " + "head up")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.007627964019775391], ['HeadPitch', 0.3711860179901123], ['LShoulderPitch', 0.9157559871673584], ['LShoulderRoll', 0.25], ['LElbowYaw', -0.46331000328063965], ['LElbowRoll', -1.1688660383224487], ['LWristYaw', -1.1474738121032715], ['LHand', 0.7103999853134155], ['RShoulderPitch', 0.9219760894775391], ['RShoulderRoll', -0.2884340286254883], ['RElbowYaw', 0.47089600563049316], ['RElbowRoll', 1.1259980201721191], ['RWristYaw', 1.6658821105957031], ['RHand', 0.29680001735687256]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 1.0], ['HeadPitch', 1.0], ['LShoulderPitch', 1.0], ['LShoulderRoll', 1.0], ['LElbowYaw', 1.0], ['LElbowRoll', 1.0], ['LWristYaw', 1.0], ['LHand', 1.0], ['RShoulderPitch', 1.0], ['RShoulderRoll', 1.0], ['RElbowYaw', 1.0], ['RElbowRoll', 1.0], ['RWristYaw', 1.0], ['RHand', 1.0]]]
meta.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
            