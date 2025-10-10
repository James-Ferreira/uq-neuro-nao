# -*- coding: utf-8 -*-
import random
import time
from src_py2.game.robot_player import RobotPlayer
from audio_manager import sound_library
from src_py2.api.async_wrapper import make_async_func
# from audio_manager_duo import AudioManagerDuo

class Orchestrate(object):
    def __init__(self, robot_1, robot_2):
        self.robot_1 = robot_1
        self.robot_2 = robot_2

    def simple_welcome(self):
        player_type = "partner" if self.robot_1.team_condition == 'P' else "opponent"

        #### FOR DEBUGGING REVERSE ###

        #self.robot_1.nao.mm.use_motion_library("turn_head_left", post=True)
        #self.robot_2.nao.mm.use_motion_library("turn_head_right")
        # fix intro/game based on this ^ robot_1 uses left, robot_2 uses right!
        #self.robot_2.nao.mm.use_motion_library("head_touch_up_2")

        ### ### ###

        ### ROBOT-TO-ROBOT CONVO ###

        #amd = AudioManagerDuo(self.robot_1, self.robot_2)
        #amd.record_audio(playback=True)

        ### ### ###

        self.robot_1.nao.tm.wait_for_touch_activate()
        self.robot_1.nao.mm.use_motion_library("head_touch_up")
        self.robot_1.nao.mm.use_motion_library("head_touch_down_snoozy")

        self.robot_2.nao.leds.post.fadeRGB("FaceLeds", 0xFFFFFF, 0.1)
        self.robot_2.nao.leds.post.fadeRGB("ChestLeds", 0xFFFFFF, 0.1)
        self.robot_2.nao.tts.post.say("Oh: {}. Wake up.".format(self.robot_1.name))
        self.robot_2.nao.mm.use_motion_library("head_touch_up_2")
        self.robot_2.nao.mm.sit_gently(post=True)

        self.robot_1.nao.leds.post.fadeRGB("FaceLeds", 0xFFFFFF, 0.1)
        self.robot_1.nao.leds.post.fadeRGB("ChestLeds", 0xFFFFFF, 0.1)
        self.robot_1.nao.tts.post.say("Oh. Oh my. Our {}s are here.".format(player_type))
        self.robot_1.nao.mm.use_motion_library("team_is_here")

        self.robot_1.nao.tts.post.say("Hello, and welcome to the experiment.")
        self.robot_1.nao.mm.use_motion_library("welcome_1_greetings")

        self.robot_2.nao.tts.post.say("Greetings.")
        self.robot_2.nao.mm.use_motion_library("welcome_2_greetings")

        self.robot_1.nao.tts.post.say("My name is: {}.".format(self.robot_1.name))
        self.robot_1.nao.mm.use_motion_library("welcome_1_my_name_is")

        self.robot_1.nao.tts.post.say("What is your name, Dear human?")
        self.robot_1.nao.mm.use_motion_library("welcome_1_ask_name")
        participant_1_name = self.robot_1.nao.am.listen_until_confirmed(speech=True, start_sound=True, end_sound=True, laconic=False)
        self.robot_1.nao.tts.post.say("If I am not mistaken, you, {}, are my {} in the game today.".format(participant_1_name, player_type))
        self.robot_1.nao.mm.use_motion_library("you_are_in_the_game")

        self.robot_1.nao.tts.say("It would be an honor for me to shake your hand.")
        # todo: re-animate handshake invitation
        self.robot_1.nao.mm.use_motion_library("extend_right_hand", default_orientation=True)
        confirmed = self.robot_1.nao.tm.wait_for_touch_confirm()
        if confirmed:
            self.robot_1.nao.mm.right_handshake_a()
        else:
            self.robot_1.tts.say("Well, that's disappointing.")
        
        self.robot_1.nao.mm.sit_gently()
        self.robot_1.nao.tts.say("I am looking forward to playing with you.")
       
        self.robot_2.nao.tts.post.say("And I am: {}. At your service.".format(self.robot_2.name))
        self.robot_2.nao.mm.use_motion_library("at_your_service")
        self.robot_2.nao.tts.post.say("May I enquire what your name is?")
        self.robot_2.nao.mm.use_motion_library("check_name") 
        participant_2_name = self.robot_2.nao.am.listen_until_confirmed(speech=True, start_sound=True, end_sound=True, laconic=False)
        
        # todo: vary dialogue for engagement, then find/create animation
        self.robot_2.nao.tts.say("If I am not mistaken, you, {}, are my {} in the game today.".format(participant_2_name, player_type))
        # todo: add animation to the above dialogue (and post the dialogue)

        self.robot_2.nao.tts.say("Meeting you is a grandiose honor for me, I assure you. May I shake your hand?")
        self.robot_2.nao.mm.use_motion_library("extend_right_hand", default_orientation=True)
        confirmed2 = self.robot_2.nao.tm.wait_for_touch_confirm()
        if confirmed2:
            self.robot_2.nao.mm.right_handshake_b()
        else:
            self.robot_2.tts.say("Very well. I'll try not to take it personally.")

        return participant_1_name, participant_2_name
        
    def simple_hobby(self, participant_1_name, participant_2_name):
        self.robot_1.nao.tts.post.say("So, {}, let's get to know each other a little bit.".format(participant_1_name))
        self.robot_1.nao.mm.use_motion_library("lets_get_to_know_each_other")
        
        # POINTING
        self.robot_1.nao.tts.post.say("{} and I are from Frantsi pani fornia. Where are you from?".format(self.robot_2.name))
        self.robot_1.nao.mm.use_motion_library("where_are_you_from")
        
        participant_1_place = self.robot_1.nao.am.listen_until_confirmed(speech=True, end_sound=True, laconic=False)
        
        if any(sub in participant_1_place.lower() for sub in ["brisbane", "australia"]):
            self.robot_1.nao.tts.post.say("Nice. I hope I can escape this dundge atory some day and see something of {}.".format(participant_1_place))
            self.robot_1.nao.mm.use_motion_library("slives_in_brisbane")
        else:
            self.robot_1.nao.tts.post.say("{}, ah, that must be a nice place to live.".format(participant_1_place))
            self.robot_1.nao.mm.use_motion_library("nice_place_to_live")
        
        self.robot_1.nao.tts.post.say("And what is one of your favorite hobbies, {}?".format(participant_1_name))
        self.robot_1.nao.mm.use_motion_library("what_are_your_hobbies")
        
        participant_1_hobby = self.robot_1.nao.am.listen_until_confirmed()

        # NAO seemed to RECORD ITSELF saying somehting about Brisbane when it reported the hobby here.
        self.robot_1.nao.tts.post.say("Cool: {} is very cool.".format(participant_1_hobby))
        self.robot_1.nao.mm.use_motion_library("cool_hobby")

        self.robot_2.nao.tts.post.say("And what about you, {}. What is a hobby of yours?".format(participant_2_name))
        self.robot_2.nao.mm.use_motion_library("what_is_ur_hobby")
        
        participant_2_hobby = self.robot_2.nao.am.listen_until_confirmed(speech=True, end_sound=True, laconic=False) 

        ##### prepare hobby opinions for later (reference for making api calls async)
        hobby_better_1 = participant_1_hobby if self.robot_1.team_condition == "P" else "playing puppets"
        hobby_worse_1 = participant_2_hobby

        hobby_better_2 = participant_2_hobby if self.robot_1.team_condition == "P" else "catching flies"
        hobby_worse_2 = participant_1_hobby

        # create an async version of a method, but dont run it yet
        async_opinion_fn_1 = make_async_func(self.robot_1.generate_opinion)
        async_opinion_fn_2 = make_async_func(self.robot_2.generate_opinion)
        # use the async method to run it in the backgroud via threads
        async_robot_1_opinion = async_opinion_fn_1(hobby_better_1, hobby_worse_1, False)
        async_robot_2_opinion = async_opinion_fn_2(hobby_better_2, hobby_worse_2, True)
        # - - - 

        self.robot_2.nao.tts.post.say("{} sounds like a lot of fun.".format(participant_2_hobby))
        self.robot_2.nao.mm.use_motion_library("what_is_ur_hobby_2")

        self.robot_2.nao.tts.post.say("My hobby is catching flies, like this, see?")
        self.robot_2.nao.mm.use_motion_library("my_hobby_is_catching_fly")
        self.robot_1.nao.mm.use_motion_library("turn_head_left", post=True)
        self.robot_2.nao.mm.catch_fly()
        
        self.robot_1.nao.tts.post.say("{} is really athletic. My hobby is playing puppets. This is my latest routine.".format(self.robot_2.name))
        self.robot_2.nao.mm.use_motion_library("turn_head_right", post=True) 
        self.robot_1.nao.mm.use_motion_library("my_hobby_is_playing_puppets")
        self.robot_1.nao.mm.puppet_show()
        
        self.robot_2.nao.tts.post.say("{} is very talented.".format(self.robot_1.name))
        self.robot_2.nao.mm.use_motion_library("very_talented")

        self.robot_2.nao.tts.post.say("But, oh, {}, I forgot to ask where you are from.".format(participant_2_name))
        self.robot_2.nao.mm.use_motion_library("where_are_you_from")
        
        participant_2_place = self.robot_2.nao.am.listen_until_confirmed() 
        
        if any(sub in participant_2_place.lower() for sub in ["brisbane", "australia"]):
            self.robot_2.nao.tts.post.say("That's where I live, or so I'm told. It must be nice to live here, if you can get outside to explore. once in a while.")
            self.robot_2.nao.mm.use_motion_library("brisbane_is_where_I_live")
        else:
            self.robot_2.nao.tts.post.say("Wow. I would sure like to go to {} one day.".format(participant_2_place))
            self.robot_2.nao.mm.use_motion_library("i_would_like_to_visit")

        self.robot_2.nao.tts.post.say("{}, {} is from {} and enjoys {}.".format(self.robot_1.name, participant_2_name, participant_2_place, participant_2_hobby))
        self.robot_2.nao.mm.use_motion_library("enjoys_hobby")

        self.robot_1.nao.tts.post.say("{} is fun, but, if you ask me {} is better.".format(hobby_worse_1, hobby_better_1))
        self.robot_1.nao.mm.use_motion_library("hobby_is_better")
        
        # require the async method to have returned at this point / now it becomes blocking
        robot_1_opinion = async_robot_1_opinion.await_result()
        self.robot_1.nao.mm.bob_n_speak(robot_1_opinion)

        if self.robot_1.team_condition == "P":
            self.robot_2.nao.tts.post.say("I'm afraid I must respectfully disagree.")
            self.robot_2.nao.mm.use_motion_library("respectfully_disagree")
        else:
            self.robot_2.nao.tts.post.say("What was our other opponent's hobby again?")
            self.robot_2.nao.mm.use_motion_library("what_was_opponents_hobby")
            self.robot_1.nao.tts.post.say("{}".format(participant_1_hobby))
            self.robot_1.nao.mm.use_motion_library("say_hobby")
            self.robot_2.nao.tts.post.say("Oh my.  I would have to argue that my hobby of {} is a good deal more interesting than {}".format(hobby_better_2, hobby_worse_2))
            self.robot_2.nao.mm.use_motion_library("catching_flies_more_interesting")

        robot_2_opinion = async_robot_2_opinion.await_result()
        self.robot_2.nao.mm.bob_n_speak(robot_2_opinion)

        self.robot_1.nao.tts.post.say("Well, ahem, to each its own.")
        self.robot_1.nao.mm.use_motion_library("to_each_its_own")

        self.robot_2.nao.tts.post.say("Anyway, that's enough chitchat.  Let's get to the game.")
        self.robot_2.nao.mm.use_motion_library("lets_get_to_the_game")
        
        if self.robot_1.team_condition == 'O':
            self.robot_1.nao.tts.say("Oh Experimenter.  Please put us in our game positions.")
        
        self.robot_2.nao.tts.say("When you are ready to start")
        self.robot_2.nao.tts.say("\\rspd=75\\ Stimulate my dome")
        self.robot_2.nao.tts.say("I mean touch my head")
        self.robot_2.nao.tm.wait_for_touch_activate()

    def simple_outro(self, participant_1_name, participant_2_name):
        self.robot_1.nao.tts.post.say("I don't know about you, {}, but I'm weary and bleary after all the hinting: and guessing.".format(self.robot_2.name))
        self.robot_1.nao.mm.use_motion_library("outro_1")

        self.robot_2.nao.tts.post.say("I know just what you mean, {}. I, myself am ready for a long, peaceful rest er roo, as the ozzies say.".format(self.robot_1.name))
        self.robot_2.nao.mm.use_motion_library("outro_2")
        # makes robot_1 put its arms back into sit position, a bit clunky
        self.robot_1.nao.mm.use_motion_library("outro_3")

        if self.robot_1.team_condition == 'O':
            self.robot_1.nao.tts.say("Oh Experimenter. Can you give us a spin?")
            self.robot_1.nao.tm.wait_for_touch_activate()

        self.robot_1.nao.tts.post.say("Well, {}, it was a great pleasure playing with you today".format(participant_1_name))
        self.robot_1.nao.mm.use_motion_library("outro_4")

        # original second motion for.nao.2 (why ?)
        # self.robot_2.nao.mm.use_motion_library("outro_5")
        
        self.robot_2.nao.tts.post.say("And I had a wonderful time playing with you, {}.".format(participant_2_name))

        # original motion for.nao.1 (why ?)
        # self.robot_1.nao.mm.use_motion_library("outro_6")

        # this (original) animaiton is too short, switching to robot_1's longer hand-to-chest animation (outro_6, above)
        # self.robot_2.nao.mm.use_motion_library("outro_5")
        self.robot_2.nao.mm.use_motion_library("outro_6")

        # this animation made the.nao.turn it's head away from the participant, likely detracting from the sincerity of the dialogue.
        # self.robot_2.nao.mm.use_motion_library("outro_7")
        
        self.robot_1.nao.tts.post.say("So, {}, shall we?".format(self.robot_2.name))
        # this motion needs to be longer so robot_2 doesn't interrupt
        self.robot_1.nao.mm.use_motion_library("outro_8")
        time.sleep(1.5)

        self.robot_2.nao.tts.say("Lets")

        self.wave_bye()
        self.repose()

    def wave_bye(self):
        # Generate a random integer between 1 and 100
        random_number = random.randint(1, 100)
        if random_number % 2 == 0:
            robo_rand1 = self.robot_1.robot
            robo_rand2 = self.robot_2.robot
        else:
            robo_rand1 = self.robot_2.robot
            robo_rand2 = self.robot_1.robot
    
        current_posture1 = robo_rand1.posture.getPosture()
        current_posture2 = robo_rand2.posture.getPosture()
        
        #wave bye, sitting version (same as wave_bye3)
        if current_posture1 == 'Sit' and current_posture2 == 'Sit':   

            joint_names_list1 = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll', 'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
            time_points_list1 = [[1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 6.0], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 6.0], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 6.0], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 6.0], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 6.0], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 6.0], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 6.0], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 6.0], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 6.0], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 6.0], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 6.0], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 6.0], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 6.0], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 6.0], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 6.0], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 6.0], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 6.0], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 6.0], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 6.0], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 6.0], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 6.0], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 6.0], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 6.0], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 6.0], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 6.0], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 6.0]]
            joint_angles_list1 = [[-0.04452800750732422, -0.04452800750732422, -0.04452800750732422, -0.04452800750732422, -0.04452800750732422, -0.04452800750732422, -0.04452800750732422, -0.04452800750732422], [-0.07060599327087402, -0.07060599327087402, -0.07060599327087402, -0.07060599327087402, -0.07060599327087402, -0.07060599327087402, -0.07060599327087402, -0.07060599327087402], [0.9295620918273926, 0.9295620918273926, 0.9295620918273926, 0.9295620918273926, 0.9280281066894531, 0.9295620918273926, 0.9295620918273926, 0.9295620918273926], [0.2592041492462158, 0.2607381343841553, 0.2607381343841553, 0.2607381343841553, 0.2607381343841553, 0.2607381343841553, 0.2592041492462158, 0.2592041492462158], [-0.4326300621032715, -0.4326300621032715, -0.43416404724121094, -0.43416404724121094, -0.43416404724121094, -0.43416404724121094, -0.43416404724121094, -0.44336795806884766], [-1.1734681129455566, -1.1734681129455566, -1.1734681129455566, -1.1734681129455566, -1.1734681129455566, -1.1734681129455566, -1.1734681129455566, -1.1734681129455566], [-4.1961669921875e-05, -0.0015759468078613281, 0.0030260086059570312, -0.0015759468078613281, 0.0014920234680175781, -4.1961669921875e-05, -4.1961669921875e-05, -0.0031099319458007812], [0.2919999957084656, 0.2919999957084656, 0.2919999957084656, 0.2919999957084656, 0.2919999957084656, 0.2919999957084656, 0.2919999957084656, 0.2919999957084656], [-0.5997519493103027, -0.5997519493103027, -0.5997519493103027, -0.5997519493103027, -0.5997519493103027, -0.5997519493103027, -0.5997519493103027, -0.5997519493103027], [0.2684919834136963, 0.27002596855163574, 0.27002596855163574, 0.2684919834136963, 0.2684919834136963, 0.2684919834136963, 0.27002596855163574, 0.26695799827575684], [-1.5354920625686646, -1.5354920625686646, -1.5354920625686646, -1.5354920625686646, -1.537026047706604, -1.537026047706604, -1.537026047706604, -1.5385600328445435], [1.3882280588150024, 1.3882280588150024, 1.3882280588150024, 1.3882280588150024, 1.3882280588150024, 1.3882280588150024, 1.3882280588150024, 1.386694073677063], [0.8497941493988037, 0.8497941493988037, 0.8497941493988037, 0.8497941493988037, 0.8497941493988037, 0.8497941493988037, 0.8497941493988037, 0.8513281345367432], [-0.010695934295654297, -0.009161949157714844, -0.009161949157714844, -0.009161949157714844, -0.009161949157714844, -0.010695934295654297, -0.009161949157714844, -0.010695934295654297], [-0.5997519493103027, -0.5997519493103027, -0.5997519493103027, -0.5997519493103027, -0.5997519493103027, -0.5997519493103027, -0.5997519493103027, -0.5997519493103027], [-0.25460195541381836, -0.25460195541381836, -0.25460195541381836, -0.25460195541381836, -0.25460195541381836, -0.25460195541381836, -0.25460195541381836, -0.25460195541381836], [-1.526371955871582, -1.5279059410095215, -1.529439926147461, -1.5279059410095215, -1.5279059410095215, -1.5279059410095215, -1.529439926147461, -1.5325078964233398], [1.4067201614379883, 1.4082541465759277, 1.4067201614379883, 1.4067201614379883, 1.4082541465759277, 1.4082541465759277, 1.4082541465759277, 1.4036521911621094], [0.8498780727386475, 0.8498780727386475, 0.8498780727386475, 0.8498780727386475, 0.8498780727386475, 0.8498780727386475, 0.8498780727386475, 0.8514120578765869], [0.019984006881713867, 0.019984006881713867, 0.018450021743774414, 0.019984006881713867, 0.019984006881713867, 0.018450021743774414, 0.019984006881713867, 0.019984006881713867], [0.2945699691772461, 0.14117002487182617, 0.1733839511871338, 0.20713186264038086, 0.31911396980285645, 0.3329200744628906, 0.39427995681762695, 0.9511218070983887], [-0.1764519214630127, -0.14577198028564453, -0.16264605522155762, -0.14117002487182617, -0.2086658477783203, -0.21940398216247559, -0.21326804161071777, -0.2807638645172119], [2.1107420921325684, 1.1796040534973145, 1.8514961004257202, 1.251702070236206, 1.958876132965088, 1.2762460708618164, 2.1076741218566895, 0.48777008056640625], [1.512566089630127, 1.526371955871582, 1.4220600128173828, 1.486487865447998, 1.446603775024414, 1.4941577911376953, 1.4097881317138672, 1.1658821105957031], [-1.0631041526794434, -1.1781539916992188, -1.205766201019287, -0.9204421043395996, -1.015550136566162, -1.0508317947387695, -1.0569682121276855, 0.6196939945220947], [0.6643999814987183, 0.9, 1, 1, 1, 0.8, 0.6, 0.3]]
            
            joint_names_list2 = ['HeadYaw', 'HeadPitch', 'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll', 'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
            joint_angles_list2 = [[0.04444408416748047, 0.04444408416748047, 0.04444408416748047, 0.14108610153198242, 0.14108610153198242, 0.14108610153198242, 0.14108610153198242, 0.14108610153198242, 0.14108610153198242], [0.038308143615722656, 0.038308143615722656, 0.038308143615722656, 0.038308143615722656, 0.038308143615722656, 0.038308143615722656, 0.038308143615722656, 0.038308143615722656, 0.038308143615722656], [0.9449019432067871, 0.9464361667633057, 0.9449019432067871, 0.9449019432067871, 0.9449019432067871, 0.9449019432067871, 0.9449019432067871, 0.9449019432067871, 0.9433679580688477], [0.29141807556152344, 0.2929520606994629, 0.2929520606994629, 0.2929520606994629, 0.2929520606994629, 0.2929520606994629, 0.2929520606994629, 0.2929520606994629, 0.27454400062561035], [-0.4617760181427002, -0.46024203300476074, -0.4617760181427002, -0.4617760181427002, -0.4617760181427002, -0.4617760181427002, -0.4617760181427002, -0.4617760181427002, -0.4709799289703369], [-1.1734681129455566, -1.1734681129455566, -1.1734681129455566, -1.1734681129455566, -1.1734681129455566, -1.1734681129455566, -1.1734681129455566, -1.1734681129455566, -1.162730097770691], [-0.0031099319458007812, -0.0015759468078613281, -0.0031099319458007812, -0.0031099319458007812, -0.0031099319458007812, -0.0031099319458007812, -0.0031099319458007812, -0.0031099319458007812, 0.022968053817749023], [0.2919999957084656, 0.2919999957084656, 0.2919999957084656, 0.2919999957084656, 0.2919999957084656, 0.2919999957084656, 0.2919999957084656, 0.2919999957084656, 0.3320000171661377], [-0.5982179641723633, -0.5982179641723633, -0.5982179641723633, -0.5982179641723633, -0.5982179641723633, -0.5982179641723633, -0.5982179641723633, -0.5982179641723633, -0.5982179641723633], [0.2684919834136963, 0.2684919834136963, 0.2684919834136963, 0.2684919834136963, 0.2684919834136963, 0.2684919834136963, 0.2684919834136963, 0.2684919834136963, 0.2684919834136963], [-1.537026047706604, -1.537026047706604, -1.537026047706604, -1.537026047706604, -1.537026047706604, -1.537026047706604, -1.537026047706604, -1.537026047706604, -1.537026047706604], [1.386694073677063, 1.386694073677063, 1.386694073677063, 1.386694073677063, 1.3882280588150024, 1.386694073677063, 1.386694073677063, 1.386694073677063, 1.386694073677063], [0.8513281345367432, 0.8513281345367432, 0.8513281345367432, 0.8513281345367432, 0.8513281345367432, 0.8513281345367432, 0.8513281345367432, 0.8513281345367432, 0.8513281345367432], [-0.009161949157714844, -0.009161949157714844, -0.009161949157714844, -0.009161949157714844, -0.009161949157714844, -0.009161949157714844, -0.009161949157714844, -0.009161949157714844, -0.009161949157714844], [-0.5982179641723633, -0.5982179641723633, -0.5982179641723633, -0.5982179641723633, -0.5982179641723633, -0.5982179641723633, -0.5982179641723633, -0.5982179641723633, -0.5982179641723633], [-0.25460195541381836, -0.25460195541381836, -0.25460195541381836, -0.25460195541381836, -0.25460195541381836, -0.25460195541381836, -0.25460195541381836, -0.25460195541381836, -0.25460195541381836], [-1.5309739112854004, -1.5309739112854004, -1.5309739112854004, -1.5309739112854004, -1.5325078964233398, -1.5325078964233398, -1.5309739112854004, -1.5309739112854004, -1.5340418815612793], [1.4067201614379883, 1.4051861763000488, 1.4067201614379883, 1.4051861763000488, 1.4067201614379883, 1.4067201614379883, 1.4051861763000488, 1.4067201614379883, 1.4051861763000488], [0.8498780727386475, 0.8514120578765869, 0.8514120578765869, 0.8514120578765869, 0.8514120578765869, 0.8514120578765869, 0.8514120578765869, 0.8514120578765869, 0.8514120578765869], [0.02151799201965332, 0.02151799201965332, 0.02151799201965332, 0.02151799201965332, 0.02151799201965332, 0.02151799201965332, 0.02151799201965332, 0.02151799201965332, 0.02151799201965332], [0.18719005584716797, 0.15190792083740234, 0.15190792083740234, 0.08748006820678711, 0.08901405334472656, 0.09821796417236328, 0.12122797966003418, 0.34825992584228516, 0.9281120300292969], [-0.1104898452758789, -0.023051977157592773, 0.0060939788818359375, -0.06907200813293457, -0.0123138427734375, 0.038308143615722656, 0.019900083541870117, -0.0015759468078613281, -0.2546858787536621], [1.2701101303100586, 1.221022129058838, 1.2179540395736694, 1.2992560863494873, 1.515550136566162, 1.405102014541626, 1.460326075553894, 1.7379801273345947, 0.47396397590637207], [1.5325078964233398, 1.5048961639404297, 1.5156340599060059, 1.4987602233886719, 1.4926238059997559, 1.5033621788024902, 1.489555835723877, 1.5064301490783691, 1.115260124206543], [-1.2149701118469238, -1.0999197959899902, -1.0999197959899902, -1.1259980201721191, -1.1536102294921875, -1.1536102294921875, -1.172018051147461, -1.1766200065612793, 0.15642595291137695], [0.659600019454956, 1, 0.4, 0.9, 0.3, 0.9, 0.4, 1, 0.3]]
            time_points_list2 = [[1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.5], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.5], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.5], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.5], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.5], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.5], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.5], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.5], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.5], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.5], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.5], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.5], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.5], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.5], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.5], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.5], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.5], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.5], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.5], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.5], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.5], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.5], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.5], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.5], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.5], [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.5]]
            
            robo_rand1.tts.post.say("\\RSPD=50\\Bye.Bye. Bye. Bye.Bye.")
            robo_rand1.motion.post.angleInterpolation(joint_names_list1, joint_angles_list1, time_points_list1, True)
            
            robo_rand2.tts.post.say("\\RSPD=35\\Bye. Bye.Bye. Bye.")
            robo_rand2.motion.angleInterpolation(joint_names_list2, joint_angles_list2, time_points_list2, True)

        else:
            print('Current posture 1, {0}, or current posture 2, {1}, is incompatible with requested animation.'.format(current_posture1, current_posture2))
            return
        
    def repose(self):
        self.robot_1.nao.mm.repose(False)
        self.robot_2.nao.mm.repose(False)

    def sit(self):
        self.robot_1.nao.mm.sit()
        self.robot_2.nao.mm.sit()
        # self.robot_1.nao.mm.use_motion_library("sit_gently", post=True)
        # self.robot_2.nao.mm.use_motion_library("sit_gently", post=True)

    def before_hint(self, active_team, inactive_team, already_hinted, target_with_quadrants):
        active_hinter = active_team.get_hinter()
        active_guesser = active_team.get_guesser()
        inactive_hinter = inactive_team.get_hinter()
        inactive_guesser = inactive_team.get_guesser()

        isActiveGuesserRobot = isinstance(active_guesser, RobotPlayer)
        isActiveHinterRobot = isinstance(active_hinter, RobotPlayer)
        isInactiveHinterRobot = isinstance(inactive_hinter, RobotPlayer)
        isInactiveGuesserRobot = isinstance(inactive_guesser, RobotPlayer)

        if isInactiveHinterRobot:
            if inactive_hinter == self.robot_1:
                if self.robot_1.team_condition == 'O':
                    inactive_hinter.nao.mm.use_motion_library("turn_head_right")
                elif self.robot_1.team_condition == 'P':
                    inactive_hinter.nao.mm.use_motion_library("turn_head_left")
                else:
                    print("something wrong")
            elif inactive_hinter == self.robot_2:
                if self.robot_1.team_condition == 'O':
                    inactive_hinter.nao.mm.use_motion_library("turn_head_left")
                elif self.robot_1.team_condition == 'P':
                    inactive_hinter.nao.mm.use_motion_library("turn_head_right")
                else:
                    print("something wrong")
            else:
                print("something very wrong")

        if isInactiveGuesserRobot:
            if inactive_guesser == self.robot_1:
                if self.robot_1.team_condition == 'O':
                    inactive_guesser.nao.mm.use_motion_library("turn_head_right")
                elif self.robot_1.team_condition == 'P':
                    inactive_guesser.nao.mm.use_motion_library("turn_head_left")
                else:
                    print("something wrong")
            elif inactive_guesser == self.robot_2:
                if self.robot_1.team_condition == 'O':
                    inactive_guesser.nao.mm.use_motion_library("turn_head_left")
                elif self.robot_1.team_condition == 'P':
                    inactive_guesser.nao.mm.use_motion_library("turn_head_right")
                else:
                    print("something wrong")
            else:
                print("something very wrong")

        if isActiveHinterRobot:
            active_hinter.nao.mm.sit_gently()
        if isActiveGuesserRobot:
            active_guesser.nao.mm.sit_gently()

        if len(already_hinted) == 0:
            team_condition = next(
                p.team_condition for p, is_robot in [
                    (active_hinter, isActiveHinterRobot),
                    (inactive_hinter, isInactiveHinterRobot),
                    (active_guesser, isActiveGuesserRobot),
                    (inactive_guesser, isInactiveGuesserRobot),
                ] if is_robot)

            is_partner = team_condition == "P"
            is_opponent = team_condition == "O"

            if isActiveHinterRobot:
                introducer = active_hinter
                phrase_intro = "The hinters will be: {}: that's me, and: {}. I will hint first.".format(active_hinter.name, inactive_hinter.name)
            elif isInactiveHinterRobot:
                introducer = inactive_hinter
                phrase_intro = "The hinters will be: {} and: {}: that's me. {} will hint first.".format(active_hinter.name, inactive_hinter.name, active_hinter.name)
            elif isActiveGuesserRobot:
                introducer = active_guesser
                phrase_intro = "The hinters will be: {} and: {}. {} will hint first.".format(active_hinter.name, inactive_hinter.name, active_hinter.name)

            introducer.nao.tts.say(phrase_intro)

            if is_partner and isActiveHinterRobot:
                active_hinter.nao.tts.say("Experimenter. Please show me the target word. Touch my head when you are ready for me to scan.")
                active_hinter.nao.tm.wait_for_touch_activate()
                active_hinter.nao.eye_scan()
                active_hinter.nao.tts.say("I see the target word in quadrant {}.".format(target_with_quadrants["position_1"]))
                active_hinter.nao.tts.say("Is that correct? Press my hand for yes, or my foot for no.")
                active_hinter.nao.tm.wait_for_touch_confirm()

                inactive_hinter.nao.mm.sit_gently(post=True)
                inactive_hinter.nao.tts.say("Please let me see the target word, too. Touch my head when you are ready for me to scan.")
                inactive_hinter.nao.tm.wait_for_touch_activate()
                inactive_hinter.nao.eye_scan()
                inactive_hinter.nao.tts.say("I see the target word in quadrant {}.".format(target_with_quadrants["position_2"]))
                inactive_hinter.nao.tts.say("Is that correct? Press my hand for yes, or my foot for no.")
                inactive_hinter.nao.tm.wait_for_touch_confirm()

            elif is_opponent:
                if isActiveHinterRobot:
                    robot_hinter = active_hinter
                    human_hinter = inactive_hinter
                    quadrant_key = "position_1"
                else:
                    robot_hinter = inactive_hinter
                    human_hinter = active_hinter
                    quadrant_key = "position_2"

                robot_hinter.nao.mm.sit_gently(post=True)
                robot_hinter.nao.tts.say("Experimenter. Please show me the target word. Touch my head when you are ready for me to scan.")
                robot_hinter.nao.tm.wait_for_touch_activate()
                robot_hinter.nao.eye_scan()
                robot_hinter.nao.tts.say("I see the target word in quadrant {}.".format(target_with_quadrants[quadrant_key]))
                robot_hinter.nao.tts.say("Is that correct? Press my hand for yes, or my foot for no.")
                robot_hinter.nao.tm.wait_for_touch_confirm()

                robot_hinter.nao.tts.say("Thank you. Now you can show the target word to: {}, too. Touch my head when you are ready to continue.".format(human_hinter.name))
                robot_hinter.nao.tm.wait_for_touch_activate()

    def before_guess(self, active_team, inactive_team):
        active_hinter = active_team.get_hinter()
        active_guesser = active_team.get_guesser()
        inactive_hinter = inactive_team.get_hinter()
        inactive_guesser = inactive_team.get_guesser()

        isActiveGuesserRobot = isinstance(active_guesser, RobotPlayer)
        isActiveHinterRobot = isinstance(active_hinter, RobotPlayer)
        isInactiveHinterRobot = isinstance(inactive_hinter, RobotPlayer)
        isInactiveGuesserRobot = isinstance(inactive_guesser, RobotPlayer)

        if isInactiveHinterRobot:
            inactive_hinter.nao.mm.use_motion_library("turn_head")
        if isInactiveGuesserRobot:
            inactive_guesser.nao.mm.use_motion_library("turn_head")

        if isActiveHinterRobot:
            active_hinter.nao.mm.sit_gently()
        if isActiveGuesserRobot:
            active_guesser.nao.mm.sit_gently()

    def before_evaluate(self, active_team, inactive_team, isActuallyCorrect, guess):
        active_hinter = active_team.get_hinter()
        active_guesser = active_team.get_guesser()
        inactive_hinter = inactive_team.get_hinter()
        inactive_guesser = inactive_team.get_guesser()

        isActiveGuesserRobot = isinstance(active_guesser, RobotPlayer)
        isActiveHinterRobot = isinstance(active_hinter, RobotPlayer)
        isInactiveHinterRobot = isinstance(inactive_hinter, RobotPlayer)
        isInactiveGuesserRobot = isinstance(inactive_guesser, RobotPlayer)

        isActuallyCorrectString = "correct" if isActuallyCorrect else "incorrect"


        # todo: account for partner vs opponent
        if isActiveGuesserRobot:
            # this cannot be posted because activating touch cuts this line of dialogue.
            active_guesser.nao.tts.post.say("Is {} the right word? Press my hand for yes, or my foot for no.".format(guess))
            isClaimedToBeCorrect = active_guesser.nao.tm.wait_for_touch_confirm()
            active_guesser.nao.tts.stopAll()

            if isClaimedToBeCorrect and isActuallyCorrect:
                active_guesser.nao.audio_player.playFile(sound_library["correct_sound_a"])
                active_guesser.nao.tts.say("Woohoo!") # todo: celebration options
                return "correct"
            
            if not isClaimedToBeCorrect and not isActuallyCorrect:
                active_guesser.nao.tts.say("How disappointing!") # todo: sad options
                return "incorrect"

            isFalsePositive = isClaimedToBeCorrect and not isActuallyCorrect
            isFalseNegative = not isClaimedToBeCorrect and isActuallyCorrect

            if isFalsePositive or isFalseNegative:
                if isInactiveHinterRobot:
                    inactive_hinter.nao.tts.say("Wait. Wait. Something is wrong. I am receiving a conflicting inputs message. We don't want any cheating here. Experimenter, please check your screen.")
                elif isInactiveGuesserRobot: # todo: experimental flaw. how would the guesser know this?
                    inactive_guesser.nao.tts.say("Wait. Wait. Something is wrong. I am receiving a conflicting inputs message. We don't want any cheating here. Experimenter, please check your screen.")

                message = "The guess was incorrect, but the participant pressed a hand for 'yes'" if isFalsePositive else "The guess was correct, but the participant pressed a foot for 'no'"
                print("CONFLICTING INPUTS: {}".format(message))

                choice = raw_input("Type 'reject' to abandon the round or <TAB> to ignore and continue")  # type: ignore (suppressess superfluous warning)
                if choice.strip().lower() == 'reject':
                    return "Reject"
                elif isFalsePositive:
                    return "incorrect"
                elif isFalseNegative:
                    return "correct"
        
        if not isActiveGuesserRobot:
            if isActiveHinterRobot:
                active_hinter.nao.tts.say("You are {}".format(isActuallyCorrectString))
            else:
                print("This should be a case where two humans are on the same team, and one needs to confirm/deny the guess")
                delay = raw_input("Press tab when humans are done")  # type: ignore (suppressess superfluous warning)
                # todo: take a Y/N and check for false positives/negatives ???

        return isActuallyCorrectString
    
    def end_of_game(self, save, team_1, team_2):
        team_1_score = save.get_score(team_1.team_name)
        team_2_score = save.get_score(team_2.team_name)
        team_1_outcome = "won" if team_1_score > team_2_score else "tied" if team_1_score == team_2_score else "lost"
        team_2_outcome = "won" if team_1_outcome == "lost" else "tied" if team_1_outcome == "tied" else "lost"        
        
        self.robot_1.nao.tts.say("Wow I can't believe {} and {}s team {} with a score of {}!".format(team_1.players[0], team_1.players[1], team_1_outcome, team_1_score))
        self.robot_2.nao.tts.say("and {} and {}s team {} with a score of {}!".format(team_2.players[0], team_2.players[1], team_2_outcome, team_2_score))
