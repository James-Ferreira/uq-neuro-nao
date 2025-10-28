      
angle_modulator = 1.0
duration_modulator = 1.0
        
joint_names_list = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
                   
# Movement: 1 : up
print("Stage: " + str(1) + ": " + "up")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.31442809104919434], ['HeadPitch', 0.477031946182251], ['LShoulderPitch', 0.3420400619506836], ['LShoulderRoll', -0.14117002487182617], ['LElbowYaw', -0.8667521476745605], ['LElbowRoll', -1.556968092918396], ['LWristYaw', -0.7701098918914795], ['LHand', 0.7580000162124634], ['RShoulderPitch', 0.9173741340637207], ['RShoulderRoll', -0.27002596855163574], ['RElbowYaw', 0.4724299907684326], ['RElbowRoll', 1.1213960647583008], ['RWristYaw', 1.3360720872879028], ['RHand', 0.7195999622344971]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 1.0], ['HeadPitch', 1.0], ['LShoulderPitch', 1.0], ['LShoulderRoll', 1.0], ['LElbowYaw', 1.0], ['LElbowRoll', 1.0], ['LWristYaw', 1.0], ['LHand', 1.0], ['RShoulderPitch', 1.0], ['RShoulderRoll', 1.0], ['RElbowYaw', 1.0], ['RElbowRoll', 1.0], ['RWristYaw', 1.0], ['RHand', 1.0]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 2 : hold
print("Stage: " + str(2) + ": " + "hold")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.31442809104919434], ['HeadPitch', 0.477031946182251], ['LShoulderPitch', 0.3420400619506836], ['LShoulderRoll', -0.1503739356994629], ['LElbowYaw', -0.8667521476745605], ['LElbowRoll', -1.556968092918396], ['LWristYaw', -0.7655079364776611], ['LHand', 0.7580000162124634], ['RShoulderPitch', 0.9158401489257812], ['RShoulderRoll', -0.27002596855163574], ['RElbowYaw', 0.4724299907684326], ['RElbowRoll', 1.1213960647583008], ['RWristYaw', 1.3360720872879028], ['RHand', 0.7195999622344971]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 1.0], ['HeadPitch', 1.0], ['LShoulderPitch', 1.0], ['LShoulderRoll', 1.0], ['LElbowYaw', 1.0], ['LElbowRoll', 1.0], ['LWristYaw', 1.0], ['LHand', 1.0], ['RShoulderPitch', 1.0], ['RShoulderRoll', 1.0], ['RElbowYaw', 1.0], ['RElbowRoll', 1.0], ['RWristYaw', 1.0], ['RHand', 1.0]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 3 : down
print("Stage: " + str(3) + ": " + "down")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.11194014549255371], ['HeadPitch', 0.2469320297241211], ['LShoulderPitch', 0.9172899723052979], ['LShoulderRoll', 0.23926210403442383], ['LElbowYaw', -0.44950389862060547], ['LElbowRoll', -1.1458560228347778], ['LWristYaw', -0.3099100589752197], ['LHand', 0.7580000162124634], ['RShoulderPitch', 0.9127721786499023], ['RShoulderRoll', -0.25315189361572266], ['RElbowYaw', 0.46169209480285645], ['RElbowRoll', 1.115260124206543], ['RWristYaw', 0.6503739356994629], ['RHand', 0.7195999622344971]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 1.0], ['HeadPitch', 1.0], ['LShoulderPitch', 1.0], ['LShoulderRoll', 1.0], ['LElbowYaw', 1.0], ['LElbowRoll', 1.0], ['LWristYaw', 1.0], ['LHand', 1.0], ['RShoulderPitch', 1.0], ['RShoulderRoll', 1.0], ['RElbowYaw', 1.0], ['RElbowRoll', 1.0], ['RWristYaw', 1.0], ['RHand', 1.0]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
            