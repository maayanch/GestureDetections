import os
import tkinter as tk
from soundhound_utils import *
from PIL import ImageTk, Image
from sys import platform

DEFAULT_TITLE = "DEFAULT"

PUPPY_LISTEN_PATH = 'puppy_listen.jpeg'
PUPPY_WATCH_PATH = 'puppy_watch.jpeg'
PUPPY_ASK_PATH = 'puppy_ask.jpeg'

CAMERA_PATH = 'camera.jpeg'
MICROPHONE_PATH = 'microphone.jpeg'
BISLY_PATH = 'bisly.jpeg'
STANDBY_PATH = 'standby.jpeg'
WTF_DUDE_PATH = 'wtf_dude.jpeg'

ICON_WIDTH = 100
ICON_HEIGHT = 100

DIRNAME = os.path.dirname(__file__)
TUTORIAL_VID = os.path.join(DIRNAME, 'images', 'oodi.mp4')
# BG_PATH = os.path.join(DIRNAME, "images/bg1.jpg")
BG_PATH = os.path.join(DIRNAME, "images", "bg1.jpg")
BUTTON_PATH = os.path.join(DIRNAME, "images", "button.png")


def get_instructions_text():
    return ""


class GUI:
    TALK_MSG = "Talk now"
    LISTEN_MSG = "...Listening..."
    DONE_LISTENING = "Done Listening"
    REPEAT_MSG = 'Sorry, I did not understand you. Please repeat your query'

    def __init__(self):
        self.__interaction_window = None
        self.__interaction_label = None
        self.__instruction_window = None
        # self.__greeting_window = None
        self.__instruction_text = get_instruction_text()

    # Instructions Window Handling

    def open_instructions_window(self):
        self.__instruction_window = tk.Toplevel(None)
        text = get_instruction_text() + "\nTo close this window, say: Close instructions"
        instructions_label = tk.Label(master=self.__instruction_window,text=text)
        instructions_label.pack()
        self.__instruction_window.update()

    def close_instructions_window(self):
        self.__instruction_window.destroy()
        self.__instruction_window.quit()
        self.__instruction_window = None

    # Interaction Window Handling:

    def interaction_window_open(self):
        return self.__interaction_window is not None

    def open_interaction_window(self):
        self.__interaction_window = tk.Tk()
        # self.__interaction_window.attributes('-topmost', True)
        # self.__interaction_window.attributes('-alpha', 0.9)
        # self.__interaction_window.attributes('-toolwindow', True)
        self.__interaction_window = self.__center_window(self.__interaction_window)
        # self.__interaction_window.geometry("300x100")
        self.__interaction_window.attributes('-topmost', True)
        self.CUR_IMG = ImageTk.PhotoImage(Image.open(STANDBY_PATH).resize((ICON_WIDTH, ICON_HEIGHT)))
        self.__interaction_window.title(DEFAULT_TITLE)
        self.__interaction_label = tk.Label(master=self.__interaction_window, image=self.CUR_IMG)
        self.__interaction_label.pack(side="bottom", expand="yes")
        # self.__interaction_window.geometry("300x100")
        self.__interaction_window.geometry("100x100")
        self.__interaction_window.update()

    def display_thinking(self):
        self.__interaction_label.config(text='...Listening...')
        self.__interaction_label.pack()
        self.__interaction_window.update()

    def change_interaction_message(self, message, new_img_path=None):
        if new_img_path is not None:
            self.CUR_IMG = ImageTk.PhotoImage(Image.open(new_img_path).resize((ICON_WIDTH, ICON_HEIGHT)))
        self.__interaction_label.config(image=self.CUR_IMG)
        self.__interaction_window.title(message)
        self.__interaction_label.pack()
        self.__interaction_window.update()

    def did_not_understand(self):
        self.__interaction_window.attributes('-alpha', 0.5)
        self.__interaction_label.config(text='Sorry, I did not understand you. Please repeat your query')
        self.__interaction_label.pack()
        self.__interaction_window.update()

    def close_interaction_window(self):
        self.__interaction_window.destroy()
        self.__interaction_window.quit()

    # Greeting Window Handling:

    def open_greeting_window(self):
        self.__greeting_window = tk.Tk()
        # self.__greeting_window = tk.Toplevel()
        if platform == "win32" or platform == "win64":
            self.__greeting_window.attributes('-fullscreen', True)
        else:
            self.__greeting_window.attributes('-zoomed', True)
        # Set Background image:
        width, height = self.__greeting_window.winfo_screenwidth(), self.__greeting_window.winfo_screenheight()
        C = tk.Canvas(self.__greeting_window, bg="blue", height=height,
                      width=width)
        filename = ImageTk.PhotoImage(file=BG_PATH)
        print(BG_PATH)
        background_label = tk.Label(self.__greeting_window, image=filename)

        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.image = filename

        # Set Text
        instructions_label = tk.Label(master=self.__greeting_window, text="Welcome to SoundHound!",
                                      bg="green")
        instructions_label.config(font=("Courier", 44))
        instructions_label.place(relx=0.5, rely=0.1, anchor="n")
        instructions_label = tk.Label(master=self.__greeting_window, text=get_instruction_text())
        instructions_label.place(relx=0.5, rely=0.2, anchor="n")
        # Set app start button
        start_button = tk.Button(master=self.__greeting_window, text="Start App",
                                 command=self.close_greeting_window_and_start,
                                 bg="dark red")
        start_button.config(font=("Courier", 44))
        start_button.place(relx=0.5, rely=0.7, anchor="n")
        # Set app quit button
        close_button = tk.Button(master=self.__greeting_window, text="Quit App",
                                 command=self.close_greeting_window_and_quit,
                                 bg="grey")
        close_button.config(font=("Courier", 30))
        close_button.place(relx=0.5, rely=0.85, anchor="n")

        self.__greeting_window.mainloop()
        print('--------------')
        # self.__greeting_window.update()
        return self.__should_start

    def close_greeting_window_and_start(self):
        self.__greeting_window.destroy()
        self.__greeting_window.quit()
        self.__should_start = True
        # TODO: call main app run

    def close_greeting_window_and_quit(self):
        self.__greeting_window.destroy()
        self.__greeting_window.quit()
        self.__should_start = False
        # TODO: call main app run

    def __play_tutorial_video(self):
        os.startfile(TUTORIAL_VID)

    def __center_window(self, root):
        windowWidth = root.winfo_reqwidth()
        windowHeight = root.winfo_reqheight()
        # Gets both half the screen width/height and window width/height
        positionRight = int(root.winfo_screenwidth() / 2 - windowWidth / 2)
        positionDown = 0  # int(root.winfo_screenheight() / 2 - windowHeight / 2)

        # Positions the window in the center of the page.
        root.geometry("+{}+{}".format(positionRight, positionDown))
        return root


if __name__ == '__main__':
    gui = GUI()
    gui.open_instructions_window()
    time.sleep(3)
    gui.close_instructions_window()
    time.sleep(3)
