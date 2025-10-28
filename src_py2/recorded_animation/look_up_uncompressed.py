      
angle_modulator = 1.0
duration_modulator = 1.0
        
joint_names_list = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
                   
# Movement: 1 : u
print("Stage: " + str(1) + ": " + "u")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.03217196464538574], ['HeadPitch', -0.44643592834472656], ['LShoulderPitch', 0.9402999877929688], ['LShoulderRoll', 0.2822141647338867], ['LElbowYaw', -0.4771158695220947], ['LElbowRoll', -1.1458560228347778], ['LWristYaw', 0.15335798263549805], ['LHand', 0.38120001554489136], ['RShoulderPitch', 1.0799779891967773], ['RShoulderRoll', -0.447969913482666], ['RElbowYaw', 0.6012859344482422], ['RElbowRoll', 1.4174580574035645], ['RWristYaw', 0.24233007431030273], ['RHand', 0.3083999752998352]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 1.2], ['HeadPitch', 1.2], ['LShoulderPitch', 1.2], ['LShoulderRoll', 1.2], ['LElbowYaw', 1.2], ['LElbowRoll', 1.2], ['LWristYaw', 1.2], ['LHand', 1.2], ['RShoulderPitch', 1.2], ['RShoulderRoll', 1.2], ['RElbowYaw', 1.2], ['RElbowRoll', 1.2], ['RWristYaw', 1.2], ['RHand', 1.2]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 2 : h
print("Stage: " + str(2) + ": " + "h")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.0060939788818359375], ['HeadPitch', -0.48938798904418945], ['LShoulderPitch', 0.9387660026550293], ['LShoulderRoll', 0.2668740749359131], ['LElbowYaw', -0.48785400390625], ['LElbowRoll', -1.1397199630737305], ['LWristYaw', 0.16256213188171387], ['LHand', 0.38120001554489136], ['RShoulderPitch', 1.0799779891967773], ['RShoulderRoll', -0.4510378837585449], ['RElbowYaw', 0.6012859344482422], ['RElbowRoll', 1.435865879058838], ['RWristYaw', 0.2438640594482422], ['RHand', 0.3083999752998352]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 1.0], ['HeadPitch', 1.0], ['LShoulderPitch', 1.0], ['LShoulderRoll', 1.0], ['LElbowYaw', 1.0], ['LElbowRoll', 1.0], ['LWristYaw', 1.0], ['LHand', 1.0], ['RShoulderPitch', 1.0], ['RShoulderRoll', 1.0], ['RElbowYaw', 1.0], ['RElbowRoll', 1.0], ['RWristYaw', 1.0], ['RHand', 1.0]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 3 : d
print("Stage: " + str(3) + ": " + "d")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.05058002471923828], ['HeadPitch', 0.25766992568969727], ['LShoulderPitch', 0.9402999877929688], ['LShoulderRoll', 0.27147603034973145], ['LElbowYaw', -0.4847860336303711], ['LElbowRoll', -1.1289820671081543], ['LWristYaw', 0.1548919677734375], ['LHand', 0.38120001554489136], ['RShoulderPitch', 1.0799779891967773], ['RShoulderRoll', -0.4510378837585449], ['RElbowYaw', 0.6012859344482422], ['RElbowRoll', 1.4143900871276855], ['RWristYaw', 0.2438640594482422], ['RHand', 0.3083999752998352]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 1.0], ['HeadPitch', 1.0], ['LShoulderPitch', 1.0], ['LShoulderRoll', 1.0], ['LElbowYaw', 1.0], ['LElbowRoll', 1.0], ['LWristYaw', 1.0], ['LHand', 1.0], ['RShoulderPitch', 1.0], ['RShoulderRoll', 1.0], ['RElbowYaw', 1.0], ['RElbowRoll', 1.0], ['RWristYaw', 1.0], ['RHand', 1.0]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
            