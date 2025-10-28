      
angle_modulator = 1.0
duration_modulator = 1.0
        
joint_names_list = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
                   
# Movement: 1 : point forward up
print("Stage: " + str(1) + ": " + "point forward up")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.0060939788818359375], ['HeadPitch', 0.07205605506896973], ['LShoulderPitch', 0.13341593742370605], ['LShoulderRoll', -0.08594608306884766], ['LElbowYaw', -0.848344087600708], ['LElbowRoll', -0.21318411827087402], ['LWristYaw', -1.4849538803100586], ['LHand', 0.7580000162124634], ['RShoulderPitch', 0.9357819557189941], ['RShoulderRoll', -0.30530786514282227], ['RElbowYaw', 0.4831681251525879], ['RElbowRoll', 1.1873579025268555], ['RWristYaw', 0.5491299629211426], ['RHand', 0.7195999622344971]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 1.2], ['HeadPitch', 1.2], ['LShoulderPitch', 1.2], ['LShoulderRoll', 1.2], ['LElbowYaw', 1.2], ['LElbowRoll', 1.2], ['LWristYaw', 1.2], ['LHand', 1.2], ['RShoulderPitch', 1.2], ['RShoulderRoll', 1.2], ['RElbowYaw', 1.2], ['RElbowRoll', 1.2], ['RWristYaw', 1.2], ['RHand', 1.2]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 2 : hold
print("Stage: " + str(2) + ": " + "hold")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', -0.01691603660583496], ['HeadPitch', 0.22852396965026855], ['LShoulderPitch', 0.21471810340881348], ['LShoulderRoll', 0.01683211326599121], ['LElbowYaw', -0.43723201751708984], ['LElbowRoll', -0.29141807556152344], ['LWristYaw', -1.7672100067138672], ['LHand', 0.7580000162124634], ['RShoulderPitch', 0.9357819557189941], ['RShoulderRoll', -0.29917192459106445], ['RElbowYaw', 0.4831681251525879], ['RElbowRoll', 1.1812219619750977], ['RWristYaw', 0.5491299629211426], ['RHand', 0.7195999622344971]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.75], ['HeadPitch', 0.75], ['LShoulderPitch', 0.75], ['LShoulderRoll', 0.75], ['LElbowYaw', 0.75], ['LElbowRoll', 0.75], ['LWristYaw', 0.75], ['LHand', 0.75], ['RShoulderPitch', 0.75], ['RShoulderRoll', 0.75], ['RElbowYaw', 0.75], ['RElbowRoll', 0.75], ['RWristYaw', 0.75], ['RHand', 0.75]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 3 : down
print("Stage: " + str(3) + ": " + "down")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', -0.01691603660583496], ['HeadPitch', 0.22852396965026855], ['LShoulderPitch', 0.9218921661376953], ['LShoulderRoll', 0.22545599937438965], ['LElbowYaw', -0.5031938552856445], ['LElbowRoll', -1.0691561698913574], ['LWristYaw', -0.5875639915466309], ['LHand', 0.7580000162124634], ['RShoulderPitch', 0.9357819557189941], ['RShoulderRoll', -0.297637939453125], ['RElbowYaw', 0.4662940502166748], ['RElbowRoll', 1.20269775390625], ['RWristYaw', 0.24846601486206055], ['RHand', 0.7195999622344971]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.8], ['HeadPitch', 0.8], ['LShoulderPitch', 0.8], ['LShoulderRoll', 0.8], ['LElbowYaw', 0.8], ['LElbowRoll', 0.8], ['LWristYaw', 0.8], ['LHand', 0.8], ['RShoulderPitch', 0.8], ['RShoulderRoll', 0.8], ['RElbowYaw', 0.8], ['RElbowRoll', 0.8], ['RWristYaw', 0.8], ['RHand', 0.8]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
            