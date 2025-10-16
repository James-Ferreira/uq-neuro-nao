      
angle_modulator = 1.0
duration_modulator = 1.0
        
joint_names_list = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
                   
# Movement: 1 : up
print("Stage: " + str(1) + ": " + "up")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', -0.015382051467895508], ['HeadPitch', -0.06293606758117676], ['LShoulderPitch', 0.16716408729553223], ['LShoulderRoll', 0.004559993743896484], ['LElbowYaw', -0.9741320610046387], ['LElbowRoll', -1.1274480819702148], ['LWristYaw', -0.02611994743347168], ['LHand', 0.29399996995925903], ['RShoulderPitch', 0.9357819557189941], ['RShoulderRoll', -0.3068418502807617], ['RElbowYaw', 0.4724299907684326], ['RElbowRoll', 1.199629783630371], ['RWristYaw', -0.007711887359619141], ['RHand', 0.2979999780654907]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 1.25], ['HeadPitch', 1.25], ['LShoulderPitch', 1.25], ['LShoulderRoll', 1.25], ['LElbowYaw', 1.25], ['LElbowRoll', 1.25], ['LWristYaw', 1.25], ['LHand', 1.25], ['RShoulderPitch', 1.25], ['RShoulderRoll', 1.25], ['RElbowYaw', 1.25], ['RElbowRoll', 1.25], ['RWristYaw', 1.25], ['RHand', 1.25]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 2 : out
print("Stage: " + str(2) + ": " + "out")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', -0.4648439884185791], ['HeadPitch', 0.027570009231567383], ['LShoulderPitch', 0.20858192443847656], ['LShoulderRoll', 0.03984212875366211], ['LElbowYaw', -2.0924181938171387], ['LElbowRoll', -1.1872740983963013], ['LWristYaw', -0.1764519214630127], ['LHand', 0.29399996995925903], ['RShoulderPitch', 0.9403839111328125], ['RShoulderRoll', -0.31297802925109863], ['RElbowYaw', 0.47089600563049316], ['RElbowRoll', 1.20269775390625], ['RWristYaw', -0.009245872497558594], ['RHand', 0.2979999780654907]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 1.0], ['HeadPitch', 1.0], ['LShoulderPitch', 1.0], ['LShoulderRoll', 1.0], ['LElbowYaw', 1.0], ['LElbowRoll', 1.0], ['LWristYaw', 1.0], ['LHand', 1.0], ['RShoulderPitch', 1.0], ['RShoulderRoll', 1.0], ['RElbowYaw', 1.0], ['RElbowRoll', 1.0], ['RWristYaw', 1.0], ['RHand', 1.0]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 3 : down
print("Stage: " + str(3) + ": " + "down")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', -0.06907200813293457], ['HeadPitch', 0.590548038482666], ['LShoulderPitch', 0.9080860614776611], ['LShoulderRoll', 0.1840381622314453], ['LElbowYaw', -0.5108640193939209], ['LElbowRoll', -1.0093300342559814], ['LWristYaw', 0.09199810028076172], ['LHand', 0.29399996995925903], ['RShoulderPitch', 0.938849925994873], ['RShoulderRoll', -0.3068418502807617], ['RElbowYaw', 0.4754979610443115], ['RElbowRoll', 1.1965618133544922], ['RWristYaw', -0.0061779022216796875], ['RHand', 0.2979999780654907]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 1.25], ['HeadPitch', 1.25], ['LShoulderPitch', 1.25], ['LShoulderRoll', 1.25], ['LElbowYaw', 1.25], ['LElbowRoll', 1.25], ['LWristYaw', 1.25], ['LHand', 1.25], ['RShoulderPitch', 1.25], ['RShoulderRoll', 1.25], ['RElbowYaw', 1.25], ['RElbowRoll', 1.25], ['RWristYaw', 1.25], ['RHand', 1.25]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
            