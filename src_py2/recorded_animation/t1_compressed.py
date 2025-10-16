      
angle_modulator = 1.0
duration_modulator = 1.0
        
joint_names_list = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
                   
joint_angles = [angles_compressed for _, angles_compressed in [['HeadYaw', [0.009161949157714844, 0.01222991943359375]], ['HeadPitch', [-0.06753802299499512, 0.3880600929260254]], ['LShoulderPitch', [0.8298521041870117, 0.8237161636352539]], ['LShoulderRoll', [-0.02611994743347168, -0.052197933197021484]], ['LElbowYaw', [-0.7394299507141113, -0.6719338893890381]], ['LElbowRoll', [-0.5475959777832031, -0.536858081817627]], ['LWristYaw', [-1.0462298393249512, -1.0569682121276855]], ['LHand', [0.7103999853134155, 0.7099999785423279]], ['RShoulderPitch', [0.9219760894775391, 0.9219760894775391]], ['RShoulderRoll', [-0.2853660583496094, -0.2884340286254883]], ['RElbowYaw', [0.4693620204925537, 0.47089600563049316]], ['RElbowRoll', [1.1183280944824219, 1.1336679458618164]], ['RWristYaw', [1.6658821105957031, 1.6658821105957031]], ['RHand', [0.29680001735687256, 0.29680001735687256]]]]
time_points = [time_points_compressed for _, time_points_compressed in [['HeadYaw', [1.2, 2.2]], ['HeadPitch', [1.2, 2.2]], ['LShoulderPitch', [1.2, 2.2]], ['LShoulderRoll', [1.2, 2.2]], ['LElbowYaw', [1.2, 2.2]], ['LElbowRoll', [1.2, 2.2]], ['LWristYaw', [1.2, 2.2]], ['LHand', [1.2, 2.2]], ['RShoulderPitch', [1.2, 2.2]], ['RShoulderRoll', [1.2, 2.2]], ['RElbowYaw', [1.2, 2.2]], ['RElbowRoll', [1.2, 2.2]], ['RWristYaw', [1.2, 2.2]], ['RHand', [1.2, 2.2]]]]
meta.motion.angleInterpolation(joint_names_list, joint_angles, time_points, True)
        