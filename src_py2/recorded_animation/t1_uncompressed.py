      
angle_modulator = 1.0
duration_modulator = 1.0
        
joint_names_list = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
                   
# Movement: 1 : up
print("Stage: " + str(1) + ": " + "up")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.009161949157714844], ['HeadPitch', -0.06753802299499512], ['LShoulderPitch', 0.8298521041870117], ['LShoulderRoll', -0.02611994743347168], ['LElbowYaw', -0.7394299507141113], ['LElbowRoll', -0.5475959777832031], ['LWristYaw', -1.0462298393249512], ['LHand', 0.7103999853134155], ['RShoulderPitch', 0.9219760894775391], ['RShoulderRoll', -0.2853660583496094], ['RElbowYaw', 0.4693620204925537], ['RElbowRoll', 1.1183280944824219], ['RWristYaw', 1.6658821105957031], ['RHand', 0.29680001735687256]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 1.2], ['HeadPitch', 1.2], ['LShoulderPitch', 1.2], ['LShoulderRoll', 1.2], ['LElbowYaw', 1.2], ['LElbowRoll', 1.2], ['LWristYaw', 1.2], ['LHand', 1.2], ['RShoulderPitch', 1.2], ['RShoulderRoll', 1.2], ['RElbowYaw', 1.2], ['RElbowRoll', 1.2], ['RWristYaw', 1.2], ['RHand', 1.2]]]
meta.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 2 : down
print("Stage: " + str(2) + ": " + "down")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.01222991943359375], ['HeadPitch', 0.3880600929260254], ['LShoulderPitch', 0.8237161636352539], ['LShoulderRoll', -0.052197933197021484], ['LElbowYaw', -0.6719338893890381], ['LElbowRoll', -0.536858081817627], ['LWristYaw', -1.0569682121276855], ['LHand', 0.7099999785423279], ['RShoulderPitch', 0.9219760894775391], ['RShoulderRoll', -0.2884340286254883], ['RElbowYaw', 0.47089600563049316], ['RElbowRoll', 1.1336679458618164], ['RWristYaw', 1.6658821105957031], ['RHand', 0.29680001735687256]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 1.0], ['HeadPitch', 1.0], ['LShoulderPitch', 1.0], ['LShoulderRoll', 1.0], ['LElbowYaw', 1.0], ['LElbowRoll', 1.0], ['LWristYaw', 1.0], ['LHand', 1.0], ['RShoulderPitch', 1.0], ['RShoulderRoll', 1.0], ['RElbowYaw', 1.0], ['RElbowRoll', 1.0], ['RWristYaw', 1.0], ['RHand', 1.0]]]
meta.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
            