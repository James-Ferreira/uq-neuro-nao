      
angle_modulator = 1.0
duration_modulator = 1.0
        
joint_names_list = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
                   
# Movement: 1 : down
print("Stage: " + str(1) + ": " + "down")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', -0.027653932571411133], ['HeadPitch', 0.25766992568969727], ['LShoulderPitch', 0.91115403175354], ['LShoulderRoll', 0.230057954788208], ['LElbowYaw', -0.46944594383239746], ['LElbowRoll', -1.0875639915466309], ['LWristYaw', -0.1764519214630127], ['LHand', 0.013599991798400879], ['RShoulderPitch', 0.9741320610046387], ['RShoulderRoll', -0.32831788063049316], ['RElbowYaw', 0.48777008056640625], ['RElbowRoll', 1.2533202171325684], ['RWristYaw', 0.13034796714782715], ['RHand', 0.012799978256225586]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.75], ['HeadPitch', 0.75], ['LShoulderPitch', 0.75], ['LShoulderRoll', 0.75], ['LElbowYaw', 0.75], ['LElbowRoll', 0.75], ['LWristYaw', 0.75], ['LHand', 0.75], ['RShoulderPitch', 0.75], ['RShoulderRoll', 0.75], ['RElbowYaw', 0.75], ['RElbowRoll', 0.75], ['RWristYaw', 0.75], ['RHand', 0.75]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 2 : up
print("Stage: " + str(2) + ": " + "up")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', -0.010779857635498047], ['HeadPitch', 0.5874800682067871], ['LShoulderPitch', 0.91115403175354], ['LShoulderRoll', 0.22852396965026855], ['LElbowYaw', -0.46944594383239746], ['LElbowRoll', -1.0875639915466309], ['LWristYaw', -0.16878199577331543], ['LHand', 0.013599991798400879], ['RShoulderPitch', 0.9741320610046387], ['RShoulderRoll', -0.3298518657684326], ['RElbowYaw', 0.48777008056640625], ['RElbowRoll', 1.2609901428222656], ['RWristYaw', 0.13034796714782715], ['RHand', 0.012799978256225586]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.75], ['HeadPitch', 0.75], ['LShoulderPitch', 0.75], ['LShoulderRoll', 0.75], ['LElbowYaw', 0.75], ['LElbowRoll', 0.75], ['LWristYaw', 0.75], ['LHand', 0.75], ['RShoulderPitch', 0.75], ['RShoulderRoll', 0.75], ['RElbowYaw', 0.75], ['RElbowRoll', 0.75], ['RWristYaw', 0.75], ['RHand', 0.75]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 3 : down
print("Stage: " + str(3) + ": " + "down")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.0014920234680175781], ['HeadPitch', 0.5245859622955322], ['LShoulderPitch', 0.9126880168914795], ['LShoulderRoll', 0.230057954788208], ['LElbowYaw', -0.46637797355651855], ['LElbowRoll', -1.0875639915466309], ['LWristYaw', -0.1733839511871338], ['LHand', 0.013599991798400879], ['RShoulderPitch', 0.9741320610046387], ['RShoulderRoll', -0.3298518657684326], ['RElbowYaw', 0.48777008056640625], ['RElbowRoll', 1.245649814605713], ['RWristYaw', 0.13034796714782715], ['RHand', 0.012799978256225586]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.65], ['HeadPitch', 0.65], ['LShoulderPitch', 0.65], ['LShoulderRoll', 0.65], ['LElbowYaw', 0.65], ['LElbowRoll', 0.65], ['LWristYaw', 0.65], ['LHand', 0.65], ['RShoulderPitch', 0.65], ['RShoulderRoll', 0.65], ['RElbowYaw', 0.65], ['RElbowRoll', 0.65], ['RWristYaw', 0.65], ['RHand', 0.65]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 4 : up
print("Stage: " + str(4) + ": " + "up")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', -0.0061779022216796875], ['HeadPitch', 0.5445280075073242], ['LShoulderPitch', 0.91115403175354], ['LShoulderRoll', 0.230057954788208], ['LElbowYaw', -0.467911958694458], ['LElbowRoll', -1.0875639915466309], ['LWristYaw', -0.17184996604919434], ['LHand', 0.013599991798400879], ['RShoulderPitch', 0.9741320610046387], ['RShoulderRoll', -0.32831788063049316], ['RElbowYaw', 0.48777008056640625], ['RElbowRoll', 1.2533202171325684], ['RWristYaw', 0.13034796714782715], ['RHand', 0.012799978256225586]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.65], ['HeadPitch', 0.65], ['LShoulderPitch', 0.65], ['LShoulderRoll', 0.65], ['LElbowYaw', 0.65], ['LElbowRoll', 0.65], ['LWristYaw', 0.65], ['LHand', 0.65], ['RShoulderPitch', 0.65], ['RShoulderRoll', 0.65], ['RElbowYaw', 0.65], ['RElbowRoll', 0.65], ['RWristYaw', 0.65], ['RHand', 0.65]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 5 : down
print("Stage: " + str(5) + ": " + "down")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.02603602409362793], ['HeadPitch', 0.5874800682067871], ['LShoulderPitch', 0.91115403175354], ['LShoulderRoll', 0.22852396965026855], ['LElbowYaw', -0.4709799289703369], ['LElbowRoll', -1.0875639915466309], ['LWristYaw', -0.16571402549743652], ['LHand', 0.013599991798400879], ['RShoulderPitch', 0.9741320610046387], ['RShoulderRoll', -0.3298518657684326], ['RElbowYaw', 0.48777008056640625], ['RElbowRoll', 1.2609901428222656], ['RWristYaw', 0.13034796714782715], ['RHand', 0.012799978256225586]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.65], ['HeadPitch', 0.65], ['LShoulderPitch', 0.65], ['LShoulderRoll', 0.65], ['LElbowYaw', 0.65], ['LElbowRoll', 0.65], ['LWristYaw', 0.65], ['LHand', 0.65], ['RShoulderPitch', 0.65], ['RShoulderRoll', 0.65], ['RElbowYaw', 0.65], ['RElbowRoll', 0.65], ['RWristYaw', 0.65], ['RHand', 0.65]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 6 : up
print("Stage: " + str(6) + ": " + "up")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.02603602409362793], ['HeadPitch', 0.5874800682067871], ['LShoulderPitch', 0.9126880168914795], ['LShoulderRoll', 0.22852396965026855], ['LElbowYaw', -0.4709799289703369], ['LElbowRoll', -1.0875639915466309], ['LWristYaw', -0.16571402549743652], ['LHand', 0.013599991798400879], ['RShoulderPitch', 0.9741320610046387], ['RShoulderRoll', -0.3298518657684326], ['RElbowYaw', 0.48777008056640625], ['RElbowRoll', 1.2609901428222656], ['RWristYaw', 0.13034796714782715], ['RHand', 0.012799978256225586]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.5], ['HeadPitch', 0.5], ['LShoulderPitch', 0.5], ['LShoulderRoll', 0.5], ['LElbowYaw', 0.5], ['LElbowRoll', 0.5], ['LWristYaw', 0.5], ['LHand', 0.5], ['RShoulderPitch', 0.5], ['RShoulderRoll', 0.5], ['RElbowYaw', 0.5], ['RElbowRoll', 0.5], ['RWristYaw', 0.5], ['RHand', 0.5]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
            