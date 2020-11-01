import os
import sys
import time
import webbrowser

STOP = {"stop"}
PLAYPAUSE = {"play", 'pause'}
NEXT = {'next'}
PREV = {'previous', 'back'}

YOUTUBE_PLAYPAUSE = {'stop YouTube','shut up YouTube','play YouTube','pause YouTube'}
YOUTUBE_NEXT = {"next YouTube", "play next song YouTube"}
YOUTUBE_PREV = {"previous YouTube", "back YouTube", "not next YouTube", "play last song YouTube", "last YouTube"}
EXIT = {"shut up", "exit", "quit"}
SCROLL_NEXT_PARA = {"scroll next"}
SCROLL_PREV_PARA = {"scroll previous", "scroll back"}
PAGE_UP = {'page up'}
PAGE_DOWN = {'page down'}
ZOOM_IN = {"zoom in"}
ZOOM_OUT = {"zoom out"}
VOLUME_UP = {"increase volume", "volume up", "louder"}
VOLUME_DOWN = {"decrease volume", "volume down"}
MUTE = {"mute", "unmute"}
GO_CRAZY = {"go crazy", "Allahu Akbar"}
SEARCH = {'Google', 'search'}
SEARCH_YOUTUBE = {'search YouTube', 'YouTube'}
CANCEL_LISTENING = {"cancel", "go away", "return", "nothing", "nevermind"}
INSTRUCTIONS = {"open instructions", "instructions", "show instructions", "commands"}
CLOSE_INSTRUCTIONS = {"close instructions"}
DONE_COMMAND = {"done"}
FULLSCREEN = {"fullscreen",'full screen', "enter fullscreen", "exit fullscreen"}
REWIND = {"rewind", "restart", "restart video"}
INCREASE_PLAYBACK_SPEED = {'increase speed', 'speed up'}
DECREASE_PLAYBACK_SPEED = {'decrease speed', 'speed down', 'slow down'}

# instructions = {"Stop": STOP, "Play": PLAY, "Next": NEXT, "Previous": PREV, "Scroll up": PAGE_UP,
# "Scroll down": PAGE_DOWN, "Zoom in": ZOOM_IN, "Zoom out": ZOOM_OUT, "Increase volume": VOLUME_UP,
# "Decrease Volume": VOLUME_DOWN, "Mute": MUTE, "Google search": SEARCH, "Youtube search": SEARCH_YOUTUBE,
# "Stop listening": DONE_COMMAND}

instructions = {"Stop": STOP, "Play": PLAYPAUSE, "Next": YOUTUBE_NEXT, "Previous": YOUTUBE_PREV,
                "Increase volume": VOLUME_UP,
                "Decrease Volume": VOLUME_DOWN, "Mute": MUTE,
                "Enter/Exit fullscreen": FULLSCREEN,
                "Rewind": REWIND,
                "Increase speed": INCREASE_PLAYBACK_SPEED,
                "Decrease speed": DECREASE_PLAYBACK_SPEED,
                "Stop listening": CANCEL_LISTENING}

# def get_instruction_text():
#     instruction_text = ""
#     for command, words in instructions.items():
#         instruction_text += command + ' : '
#         for i in range(len(words)):
#             instruction_text += words[i]
#             if i != len(words) - 1:
#                 instruction_text += ', '
#         instruction_text += '\n'
#     return instruction_text

def get_instruction_text():
    instruction_text = "Point your hand to the screen, and when asked to, say one of the words on the right to " \
                       "perform the command to the left " \
                       ".\n" \
                       "For Example: To search Youtube for a video, say: Search Youtube {name of video}\n"

    for command, words in instructions.items():
        instruction_text += command + ' : '
        i = 0
        for word in words:
            instruction_text += word
            if i != len(words) - 1:
                instruction_text += ', '
            i += 1
        instruction_text += '\n'
    return instruction_text


#
# def get_instruction_text():
#     return "To perform any action, hold your hand to the screen, and say any of the words listed here:"


def play_tutorial():
    webbrowser.open_new("https://www.youtube.com/watch?v=iYZIUtDAFIw")

LINUX_FIND_SOUND_INPUTS_CMD = "pacmd list-sink-inputs"
LINUX_SET_MUTE_STATE_CMD = 'pacmd set-sink-input-mute {} {}' # expects input index and true|false

def mute_all(mute=False):
    msg = "Muting all" if mute else "Unmuting all"
    print(msg+" on platform {}".format(sys.platform))
    if sys.platform == 'linux':
        x = os.popen(LINUX_FIND_SOUND_INPUTS_CMD).readlines()
        indices = [line.strip().split('index: ')[1] for line in x if line.strip().startswith('index')]
        should_mute = 'true' if mute else 'false'
        procs_mute_cmds = [LINUX_SET_MUTE_STATE_CMD.format(index, should_mute) for index in indices]
        for cmd in procs_mute_cmds:
            os.popen(cmd)

if __name__=='__main__':
    print("Testing mute/unmute function...")
    mute_all(mute=True)
    sleep_time_secs = 3
    print("Sleeping for {} seconds...".format(sleep_time_secs))
    time.sleep(sleep_time_secs)
    mute_all(mute=False)
