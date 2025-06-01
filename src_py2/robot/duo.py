import paramiko # type: ignore (suppressess superfluous warning)
import time

#The Duo class has been created to take method attributes that instruct both robots to do the same thing, whether simultaneously or in sequence.
#The Duo class is not a necessary class.  Since go.py is called first in loader.py, the clas and meta Robot class objects are also available to Robot class attribute methods
#and can replace self. in proxy calls.
#It seems clearer to assign duo methods to a duo class object, though.  This may be debatable.
class Duo:
    
    offset_time = 1.5

    def __init__(self, clas, meta):
        self.clas = clas
        self.meta = meta

    def crouch(self, post=None):        
        speed = 0.75
        if post == 1:
            self.meta.posture.post.goToPosture('Crouch', speed)
            self.clas.posture.post.goToPosture('Crouch', speed)
        if post == 2:
            self.meta.posture.post.goToPosture('Crouch', speed)
            time.sleep(self.offset_time)
            self.clas.posture.post.goToPosture('Crouch', speed)
        else:
            self.meta.posture.post.goToPosture('Crouch', speed)
            self.clas.posture.goToPosture('Crouch', speed)

    def lie_back(self, post=None):
        speed = 0.75
        if post == 1:
            self.meta.posture.post.goToPosture('LyingBack', speed)
            self.clas.posture.post.goToPosture('LyingBack', speed)
        if post == 2:
             self.meta.posture.post.goToPosture('LyingBack', speed)
             time.sleep(self.offset_time)
             self.clas.posture.post.goToPosture('LyingBack', speed)
        else:
            self.meta.posture.post.goToPosture('LyingBack', speed)
            self.clas.posture.goToPosture('LyingBack', speed)

    def lie_belly(self, post=None):
        speed = 0.75
        if post == 1:
            self.meta.posture.post.goToPosture('LyingBelly', speed)
            self.clas.posture.post.goToPosture('LyingBelly', speed)
        if post == 2:
            self.meta.posture.post.goToPosture('LyingBelly', speed)
            time.sleep(self.offset_time)
            self.clas.posture.post.goToPosture('LyingBelly', speed)
        else:
            self.meta.posture.post.goToPosture('LyingBelly', speed)
            self.clas.posture.goToPosture('LyingBelly', speed)

    def repose(self, leds=True):

        if leds == False:
            self.clas.leds.post.fadeRGB("AllLeds", 0x000000, 0.1)
            self.meta.leds.post.fadeRGB("AllLeds", 0x000000, 0.1)

        if not self.meta.posture_check('sit') and not self.clas.posture_check('sit'):
            return
        else:
            joint_names_list = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
            joint_angles = [angles_compressed for _, angles_compressed in [['HeadYaw', [-0.013848066329956055]], ['HeadPitch', [0.5752079486846924]], ['LShoulderPitch', [0.8896780014038086]], ['LShoulderRoll', [0.16716408729553223]], ['LElbowYaw', [-0.48018407821655273]], ['LElbowRoll', [-0.9970581531524658]], ['LWristYaw', [-0.8299360275268555]], ['LHand', [0.6647999882698059]], ['RShoulderPitch', [0.8575479984283447]], ['RShoulderRoll', [-0.127363920211792]], ['RElbowYaw', [0.4371480941772461]], ['RElbowRoll', [0.9112381935119629]], ['RWristYaw', [0.891211986541748]], ['RHand', [0.5971999764442444]]]]
            time_points = [time_points_compressed for _, time_points_compressed in [['HeadYaw', [1.25]], ['HeadPitch', [1.25]], ['LShoulderPitch', [1.25]], ['LShoulderRoll', [1.25]], ['LElbowYaw', [1.25]], ['LElbowRoll', [1.25]], ['LWristYaw', [1.25]], ['LHand', [1.25]], ['RShoulderPitch', [1.25]], ['RShoulderRoll', [1.25]], ['RElbowYaw', [1.25]], ['RElbowRoll', [1.25]], ['RWristYaw', [1.25]], ['RHand', [1.25]]]]
            self.clas.motion.post.angleInterpolation(joint_names_list, joint_angles, time_points, True)
            self.meta.motion.post.angleInterpolation(joint_names_list, joint_angles, time_points, True)
  
    def stand(self, post=None):
        speed = 0.75
        if post == 1:
            self.meta.posture.post.goToPosture('Stand', speed)
            self.clas.posture.post.goToPosture('Stand', speed)
        if post == 2:
            self.meta.posture.post.goToPosture('Stand', speed)
            time.sleep(self.offset_time)
            self.clas.posture.post.goToPosture('Stand', speed)            
        else:
            self.meta.posture.post.goToPosture('Stand', speed)
            self.clas.posture.goToPosture('Stand', speed)
    
    def sit(self, post=None):
        speed = 0.75
        if post == 1:
            self.meta.posture.post.goToPosture('Sit', speed)
            self.clas.posture.post.goToPosture('Sit', speed)
        if post == 2:
            self.meta.posture.post.goToPosture('Sit', speed)
            time.sleep(self.offset_time)
            self.clas.posture.post.goToPosture('Sit', speed)
        else:
            self.meta.posture.post.goToPosture('Sit', speed)
            self.clas.posture.goToPosture('Sit', speed)      
    
    def shutdown(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.clas.ip, username=self.clas.usrnme, password=self.clas.pword)
        ssh.exec_command('sudo shutdown -h now')
        ssh.connect(self.meta.ip, username=self.meta.usrnme, password=self.meta.pword)
        ssh.exec_command('sudo shutdown -h now')
        ssh.close()    