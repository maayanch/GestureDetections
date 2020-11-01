STOP = {"stop", "pause"}
PLAY = {"play"}
NEXT = {"next"}
PREV = {"previous", "back"}
EXIT = {"shut up"}
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
SEARCH_YOUTUBE = {'search YouTube', 'YouTube', 'search in YouTube'}

INSTRUCTIONS = {"open instructions", "instructions", "commands"}
DONE_COMMAND = {"done"}

instructions = {"Stop": STOP, "Play": PLAY, "Next": NEXT, "Previous": PREV, "Scroll up": PAGE_UP,
                "Scroll down": PAGE_DOWN, "Zoom in": ZOOM_IN, "Zoom out": ZOOM_OUT, "Increase volume": VOLUME_UP,
                "Decrease Volume": VOLUME_DOWN, "Mute": MUTE, "Google search": SEARCH, "Youtube search": SEARCH_YOUTUBE,
                "Stop listening": DONE_COMMAND}


def get_instruction_text():
    instruction_text = ""
    for command, words in instructions.items():
        instruction_text += command + ' : '
        for i in range(len(words)):
            instruction_text += words[i]
            if i != len(words) - 1:
                instruction_text += ', '
        instruction_text += '\n'
    return instruction_text


