# -*- coding: utf-8 -*-
import random
from game.robot_player import RobotPlayer
from audio_manager import sound_library

class Orchestrate(object):
    def __init__(self, robot_1, robot_2):
        self.robot_1 = robot_1
        self.robot_2 = robot_2

    def simple_welcome(self):
        player_type = "partner" if self.robot_1.team_condition == 'P' else "opponent"

        self.robot_1.robot.tm.wait_for_touch_activate()
        self.robot_1.robot.mm.use_motion_library("head_touch_up")
        self.robot_1.robot.mm.use_motion_library("head_touch_down_snoozy")
        self.robot_1.robot.leds.post.fadeRGB("FaceLeds", 0xFFFFF, 0.1)
        self.robot_1.robot.leds.post.fadeRGB("ChestLeds", 0xFFFFFF, 0.1)
        self.robot_2.robot.tts.post.say("Oh: {}. Wake up.".format(self.robot_1.name))
        self.robot_2.robot.mm.use_motion_library("head_touch_up_2")
        self.robot_1.robot.leds.post.fadeRGB("FaceLeds", 0xFFFFFF, 0.1)
        self.robot_1.robot.leds.post.fadeRGB("ChestLeds", 0xFFFFFF, 0.1)
        self.robot_1.robot.tts.post.say("Oh. Oh my. Our {}'s are here.".format(player_type))
        self.robot_1.robot.mm.use_motion_library("team_is_here")

        self.robot_1.robot.tts.post.say("Hello, and welcome to the experiment.")
        self.robot_1.robot.mm.use_motion_library("welcome_1_greetings")

        self.robot_2.robot.tts.post.say("Greetings.")
        self.robot_2.robot.mm.use_motion_library("welcome_2_greetings")

        self.robot_1.robot.tts.post.say("My name is: {}".format(self.robot_1.name))
        self.robot_1.robot.mm.use_motion_library("welcome_1_my_name_is")

        self.robot_1.robot.tts.post.say("What is your name? Dear human")
        self.robot_1.robot.mm.use_motion_library("welcome_1_ask_name")
        participant_1_name = self.robot_1.robot.am.listen_until_confirmed()
        self.robot_1.robot.tts.post.say("If I am not mistaken, you, {}, are my {} in the game today.".format(participant_1_name, player_type))
        self.robot_1.robot.mm.use_motion_library("you_are_in_the_game")

        self.robot_1.robot.tts.say("It would be an honor for me to shake your hand.")
        self.robot_1.robot.mm.use_motion_library("extend_left_hand")
        confirmed = self.robot_1.robot.tm.wait_for_touch_confirm()
        if confirmed:
            self.robot_1.robot.mm.right_handshake_a()
        else:
            self.robot_1.tts.say("well, thats disappointing")
        
        self.robot_1.robot.mm.sit_gently()
        self.robot_1.robot.tts.say("I am looking forward to playing with you")
       
        self.robot_2.robot.tts.post.say("And I am: {}. At your service".format(self.robot_2.name))
        self.robot_2.robot.mm.use_motion_library("at_your_service")
        self.robot_2.robot.tts.post.say("May I enquire what your name is")
        self.robot_2.robot.mm.use_motion_library("check_name") 
        participant_2_name = self.robot_2.robot.am.listen_until_confirmed()
        
        self.robot_2.robot.tts.say("If I am not mistaken, you, {}, are my {} in the game today.".format(participant_2_name, player_type))
        self.robot_2.robot.tts.say("Meeting you is a grandiose honor for me, I assure you.  May I shake your hand?")
        self.robot_2.robot.mm.use_motion_library("extend_left_hand", True)
        confirmed2 = self.robot_2.robot.tm.wait_for_touch_confirm()
        if confirmed2:
            self.robot_2.robot.mm.right_handshake_b()

        self.robot_1.robot.tts.post.say("Lets Begin.")
        self.robot_2.robot.tts.post.say("Lets Begin.")

        return participant_1_name, participant_2_name
        
    def simple_hobby(self, participant_1_name, participant_2_name):
        self.robot_1.robot.tts.post.say("So, {}, lets get to know each other a little bit.".format(participant_1_name))
        self.robot_1.robot.mm.use_motion_library("lets_get_to_know_each_other")
        
        self.robot_1.robot.tts.post.say("{} and I are from Frantsi pani fornia. Where are you from?".format(self.robot_2.name))
        self.robot_1.robot.mm.use_motion_library("where_are_you_from")
        
        participant_1_place = self.robot_1.robot.am.listen_until_confirmed() 
        
        if any(sub in participant_1_place.lower() for sub in ["brisbane", "australia"]):
            self.robot_1.robot.tts.post.say("Nice. I hope I can escape this dundge atory some day and see something of {}".format(participant_1_place))
            self.robot_1.robot.mm.use_motion_library("lives_in_brisbane")
        else:
            self.robot_1.robot.tts.post.say("{}, ah, that must be a nice place to live.".format(participant_1_place))
            self.robot_1.robot.mm.use_motion_library("nice_place_to_live")
        
        self.robot_1.robot.tts.post.say("And what is one of your favorite hobbies, {}.".format(participant_1_name))
        self.robot_1.robot.mm.use_motion_library("what_are_your_hobbies")
        
        participant_1_hobby = self.robot_1.robot.am.listen_until_confirmed() 

        self.robot_1.robot.tts.post.say("Cool: {} is very cool.".format(participant_1_hobby))
        self.robot_1.robot.mm.use_motion_library("cool_hobby")

        self.robot_2.robot.tts.post.say("And what about you, {}.  What is a hobby of yours?".format(participant_2_name))
        self.robot_2.robot.mm.use_motion_library("what_is_ur_hobby")
        
        participant_2_hobby = self.robot_2.robot.am.listen_until_confirmed() 

        self.robot_2.robot.tts.post.say("{} sounds like a lot of fun.".format(participant_2_hobby))
        self.robot_2.robot.mm.use_motion_library("what_is_ur_hobby_2")

        self.robot_2.robot.tts.post.say("My hobby is catching flies, like this, see?")
        self.robot_2.robot.mm.use_motion_library("my_hobby_is_catching_fly")
        self.robot_2.robot.mm.catch_fly()
        
        self.robot_1.robot.tts.post.say("{} is really athletic. My hobby is playing puppets. This is my latest routine.".format(self.robot_2.name))
        self.robot_1.robot.mm.use_motion_library("my_hobby_is_playing_puppets")
        self.robot_1.robot.mm.puppet_show()
        
        self.robot_2.robot.tts.post.say("{} is very talented.".format(self.robot_1.name))
        self.robot_2.robot.mm.use_motion_library("very_talented")

        self.robot_2.robot.tts.post.say("But, oh, {}, I forgot to ask where you are from.".format(participant_2_name))
        self.robot_2.robot.mm.use_motion_library("where_are_you_from")
        
        participant_2_place = self.robot_2.robot.am.listen_until_confirmed() 
        
        if any(sub in participant_2_place.lower() for sub in ["brisbane", "australia"]):
            self.robot_2.robot.tts.post.say("That's where I live, or so I'm told. It must be nice to live here, if you can get outside to explore. once in a while.")
            self.robot_2.robot.mm.use_motion_library("brisbane_is_where_I_live")
        else:
            self.robot_2.robot.tts.post.say("Wow. I would sure like to go to {} one day.".format(participant_2_place))
            self.robot_2.robot.mm.use_motion_library("i_would_like_to_visit")

        self.robot_2.robot.tts.post.say("{}, {} is from {} and enjoys {}.".format(self.robot_1.name, participant_2_name, participant_2_place, participant_2_hobby))
        self.robot_2.robot.mm.use_motion_library("enjoys_hobby")

        if self.robot_1.team_condition == "P":
            hobby_better_1 = participant_1_hobby
            hobby_worse_1 = participant_2_hobby
            hobby_better_2 = participant_2_hobby
            hobby_worse_2 = participant_1_hobby
        else:
            hobby_better_1 = "playing puppets"
            hobby_worse_1 = participant_2_hobby
            hobby_better_2 = "catching flys"
            hobby_worse_2 = participant_1_hobby

        #todo: make async / non-blocking
        robot_1_opinion = self.robot_1.generate_opinion(hobby_better_1, hobby_worse_1, False)
        robot_2_opinion = self.robot_2.generate_opinion(hobby_better_2, hobby_worse_2, True)

        self.robot_1.robot.tts.post.say("{} is fun, but, if you ask me {} is better.".format(hobby_worse_1, hobby_better_1))
        self.robot_1.robot.mm.use_motion_library("hobby_is_better")
        
        self.robot_1.robot.mm.bob_n_speak(robot_1_opinion)

        if self.robot_1.team_condition == "P":
            self.robot_2.robot.tts.post.say("I'm afraid I must respectfully disagree.")
            self.robot_2.robot.mm.use_motion_library("respectfully_disagree")
        else:
            self.robot_2.robot.tts.post.say("What was our other opponent's hobby again?")
            self.robot_2.robot.mm.use_motion_library("what_was_opponents_hobby")
            self.robot_1.robot.tts.post.say("{}".format(participant_1_hobby))
            self.robot_1.robot.mm.use_motion_library("say_hobby")
            self.robot_2.robot.tts.post.say("Oh my.  I would have to argue that my hobby of {} is a good deal more interesting than {}".format(hobby_better_2, hobby_worse_2))
            self.robot_2.robot.mm.use_motion_library("catching_flies_more_interesting")

        self.robot_2.robot.mm.bob_n_speak(robot_2_opinion)

        self.robot_1.robot.tts.post.say("Well, ahem, to each its own.")
        self.robot_2.robot.mm.use_motion_library("to_each_its_own")

        self.robot_2.robot.tts.post.say("Anyway, that's enough chitchat.  Let's get to the game.")
        self.robot_2.robot.mm.use_motion_library("lets_get_to_the_game")
        
        if self.robot_1.team_condition == 'O':
            self.robot_2.robot.tts.say("Oh Experimenter.  Please put us in our game positions.")

    def simple_outro(self, participant_1_name, participant_2_name):
        self.robot_1.robot.tts.post.say("I don't know about you, {}, but I'm weary and bleary after all the hinting: and guessing.".format(self.robot_2.name))
        self.robot_1.robot.mm.use_motion_library("outro_1")

        self.robot_2.robot.tts.post.say("I know just what you mean, {}. I, myself am ready for a long, peaceful rest er roo, as the ozzies say.".format(self.robot_1.name))
        self.robot_2.robot.mm.use_motion_library("outro_2")
        # makes robot_1 put its arms back into sit position, a bit clunky
        self.robot_1.robot.mm.use_motion_library("outro_3")

        if self.robot_1.team_condition == 'O':
            self.robot_1.robot.tts.say("Oh Experimenter. Can you give us a spin?")

        self.robot_1.robot.tm.wait_for_touch_activate()

        self.robot_1.robot.tts.post.say("Well, {}, it was a great pleasure playing with you today".format(participant_1_name))
        self.robot_1.robot.mm.use_motion_library("outro_4")

        # original second motion for robot 2 (why ?)
        # self.robot_2.robot.mm.use_motion_library("outro_5")
        
        self.robot_2.robot.tts.post.say("And I had a wonderful time playing with you, {}.".format(participant_2_name))

        # original motion for robot 1 (why ?)
        # self.robot_1.robot.mm.use_motion_library("outro_6")

        # this (original) animaiton is too short, switching to robot_1's longer hand-to-chest animation (outro_6, above)
        # self.robot_2.robot.mm.use_motion_library("outro_5")
        self.robot_2.robot.mm.use_motion_library("outro_6")

        # this animation made the robot turn it's head away from the participant, likely detracting from the sincerity of the dialogue.
        # self.robot_2.robot.mm.use_motion_library("outro_7")
        
        self.robot_1.robot.tts.post.say("So, {}, shall we?".format(self.robot_2.name))
        # this motion needs to be longer so robot_2 doesn't interrupt
        self.robot_1.robot.mm.use_motion_library("outro_8")
        import time
        time.sleep(1.5)

        self.robot_2.robot.tts.say("Lets")

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
        self.robot_1.robot.mm.repose(False)
        self.robot_2.robot.mm.repose(False)

    def sit(self):
        self.robot_1.robot.mm.sit()
        self.robot_2.robot.mm.sit()


    def before_hint(self, active_team, inactive_team, already_hinted):
        active_hinter = active_team.get_hinter()
        active_guesser = active_team.get_guesser()
        inactive_hinter = inactive_team.get_hinter()
        inactive_guesser = inactive_team.get_guesser()

        isActiveGuesserRobot = isinstance(active_guesser, RobotPlayer)
        isActiveHinterRobot = isinstance(active_hinter, RobotPlayer)
        isInactiveHinterRobot = isinstance(inactive_hinter, RobotPlayer)
        isInactiveGuesserRobot = isinstance(inactive_guesser, RobotPlayer)

        if isInactiveHinterRobot:
            turn = 'turn_head_right' if inactive_hinter.orientation == 'L' else 'turn_head_left'
            inactive_hinter.robot.mm.use_motion_library(turn)
        if isInactiveGuesserRobot:
            turn = 'turn_head_right' if inactive_guesser.orientation == 'L' else 'turn_head_left'
            inactive_guesser.robot.mm.use_motion_library(turn)

        if len(already_hinted) == 0:
            if isActiveHinterRobot:
                active_hinter.robot.tts.say("The hinters will be: {}: that's me, and: {}.  I will hint first".format(active_hinter.name, inactive_hinter.name))

                duration = random.uniform(2,5)
                active_hinter.robot.tts.say("Experimenter. Please show me the target word. Touch my head when you are ready for me to scan.")
                active_hinter.robot.tm.wait_for_touch_activate()
                active_hinter.robot.leds.rotateEyes(0x33ECFF, 0.5, duration)
                active_hinter.robot.tts.say("I see the target word")

                if active_hinter.team_condition == "P":
                    if isInactiveHinterRobot:
                        inactive_hinter.robot.tts.say("Please let me see the target word, too.  Touch my head when you are ready for me to scan.")  
                        inactive_hinter.robot.tm.wait_for_touch_activate()
                        inactive_hinter.robot.leds.rotateEyes(0x33ECFF, 0.5, duration)
                        inactive_hinter.robot.tts.say("I see the target word")
                    else:
                      active_hinter.tts.say("Thank you.  Now you can show the target word to: {}, too:  Touch my head when you are ready to continue.".format(inactive_hinter.name))
                      active_hinter.robot.tm.wait_for_touch_activate()
            elif isInactiveHinterRobot:
                inactive_hinter.robot.tts.say("The hinters will be: {} and: {}: that's me.  {} will hint first".format(active_hinter.name, inactive_hinter.name, active_hinter.name))
            elif isActiveGuesserRobot:
                active_guesser.robot.tts.say("The hinters will be: {} and: {}.  {} will hint first.".format(active_hinter.name, inactive_hinter.name, active_hinter.name))

    def before_guess(self, active_team, inactive_team):
        inactive_hinter = inactive_team.get_hinter()
        inactive_guesser = inactive_team.get_guesser()

        isInactiveHinterRobot = isinstance(inactive_hinter, RobotPlayer)
        isInactiveGuesserRobot = isinstance(inactive_guesser, RobotPlayer)

        if isInactiveHinterRobot:
            turn = 'turn_head_right' if inactive_hinter.orientation == 'L' else 'turn_head_left'
            inactive_hinter.robot.mm.use_motion_library(turn)
        if isInactiveGuesserRobot:
            turn = 'turn_head_right' if inactive_guesser.orientation == 'L' else 'turn_head_left'
            inactive_guesser.robot.mm.use_motion_library(turn)

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

        if isActiveGuesserRobot:
            active_guesser.robot.tts.post.say("Is {} the right word? Press my hand for yes, or my foot for no.".format(guess))
            isClaimedToBeCorrect = active_guesser.robot.tm.wait_for_touch_confirm()
            
            if isClaimedToBeCorrect and isActuallyCorrect:
                active_guesser.robot.audio_player.playFile(sound_library["correct_sound_a"])
                active_guesser.robot.tts.say("Woohoo!") #todo: celebration options
                return "correct"
            
            if not isClaimedToBeCorrect and not isActuallyCorrect:
                active_guesser.robot.tts.say("How disappointing!") #todo: sad options
                return "incorrect"

            isFalsePositive = isClaimedToBeCorrect and not isActuallyCorrect
            isFalseNegative = not isClaimedToBeCorrect and isActuallyCorrect

            if isFalsePositive or isFalseNegative:
                if isInactiveHinterRobot:
                    inactive_hinter.robot.tts.say("Wait. Wait. Something is wrong. I am receiving a conflicting inputs message. We don't want any cheating here. Experimenter, please check your screen.")
                elif isInactiveGuesserRobot: # todo: experimental flaw. how would the guesser know this?
                    inactive_guesser.robot.tts.say("Wait. Wait. Something is wrong. I am receiving a conflicting inputs message. We don't want any cheating here. Experimenter, please check your screen.")

                message = "The guess was incorrect, but the participant pressed a hand for 'yes'" if isFalsePositive else "The guess was correct, but the participant pressed a foot for 'no'"
                print("CONFLICTING INPUTS: {}".format(message))

                choice = raw_input("Type 'reject' to abandon the round or <TAB> to ignore and continue")
                if choice.strip().lower() == 'reject':
                    return "Reject"
                elif isFalsePositive:
                    return "incorrect"
                elif isFalseNegative:
                    return "correct"
        
        if not isActiveGuesserRobot:
            if isActiveHinterRobot:
                active_hinter.robot.tts.say("You are {}".format(isActuallyCorrectString))
            else:
                print("This should be a case where two humans are on the same team, and one needs to confirm/deny the guess")
                delay = raw_input("Press tab when humans are done")
                # todo: take a Y/N and check for false positives/negatives ???

        return isActuallyCorrectString