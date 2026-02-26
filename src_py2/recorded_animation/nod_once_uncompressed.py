      
angle_modulator = 1.0
duration_modulator = 1.0
        
joint_names_list = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
                   
# Movement: 1 : down
print("Stage: " + str(1) + ": " + "down")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', -0.0061779022216796875], ['HeadPitch', 0.3082921504974365], ['LShoulderPitch', 0.9019501209259033], ['LShoulderRoll', 0.23619413375854492], ['LElbowYaw', -0.44029998779296875], ['LElbowRoll', -1.0875639915466309], ['LWristYaw', -0.17184996604919434], ['LHand', 0.013599991798400879], ['RShoulderPitch', 0.964928150177002], ['RShoulderRoll', -0.3145120143890381], ['RElbowYaw', 0.4893040657043457], ['RElbowRoll', 1.2180380821228027], ['RWristYaw', 0.13034796714782715], ['RHand', 0.012799978256225586]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.75], ['HeadPitch', 0.75], ['LShoulderPitch', 0.75], ['LShoulderRoll', 0.75], ['LElbowYaw', 0.75], ['LElbowRoll', 0.75], ['LWristYaw', 0.75], ['LHand', 0.75], ['RShoulderPitch', 0.75], ['RShoulderRoll', 0.75], ['RElbowYaw', 0.75], ['RElbowRoll', 0.75], ['RWristYaw', 0.75], ['RHand', 0.75]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 2 : up and back
print("Stage: " + str(2) + ": " + "up and back")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', -0.0015759468078613281], ['HeadPitch', 0.5874800682067871], ['LShoulderPitch', 0.9019501209259033], ['LShoulderRoll', 0.23619413375854492], ['LElbowYaw', -0.44029998779296875], ['LElbowRoll', -1.0998361110687256], ['LWristYaw', -0.1764519214630127], ['LHand', 0.013599991798400879], ['RShoulderPitch', 0.9664621353149414], ['RShoulderRoll', -0.31604599952697754], ['RElbowYaw', 0.4893040657043457], ['RElbowRoll', 1.2272419929504395], ['RWristYaw', 0.13034796714782715], ['RHand', 0.012799978256225586]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.75], ['HeadPitch', 0.75], ['LShoulderPitch', 0.75], ['LShoulderRoll', 0.75], ['LElbowYaw', 0.75], ['LElbowRoll', 0.75], ['LWristYaw', 0.75], ['LHand', 0.75], ['RShoulderPitch', 0.75], ['RShoulderRoll', 0.75], ['RElbowYaw', 0.75], ['RElbowRoll', 0.75], ['RWristYaw', 0.75], ['RHand', 0.75]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 3 : restore
print("Stage: " + str(3) + ": " + "restore")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', -0.03072190284729004], ['HeadPitch', 0.21471810340881348], ['LShoulderPitch', 0.9019501209259033], ['LShoulderRoll', 0.2239220142364502], ['LElbowYaw', -0.4648439884185791], ['LElbowRoll', -1.1121079921722412], ['LWristYaw', -0.1733839511871338], ['LHand', 0.013599991798400879], ['RShoulderPitch', 0.9664621353149414], ['RShoulderRoll', -0.31297802925109863], ['RElbowYaw', 0.4893040657043457], ['RElbowRoll', 1.2763299942016602], ['RWristYaw', 0.13034796714782715], ['RHand', 0.012799978256225586]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.5], ['HeadPitch', 0.5], ['LShoulderPitch', 0.5], ['LShoulderRoll', 0.5], ['LElbowYaw', 0.5], ['LElbowRoll', 0.5], ['LWristYaw', 0.5], ['LHand', 0.5], ['RShoulderPitch', 0.5], ['RShoulderRoll', 0.5], ['RElbowYaw', 0.5], ['RElbowRoll', 0.5], ['RWristYaw', 0.5], ['RHand', 0.5]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
            