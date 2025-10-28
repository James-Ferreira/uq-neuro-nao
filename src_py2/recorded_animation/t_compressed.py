      
angle_modulator = 1.0
duration_modulator = 1.0
        
joint_names_list = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
                   
joint_angles = [angles_compressed for _, angles_compressed in [['HeadYaw', [0.0060939788818359375, 0.0060939788818359375]], ['HeadPitch', [0.07205605506896973, 0.07052206993103027]], ['LShoulderPitch', [0.7792301177978516, 0.1487560272216797]], ['LShoulderRoll', [-0.22400593757629395, -0.11816000938415527]], ['LElbowYaw', [-0.8207318782806396, -0.8268680572509766]], ['LElbowRoll', [-0.19170808792114258, -0.1978440284729004]], ['LWristYaw', [-1.5110321044921875, -1.5048961639404297]], ['LHand', [0.7580000162124634, 0.7580000162124634]], ['RShoulderPitch', [0.9449858665466309, 0.9449858665466309]], ['RShoulderRoll', [-0.3068418502807617, -0.3083760738372803]], ['RElbowYaw', [0.4862360954284668, 0.4862360954284668]], ['RElbowRoll', [1.1842899322509766, 1.185823917388916]], ['RWristYaw', [0.5199840068817139, 0.5199840068817139]], ['RHand', [0.7195999622344971, 0.7195999622344971]]]]
time_points = [time_points_compressed for _, time_points_compressed in [['HeadYaw', [4.0, 5.0]], ['HeadPitch', [4.0, 5.0]], ['LShoulderPitch', [4.0, 5.0]], ['LShoulderRoll', [4.0, 5.0]], ['LElbowYaw', [4.0, 5.0]], ['LElbowRoll', [4.0, 5.0]], ['LWristYaw', [4.0, 5.0]], ['LHand', [4.0, 5.0]], ['RShoulderPitch', [4.0, 5.0]], ['RShoulderRoll', [4.0, 5.0]], ['RElbowYaw', [4.0, 5.0]], ['RElbowRoll', [4.0, 5.0]], ['RWristYaw', [4.0, 5.0]], ['RHand', [4.0, 5.0]]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, time_points, True)
        