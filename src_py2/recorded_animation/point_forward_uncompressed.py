      
angle_modulator = 1.0
duration_modulator = 1.0
        
joint_names_list = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
                   
# Movement: 1 : u
print("Stage: " + str(1) + ": " + "u")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.11347413063049316], ['HeadPitch', 0.0858621597290039], ['LShoulderPitch', 0.21471810340881348], ['LShoulderRoll', -0.08748006820678711], ['LElbowYaw', -1.0400938987731934], ['LElbowRoll', -0.01683211326599121], ['LWristYaw', -0.955723762512207], ['LHand', 0.6891999840736389], ['RShoulderPitch', 0.9357819557189941], ['RShoulderRoll', -0.31297802925109863], ['RElbowYaw', 0.4954400062561035], ['RElbowRoll', 1.199629783630371], ['RWristYaw', 0.02143406867980957], ['RHand', 0.30400002002716064]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 1.2], ['HeadPitch', 1.2], ['LShoulderPitch', 1.2], ['LShoulderRoll', 1.2], ['LElbowYaw', 1.2], ['LElbowRoll', 1.2], ['LWristYaw', 1.2], ['LHand', 1.2], ['RShoulderPitch', 1.2], ['RShoulderRoll', 1.2], ['RElbowYaw', 1.2], ['RElbowRoll', 1.2], ['RWristYaw', 1.2], ['RHand', 1.2]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 2 : h
print("Stage: " + str(2) + ": " + "h")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.11194014549255371], ['HeadPitch', 0.08739614486694336], ['LShoulderPitch', 0.21471810340881348], ['LShoulderRoll', -0.09514999389648438], ['LElbowYaw', -1.0400938987731934], ['LElbowRoll', -0.01683211326599121], ['LWristYaw', -0.9480538368225098], ['LHand', 0.6891999840736389], ['RShoulderPitch', 0.9357819557189941], ['RShoulderRoll', -0.31297802925109863], ['RElbowYaw', 0.4954400062561035], ['RElbowRoll', 1.1980957984924316], ['RWristYaw', 0.02143406867980957], ['RHand', 0.30400002002716064]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 1.0], ['HeadPitch', 1.0], ['LShoulderPitch', 1.0], ['LShoulderRoll', 1.0], ['LElbowYaw', 1.0], ['LElbowRoll', 1.0], ['LWristYaw', 1.0], ['LHand', 1.0], ['RShoulderPitch', 1.0], ['RShoulderRoll', 1.0], ['RElbowYaw', 1.0], ['RElbowRoll', 1.0], ['RWristYaw', 1.0], ['RHand', 1.0]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 3 : d
print("Stage: " + str(3) + ": " + "d")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.11347413063049316], ['HeadPitch', 0.0858621597290039], ['LShoulderPitch', 0.9955241680145264], ['LShoulderRoll', 0.34664201736450195], ['LElbowYaw', -0.5216019153594971], ['LElbowRoll', -1.2563040256500244], ['LWristYaw', -0.22707390785217285], ['LHand', 0.6891999840736389], ['RShoulderPitch', 0.9373159408569336], ['RShoulderRoll', -0.31297802925109863], ['RElbowYaw', 0.4954400062561035], ['RElbowRoll', 1.185823917388916], ['RWristYaw', 0.02143406867980957], ['RHand', 0.30400002002716064]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.75], ['HeadPitch', 0.75], ['LShoulderPitch', 0.75], ['LShoulderRoll', 0.75], ['LElbowYaw', 0.75], ['LElbowRoll', 0.75], ['LWristYaw', 0.75], ['LHand', 0.75], ['RShoulderPitch', 0.75], ['RShoulderRoll', 0.75], ['RElbowYaw', 0.75], ['RElbowRoll', 0.75], ['RWristYaw', 0.75], ['RHand', 0.75]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
            