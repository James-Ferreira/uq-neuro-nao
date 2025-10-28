      
angle_modulator = 1.0
duration_modulator = 1.0
        
joint_names_list = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
                   
# Movement: 1 : up
print("Stage: " + str(1) + ": " + "up")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.08893013000488281], ['HeadPitch', 0.26840806007385254], ['LShoulderPitch', -0.0031099319458007812], ['LShoulderRoll', 0.5107800960540771], ['LElbowYaw', -2.1062240600585938], ['LElbowRoll', -1.155060052871704], ['LWristYaw', -0.7609059810638428], ['LHand', 0.7580000162124634], ['RShoulderPitch', -0.038308143615722656], ['RShoulderRoll', -0.2546858787536621], ['RElbowYaw', 2.112276077270508], ['RElbowRoll', 1.3008737564086914], ['RWristYaw', 1.2394300699234009], ['RHand', 0.7195999622344971]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 1.0], ['HeadPitch', 1.0], ['LShoulderPitch', 1.0], ['LShoulderRoll', 1.0], ['LElbowYaw', 1.0], ['LElbowRoll', 1.0], ['LWristYaw', 1.0], ['LHand', 1.0], ['RShoulderPitch', 1.0], ['RShoulderRoll', 1.0], ['RElbowYaw', 1.0], ['RElbowRoll', 1.0], ['RWristYaw', 1.0], ['RHand', 1.0]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 2 : hold
print("Stage: " + str(2) + ": " + "hold")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.08739614486694336], ['HeadPitch', 0.12421202659606934], ['LShoulderPitch', -0.02151799201965332], ['LShoulderRoll', 0.40953612327575684], ['LElbowYaw', -1.7058501243591309], ['LElbowRoll', -1.101370096206665], ['LWristYaw', -1.1796879768371582], ['LHand', 0.7580000162124634], ['RShoulderPitch', 0.18872404098510742], ['RShoulderRoll', -0.22093796730041504], ['RElbowYaw', 2.0217700004577637], ['RElbowRoll', 0.9097042083740234], ['RWristYaw', 1.0983021259307861], ['RHand', 0.7195999622344971]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.75], ['HeadPitch', 0.75], ['LShoulderPitch', 0.75], ['LShoulderRoll', 0.75], ['LElbowYaw', 0.75], ['LElbowRoll', 0.75], ['LWristYaw', 0.75], ['LHand', 0.75], ['RShoulderPitch', 0.75], ['RShoulderRoll', 0.75], ['RElbowYaw', 0.75], ['RElbowRoll', 0.75], ['RWristYaw', 0.75], ['RHand', 0.75]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 3 : down
print("Stage: " + str(3) + ": " + "down")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.08893013000488281], ['HeadPitch', 0.12421202659606934], ['LShoulderPitch', 0.8053081035614014], ['LShoulderRoll', 0.13801813125610352], ['LElbowYaw', -0.3206479549407959], ['LElbowRoll', -0.8436579704284668], ['LWristYaw', -1.1029877662658691], ['LHand', 0.7580000162124634], ['RShoulderPitch', 0.8621501922607422], ['RShoulderRoll', -0.21173405647277832], ['RElbowYaw', 0.41260409355163574], ['RElbowRoll', 1.0247540473937988], ['RWristYaw', 0.4524879455566406], ['RHand', 0.7195999622344971]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 1.0], ['HeadPitch', 1.0], ['LShoulderPitch', 1.0], ['LShoulderRoll', 1.0], ['LElbowYaw', 1.0], ['LElbowRoll', 1.0], ['LWristYaw', 1.0], ['LHand', 1.0], ['RShoulderPitch', 1.0], ['RShoulderRoll', 1.0], ['RElbowYaw', 1.0], ['RElbowRoll', 1.0], ['RWristYaw', 1.0], ['RHand', 1.0]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
            