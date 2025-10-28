      
angle_modulator = 1.0
duration_modulator = 1.0
        
joint_names_list = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
                   
# Movement: 1 : e
print("Stage: " + str(1) + ": " + "e")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.0060939788818359375], ['HeadPitch', 0.07205605506896973], ['LShoulderPitch', 0.7792301177978516], ['LShoulderRoll', -0.22400593757629395], ['LElbowYaw', -0.8207318782806396], ['LElbowRoll', -0.19170808792114258], ['LWristYaw', -1.5110321044921875], ['LHand', 0.7580000162124634], ['RShoulderPitch', 0.9449858665466309], ['RShoulderRoll', -0.3068418502807617], ['RElbowYaw', 0.4862360954284668], ['RElbowRoll', 1.1842899322509766], ['RWristYaw', 0.5199840068817139], ['RHand', 0.7195999622344971]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 4.0], ['HeadPitch', 4.0], ['LShoulderPitch', 4.0], ['LShoulderRoll', 4.0], ['LElbowYaw', 4.0], ['LElbowRoll', 4.0], ['LWristYaw', 4.0], ['LHand', 4.0], ['RShoulderPitch', 4.0], ['RShoulderRoll', 4.0], ['RElbowYaw', 4.0], ['RElbowRoll', 4.0], ['RWristYaw', 4.0], ['RHand', 4.0]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 2 : point
print("Stage: " + str(2) + ": " + "point")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.0060939788818359375], ['HeadPitch', 0.07052206993103027], ['LShoulderPitch', 0.1487560272216797], ['LShoulderRoll', -0.11816000938415527], ['LElbowYaw', -0.8268680572509766], ['LElbowRoll', -0.1978440284729004], ['LWristYaw', -1.5048961639404297], ['LHand', 0.7580000162124634], ['RShoulderPitch', 0.9449858665466309], ['RShoulderRoll', -0.3083760738372803], ['RElbowYaw', 0.4862360954284668], ['RElbowRoll', 1.185823917388916], ['RWristYaw', 0.5199840068817139], ['RHand', 0.7195999622344971]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 1.0], ['HeadPitch', 1.0], ['LShoulderPitch', 1.0], ['LShoulderRoll', 1.0], ['LElbowYaw', 1.0], ['LElbowRoll', 1.0], ['LWristYaw', 1.0], ['LHand', 1.0], ['RShoulderPitch', 1.0], ['RShoulderRoll', 1.0], ['RElbowYaw', 1.0], ['RElbowRoll', 1.0], ['RWristYaw', 1.0], ['RHand', 1.0]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
            