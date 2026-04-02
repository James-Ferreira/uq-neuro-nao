from naoqi import ALModule
from enum import Enum
import threading
import time
from motion_library import joint_names_list

# confirmation_path = "/tmp/confirmation.txt"

class TouchMode(Enum):
    HEAD_BASIC = "TouchModuleHead"
    SEE_TARGET = "TouchModuleSeeTarget"
    SHAKE_HAND_CLAS = "TouchModuleShakeHand_clas"
    SHAKE_HAND_META = "TouchModuleShakeHand_meta"
    FOOT_COMPLETE = "TouchModuleFoot"
    CONFIRMATION = "TouchModuleConfirm"
    HANKIE = "TouchModuleHankie"
    HEAD_SMASH = "TouchModuleHeadSmash"
    LEFT_HAND_LAUGH = "TouchModuleLaugh"
    RIGHT_FOOT_SCREAM = "TouchModuleScream"

class TouchModule(ALModule):
    def __init__(self, nao, module_name):
        ALModule.__init__(self, module_name)

        import __main__
        __main__.__dict__[module_name] = self

        self.nao = nao
        self.module_name = module_name
        self.processing_touch = False

        # ------- helpers for confirmation -------
        self._lock_confirm = threading.Lock()
        self._awaiting_confirm = False
        self._confirm_event = threading.Event()
        self._confirm_result = None

        self._lock_activate = threading.Lock()
        self._awaiting_activate = False
        self._activate_event = threading.Event()
        self._activate_result = None

        # helpers for hold to talk
        self._lock_hold = threading.Lock()
        self._awaiting_hold = False
        self._hold_press_event = threading.Event()
        self._hold_release_event = threading.Event()
        self._hold_pressed = False

        self._subscribe_events()

    def _log(self, message):
        stamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print("[TOUCH {}] {}".format(stamp, message))

    def _subscribe_events(self):
        self.nao.memory.subscribeToEvent("TouchChanged", self.module_name, "onTouchChanged")
        self.nao.memory.subscribeToEvent("LeftBumperPressed", self.module_name, "onLeftBumperPressed")
        self._log("Subscribed to TouchChanged and LeftBumperPressed for {}".format(self.module_name))

    def refresh_event_subscriptions(self):
        try:
            self._log("Refreshing touch event subscriptions")
            self._subscribe_events()
        except Exception as e:
            self._log("WARN: refresh_event_subscriptions failed: {}".format(e))


    def onTouchChanged(self, strVarName, value):
        if self.processing_touch or not value:
            return
        
        self.processing_touch = True
        try:
            if len(value) > 1 and isinstance(value[1], list) and len(value[1]) > 0:
                specific_touch = value[1][0]
            else:
                specific_touch = value[0][0]

            # touch module will send one message for pressed down, and one for released
            # we only care about the first one
            pressedDown = False
            if len(value) > 1:
                pressedDown = value[1][1]
            else:
                pressedDown = value[0][1]

            if self._awaiting_confirm and pressedDown:
                    with self._lock_confirm:
                        if "Foot" in specific_touch:
                            self._confirm_result = False
                            self._confirm_event.set()

                        if "Hand" in specific_touch:
                            self._confirm_result = True
                            self._confirm_event.set()

            if self._awaiting_activate and pressedDown:
                with self._lock_activate:
                        if "Head" in specific_touch:
                            self._activate_result = True
                            self._activate_event.set()
        except Exception as e:
            self._log("WARN: onTouchChanged failed: {}".format(e))
        finally:
            self.processing_touch = False

    def wait_for_touch_activate(self):
        with self._lock_activate:
            self._awaiting_activate = True
            self._activate_result   = None
            self._activate_event.clear()

        signalled = self._activate_event.wait()

        with self._lock_activate:
            self._awaiting_activate = False
            return self._activate_result if signalled else None

    def wait_for_touch_confirm(self):
        with self._lock_confirm:
            self._awaiting_confirm = True
            self._confirm_result   = None
            self._confirm_event.clear()

        signalled = self._confirm_event.wait()
        with self._lock_confirm:
            self._awaiting_confirm = False
            return self._confirm_result if signalled else None
    
    def onLeftBumperPressed(self, strVarName, value):
        isPressed = bool(value)
        with self._lock_hold:
            if not self._awaiting_hold:
                return
            if isPressed and not self._hold_pressed:
                self._hold_pressed = True
                self._log("Left bumper press event received")
                self._hold_press_event.set()
            elif (not isPressed) and self._hold_pressed:
                self._hold_pressed = False
                self._log("Left bumper release event received")
                self._hold_release_event.set()

    def reset_hold_state(self):
        with self._lock_hold:
            self._awaiting_hold = False
            self._hold_pressed = False
            self._hold_press_event.clear()
            self._hold_release_event.clear()
        self._log("Hold state reset")

    def wait_for_left_bumper_press(self, timeout=None):
        with self._lock_hold:
            self._awaiting_hold = True
            self._hold_pressed = False
            self._hold_press_event.clear()
            self._hold_release_event.clear()
        self._log("Waiting for left bumper press (timeout={})".format(timeout))
        ok = self._hold_press_event.wait(timeout)
        self._log("Wait for left bumper press completed: {}".format(ok))
        return ok

    def wait_for_left_bumper_release(self, timeout=None):
        self._log("Waiting for left bumper release (timeout={})".format(timeout))
        ok = self._hold_release_event.wait(timeout)
        with self._lock_hold:
            self._awaiting_hold = False
            if not ok:
                self._hold_pressed = False
        self._log("Wait for left bumper release completed: {}".format(ok))
        return ok
