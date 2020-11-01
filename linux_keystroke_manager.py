from pynput.keyboard import Key, Controller, Listener, KeyCode

MUTE = 269025042
UNMUTE = 269025042
PLAY = 269025044
PAUSE = 269025044
NEXT = 269025047
PREVIOUS = 269025046
STOP = 269025045
VOL_DOWN = 269025041
VOL_UP = 269025043

def press_key(key):
    keyboard_controller = Controller()
    keyboard_controller.press(key)
    keyboard_controller.release(key)

def press_media_key(action):
    key = KeyCode.from_vk(action)
    press_key(key)
