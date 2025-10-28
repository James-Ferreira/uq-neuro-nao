      
angle_modulator = 1.0
duration_modulator = 1.0
        
joint_names_list = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
                   
# Movement: 1 : up
print("Stage: " + str(1) + ": " + "up")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', -0.03072190284729004], ['HeadPitch', -0.042994022369384766], ['LShoulderPitch', 0.3220980167388916], ['LShoulderRoll', 1.104438066482544], ['LElbowYaw', -2.1062240600585938], ['LElbowRoll', -0.30062198638916016], ['LWristYaw', -0.21633601188659668], ['LHand', 0.6003999710083008], ['RShoulderPitch', 0.20406389236450195], ['RShoulderRoll', -0.8391399383544922], ['RElbowYaw', 1.010864019393921], ['RElbowRoll', 0.27922987937927246], ['RWristYaw', 1.7257081270217896], ['RHand', 0.5591999888420105]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 1.2], ['HeadPitch', 1.2], ['LShoulderPitch', 1.2], ['LShoulderRoll', 1.2], ['LElbowYaw', 1.2], ['LElbowRoll', 1.2], ['LWristYaw', 1.2], ['LHand', 1.2], ['RShoulderPitch', 1.2], ['RShoulderRoll', 1.2], ['RElbowYaw', 1.2], ['RElbowRoll', 1.2], ['RWristYaw', 1.2], ['RHand', 1.2]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 2 : hold
print("Stage: " + str(2) + ": " + "hold")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', -0.03072190284729004], ['HeadPitch', -0.042994022369384766], ['LShoulderPitch', 0.3220980167388916], ['LShoulderRoll', 1.104438066482544], ['LElbowYaw', -2.1062240600585938], ['LElbowRoll', -0.30062198638916016], ['LWristYaw', -0.21633601188659668], ['LHand', 0.6003999710083008], ['RShoulderPitch', 0.20406389236450195], ['RShoulderRoll', -0.8176639080047607], ['RElbowYaw', 1.010864019393921], ['RElbowRoll', 0.27922987937927246], ['RWristYaw', 1.7257081270217896], ['RHand', 0.5591999888420105]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 1.0], ['HeadPitch', 1.0], ['LShoulderPitch', 1.0], ['LShoulderRoll', 1.0], ['LElbowYaw', 1.0], ['LElbowRoll', 1.0], ['LWristYaw', 1.0], ['LHand', 1.0], ['RShoulderPitch', 1.0], ['RShoulderRoll', 1.0], ['RElbowYaw', 1.0], ['RElbowRoll', 1.0], ['RWristYaw', 1.0], ['RHand', 1.0]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 3 : down
print("Stage: " + str(3) + ": " + "down")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.02603602409362793], ['HeadPitch', 0.10426998138427734], ['LShoulderPitch', 0.8820080757141113], ['LShoulderRoll', 0.10273599624633789], ['LElbowYaw', -0.6657979488372803], ['LElbowRoll', -0.8129780292510986], ['LWristYaw', -0.1733839511871338], ['LHand', 0.6043999791145325], ['RShoulderPitch', 0.8636841773986816], ['RShoulderRoll', -0.1503739356994629], ['RElbowYaw', 0.46782803535461426], ['RElbowRoll', 0.9173741340637207], ['RWristYaw', 1.0200681686401367], ['RHand', 0.5591999888420105]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 1.2], ['HeadPitch', 1.2], ['LShoulderPitch', 1.2], ['LShoulderRoll', 1.2], ['LElbowYaw', 1.2], ['LElbowRoll', 1.2], ['LWristYaw', 1.2], ['LHand', 1.2], ['RShoulderPitch', 1.2], ['RShoulderRoll', 1.2], ['RElbowYaw', 1.2], ['RElbowRoll', 1.2], ['RWristYaw', 1.2], ['RHand', 1.2]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
            