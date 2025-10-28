      
angle_modulator = 1.0
duration_modulator = 1.0
        
joint_names_list = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
                   
# Movement: 1 : up
print("Stage: " + str(1) + ": " + "up")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.24233007431030273], ['HeadPitch', -0.03685808181762695], ['LShoulderPitch', -0.2945699691772461], ['LShoulderRoll', 0.15029001235961914], ['LElbowYaw', -1.3745059967041016], ['LElbowRoll', -1.3805580139160156], ['LWristYaw', -0.5231359004974365], ['LHand', 0.3808000087738037], ['RShoulderPitch', 1.0799779891967773], ['RShoulderRoll', -0.44950389862060547], ['RElbowYaw', 0.6012859344482422], ['RElbowRoll', 1.418992042541504], ['RWristYaw', 0.2438640594482422], ['RHand', 0.3083999752998352]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 1.3], ['HeadPitch', 1.3], ['LShoulderPitch', 1.3], ['LShoulderRoll', 1.3], ['LElbowYaw', 1.3], ['LElbowRoll', 1.3], ['LWristYaw', 1.3], ['LHand', 1.3], ['RShoulderPitch', 1.3], ['RShoulderRoll', 1.3], ['RElbowYaw', 1.3], ['RElbowRoll', 1.3], ['RWristYaw', 1.3], ['RHand', 1.3]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 2 : d
print("Stage: " + str(2) + ": " + "d")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.24233007431030273], ['HeadPitch', -0.0353238582611084], ['LShoulderPitch', 0.1518239974975586], ['LShoulderRoll', 0.17330002784729004], ['LElbowYaw', -1.3300199508666992], ['LElbowRoll', -1.3299360275268555], ['LWristYaw', -0.4771158695220947], ['LHand', 0.3808000087738037], ['RShoulderPitch', 1.0799779891967773], ['RShoulderRoll', -0.44950389862060547], ['RElbowYaw', 0.6012859344482422], ['RElbowRoll', 1.4266619682312012], ['RWristYaw', 0.2438640594482422], ['RHand', 0.3083999752998352]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.3], ['HeadPitch', 0.3], ['LShoulderPitch', 0.3], ['LShoulderRoll', 0.3], ['LElbowYaw', 0.3], ['LElbowRoll', 0.3], ['LWristYaw', 0.3], ['LHand', 0.3], ['RShoulderPitch', 0.3], ['RShoulderRoll', 0.3], ['RElbowYaw', 0.3], ['RElbowRoll', 0.3], ['RWristYaw', 0.3], ['RHand', 0.3]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 3 : u
print("Stage: " + str(3) + ": " + "u")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.24233007431030273], ['HeadPitch', -0.03685808181762695], ['LShoulderPitch', -0.16724801063537598], ['LShoulderRoll', 0.2730100154876709], ['LElbowYaw', -1.3668360710144043], ['LElbowRoll', -1.478734016418457], ['LWristYaw', -0.47251391410827637], ['LHand', 0.38120001554489136], ['RShoulderPitch', 1.0799779891967773], ['RShoulderRoll', -0.44950389862060547], ['RElbowYaw', 0.6012859344482422], ['RElbowRoll', 1.415924072265625], ['RWristYaw', 0.2438640594482422], ['RHand', 0.3083999752998352]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.3], ['HeadPitch', 0.3], ['LShoulderPitch', 0.3], ['LShoulderRoll', 0.3], ['LElbowYaw', 0.3], ['LElbowRoll', 0.3], ['LWristYaw', 0.3], ['LHand', 0.3], ['RShoulderPitch', 0.3], ['RShoulderRoll', 0.3], ['RElbowYaw', 0.3], ['RElbowRoll', 0.3], ['RWristYaw', 0.3], ['RHand', 0.3]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 4 : d
print("Stage: " + str(4) + ": " + "d")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.24233007431030273], ['HeadPitch', -0.0353238582611084], ['LShoulderPitch', 0.30062198638916016], ['LShoulderRoll', 0.27147603034973145], ['LElbowYaw', -1.2333779335021973], ['LElbowRoll', -1.4910061359405518], ['LWristYaw', -0.4218919277191162], ['LHand', 0.38120001554489136], ['RShoulderPitch', 1.0799779891967773], ['RShoulderRoll', -0.44950389862060547], ['RElbowYaw', 0.6012859344482422], ['RElbowRoll', 1.4174580574035645], ['RWristYaw', 0.2438640594482422], ['RHand', 0.3083999752998352]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.3], ['HeadPitch', 0.3], ['LShoulderPitch', 0.3], ['LShoulderRoll', 0.3], ['LElbowYaw', 0.3], ['LElbowRoll', 0.3], ['LWristYaw', 0.3], ['LHand', 0.3], ['RShoulderPitch', 0.3], ['RShoulderRoll', 0.3], ['RElbowYaw', 0.3], ['RElbowRoll', 0.3], ['RWristYaw', 0.3], ['RHand', 0.3]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 5 : u
print("Stage: " + str(5) + ": " + "u")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.24233007431030273], ['HeadPitch', -0.03685808181762695], ['LShoulderPitch', -0.20099592208862305], ['LShoulderRoll', 0.23466014862060547], ['LElbowYaw', -1.2487177848815918], ['LElbowRoll', -1.4910061359405518], ['LWristYaw', -0.4249598979949951], ['LHand', 0.3808000087738037], ['RShoulderPitch', 1.0799779891967773], ['RShoulderRoll', -0.44950389862060547], ['RElbowYaw', 0.6012859344482422], ['RElbowRoll', 1.4097881317138672], ['RWristYaw', 0.2438640594482422], ['RHand', 0.3083999752998352]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.3], ['HeadPitch', 0.3], ['LShoulderPitch', 0.3], ['LShoulderRoll', 0.3], ['LElbowYaw', 0.3], ['LElbowRoll', 0.3], ['LWristYaw', 0.3], ['LHand', 0.3], ['RShoulderPitch', 0.3], ['RShoulderRoll', 0.3], ['RElbowYaw', 0.3], ['RElbowRoll', 0.3], ['RWristYaw', 0.3], ['RHand', 0.3]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 6 : down
print("Stage: " + str(6) + ": " + "down")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.24233007431030273], ['HeadPitch', -0.0353238582611084], ['LShoulderPitch', 1.0123980045318604], ['LShoulderRoll', 0.30675792694091797], ['LElbowYaw', -0.6642639636993408], ['LElbowRoll', -1.213352084159851], ['LWristYaw', 0.37578797340393066], ['LHand', 0.38120001554489136], ['RShoulderPitch', 1.0799779891967773], ['RShoulderRoll', -0.4510378837585449], ['RElbowYaw', 0.6012859344482422], ['RElbowRoll', 1.4281959533691406], ['RWristYaw', 0.2438640594482422], ['RHand', 0.3083999752998352]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 1.0], ['HeadPitch', 1.0], ['LShoulderPitch', 1.0], ['LShoulderRoll', 1.0], ['LElbowYaw', 1.0], ['LElbowRoll', 1.0], ['LWristYaw', 1.0], ['LHand', 1.0], ['RShoulderPitch', 1.0], ['RShoulderRoll', 1.0], ['RElbowYaw', 1.0], ['RElbowRoll', 1.0], ['RWristYaw', 1.0], ['RHand', 1.0]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
            