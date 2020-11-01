import pyautogui
import webbrowser
import time
import urllib.request, urllib.parse
import re

STOP = ["stop", "pause"]
PLAY = ["play"]
NEXT = ["next"]
PREV = ["previous", "back"]
EXIT = ["shut up"]
SCROLL_NEXT_PARA = ["scroll next"]
SCROLL_PREV_PARA = ["scroll previous", "scroll back"]
PAGE_UP = ['page up']
PAGE_DOWN = ['page down']
ZOOM_IN = ["zoom in"]
ZOOM_OUT = ["zoom out"]
VOLUME_UP = ["increase volume", "volume up", "louder"]
VOLUME_DOWN = ["decrease volume", "volume down"]
MUTE = ["mute", "unmute"]
GO_CRAZY = ["go crazy", "Allahu Akbar"]
SEARCH = ['Google', 'search']
SEARCH_YOUTUBE = ['search YouTube', 'YouTube']


def input_command(user_text):
    if any(word in user_text for word in STOP):
        pyautogui.press('playpause')
        # keyboard.send('space')
        # keyboard.send('<179>') # Trying to get media key to work...it a snag
    elif any(word in user_text for word in PLAY):
        # keyboard.send('space')
        pyautogui.press('playpause')
    elif any(word in user_text for word in NEXT):
        # keyboard.send('Shift+N')
        pyautogui.hotkey('shift', 'n')
    elif any(word in user_text for word in PREV):
        # keyboard.send('alt+left')  # this goes back in browser.
        pyautogui.hotkey('alt', 'left')
    elif any(word in user_text for word in SCROLL_NEXT_PARA):
        # print("scrolling down")
        # keyboard.send('ctrl+down')
        pyautogui.hotkey('ctrl', 'down')
    elif any(word in user_text for word in SCROLL_PREV_PARA):
        pyautogui.hotkey('ctrl', 'up')
        # keyboard.send('ctrl+up')
    elif any(word in user_text for word in PAGE_UP):
        # keyboard.send('page up')
        pyautogui.press('pageup')
    elif any(word in user_text for word in PAGE_DOWN):
        # keyboard.send('page down')
        pyautogui.press('pagedown')
    elif any(word in user_text for word in ZOOM_IN):
        pyautogui.hotkey('ctrl', '+')
    elif any(word in user_text for word in ZOOM_IN):
        pyautogui.hotkey('ctrl', '-')
    elif any(word in user_text for word in GO_CRAZY):
        # self.__go_crazy()
        webbrowser.open_new('https://www.youtube.com/watch?v=gkTb9GP9lVI')
    elif any(word in user_text for word in SEARCH_YOUTUBE):
        search_and_play_youtube("borderlands 2 face mcshooty shoot me in the face")
    elif any(word in user_text for word in VOLUME_UP):
        pyautogui.press('volumeup', presses=5)
    elif any(word in user_text for word in VOLUME_DOWN):
        pyautogui.press('volumedown', presses=5)
    elif any(word in user_text for word in MUTE):
        # pyautogui.press('volumemute')
        pyautogui.press('m')
    elif any(word in user_text for word in EXIT):
        # playsound.playsound('shutup.mp3')
        exit(0)


def search_and_play_youtube(text_request):
    query_string = urllib.parse.urlencode({"search_query": text_request})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"/watch\?v=(.{11})', html_content.read().decode())
    webbrowser.open_new("http://www.youtube.com/watch?v=" + search_results[0])


def test_commands():
    input_command("YouTube")
    print("Playing youtube video")
    time.sleep(5)
    input_command("stop")
    print("Stopping youtube video")
    time.sleep(5)
    input_command("next")
    print("Playing next youtube video")
    time.sleep(5)
    input_command("previous")
    print("Playing  previous youtube video")
    time.sleep(5)
    input_command("louder")
    print("Increasing volume")
    time.sleep(5)
    input_command("volume down")
    print("Decreasing volume")
    time.sleep(5)
    input_command("mute")
    print("Muting volume")
    time.sleep(5)
    input_command("zoom in")
    time.sleep(2)
    input_command("zoom in")
    time.sleep(2)
    input_command("zoom in")
    time.sleep(2)
    input_command("zoom in")
    time.sleep(2)
    input_command("shut up")

if __name__ == '__main__':
    test_commands()
