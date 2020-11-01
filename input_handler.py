import os
import random
import sys

import mutagen.mp3
import pyautogui
import keyboard
import speech_recognition as sr
from gtts import gTTS
import playsound
import pygame
import webbrowser
import time
import urllib.request, urllib.parse
import re
import linux_keystroke_manager as lkm
import gui_handler
from soundhound_utils import *

YOUTUBE_VIEW_URL = "http://www.youtube.com/watch?v="

PAUSE = 4
PLAY_PREV = 3
PLAY_NEXT = 2
ASK_AGAIN = "Shoshi_ask_again_0"
ASK_WHAT = 0
SEARCH_NUM = 5
YOUTUBE_FAIL = "youtube_fail_0"
CASH_REGISTER = 'cash_register_0'


class InputHandler:

    def __init__(self, GUI, create=True, let_the_nice_lady_speak=False):
        self.speech_enabled = let_the_nice_lady_speak
        self.ask_what = None
        self.play_next = None
        self.play_prev = None
        self.stop_music = None
        self.recorder = sr.Recognizer()
        self.recorder.pause_threshold = 0.6
        self.gui = GUI
        self.music_playing = False

    def play_sound_from_file(self, path, volume=1, freq_modifier=1):
        if sys.platform == 'linux':
            print('linux play sound')
            mp3 = mutagen.mp3.MP3(path)
            pygame.mixer.init(frequency=mp3.info.sample_rate * freq_modifier)
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            pygame.mixer.quit()
            print('finished linux play sound')
        elif sys.platform == 'win32':
            playsound.playsound(path, True)
        else:
            raise Exception("Unknown platform inaal rabak.")

    def __input_command(self, user_text):
        """
        I hereby remove myself from any responsibility of the below huge pile of crap code. # David.
        """

        if user_text in STOP:
            if sys.platform == 'linux':
                lkm.press_media_key(lkm.STOP)
                return
            pyautogui.press('stop')
        elif user_text in PLAYPAUSE:
            if sys.platform == 'linux':
                lkm.press_media_key(lkm.PLAY)
                return
            pyautogui.press('playpause')
        elif user_text in NEXT:
            if sys.platform == 'linux':
                lkm.press_media_key(lkm.NEXT)
                return
        elif user_text in PREV:
            if sys.platform == 'linux':
                lkm.press_media_key(lkm.PREVIOUS)
                return
        elif user_text in YOUTUBE_PLAYPAUSE:
            self.__click()
            pyautogui.hotkey('Space')
        elif user_text in YOUTUBE_NEXT:
            self.__click()
            pyautogui.hotkey('Shift', 'N')
        elif user_text in YOUTUBE_PREV:
            self.__click()
            pyautogui.hotkey('alt', 'left')
        elif user_text in SCROLL_NEXT_PARA:
            self.__click()
            pyautogui.hotkey('ctrl', 'down')
        elif user_text in SCROLL_PREV_PARA:
            self.__click()
            pyautogui.hotkey('ctrl', 'up')
        elif user_text in PAGE_UP:
            self.__click()
            pyautogui.press('pageup')
        elif user_text in PAGE_DOWN:
            self.__click()
            pyautogui.press('pagedown')
        elif user_text in ZOOM_IN:
            self.__click()
            pyautogui.hotkey('ctrl', '+')
        elif user_text in ZOOM_OUT:
            self.__click()
            pyautogui.hotkey('ctrl', '-')
        elif user_text in GO_CRAZY:
            # self.__go_crazy()
            webbrowser.open_new('https://www.youtube.com/watch?v=gkTb9GP9lVI')
        elif self.user_wants_engine(user_text, SEARCH):
            self.search_google(user_text)
        elif self.user_wants_engine(user_text, SEARCH_YOUTUBE):

            self.search_and_play_youtube(user_text)
        elif user_text in VOLUME_UP:
            if sys.platform == 'linux':
                lkm.press_media_key(lkm.VOL_UP), lkm.press_media_key(lkm.VOL_UP), lkm.press_media_key(lkm.VOL_UP)
                return
            pyautogui.press('volumeup', presses=5)
        elif user_text in VOLUME_DOWN:
            if sys.platform == 'linux':
                lkm.press_media_key(lkm.VOL_DOWN), lkm.press_media_key(lkm.VOL_DOWN), lkm.press_media_key(lkm.VOL_DOWN)
                return
            pyautogui.press('volumedown', presses=5)
        elif user_text in MUTE:
            # pyautogui.press('volumemute')
            self.__click()
            if sys.platform == 'linux':
                lkm.press_key('m')
                return
            pyautogui.press('m')
        elif user_text in INSTRUCTIONS:
            self.gui.open_instructions_window()
        elif user_text in CLOSE_INSTRUCTIONS:
            self.gui.close_instructions_window()
        elif user_text in EXIT:  # Closes program
            if self.speech_enabled and "".join(user_text) == "shut up":
                self.play_sound_from_file('shutup.mp3', volume=1)
            print("Exiting app...")
            exit(0)
        elif "".join(user_text) in CANCEL_LISTENING:  # Stops listening
            return None
        elif "".join(user_text) in FULLSCREEN:  # Enters/exits fullscreen in youtube
            self.__click()
            if sys.platform == 'linux':
                lkm.press_key('f')
                return
            pyautogui.hotkey('f')
        elif user_text in REWIND:  # Rewinds video to start
            self.__click()
            if sys.platform == 'linux':
                lkm.press_key('0')
                return
            pyautogui.press('0')
        elif user_text in INCREASE_PLAYBACK_SPEED:  # Increases playback speed
            pyautogui.hotkey('shift', '>')
        elif user_text in DECREASE_PLAYBACK_SPEED:  # Decreases playback speed
            pyautogui.hotkey('shift', '<')
        else:
            raise Exception("Unsupported request {}".format(user_text))
        self.listen_for_command(implicit_listen=True)

    def user_wants_engine(self, user_text, engine_keywords):
        user_text_split = user_text.split(' ')
        return user_text_split[0] in engine_keywords or ' '.join(user_text_split[:2]) in engine_keywords

    def __mute_for_command(self):
        if self.music_playing:
            pyautogui.press('m')

    def __go_crazy(self):
        commands = ["alt+tab", 'page up', 'page down']
        for i in range(50):
            webbrowser.open_new('https://www.youtube.com/watch?v=gkTb9GP9lVI')
            command = random.choice(commands)
            keyboard.send(command)
            # keyboard.send('alt+tab')
            time.sleep(0.33)

    def __click(self):
        """
        Clicks on the screen, near the left-bottom corner.
        :return:
        """
        size = pyautogui.size()
        pyautogui.click(50, size[1] - 100)

    def search_google(self, text_request):
        from urllib import parse
        text_request = self.__clean_string(text_request, SEARCH)
        base_url = "http://www.google.com/?#q="
        # https://www.youtube.com/results?search_query=
        final_url = base_url + parse.quote_plus(text_request)
        webbrowser.open_new(final_url)

    def search_and_play_youtube(self, text_request, try_num=0):
        print("Attempting to find {} in youtube, try num = {}".format(text_request, try_num))
        try:
            text_request = self.__clean_string(text_request, SEARCH_YOUTUBE)
            if len(text_request) == 0:
                raise Exception("text_request length is 0!")
            print("Searching for {} in Youtube...".format(text_request))
            query_string = urllib.parse.urlencode({"search_query": text_request})
            html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
            search_results = re.findall(r'href=\"/watch\?v=(.{11})', html_content.read().decode())
            if search_results is None or len(search_results) == 0:
                msg = "Youtube has failed to find results for {}".format(text_request)
                print(msg)
                raise Exception(msg)
            url = YOUTUBE_VIEW_URL + search_results[0]
            print("Found {} in youtube successfully! opening in browser, url:\n\t{}.".format(text_request, url))
            try:
                webbrowser.get(using='google-chrome').open(url, new=2)
            except Exception as e:  # if failed to execute google chrome, use default browser
                print("Failed to execute google-chrome on url {}\nrunning default browse".format(url))
                webbrowser.open_new(url)

        except Exception as e:
            msg = "Failed to play in youtube.. Error:\n{}".format(e)
            print(msg)
            if try_num < 3:
                print("Try num: {}, trying again... exception was: \n{}".format(try_num, e))
                self.search_and_play_youtube(text_request, try_num)
                return
            raise Exception(msg)

    def listen_for_command(self, implicit_listen=False, ask_again_file=ASK_WHAT):
        """
        Called when user had indicated he wants the app to listen to a voice
        command.
        :return:
        """
        mute_all(mute=True)
        if implicit_listen:
            print("Implicitely listening...")
        self.gui.change_interaction_message("Listening to you...", new_img_path=gui_handler.WTF_DUDE_PATH)
        if not implicit_listen:
            print("asking 'what would you like to do'")
            if self.speech_enabled:
                self.play_sound_from_file(f'{ask_again_file}.mp3', volume=1)
        self.gui.change_interaction_message("Listening to you...", new_img_path=gui_handler.MICROPHONE_PATH)
        try:
            with sr.Microphone() as source:
                self.recorder.adjust_for_ambient_noise(source, duration=0.3)
                audio_request = self.recorder.listen(source, phrase_time_limit=2.5)  # TODO: removed timeout=5
            text_request = self.recorder.recognize_google(audio_request)
            self.gui.change_interaction_message(text_request, new_img_path=gui_handler.BISLY_PATH)
            print('--User message:', text_request)
            if self.speech_enabled:
                self.play_sound_from_file(f'{CASH_REGISTER}.mp3', volume=0.5, freq_modifier=2)
            self.__input_command(text_request)
            mute_all(mute=False)
        except Exception as e:
            print('Exception caught when attempting to listen to user:\n{}'.format(e))
            if implicit_listen:
                print("No msg when implicitely asked, returning.")
                mute_all(mute=False)
                return
            if 'youtube' in str(e):
                print("Youtube error, asking to retry search")
                self.gui.change_interaction_message(self.gui.REPEAT_MSG, new_img_path=gui_handler.PUPPY_ASK_PATH)
                self.listen_for_command(ask_again_file=YOUTUBE_FAIL)
            else:
                print("The app didn't understand, asking again")
                self.gui.change_interaction_message(self.gui.REPEAT_MSG, new_img_path=gui_handler.PUPPY_ASK_PATH)
                # if self.speech_enabled:
                #     playsound.playsound(f'{ASK_AGAIN}.mp3', True)
                self.listen_for_command(ask_again_file=ASK_AGAIN)

    def __clean_string(self, text_request, string_set):
        for stri in string_set:
            if text_request.find(stri) == 0:
                text_request = text_request.replace(stri, '', 1)
                break
        return text_request.lstrip()


if __name__ == '__main__':
    # listener = InputHandler(gui_handler.GUI())
    # # listener.shutdown()
    # while True:
    #     listener.listen_for_command()
    # gui = GUI()
    # gui.open_greeting_window()
    # time.sleep(1)
    print("zibby")
