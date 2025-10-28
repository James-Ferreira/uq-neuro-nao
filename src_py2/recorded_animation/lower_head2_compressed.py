      
angle_modulator = 1.0
duration_modulator = 1.0
        
joint_names_list = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
                   
joint_angles = [angles_compressed for _, angles_compressed in [['HeadYaw', [-0.23627805709838867]], ['HeadPitch', [0.5859460830688477]], ['LShoulderPitch', [0.931096076965332]], ['LShoulderRoll', [0.2668740749359131]], ['LElbowYaw', [-0.4786500930786133]], ['LElbowRoll', [-1.1289820671081543]], ['LWristYaw', [0.16563010215759277]], ['LHand', [0.38520002365112305]], ['RShoulderPitch', [1.089181900024414]], ['RShoulderRoll', [-0.45717406272888184]], ['RElbowYaw', [0.610490083694458]], ['RElbowRoll', [1.435865879058838]], ['RWristYaw', [0.2638061046600342]], ['RHand', [0.30879998207092285]]]]
time_points = [time_points_compressed for _, time_points_compressed in [['HeadYaw', [1.25]], ['HeadPitch', [1.25]], ['LShoulderPitch', [1.25]], ['LShoulderRoll', [1.25]], ['LElbowYaw', [1.25]], ['LElbowRoll', [1.25]], ['LWristYaw', [1.25]], ['LHand', [1.25]], ['RShoulderPitch', [1.25]], ['RShoulderRoll', [1.25]], ['RElbowYaw', [1.25]], ['RElbowRoll', [1.25]], ['RWristYaw', [1.25]], ['RHand', [1.25]]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, time_points, True)
        