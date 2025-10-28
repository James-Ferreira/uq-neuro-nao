      
angle_modulator = 1.0
duration_modulator = 1.0
        
joint_names_list = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
                   
# Movement: 1 : u
print("Stage: " + str(1) + ": " + "u")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.21011614799499512], ['HeadPitch', 0.21165013313293457], ['LShoulderPitch', 0.7362780570983887], ['LShoulderRoll', 0.06898808479309082], ['LElbowYaw', -0.38814401626586914], ['LElbowRoll', -1.560036063194275], ['LWristYaw', -1.3699040412902832], ['LHand', 0.38520002365112305], ['RShoulderPitch', 1.112192153930664], ['RShoulderRoll', -0.4786500930786133], ['RElbowYaw', 0.6212279796600342], ['RElbowRoll', 1.4389338493347168], ['RWristYaw', 0.891211986541748], ['RHand', 0.30879998207092285]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 1.0], ['HeadPitch', 1.0], ['LShoulderPitch', 1.0], ['LShoulderRoll', 1.0], ['LElbowYaw', 1.0], ['LElbowRoll', 1.0], ['LWristYaw', 1.0], ['LHand', 1.0], ['RShoulderPitch', 1.0], ['RShoulderRoll', 1.0], ['RElbowYaw', 1.0], ['RElbowRoll', 1.0], ['RWristYaw', 1.0], ['RHand', 1.0]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 2 : h
print("Stage: " + str(2) + ": " + "h")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.21011614799499512], ['HeadPitch', 0.21165013313293457], ['LShoulderPitch', 0.7362780570983887], ['LShoulderRoll', 0.07205605506896973], ['LElbowYaw', -0.38814401626586914], ['LElbowRoll', -1.560036063194275], ['LWristYaw', -1.3699040412902832], ['LHand', 0.38520002365112305], ['RShoulderPitch', 1.1137261390686035], ['RShoulderRoll', -0.4786500930786133], ['RElbowYaw', 0.6212279796600342], ['RElbowRoll', 1.4389338493347168], ['RWristYaw', 0.891211986541748], ['RHand', 0.30879998207092285]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 1.5], ['HeadPitch', 1.5], ['LShoulderPitch', 1.5], ['LShoulderRoll', 1.5], ['LElbowYaw', 1.5], ['LElbowRoll', 1.5], ['LWristYaw', 1.5], ['LHand', 1.5], ['RShoulderPitch', 1.5], ['RShoulderRoll', 1.5], ['RElbowYaw', 1.5], ['RElbowRoll', 1.5], ['RWristYaw', 1.5], ['RHand', 1.5]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 3 : d
print("Stage: " + str(3) + ": " + "d")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.21165013313293457], ['HeadPitch', 0.21165013313293457], ['LShoulderPitch', 0.7362780570983887], ['LShoulderRoll', 0.07512402534484863], ['LElbowYaw', -0.38814401626586914], ['LElbowRoll', -1.560036063194275], ['LWristYaw', -1.3714380264282227], ['LHand', 0.38520002365112305], ['RShoulderPitch', 1.1137261390686035], ['RShoulderRoll', -0.4786500930786133], ['RElbowYaw', 0.6212279796600342], ['RElbowRoll', 1.4389338493347168], ['RWristYaw', 0.891211986541748], ['RHand', 0.30879998207092285]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.8], ['HeadPitch', 0.8], ['LShoulderPitch', 0.8], ['LShoulderRoll', 0.8], ['LElbowYaw', 0.8], ['LElbowRoll', 0.8], ['LWristYaw', 0.8], ['LHand', 0.8], ['RShoulderPitch', 0.8], ['RShoulderRoll', 0.8], ['RElbowYaw', 0.8], ['RElbowRoll', 0.8], ['RWristYaw', 0.8], ['RHand', 0.8]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 4 : d
print("Stage: " + str(4) + ": " + "d")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.21011614799499512], ['HeadPitch', 0.21165013313293457], ['LShoulderPitch', 0.9571740627288818], ['LShoulderRoll', 0.34050607681274414], ['LElbowYaw', -0.4740478992462158], ['LElbowRoll', -1.2424980401992798], ['LWristYaw', -0.9204421043395996], ['LHand', 0.38520002365112305], ['RShoulderPitch', 1.112192153930664], ['RShoulderRoll', -0.4786500930786133], ['RElbowYaw', 0.6212279796600342], ['RElbowRoll', 1.446603775024414], ['RWristYaw', 0.891211986541748], ['RHand', 0.30879998207092285]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.5], ['HeadPitch', 0.5], ['LShoulderPitch', 0.5], ['LShoulderRoll', 0.5], ['LElbowYaw', 0.5], ['LElbowRoll', 0.5], ['LWristYaw', 0.5], ['LHand', 0.5], ['RShoulderPitch', 0.5], ['RShoulderRoll', 0.5], ['RElbowYaw', 0.5], ['RElbowRoll', 0.5], ['RWristYaw', 0.5], ['RHand', 0.5]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
            