      
angle_modulator = 1.0
duration_modulator = 1.0
        
joint_names_list = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
                   
# Movement: 1 : left
print("Stage: " + str(1) + ": " + "left")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', -0.0061779022216796875], ['HeadPitch', 0.0367741584777832], ['LShoulderPitch', 0.91115403175354], ['LShoulderRoll', 0.22852396965026855], ['LElbowYaw', -0.46944594383239746], ['LElbowRoll', -1.0875639915466309], ['LWristYaw', -0.16724801063537598], ['LHand', 0.013599991798400879], ['RShoulderPitch', 0.9741320610046387], ['RShoulderRoll', -0.3298518657684326], ['RElbowYaw', 0.48777008056640625], ['RElbowRoll', 1.2579221725463867], ['RWristYaw', 0.13034796714782715], ['RHand', 0.012799978256225586]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.5], ['HeadPitch', 0.5], ['LShoulderPitch', 0.5], ['LShoulderRoll', 0.5], ['LElbowYaw', 0.5], ['LElbowRoll', 0.5], ['LWristYaw', 0.5], ['LHand', 0.5], ['RShoulderPitch', 0.5], ['RShoulderRoll', 0.5], ['RElbowYaw', 0.5], ['RElbowRoll', 0.5], ['RWristYaw', 0.5], ['RHand', 0.5]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 2 : right
print("Stage: " + str(2) + ": " + "right")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.6994619369506836], ['HeadPitch', -0.0061779022216796875], ['LShoulderPitch', 0.91115403175354], ['LShoulderRoll', 0.22852396965026855], ['LElbowYaw', -0.4709799289703369], ['LElbowRoll', -1.0860300064086914], ['LWristYaw', -0.16724801063537598], ['LHand', 0.013599991798400879], ['RShoulderPitch', 0.9741320610046387], ['RShoulderRoll', -0.3298518657684326], ['RElbowYaw', 0.48777008056640625], ['RElbowRoll', 1.2563881874084473], ['RWristYaw', 0.13034796714782715], ['RHand', 0.012799978256225586]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.8], ['HeadPitch', 0.8], ['LShoulderPitch', 0.8], ['LShoulderRoll', 0.8], ['LElbowYaw', 0.8], ['LElbowRoll', 0.8], ['LWristYaw', 0.8], ['LHand', 0.8], ['RShoulderPitch', 0.8], ['RShoulderRoll', 0.8], ['RElbowYaw', 0.8], ['RElbowRoll', 0.8], ['RWristYaw', 0.8], ['RHand', 0.8]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 3 : left
print("Stage: " + str(3) + ": " + "left")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.6933259963989258], ['HeadPitch', 0.013764142990112305], ['LShoulderPitch', 0.91115403175354], ['LShoulderRoll', 0.230057954788208], ['LElbowYaw', -0.46944594383239746], ['LElbowRoll', -1.0875639915466309], ['LWristYaw', -0.16571402549743652], ['LHand', 0.013599991798400879], ['RShoulderPitch', 0.9741320610046387], ['RShoulderRoll', -0.3298518657684326], ['RElbowYaw', 0.48777008056640625], ['RElbowRoll', 1.2487177848815918], ['RWristYaw', 0.13034796714782715], ['RHand', 0.012799978256225586]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.8], ['HeadPitch', 0.8], ['LShoulderPitch', 0.8], ['LShoulderRoll', 0.8], ['LElbowYaw', 0.8], ['LElbowRoll', 0.8], ['LWristYaw', 0.8], ['LHand', 0.8], ['RShoulderPitch', 0.8], ['RShoulderRoll', 0.8], ['RElbowYaw', 0.8], ['RElbowRoll', 0.8], ['RWristYaw', 0.8], ['RHand', 0.8]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 4 : right
print("Stage: " + str(4) + ": " + "right")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', -0.7455658912658691], ['HeadPitch', 0.01683211326599121], ['LShoulderPitch', 0.9126880168914795], ['LShoulderRoll', 0.22852396965026855], ['LElbowYaw', -0.4709799289703369], ['LElbowRoll', -1.0875639915466309], ['LWristYaw', -0.16264605522155762], ['LHand', 0.013599991798400879], ['RShoulderPitch', 0.9756660461425781], ['RShoulderRoll', -0.3298518657684326], ['RElbowYaw', 0.48777008056640625], ['RElbowRoll', 1.2594561576843262], ['RWristYaw', 0.13034796714782715], ['RHand', 0.012799978256225586]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.8], ['HeadPitch', 0.8], ['LShoulderPitch', 0.8], ['LShoulderRoll', 0.8], ['LElbowYaw', 0.8], ['LElbowRoll', 0.8], ['LWristYaw', 0.8], ['LHand', 0.8], ['RShoulderPitch', 0.8], ['RShoulderRoll', 0.8], ['RElbowYaw', 0.8], ['RElbowRoll', 0.8], ['RWristYaw', 0.8], ['RHand', 0.8]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 5 : retore
print("Stage: " + str(5) + ": " + "retore")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', -0.07980990409851074], ['HeadPitch', 0.17023205757141113], ['LShoulderPitch', 0.91115403175354], ['LShoulderRoll', 0.22852396965026855], ['LElbowYaw', -0.4709799289703369], ['LElbowRoll', -1.0875639915466309], ['LWristYaw', -0.16111207008361816], ['LHand', 0.013599991798400879], ['RShoulderPitch', 0.9741320610046387], ['RShoulderRoll', -0.3298518657684326], ['RElbowYaw', 0.48777008056640625], ['RElbowRoll', 1.262524127960205], ['RWristYaw', 0.13034796714782715], ['RHand', 0.012799978256225586]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.4], ['HeadPitch', 0.4], ['LShoulderPitch', 0.4], ['LShoulderRoll', 0.4], ['LElbowYaw', 0.4], ['LElbowRoll', 0.4], ['LWristYaw', 0.4], ['LHand', 0.4], ['RShoulderPitch', 0.4], ['RShoulderRoll', 0.4], ['RElbowYaw', 0.4], ['RElbowRoll', 0.4], ['RWristYaw', 0.4], ['RHand', 0.4]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
            