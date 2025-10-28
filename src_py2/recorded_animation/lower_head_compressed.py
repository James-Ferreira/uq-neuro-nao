      
angle_modulator = 1.0
duration_modulator = 1.0
        
joint_names_list = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
                   
joint_angles = [angles_compressed for _, angles_compressed in [['HeadYaw', [0.06898808479309082, 0.07819199562072754]], ['HeadPitch', [0.019900083541870117, 0.5874800682067871]], ['LShoulderPitch', [0.9648439884185791, 0.9648439884185791]], ['LShoulderRoll', [0.31749606132507324, 0.3159620761871338]], ['LElbowYaw', [-0.5016598701477051, -0.49859189987182617]], ['LElbowRoll', [-1.2271580696105957, -1.21642005443573]], ['LWristYaw', [-0.9480538368225098, -0.2224719524383545]], ['LHand', [0.38520002365112305, 0.38520002365112305]], ['RShoulderPitch', [1.1091241836547852, 1.0769100189208984]], ['RShoulderRoll', [-0.4771158695220947, -0.4449019432067871]], ['RElbowYaw', [0.6258301734924316, 0.5936160087585449]], ['RElbowRoll', [1.455808162689209, 1.4113221168518066]], ['RWristYaw', [0.9019501209259033, 0.23926210403442383]], ['RHand', [0.30879998207092285, 0.30879998207092285]]]]
time_points = [time_points_compressed for _, time_points_compressed in [['HeadYaw', [0.4, 3.0]], ['HeadPitch', [0.4, 3.0]], ['LShoulderPitch', [0.4, 3.0]], ['LShoulderRoll', [0.4, 3.0]], ['LElbowYaw', [0.4, 3.0]], ['LElbowRoll', [0.4, 3.0]], ['LWristYaw', [0.4, 3.0]], ['LHand', [0.4, 3.0]], ['RShoulderPitch', [0.4, 3.0]], ['RShoulderRoll', [0.4, 3.0]], ['RElbowYaw', [0.4, 3.0]], ['RElbowRoll', [0.4, 3.0]], ['RWristYaw', [0.4, 3.0]], ['RHand', [0.4, 3.0]]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, time_points, True)
        