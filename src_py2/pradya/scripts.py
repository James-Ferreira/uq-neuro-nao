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

#    robot.mm.use_motion_library("", post=False)

def gestures0110(robot):
    robot.tts.post.say("Facepalm.")
    robot.mm.use_motion_library("facepalm", post=False)
    robot.tts.post.say("Point up.")
    robot.mm.use_motion_library("point up", post=False)
    robot.tts.post.say("Point forward.")
    robot.mm.use_motion_library("point forward", post=False)
    robot.tts.post.say("Point down.")
    robot.mm.use_motion_library("point down", post=False)
    robot.tts.post.say("Scratch head,")
    robot.mm.use_motion_library("scratch head", post=False)
    robot.tts.post.say("Shake fist.")
    robot.mm.use_motion_library("shake fist", post=False)
    robot.tts.post.say("Look upward.")
    robot.mm.use_motion_library("look upward", post=False)
    robot.tts.post.say("Pump fist.")
    robot.mm.use_motion_library("pump fist", post=False)
    robot.tts.post.say("Wave hand.")
    robot.mm.use_motion_library("wave hand", post=False)
    robot.tts.post.say("Spread arms.")
    robot.mm.use_motion_library("spread arms", post=False)

def gestures1120(robot):
    robot.tts.post.say("Shrug.")
    robot.tts.post.say("Point to self.")
    robot.tts.post.say("Sit gently.")
    robot.tts.post.say("Head touch up.")
    robot.tts.post.say("Head touch down snoozy.")
    robot.tts.post.say("Head touch up 2.")
    robot.tts.post.say("Team is here.")
    robot.tts.post.say("Welcome 1 greetings.")
    robot.tts.post.say("Welcome 2 greetings.")
    robot.tts.post.say("Welcome 1 my name is.")

def gestures2130(robot):
    robot.tts.post.say("Welcome 1 ask name.")
    robot.tts.post.say("Am I saying that right?")
    robot.tts.post.say("Apologise awkward voice.")
    robot.tts.post.say("How about.")
    robot.tts.post.say("Don't take offense.")
    robot.tts.post.say("Apologise awkward voice 2.")
    robot.tts.post.say("Don't take offense 2.")
    robot.tts.post.say("You are in the game.")
    robot.tts.post.say("At your service.")
    robot.tts.post.say("Check name.")

def gestures3140(robot):
    robot.tts.post.say("Check name 2.")
    robot.tts.post.say("Apologise awkward voice 3.")
    robot.tts.post.say("At your service.")
    robot.tts.post.say("Check name failure.")
    robot.tts.post.say("Apologise incompetent programmers.")
    robot.tts.post.say("How about.")
    robot.tts.post.say("Check name failure.")
    robot.tts.post.say("Don't want to overheat.")
    robot.tts.post.say("Let's get to know each other.")
    robot.tts.post.say("Where are you from?")

def gestures4150(robot):
    robot.tts.post.say("Lives in Brisbane.")
    robot.tts.post.say("Nice place to live.")
    robot.tts.post.say("What are your hobbies.")
    robot.tts.post.say("Cool hobby.")
    robot.tts.post.say("What is your hobby?")
    robot.tts.post.say("What is your hobby 2?")
    robot.tts.post.say("My hobby is catching fly.")
    robot.tts.post.say("My hobby is playing puppets.")
    robot.tts.post.say("Very talented.")
    robot.tts.post.say("Where are you from?")

def gestures5160(robot):
    robot.tts.post.say("Brisbane is where I live.")
    robot.tts.post.say("I would like to visit.")
    robot.tts.post.say("Enjoys hobby.")
    robot.tts.post.say("Hobby is better.")
    robot.tts.post.say("Respectfully disagree.")
    robot.tts.post.say("What was opponents hobby.")
    robot.tts.post.say("Say hobby.")
    robot.tts.post.say("Catching flies more interesting.")
    robot.tts.post.say("To each its own.")
    robot.tts.post.say("Let's get to the game.")

def gestures6170(robot):
    robot.tts.post.say("Outro 1.")
    robot.tts.post.say("Outro 2.")
    robot.tts.post.say("Outro 3.")
    robot.tts.post.say("Outro 4.")
    robot.tts.post.say("Outro 5.")
    robot.tts.post.say("Outro 6.")
    robot.tts.post.say("Outro 7.")
    robot.tts.post.say("Outro 8.")
    robot.tts.post.say("Demo intro.")
    robot.tts.post.say("Ready to guess.")

def gestures7175(robot):
    robot.tts.post.say("WW.")
    robot.tts.post.say("Turn head right.")
    robot.tts.post.say("Turn head left.")
    robot.tts.post.say("Extend right hand.")