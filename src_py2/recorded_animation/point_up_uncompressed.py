      
angle_modulator = 1.0
duration_modulator = 1.0
        
joint_names_list = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
                   
# Movement: 1 : up
print("Stage: " + str(1) + ": " + "up")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.3313021659851074], ['HeadPitch', -0.3958139419555664], ['LShoulderPitch', -1.0078802108764648], ['LShoulderRoll', 0.2239220142364502], ['LElbowYaw', -1.1167941093444824], ['LElbowRoll', -0.5491299629211426], ['LWristYaw', -0.4218919277191162], ['LHand', 0.6763999462127686], ['RShoulderPitch', 1.0799779891967773], ['RShoulderRoll', -0.44950389862060547], ['RElbowYaw', 0.6028201580047607], ['RElbowRoll', 1.3944478034973145], ['RWristYaw', 1.742582082748413], ['RHand', 0.5680000185966492]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 1.4], ['HeadPitch', 1.4], ['LShoulderPitch', 1.4], ['LShoulderRoll', 1.4], ['LElbowYaw', 1.4], ['LElbowRoll', 1.4], ['LWristYaw', 1.4], ['LHand', 1.4], ['RShoulderPitch', 1.4], ['RShoulderRoll', 1.4], ['RElbowYaw', 1.4], ['RElbowRoll', 1.4], ['RWristYaw', 1.4], ['RHand', 1.4]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 2 : hold
print("Stage: " + str(2) + ": " + "hold")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.3313021659851074], ['HeadPitch', -0.39734792709350586], ['LShoulderPitch', -1.0078802108764648], ['LShoulderRoll', 0.22852396965026855], ['LElbowYaw', -1.1167941093444824], ['LElbowRoll', -0.5491299629211426], ['LWristYaw', -0.4218919277191162], ['LHand', 0.6763999462127686], ['RShoulderPitch', 1.0799779891967773], ['RShoulderRoll', -0.44950389862060547], ['RElbowYaw', 0.6028201580047607], ['RElbowRoll', 1.3944478034973145], ['RWristYaw', 1.742582082748413], ['RHand', 0.5680000185966492]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.75], ['HeadPitch', 0.75], ['LShoulderPitch', 0.75], ['LShoulderRoll', 0.75], ['LElbowYaw', 0.75], ['LElbowRoll', 0.75], ['LWristYaw', 0.75], ['LHand', 0.75], ['RShoulderPitch', 0.75], ['RShoulderRoll', 0.75], ['RElbowYaw', 0.75], ['RElbowRoll', 0.75], ['RWristYaw', 0.75], ['RHand', 0.75]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 3 : d
print("Stage: " + str(3) + ": " + "d")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.14108610153198242], ['HeadPitch', 0.1518239974975586], ['LShoulderPitch', 0.877406120300293], ['LShoulderRoll', 0.09813404083251953], ['LElbowYaw', -0.5768260955810547], ['LElbowRoll', -0.8221821784973145], ['LWristYaw', -0.06447005271911621], ['LHand', 0.6763999462127686], ['RShoulderPitch', 1.061570167541504], ['RShoulderRoll', -0.4295620918273926], ['RElbowYaw', 0.5844120979309082], ['RElbowRoll', 1.3852438926696777], ['RWristYaw', 0.9801840782165527], ['RHand', 0.5676000118255615]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 1.2], ['HeadPitch', 1.2], ['LShoulderPitch', 1.2], ['LShoulderRoll', 1.2], ['LElbowYaw', 1.2], ['LElbowRoll', 1.2], ['LWristYaw', 1.2], ['LHand', 1.2], ['RShoulderPitch', 1.2], ['RShoulderRoll', 1.2], ['RElbowYaw', 1.2], ['RElbowRoll', 1.2], ['RWristYaw', 1.2], ['RHand', 1.2]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
            