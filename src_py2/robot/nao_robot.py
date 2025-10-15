# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from naoqi import ALProxy, ALProxy, ALBroker
import paramiko
import random
import re

class NAORobot(object):
    def __init__(self, name, ip=None, port=9559, connect_on_init=True,
                 usrnme=None, pword=None, reversed=False):
        self.name = name
        self.port = port     
        self.usrnme = usrnme
        self.pword = pword
        self.reversed = reversed

        # Build an IP pool. If a preferred ip is provided, try it first.
        pool = self._ips_for(name)
        if ip:
            pool = [ip] + [x for x in pool if x != ip]
        self._ip_pool = pool

        # Connection state
        self.ip = None
        self.ip_used = None
        self._proxies_initialized = False

        # Proxies you will initialize on connect
        self.animation = None
        self.animated_speech = None
        self.audio_device = None
        self.audio_player = None
        self.audio_recorder = None
        self.basic_awareness = None
        self.battery = None
        self.broker = None
        self.dialog = None
        self.leds = None
        self.life = None
        self.memory = None
        self.motion = None
        self.posture = None
        self.speaking_movement = None
        self.tts = None

        # Managers/modules that depend on proxies
        self.mm = None
        self.am = None
        self.tm = None

        if connect_on_init:
            self.connect()

    # -------------------- IP handling --------------------

    def _ips_for(self, name):
        """Return list of known IPs for a robot name; allow raw IP as name."""
        if name == "meta":
            return ["192.168.0.78", "192.168.0.79"]
        elif name == "clas":
            return ["192.168.0.183"]
        # If the "name" looks like an IP, treat it as the only candidate.
        if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", name):
            return [name]
        return []

    # -------------------- Connect / Reconnect --------------------

    def connect(self):
        """
        Try each known IP until connecting proxies succeeds.
        Sets self.ip / self.ip_used on success.
        """
        if not self._ip_pool:
            raise ValueError("Unknown robot name '{}' (no IPs configured).".format(self.name))

        last_err = None
        for ip in self._ip_pool:
            try:
                self._try_connect(ip)               # <— no re-instantiation here
                self.ip = ip
                self.ip_used = ip
                self._post_connect_init()
                return True
            except Exception as e:
                last_err = e
                print("WARN: Failed to connect to {} @ {}: {}".format(self.name, ip, e))

        # If we got here, all IPs failed
        self.ip = None
        self.ip_used = None
        raise RuntimeError(
            "Could not connect to {} using any known IPs: {}. Last error: {}".format(
                self.name, ", ".join(self._ip_pool), last_err
            )
        )

    def reconnect(self, prefer_ip=None):
        """
        Force a reconnect. Optionally try a specific IP first.
        """
        if prefer_ip is not None:
            self._ip_pool = [prefer_ip] + [x for x in self._ip_pool if x != prefer_ip]
        # Tear down lightweight state if you need to; then connect again
        self._proxies_initialized = False
        return self.connect()

    @property
    def is_connected(self):
        return bool(self._proxies_initialized and self.ip is not None)

    # -------------------- Low-level wiring --------------------

    def _try_connect(self, ip):
        """
        Attempt to create the core NAOqi proxies against a specific IP.
        Raise if anything fails so the caller can try the next IP.
        """
        # Core proxies
        self.animation = ALProxy("ALAnimationPlayer", ip, self.port)
        self.animated_speech = ALProxy('ALAnimatedSpeech', ip, self.port)
        self.audio_device = ALProxy("ALAudioDevice", ip, self.port)
        self.audio_player = ALProxy('ALAudioPlayer', ip, self.port)
        self.audio_recorder = ALProxy('ALAudioRecorder', ip, self.port)
        self.basic_awareness = ALProxy("ALBasicAwareness", ip, self.port)
        self.battery = ALProxy("ALBattery", ip, self.port)
        self.dialog = ALProxy("ALDialog", ip, self.port)
        self.leds = ALProxy('ALLeds', ip, self.port)
        self.life = ALProxy('ALAutonomousLife', ip, self.port)
        self.memory = ALProxy("ALMemory", ip, self.port)
        self.motion = ALProxy('ALMotion', ip, self.port)
        self.posture = ALProxy('ALRobotPosture', ip, self.port)
        self.speaking_movement = ALProxy('ALSpeakingMovement', ip, self.port)
        self.tts = ALProxy('ALTextToSpeech', ip, self.port)

        # If we got here, proxies are alive for this IP
        self._proxies_initialized = True

    def _post_connect_init(self):
        """
        One-time post-connect configuration that depends on proxies being valid.
        Safe to call multiple times; should be idempotent.
        """
        if not self._proxies_initialized:
            return

        # Example audio defaults
        try:
            self.audio_device.setOutputVolume(65)
        except Exception:
            pass
        try:
            self.audio_player.setMasterVolume(0.5)
        except Exception:
            pass
        try:
            self.tts.setParameter('speed', 88)
        except Exception:
            pass

        # Broker and modules that require an active session
        try:
            if not self.broker:
                self.broker = ALBroker("broker-{}".format(self.name), "0.0.0.0", 0, self.ip, self.port)
        except Exception as e:
            print("WARN: Failed to create ALBroker: {}".format(e))

        # Your managers that depend on proxies
        try:
            from src_py2.robot.animation_manager import AnimationManager
            from src_py2.robot.audio_manager import AudioManager, sound_library
            from src_py2.robot.conversation_manager import ConversationManager           
            from src_py2.robot.motion_manager import MotionManager            
            from src_py2.robot.touch_manager import TouchModule      

            self.anm = AnimationManager(self)
            self.am = AudioManager(self)            
            self.cm = ConversationManager(self)
            self.mm = MotionManager(self)          
            self.tm = TouchModule(self, "touch_{}".format(self.name))
        except Exception as e:
            print("WARN: Failed to init managers/modules: {}".format(e))

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
 

    # NOT BASIC, PROBABLY DON'T BELONG HERE      

    def speak_and_move(self, message, motion_key):
        self.tts.post.say(message)
        self.mm.use_motion_library(motion_key)

    def eye_scan(self):
        duration = random.uniform(2,5)
        self.audio_player.post.playFile(sound_library["scanning"])
        self.leds.rotateEyes(0x33ECFF, 0.5, duration)
        self.audio_player.stopAll()
        self.leds.post.fadeRGB("AllLeds", 0xFFFFFF, 0.1)
