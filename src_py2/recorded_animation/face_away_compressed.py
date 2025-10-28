      
angle_modulator = 1.0
duration_modulator = 1.0
        
joint_names_list = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
                   
[angles_compressed for _, angles_compressed in [['HeadYaw', [-2.11696195602417]], ['HeadPitch', [0.07512402534484863]], ['LShoulderPitch', [0.8390560150146484]], ['LShoulderRoll', [0.12727999687194824]], ['LElbowYaw', [-0.39121198654174805]], ['LElbowRoll', [-0.8666679859161377]], ['LWristYaw', [0.38345813751220703]], ['LHand', [0.8320000171661377]], ['RShoulderPitch', [0.8191978931427002]], ['RShoulderRoll', [-0.04452800750732422]], ['RElbowYaw', [0.47856616973876953]], ['RElbowRoll', [0.7470998764038086]], ['RWristYaw', [-0.6397199630737305]], ['RHand', [0.5175999999046326]]]]
[time_points_compressed for _, time_points_compressed in [['HeadYaw', [1.3]], ['HeadPitch', [1.3]], ['LShoulderPitch', [1.3]], ['LShoulderRoll', [1.3]], ['LElbowYaw', [1.3]], ['LElbowRoll', [1.3]], ['LWristYaw', [1.3]], ['LHand', [1.3]], ['RShoulderPitch', [1.3]], ['RShoulderRoll', [1.3]], ['RElbowYaw', [1.3]], ['RElbowRoll', [1.3]], ['RWristYaw', [1.3]], ['RHand', [1.3]]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, time_points, True)
        