      
angle_modulator = 1.0
duration_modulator = 1.0
        
joint_names_list = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
                   
# Movement: 1 : u
print("Stage: " + str(1) + ": " + "u")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.0030260086059570312], ['HeadPitch', -0.004643917083740234], ['LShoulderPitch', 0.007627964019775391], ['LShoulderRoll', 0.15949392318725586], ['LElbowYaw', -1.0400938987731934], ['LElbowRoll', -1.1151759624481201], ['LWristYaw', 0.2039799690246582], ['LHand', 0.6043999791145325], ['RShoulderPitch', 0.8575479984283447], ['RShoulderRoll', -0.13810205459594727], ['RElbowYaw', 0.47089600563049316], ['RElbowRoll', 0.9066357612609863], ['RWristYaw', 1.047680139541626], ['RHand', 0.5591999888420105]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.8], ['HeadPitch', 0.8], ['LShoulderPitch', 0.8], ['LShoulderRoll', 0.8], ['LElbowYaw', 0.8], ['LElbowRoll', 0.8], ['LWristYaw', 0.8], ['LHand', 0.8], ['RShoulderPitch', 0.8], ['RShoulderRoll', 0.8], ['RElbowYaw', 0.8], ['RElbowRoll', 0.8], ['RWristYaw', 0.8], ['RHand', 0.8]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 2 : out
print("Stage: " + str(2) + ": " + "out")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.0030260086059570312], ['HeadPitch', -0.004643917083740234], ['LShoulderPitch', 0.10733795166015625], ['LShoulderRoll', 0.2852821350097656], ['LElbowYaw', -1.9114060401916504], ['LElbowRoll', -1.3406740427017212], ['LWristYaw', 0.8835420608520508], ['LHand', 0.6043999791145325], ['RShoulderPitch', 0.8621501922607422], ['RShoulderRoll', -0.16264605522155762], ['RElbowYaw', 0.4494199752807617], ['RElbowRoll', 0.955723762512207], ['RWristYaw', -0.07674193382263184], ['RHand', 0.5591999888420105]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.4], ['HeadPitch', 0.4], ['LShoulderPitch', 0.4], ['LShoulderRoll', 0.4], ['LElbowYaw', 0.4], ['LElbowRoll', 0.4], ['LWristYaw', 0.4], ['LHand', 0.4], ['RShoulderPitch', 0.4], ['RShoulderRoll', 0.4], ['RElbowYaw', 0.4], ['RElbowRoll', 0.4], ['RWristYaw', 0.4], ['RHand', 0.4]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 3 : in
print("Stage: " + str(3) + ": " + "in")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.0030260086059570312], ['HeadPitch', -0.004643917083740234], ['LShoulderPitch', 0.09966802597045898], ['LShoulderRoll', 0.1349501609802246], ['LElbowYaw', -0.961860179901123], ['LElbowRoll', -1.3391400575637817], ['LWristYaw', 0.8129780292510986], ['LHand', 0.6039999723434448], ['RShoulderPitch', 0.8621501922607422], ['RShoulderRoll', -0.16418004035949707], ['RElbowYaw', 0.4494199752807617], ['RElbowRoll', 0.955723762512207], ['RWristYaw', -0.06753802299499512], ['RHand', 0.5591999888420105]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.4], ['HeadPitch', 0.4], ['LShoulderPitch', 0.4], ['LShoulderRoll', 0.4], ['LElbowYaw', 0.4], ['LElbowRoll', 0.4], ['LWristYaw', 0.4], ['LHand', 0.4], ['RShoulderPitch', 0.4], ['RShoulderRoll', 0.4], ['RElbowYaw', 0.4], ['RElbowRoll', 0.4], ['RWristYaw', 0.4], ['RHand', 0.4]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 4 : out
print("Stage: " + str(4) + ": " + "out")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.0030260086059570312], ['HeadPitch', -0.004643917083740234], ['LShoulderPitch', 0.09660005569458008], ['LShoulderRoll', 0.19170808792114258], ['LElbowYaw', -1.8807258605957031], ['LElbowRoll', -1.2869840860366821], ['LWristYaw', 0.8467259407043457], ['LHand', 0.6043999791145325], ['RShoulderPitch', 0.8621501922607422], ['RShoulderRoll', -0.16418004035949707], ['RElbowYaw', 0.4494199752807617], ['RElbowRoll', 0.955723762512207], ['RWristYaw', -0.06600403785705566], ['RHand', 0.5591999888420105]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.4], ['HeadPitch', 0.4], ['LShoulderPitch', 0.4], ['LShoulderRoll', 0.4], ['LElbowYaw', 0.4], ['LElbowRoll', 0.4], ['LWristYaw', 0.4], ['LHand', 0.4], ['RShoulderPitch', 0.4], ['RShoulderRoll', 0.4], ['RElbowYaw', 0.4], ['RElbowRoll', 0.4], ['RWristYaw', 0.4], ['RHand', 0.4]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 5 : d1
print("Stage: " + str(5) + ": " + "d1")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.0030260086059570312], ['HeadPitch', -0.004643917083740234], ['LShoulderPitch', 0.41874003410339355], ['LShoulderRoll', 0.31442809104919434], ['LElbowYaw', -0.6213119029998779], ['LElbowRoll', -1.2378960847854614], ['LWristYaw', 0.4862360954284668], ['LHand', 0.6043999791145325], ['RShoulderPitch', 0.8621501922607422], ['RShoulderRoll', -0.16264605522155762], ['RElbowYaw', 0.4494199752807617], ['RElbowRoll', 0.955723762512207], ['RWristYaw', -0.06447005271911621], ['RHand', 0.5591999888420105]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.3], ['HeadPitch', 0.3], ['LShoulderPitch', 0.3], ['LShoulderRoll', 0.3], ['LElbowYaw', 0.3], ['LElbowRoll', 0.3], ['LWristYaw', 0.3], ['LHand', 0.3], ['RShoulderPitch', 0.3], ['RShoulderRoll', 0.3], ['RElbowYaw', 0.3], ['RElbowRoll', 0.3], ['RWristYaw', 0.3], ['RHand', 0.3]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 6 : d2
print("Stage: " + str(6) + ": " + "d2")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.0030260086059570312], ['HeadPitch', -0.004643917083740234], ['LShoulderPitch', 0.9157559871673584], ['LShoulderRoll', 0.21625208854675293], ['LElbowYaw', -0.507796049118042], ['LElbowRoll', -1.0507481098175049], ['LWristYaw', -0.1304318904876709], ['LHand', 0.6043999791145325], ['RShoulderPitch', 0.8621501922607422], ['RShoulderRoll', -0.1595778465270996], ['RElbowYaw', 0.4494199752807617], ['RElbowRoll', 0.955723762512207], ['RWristYaw', -0.06293606758117676], ['RHand', 0.5591999888420105]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.3], ['HeadPitch', 0.3], ['LShoulderPitch', 0.3], ['LShoulderRoll', 0.3], ['LElbowYaw', 0.3], ['LElbowRoll', 0.3], ['LWristYaw', 0.3], ['LHand', 0.3], ['RShoulderPitch', 0.3], ['RShoulderRoll', 0.3], ['RElbowYaw', 0.3], ['RElbowRoll', 0.3], ['RWristYaw', 0.3], ['RHand', 0.3]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
            