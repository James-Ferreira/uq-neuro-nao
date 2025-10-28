      
angle_modulator = 1.0
duration_modulator = 1.0
        
joint_names_list = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
                   
# Movement: 1 : u
print("Stage: " + str(1) + ": " + "u")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.3389720916748047], ['HeadPitch', 0.43254613876342773], ['LShoulderPitch', -0.33138608932495117], ['LShoulderRoll', 0.47089600563049316], ['LElbowYaw', -0.7793140411376953], ['LElbowRoll', -1.553900122642517], ['LWristYaw', -1.5033621788024902], ['LHand', 0.765999972820282], ['RShoulderPitch', 0.925044059753418], ['RShoulderRoll', -0.277695894241333], ['RElbowYaw', 0.46782803535461426], ['RElbowRoll', 1.132133960723877], ['RWristYaw', 0.11961007118225098], ['RHand', 0.46160000562667847]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 1.0], ['HeadPitch', 1.0], ['LShoulderPitch', 1.0], ['LShoulderRoll', 1.0], ['LElbowYaw', 1.0], ['LElbowRoll', 1.0], ['LWristYaw', 1.0], ['LHand', 1.0], ['RShoulderPitch', 1.0], ['RShoulderRoll', 1.0], ['RElbowYaw', 1.0], ['RElbowRoll', 1.0], ['RWristYaw', 1.0], ['RHand', 1.0]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 2 : d
print("Stage: " + str(2) + ": " + "d")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.3389720916748047], ['HeadPitch', 0.43254613876342773], ['LShoulderPitch', -0.06753802299499512], ['LShoulderRoll', 0.2960200309753418], ['LElbowYaw', -0.7915859222412109], ['LElbowRoll', -1.5354920625686646], ['LWristYaw', -1.8255019187927246], ['LHand', 0.7663999795913696], ['RShoulderPitch', 0.925044059753418], ['RShoulderRoll', -0.2807638645172119], ['RElbowYaw', 0.46782803535461426], ['RElbowRoll', 1.1474738121032715], ['RWristYaw', 0.11961007118225098], ['RHand', 0.4611999988555908]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.25], ['HeadPitch', 0.25], ['LShoulderPitch', 0.25], ['LShoulderRoll', 0.25], ['LElbowYaw', 0.25], ['LElbowRoll', 0.25], ['LWristYaw', 0.25], ['LHand', 0.25], ['RShoulderPitch', 0.25], ['RShoulderRoll', 0.25], ['RElbowYaw', 0.25], ['RElbowRoll', 0.25], ['RWristYaw', 0.25], ['RHand', 0.25]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 3 : u
print("Stage: " + str(3) + ": " + "u")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.34050607681274414], ['HeadPitch', 0.43254613876342773], ['LShoulderPitch', -0.5047280788421631], ['LShoulderRoll', 0.41567206382751465], ['LElbowYaw', -0.8253340721130371], ['LElbowRoll', -1.5354920625686646], ['LWristYaw', -1.8147640228271484], ['LHand', 0.765999972820282], ['RShoulderPitch', 0.925044059753418], ['RShoulderRoll', -0.27922987937927246], ['RElbowYaw', 0.46782803535461426], ['RElbowRoll', 1.1398038864135742], ['RWristYaw', 0.11961007118225098], ['RHand', 0.46160000562667847]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.25], ['HeadPitch', 0.25], ['LShoulderPitch', 0.25], ['LShoulderRoll', 0.25], ['LElbowYaw', 0.25], ['LElbowRoll', 0.25], ['LWristYaw', 0.25], ['LHand', 0.25], ['RShoulderPitch', 0.25], ['RShoulderRoll', 0.25], ['RElbowYaw', 0.25], ['RElbowRoll', 0.25], ['RWristYaw', 0.25], ['RHand', 0.25]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 4 : d
print("Stage: " + str(4) + ": " + "d")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.34050607681274414], ['HeadPitch', 0.4340801239013672], ['LShoulderPitch', -0.09821796417236328], ['LShoulderRoll', 0.2990880012512207], ['LElbowYaw', -0.8253340721130371], ['LElbowRoll', -1.5446960926055908], ['LWristYaw', -1.8147640228271484], ['LHand', 0.765999972820282], ['RShoulderPitch', 0.925044059753418], ['RShoulderRoll', -0.27922987937927246], ['RElbowYaw', 0.46782803535461426], ['RElbowRoll', 1.1413378715515137], ['RWristYaw', 0.11961007118225098], ['RHand', 0.4611999988555908]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.2], ['HeadPitch', 0.2], ['LShoulderPitch', 0.2], ['LShoulderRoll', 0.2], ['LElbowYaw', 0.2], ['LElbowRoll', 0.2], ['LWristYaw', 0.2], ['LHand', 0.2], ['RShoulderPitch', 0.2], ['RShoulderRoll', 0.2], ['RElbowYaw', 0.2], ['RElbowRoll', 0.2], ['RWristYaw', 0.2], ['RHand', 0.2]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 5 : u
print("Stage: " + str(5) + ": " + "u")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.2239220142364502], ['HeadPitch', 0.43254613876342773], ['LShoulderPitch', -0.44336795806884766], ['LShoulderRoll', 0.289884090423584], ['LElbowYaw', -0.8682861328125], ['LElbowRoll', -1.5431621074676514], ['LWristYaw', -1.8147640228271484], ['LHand', 0.765999972820282], ['RShoulderPitch', 0.925044059753418], ['RShoulderRoll', -0.27922987937927246], ['RElbowYaw', 0.46782803535461426], ['RElbowRoll', 1.1398038864135742], ['RWristYaw', 0.11961007118225098], ['RHand', 0.4611999988555908]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 0.25], ['HeadPitch', 0.25], ['LShoulderPitch', 0.25], ['LShoulderRoll', 0.25], ['LElbowYaw', 0.25], ['LElbowRoll', 0.25], ['LWristYaw', 0.25], ['LHand', 0.25], ['RShoulderPitch', 0.25], ['RShoulderRoll', 0.25], ['RElbowYaw', 0.25], ['RElbowRoll', 0.25], ['RWristYaw', 0.25], ['RHand', 0.25]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
               
# Movement: 6 : d
print("Stage: " + str(6) + ": " + "d")
joint_angles = [angle_modulator * angle for  _, angle in [['HeadYaw', 0.13801813125610352], ['HeadPitch', 0.1748340129852295], ['LShoulderPitch', 1.047680139541626], ['LShoulderRoll', 0.4033999443054199], ['LElbowYaw', -0.561486005783081], ['LElbowRoll', -1.3406740427017212], ['LWristYaw', -1.7549381256103516], ['LHand', 0.7663999795913696], ['RShoulderPitch', 0.925044059753418], ['RShoulderRoll', -0.28229808807373047], ['RElbowYaw', 0.46782803535461426], ['RElbowRoll', 1.1444058418273926], ['RWristYaw', 0.11961007118225098], ['RHand', 0.4611999988555908]]]
action_durations = [duration_modulator * duration for _, duration in [['HeadYaw', 1.0], ['HeadPitch', 1.0], ['LShoulderPitch', 1.0], ['LShoulderRoll', 1.0], ['LElbowYaw', 1.0], ['LElbowRoll', 1.0], ['LWristYaw', 1.0], ['LHand', 1.0], ['RShoulderPitch', 1.0], ['RShoulderRoll', 1.0], ['RElbowYaw', 1.0], ['RElbowRoll', 1.0], ['RWristYaw', 1.0], ['RHand', 1.0]]]
clas.motion.angleInterpolation(joint_names_list, joint_angles, action_durations, True)
            