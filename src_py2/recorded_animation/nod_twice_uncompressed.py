      
angle_modulator = 1.0
duration_modulator = 1.0
        
joint_names_list = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
                   
# Movement: 1 : down
print("Stage: " + str(1) + ": " + "down")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', -0.03072190284729004], ['HeadPitch', 0.5859460830688477], ['LShoulderPitch', 0.9096200466156006], ['LShoulderRoll', 0.22545599937438965], ['LElbowYaw', -0.46331000328063965], ['LElbowRoll', -1.0967681407928467], ['LWristYaw', -0.17798590660095215], ['LHand', 0.013599991798400879], ['RShoulderPitch', 0.9725980758666992], ['RShoulderRoll', -0.3267838954925537], ['RElbowYaw', 0.4893040657043457], ['RElbowRoll', 1.2548542022705078], ['RWristYaw', 0.13034796714782715], ['RHand', 0.012799978256225586]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.75], ['HeadPitch', 0.75], ['LShoulderPitch', 0.75], ['LShoulderRoll', 0.75], ['LElbowYaw', 0.75], ['LElbowRoll', 0.75], ['LWristYaw', 0.75], ['LHand', 0.75], ['RShoulderPitch', 0.75], ['RShoulderRoll', 0.75], ['RElbowYaw', 0.75], ['RElbowRoll', 0.75], ['RWristYaw', 0.75], ['RHand', 0.75]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 2 : up
print("Stage: " + str(2) + ": " + "up")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', -0.019984006881713867], ['HeadPitch', -0.3007059097290039], ['LShoulderPitch', 0.9096200466156006], ['LShoulderRoll', 0.2269899845123291], ['LElbowYaw', -0.46331000328063965], ['LElbowRoll', -1.0906319618225098], ['LWristYaw', -0.17798590660095215], ['LHand', 0.013599991798400879], ['RShoulderPitch', 0.9741320610046387], ['RShoulderRoll', -0.3267838954925537], ['RElbowYaw', 0.4893040657043457], ['RElbowRoll', 1.251786231994629], ['RWristYaw', 0.13034796714782715], ['RHand', 0.012799978256225586]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.75], ['HeadPitch', 0.75], ['LShoulderPitch', 0.75], ['LShoulderRoll', 0.75], ['LElbowYaw', 0.75], ['LElbowRoll', 0.75], ['LWristYaw', 0.75], ['LHand', 0.75], ['RShoulderPitch', 0.75], ['RShoulderRoll', 0.75], ['RElbowYaw', 0.75], ['RElbowRoll', 0.75], ['RWristYaw', 0.75], ['RHand', 0.75]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 3 : down
print("Stage: " + str(3) + ": " + "down")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', -0.019984006881713867], ['HeadPitch', 0.5844120979309082], ['LShoulderPitch', 0.9096200466156006], ['LShoulderRoll', 0.2269899845123291], ['LElbowYaw', -0.46944594383239746], ['LElbowRoll', -1.0890979766845703], ['LWristYaw', -0.17798590660095215], ['LHand', 0.013599991798400879], ['RShoulderPitch', 0.9741320610046387], ['RShoulderRoll', -0.32831788063049316], ['RElbowYaw', 0.48777008056640625], ['RElbowRoll', 1.2579221725463867], ['RWristYaw', 0.13034796714782715], ['RHand', 0.012799978256225586]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.75], ['HeadPitch', 0.75], ['LShoulderPitch', 0.75], ['LShoulderRoll', 0.75], ['LElbowYaw', 0.75], ['LElbowRoll', 0.75], ['LWristYaw', 0.75], ['LHand', 0.75], ['RShoulderPitch', 0.75], ['RShoulderRoll', 0.75], ['RElbowYaw', 0.75], ['RElbowRoll', 0.75], ['RWristYaw', 0.75], ['RHand', 0.75]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 4 : up
print("Stage: " + str(4) + ": " + "up")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', -0.019984006881713867], ['HeadPitch', 0.5844120979309082], ['LShoulderPitch', 0.9096200466156006], ['LShoulderRoll', 0.2269899845123291], ['LElbowYaw', -0.46944594383239746], ['LElbowRoll', -1.0890979766845703], ['LWristYaw', -0.17798590660095215], ['LHand', 0.013599991798400879], ['RShoulderPitch', 0.9741320610046387], ['RShoulderRoll', -0.32831788063049316], ['RElbowYaw', 0.48777008056640625], ['RElbowRoll', 1.2579221725463867], ['RWristYaw', 0.13034796714782715], ['RHand', 0.012799978256225586]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.75], ['HeadPitch', 0.75], ['LShoulderPitch', 0.75], ['LShoulderRoll', 0.75], ['LElbowYaw', 0.75], ['LElbowRoll', 0.75], ['LWristYaw', 0.75], ['LHand', 0.75], ['RShoulderPitch', 0.75], ['RShoulderRoll', 0.75], ['RElbowYaw', 0.75], ['RElbowRoll', 0.75], ['RWristYaw', 0.75], ['RHand', 0.75]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 5 : restore
print("Stage: " + str(5) + ": " + "restore")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', -0.027653932571411133], ['HeadPitch', 0.25766992568969727], ['LShoulderPitch', 0.9126880168914795], ['LShoulderRoll', 0.230057954788208], ['LElbowYaw', -0.4709799289703369], ['LElbowRoll', -1.0875639915466309], ['LWristYaw', -0.1764519214630127], ['LHand', 0.013599991798400879], ['RShoulderPitch', 0.9756660461425781], ['RShoulderRoll', -0.3298518657684326], ['RElbowYaw', 0.48777008056640625], ['RElbowRoll', 1.2533202171325684], ['RWristYaw', 0.13034796714782715], ['RHand', 0.012799978256225586]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.5], ['HeadPitch', 0.5], ['LShoulderPitch', 0.5], ['LShoulderRoll', 0.5], ['LElbowYaw', 0.5], ['LElbowRoll', 0.5], ['LWristYaw', 0.5], ['LHand', 0.5], ['RShoulderPitch', 0.5], ['RShoulderRoll', 0.5], ['RElbowYaw', 0.5], ['RElbowRoll', 0.5], ['RWristYaw', 0.5], ['RHand', 0.5]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
            