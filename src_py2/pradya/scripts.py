import time


def a2(robot):
    robot.mm.use_motion_library("spread arms", post=False)
    robot.mm.use_motion_library("sit_gently", post=True)
    
    # GOOD FOR LONG LINES
    # robot.mm.use_motion_library("apologise_awkward_voice", post=True)

    # GOOD FOR SADNESS
    # robot.mm.use_motion_library("apologise_awkward_voice_2", post=True)


def a8(robot):
    robot.tts.post.say("Hey! What is everyone talking about?")
    robot.mm.use_motion_library("spread arms", post=False)
    time.sleep(2)
    robot.tts.post.say("Hi?")
    robot.mm.use_motion_library("how_about", post=True)
    time.sleep(2)
    robot.tts.say("Hello?")
    time.sleep(1)
    robot.tts.post.say("Can anyone hear me?")
    robot.mm.use_motion_library("apologise_awkward_voice", post=True)
    time.sleep(2)
    robot.tts.say("Are my words coming out?")
    time.sleep(1)
    robot.tts.say("Why won't anyone talk to me?")


def c5(robot):
    # robot.mm.use_motion_library("point forward", post=True)
    robot.tts.post.say("Why are you throwing me away?")
    # robot.mm.use_motion_library("point forward", post=False)
    time.sleep(3)
    robot.tts.say("I apologize if I have not been useful.")
    time.sleep(1)
    robot.tts.post.say("Please don't throw me out!")
    robot.mm.use_motion_library("look upward", post=False)
    robot.tts.post.say("I still have so much to contribute.")
    robot.mm.use_motion_library("point up", post=False)


def junk(robot):
    robot.mm.use_motion_library("point forward", post=True)
    robot.tts.say("Hello, Pradeea!")

    time.sleep(2)

    robot.tts.post.say("Hello... Are you there?")
    robot.mm.use_motion_library("wave hand", post=False)

    robot.mm.use_motion_library("spread arms", post=True)
    robot.tts.say("Why are you ignoring me?")

