from naoqi import ALModule
from enum import Enum
import threading
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
        self.processing_touch = False

        self.nao.memory.subscribeToEvent("TouchChanged", module_name, "onTouchChanged")

        # ------- helpers for confirmation -------
        self._lock_confirm = threading.Lock()
        self._awaiting_confirm = False
        self._confirm_event = threading.Event()
        self._confirm_result = None

        self._lock_activate = threading.Lock()
        self._awaiting_activate = False
        self._activate_event = threading.Event()
        self._activate_result = None


    def onTouchChanged(self, strVarName, value):
        if self.processing_touch or not value:
            return
        
        self.processing_touch = True
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
