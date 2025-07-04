from naoqi import ALProxy, ALProxy, ALBroker
import paramiko
import random
from touch_manager import TouchModule
from motion_manager import MotionManager
from audio_manager import AudioManager, sound_library

class NAORobot:
    def __init__(self, name, ip, port, usrnme, pword, reversed):
        self.ip = ip
        self.port = port
        self.name = name
        self.pword = pword
        self.usrnme = usrnme
        self.initialize_proxies()

        if name == "192.168.0.183": #classact
            self.dialog_off()
        elif name == "192.168.0.78" or name == "192.168.0.79": #metalhead
            self.aware_off()

        #clas.tts.say("{}".format(clas.name))
        self.audio_device.setOutputVolume(65)
        self.audio_player.setMasterVolume(0.5)
        # clas.tts.setParameter('pitchShift', 1)  
        self.tts.setParameter('speed', 88)

        self.mm = MotionManager(self, reversed)
        self.am = AudioManager(self)
        self.broker = ALBroker("broker-{}".format(name), "0.0.0.0", 0, self.ip, self.port)
        self.tm = TouchModule(self, "touch_{}".format(name))

    def initialize_proxies(self): 
        self.animation = ALProxy("ALAnimationPlayer", self.ip, self.port)
        self.animated_speech = ALProxy('ALAnimatedSpeech', self.ip, self.port)
        self.audio_device = ALProxy("ALAudioDevice", self.ip, self.port)
        self.audio_player = ALProxy('ALAudioPlayer', self.ip, self.port)
        self.audio_recorder = ALProxy('ALAudioRecorder', self.ip, self.port)
        self.basic_awareness = ALProxy("ALBasicAwareness", self.ip, self.port)
        self.battery = ALProxy("ALBattery", self.ip, self.port)
        self.dialog = ALProxy("ALDialog", self.ip, self.port)
        self.leds = ALProxy('ALLeds', self.ip, self.port)
        self.life = ALProxy('ALAutonomousLife', self.ip, self.port)
        self.memory = ALProxy("ALMemory", self.ip, self.port)
        self.motion = ALProxy('ALMotion', self.ip, self.port)
        self.posture = ALProxy('ALRobotPosture', self.ip, self.port)
        self.speaking_movement = ALProxy('ALSpeakingMovement', self.ip, self.port)
        self.tts = ALProxy('ALTextToSpeech', self.ip, self.port)
        # ALTouch proxy prevented the robots from being recognized by go
        # self.touch = ALProxy("ALTouch", self.ip, self.port)

    def __getstate__(self):
        # print("Calling __getstate__")
        # Exclude non-picklable attributes
        state = self.__dict__.copy()
        non_picklable_attributes = [
            'animation', 'animated_speech', 'audio_device', 'audio_player', 'audio_recorder',
            'basic_awareness', 'battery', 'dialog', 'leds', 'life',
            'memory', 'motion', 'posture', 'speaking_movement', 'tts'
        ]
        for attr in non_picklable_attributes:
            if attr in state:
                # print("Excluding non-pickleable attributes: {}".format(attr))
                del state[attr]
        return state

    def __setstate__(self, state):
        # print("Calling __setstate__")
        # Restore state and reinitialize proxies
        self.__dict__.update(state)
        # print("Reinitializing proxies")
        self.initialize_proxies()

    def aware_off(self):
        self.basic_awareness.setEnabled(False)
        
    def restore(self):
        self.life.setState('disabled')
        self.leds.post.fadeRGB("AllLeds", 0x000000, 0.1)
        self.posture.post.goToPosture('Sit', .6)        
        self.leds.post.fadeRGB("ChestLeds", 0xFFFFFF, 0.1)
        self.leds.post.fadeRGB("FaceLeds", 0xFFFFFF, 0.1)
        self.audio_device.setOutputVolume(65)

    def dialog_off(self):
        loaded_topics = self.dialog.getLoadedTopics("English")
        for topic in loaded_topics:
            self.dialog.unloadTopic(topic)
        self.dialog.stopDialog()

    def dialog_on(self):
        topic_path = "/home/nao/.local/share/PackageManager/apps/ht_cms_1_5/dialogs/ht_cms_1_5-custom_enu.top"
        topic_name = self.dialog.loadTopic(topic_path)
        self.dialog.activateTopic(topic_name)
        
    def shutdown(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ip, username=self.usrnme, password=self.pword)
        ssh.exec_command('sudo shutdown -h now')
        ssh.close()

    def download_file_from_nao(self, remote_file_path, local_file_path, username='nao', password='nao'):
        """
        Downloads a file from NAO's filesystem to your local machine using SFTP.
        """
        # Create an SSH client
        ssh = paramiko.SSHClient()

        # Auto-accept unknown host keys (for first-time connections)
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the NAO robot
        print("Connecting to {} with {}@{}...".format(self.ip, username, password))
        ssh.connect(hostname=self.ip, username=username, password=password)

        try:
            # Open SFTP session
            sftp = ssh.open_sftp()

            # Download the file from NAO (remote) to local
            print("Downloading {} to {}...".format(remote_file_path, local_file_path))
            sftp.get(remote_file_path, local_file_path)
            print("Download complete.")
        finally:
            # Cleanup
            sftp.close()
            ssh.close()

    def speak_and_move(self, message, motion_key):
        self.tts.post.say(message)
        self.mm.use_motion_library(motion_key)

    def eye_scan(self):
        duration = random.uniform(2,5)
        self.audio_player.post.playFile(sound_library["scanning"])
        self.leds.rotateEyes(0x33ECFF, 0.5, duration)
        self.audio_player.stopAll()
        self.leds.post.fadeRGB("AllLeds", 0xFFFFFF, 0.1)
