      
angle_modulator = 1.0
duration_modulator = 1.0
        
joint_names_list = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
                   
# Movement: 1 : right
print("Stage: " + str(1) + ": " + "right")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', -0.07980990409851074], ['HeadPitch', 0.16869807243347168], ['LShoulderPitch', 0.91115403175354], ['LShoulderRoll', 0.2269899845123291], ['LElbowYaw', -0.4709799289703369], ['LElbowRoll', -1.0875639915466309], ['LWristYaw', -0.16264605522155762], ['LHand', 0.013599991798400879], ['RShoulderPitch', 0.9741320610046387], ['RShoulderRoll', -0.3298518657684326], ['RElbowYaw', 0.48777008056640625], ['RElbowRoll', 1.262524127960205], ['RWristYaw', 0.13034796714782715], ['RHand', 0.012799978256225586]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.4], ['HeadPitch', 0.4], ['LShoulderPitch', 0.4], ['LShoulderRoll', 0.4], ['LElbowYaw', 0.4], ['LElbowRoll', 0.4], ['LWristYaw', 0.4], ['LHand', 0.4], ['RShoulderPitch', 0.4], ['RShoulderRoll', 0.4], ['RElbowYaw', 0.4], ['RElbowRoll', 0.4], ['RWristYaw', 0.4], ['RHand', 0.4]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 2 : left
print("Stage: " + str(2) + ": " + "left")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.34050607681274414], ['HeadPitch', 0.19631004333496094], ['LShoulderPitch', 0.91115403175354], ['LShoulderRoll', 0.230057954788208], ['LElbowYaw', -0.46944594383239746], ['LElbowRoll', -1.0875639915466309], ['LWristYaw', -0.15804386138916016], ['LHand', 0.013599991798400879], ['RShoulderPitch', 0.9741320610046387], ['RShoulderRoll', -0.3298518657684326], ['RElbowYaw', 0.48777008056640625], ['RElbowRoll', 1.2533202171325684], ['RWristYaw', 0.13034796714782715], ['RHand', 0.012799978256225586]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.6], ['HeadPitch', 0.6], ['LShoulderPitch', 0.6], ['LShoulderRoll', 0.6], ['LElbowYaw', 0.6], ['LElbowRoll', 0.6], ['LWristYaw', 0.6], ['LHand', 0.6], ['RShoulderPitch', 0.6], ['RShoulderRoll', 0.6], ['RElbowYaw', 0.6], ['RElbowRoll', 0.6], ['RWristYaw', 0.6], ['RHand', 0.6]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 3 : right
print("Stage: " + str(3) + ": " + "right")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', -0.5584180355072021], ['HeadPitch', 0.14568805694580078], ['LShoulderPitch', 0.91115403175354], ['LShoulderRoll', 0.230057954788208], ['LElbowYaw', -0.46944594383239746], ['LElbowRoll', -1.0875639915466309], ['LWristYaw', -0.15804386138916016], ['LHand', 0.013599991798400879], ['RShoulderPitch', 0.9741320610046387], ['RShoulderRoll', -0.3298518657684326], ['RElbowYaw', 0.48777008056640625], ['RElbowRoll', 1.2548542022705078], ['RWristYaw', 0.13034796714782715], ['RHand', 0.012799978256225586]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.6], ['HeadPitch', 0.6], ['LShoulderPitch', 0.6], ['LShoulderRoll', 0.6], ['LElbowYaw', 0.6], ['LElbowRoll', 0.6], ['LWristYaw', 0.6], ['LHand', 0.6], ['RShoulderPitch', 0.6], ['RShoulderRoll', 0.6], ['RElbowYaw', 0.6], ['RElbowRoll', 0.6], ['RWristYaw', 0.6], ['RHand', 0.6]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 4 : left
print("Stage: " + str(4) + ": " + "left")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.39879798889160156], ['HeadPitch', 0.18710613250732422], ['LShoulderPitch', 0.91115403175354], ['LShoulderRoll', 0.230057954788208], ['LElbowYaw', -0.467911958694458], ['LElbowRoll', -1.0860300064086914], ['LWristYaw', -0.15804386138916016], ['LHand', 0.013599991798400879], ['RShoulderPitch', 0.9741320610046387], ['RShoulderRoll', -0.3298518657684326], ['RElbowYaw', 0.48777008056640625], ['RElbowRoll', 1.2502517700195312], ['RWristYaw', 0.1288139820098877], ['RHand', 0.012799978256225586]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.6], ['HeadPitch', 0.6], ['LShoulderPitch', 0.6], ['LShoulderRoll', 0.6], ['LElbowYaw', 0.6], ['LElbowRoll', 0.6], ['LWristYaw', 0.6], ['LHand', 0.6], ['RShoulderPitch', 0.6], ['RShoulderRoll', 0.6], ['RElbowYaw', 0.6], ['RElbowRoll', 0.6], ['RWristYaw', 0.6], ['RHand', 0.6]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 5 : right
print("Stage: " + str(5) + ": " + "right")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', -0.524669885635376], ['HeadPitch', 0.13648414611816406], ['LShoulderPitch', 0.9126880168914795], ['LShoulderRoll', 0.230057954788208], ['LElbowYaw', -0.46944594383239746], ['LElbowRoll', -1.0875639915466309], ['LWristYaw', -0.15804386138916016], ['LHand', 0.013599991798400879], ['RShoulderPitch', 0.9741320610046387], ['RShoulderRoll', -0.3298518657684326], ['RElbowYaw', 0.48777008056640625], ['RElbowRoll', 1.2563881874084473], ['RWristYaw', 0.13034796714782715], ['RHand', 0.012799978256225586]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.6], ['HeadPitch', 0.6], ['LShoulderPitch', 0.6], ['LShoulderRoll', 0.6], ['LElbowYaw', 0.6], ['LElbowRoll', 0.6], ['LWristYaw', 0.6], ['LHand', 0.6], ['RShoulderPitch', 0.6], ['RShoulderRoll', 0.6], ['RElbowYaw', 0.6], ['RElbowRoll', 0.6], ['RWristYaw', 0.6], ['RHand', 0.6]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 6 : left
print("Stage: " + str(6) + ": " + "left")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.4632260799407959], ['HeadPitch', 0.21011614799499512], ['LShoulderPitch', 0.9126880168914795], ['LShoulderRoll', 0.230057954788208], ['LElbowYaw', -0.46944594383239746], ['LElbowRoll', -1.0875639915466309], ['LWristYaw', -0.15804386138916016], ['LHand', 0.013599991798400879], ['RShoulderPitch', 0.9741320610046387], ['RShoulderRoll', -0.32831788063049316], ['RElbowYaw', 0.48777008056640625], ['RElbowRoll', 1.251786231994629], ['RWristYaw', 0.13034796714782715], ['RHand', 0.012799978256225586]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.6], ['HeadPitch', 0.6], ['LShoulderPitch', 0.6], ['LShoulderRoll', 0.6], ['LElbowYaw', 0.6], ['LElbowRoll', 0.6], ['LWristYaw', 0.6], ['LHand', 0.6], ['RShoulderPitch', 0.6], ['RShoulderRoll', 0.6], ['RElbowYaw', 0.6], ['RElbowRoll', 0.6], ['RWristYaw', 0.6], ['RHand', 0.6]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 7 : restor
print("Stage: " + str(7) + ": " + "restor")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', -0.09361600875854492], ['HeadPitch', 0.18864011764526367], ['LShoulderPitch', 0.91115403175354], ['LShoulderRoll', 0.230057954788208], ['LElbowYaw', -0.46944594383239746], ['LElbowRoll', -1.0860300064086914], ['LWristYaw', -0.15804386138916016], ['LHand', 0.013599991798400879], ['RShoulderPitch', 0.9741320610046387], ['RShoulderRoll', -0.3298518657684326], ['RElbowYaw', 0.48777008056640625], ['RElbowRoll', 1.2548542022705078], ['RWristYaw', 0.13034796714782715], ['RHand', 0.012799978256225586]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.4], ['HeadPitch', 0.4], ['LShoulderPitch', 0.4], ['LShoulderRoll', 0.4], ['LElbowYaw', 0.4], ['LElbowRoll', 0.4], ['LWristYaw', 0.4], ['LHand', 0.4], ['RShoulderPitch', 0.4], ['RShoulderRoll', 0.4], ['RElbowYaw', 0.4], ['RElbowRoll', 0.4], ['RWristYaw', 0.4], ['RHand', 0.4]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
            