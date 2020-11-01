import time

from input_handler import InputHandler
import speech_recognition as sr
from gesture_detection_handler import wait_for_gesture
from input_handler import InputHandler
from gui_handler import GUI
import gui_handler
from soundhound_utils import *
from pynput import keyboard

ENTER_VOICE_MOOD = 0
EXIT_APP = 2


class Better_Soundhound:

    def __init__(self):
        self.gui = GUI()

        self.input_handler = InputHandler(self.gui, let_the_nice_lady_speak=True)
        self.mic = sr.Microphone()
        self.recorder = sr.Recognizer()
        self.recorder.pause_threshold = 0.6
        self.recorder.operation_timeout = 1
        self.action_dict = {ENTER_VOICE_MOOD: self.listen_to_command_mode,
                            EXIT_APP: self.close_app}
        time.sleep(1)

    def listen_to_command_mode(self):
        # todo change icon
        self.input_handler.listen_for_command()
        # todo change icon for action

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.gui.interaction_window_open():
            self.gui.close_interaction_window()
        mute_all(mute=False)

    def show_start_screen_and_run_app(self):
        start_the_app = self.gui.open_greeting_window()
        time.sleep(1)
        if start_the_app:
            self.gui.open_interaction_window()
            self.gui.change_interaction_message(message="Initializing...")
        else:
            print("User clicked exit.")
            self.close_app()

    # [detected_face, detected_left_arm, detected_left_palm, detected_left_hold_it, detected_right_arm, detected_right_palm, detected_right_hold_it, stop]
    def run_app(self, show_detection_screen=False):
        # Open greeting window - when closed, will continue from this point in code. Blocking!
        self.show_start_screen_and_run_app()
        finished = False
        detection_generator = wait_for_gesture(verbose=True, show_detection_screen=show_detection_screen)
        while not finished:
            self.gui.change_interaction_message(message="Watching you.......", new_img_path=gui_handler.CAMERA_PATH)
            detections = next(detection_generator)
            action = self.action_from_detection(detections)
            if action is None:  # if the detected gesture does not specify an action, skip it
                continue
            self.handle_action(action)
            # self.handle_action(action)
            # if something = exit app:
            # finished = True
        self.close_app()

    def action_from_detection(self, detections):
        #  todo - add more!!!
        print(detections[7])
        if detections[7]:
            return EXIT_APP
        elif (detections[3] or detections[6]) and not detections[7]:  # only one sided hold it gesture
            return ENTER_VOICE_MOOD
        else:
            return None

    def handle_action(self, action):
        assert action in self.action_dict
        action = self.action_dict[action]
        print("About to initiate {}".format(action))
        action()

    def close_app(self):
        print("User used exit app gesture, exiting.")
        mute_all(mute=False)
        exit()


if __name__ == '__main__':
    # check args
    # bsh = Better_Soundhound()
    with Better_Soundhound() as bsh:
        try:
            bsh.run_app(show_detection_screen=False)
        except Exception as e:
            mute_all(mute=False)
            print("During run of bsh found exception:\n{}".format(e))
            exit(-1)
