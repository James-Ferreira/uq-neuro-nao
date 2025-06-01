from naoqi import ALModule, ALBroker, ALProxy
import sys
import time
# import sys
import logging
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

class TouchModule(ALModule):
    def __init__(self, name):
        ALModule.__init__(self, name)
        self.touch = ALProxy("ALTouch")
        self.memory = ALProxy("ALMemory")
        self.tts = ALProxy("ALTextToSpeech")
        print("Subscribing to TouchChanged event...")
        self.memory.subscribeToEvent("TouchChanged", "TouchModule", "onTouchChanged")
        print("Subscribed!")
        self.processing_touch = False

    def onTouchChanged(self, strVarName, value):
        print("onTouchChanged")
        if self.processing_touch or not value:
            return
        

        self.processing_touch = True

        if len(value) > 1 and isinstance(value[1], list) and len(value[1]) > 0:
            specific_touch = value[1][0]
        else:
            specific_touch = value[0][0]

	# print(specific_touch)
        self.tts.say("You touched my {}".format(specific_touch))

        time.sleep(1)
        self.processing_touch = False


def main():
    myBroker = ALBroker("myBroker", "0.0.0.0", 0, "192.168.0.78", 9559)
    global TouchModule
    TouchModule = TouchModule("TouchModule")
    try:
        while True:
            print("polling...")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Interrupted by user, shutting down")
        myBroker.shutdown()
        sys.exit(0)

if __name__ == "__main__":
    main()