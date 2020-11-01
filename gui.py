import tkinter as tk
from soundhound_utils import get_instruction_text
from soundhound_utils import play_tutorial
from PIL import ImageTk, Image


class GUI:
    TALK_MSG = "Talk now"
    LISTEN_MSG = "...Listening..."
    DONE_LISTENING = "Done Listening"
    REPEAT_MSG = 'Sorry, I did not understand you. Please repeat your query'

    def __init__(self):
        self.__canvas_img = None
        self.__interaction_window = None
        self.__interaction_label = None
        self.__instruction_window = None
        self.__greeting_window = None

        self.__icon = None
        self.__icon_label = None
        self.__img_watching = None
        self.__img_recording = None
        self.__icon_canvas = None

        self.__instruction_text = get_instruction_text()

    # Instructions Window Handling

    def open_instructions_window(self):
        self.__instruction_window = tk.Tk()
        instructions_label = tk.Label(text=self.__instruction_text)
        instructions_label.pack()
        # self.__instruction_window.after(4000)
        # self.__instruction_window.mainloop()
        self.__instruction_window.update()

    def close_instructions_window(self):
        self.__instruction_window.destroy()

    # Interaction Window Handling:

    def open_interaction_window(self):
        self.__interaction_window = tk.Tk()
        self.__interaction_label = tk.Label(master=self.__interaction_window, text="Talk now")
        self.__interaction_label.pack()
        # self.__interaction_window.mainloop()
        self.__interaction_window.update()

    def display_thinking(self):
        self.__interaction_label.config(text='...Listening...')
        self.__interaction_label.pack()
        self.__interaction_window.update()

    def change_interaction_message(self, message):
        self.__interaction_label.config(text=message)
        self.__interaction_label.pack()
        self.__interaction_window.update()

    def did_not_understand(self):
        self.__interaction_label.config(text='Sorry, I did not understand you. Please repeat your query')
        self.__interaction_label.pack()
        self.__interaction_window.update()

    def close_interaction_window(self):
        self.__interaction_window.destroy()

    # Greeting Window Handling:

    def open_greeting_window(self):
        self.__greeting_window = tk.Tk()
        frame = tk.Frame()
        instructions_label = tk.Label(master=frame, text="Welcome to SoundHound!")
        instructions_label.pack()
        tutorial_button = tk.Button(master=frame, text="Play tutorial", command=play_tutorial)
        tutorial_button.pack()
        frame.pack()
        self.__greeting_window.mainloop()
        # self.__greeting_window.update()

    def close_greeting_window(self):
        self.__greeting_window.destroy()

    # Small Icon?

    def open_icon(self):
        self.__icon = tk.Tk()
        self.__icon.attributes('-topmost', True)
        self.__icon.attributes('-alpha', 0.5)
        self.__icon.attributes('-toolwindow', True)
        self.__img_recording = ImageTk.PhotoImage(Image.open("images/record.jpg"))
        self.__img_watching = ImageTk.PhotoImage(Image.open("images/watching.png"))
        self.__icon = self.__center_window(self.__icon)
        self.__icon.wm_attributes("-transparentcolor", 'white')
        # self.__icon_label = tk.Label(self.__icon, image=self.__img_recording, bg="white")
        # self.__icon_label.pack()
        self.__icon_canvas = tk.Canvas(self.__icon, bg='black', width=100, height=100)
        self.__icon_canvas.pack()
        self.__canvas_img = self.__img_watching
        self.__icon_canvas.create_image(0, 0, anchor=tk.NW, image=self.__canvas_img)
        self.__icon.update()
        # self.__icon.mainloop()

    def icon_display_recording(self):
        # self.__icon_label.configure(image=self.__img_recording)
        # self.__icon_label.pack()
        self.__icon_canvas.itemconfig(self.__canvas_img, image=self.__img_recording)
        self.__icon_canvas.pack()

        self.__icon.update()

    def icon_display_watching(self):
        # self.__icon_label.configure(image=self.__img_watching
        # self.__icon_label.pack()
        self.__icon_canvas.itemconfig(self.__canvas_img, image=self.__img_watching)
        self.__icon_canvas.pack()
        self.__icon.update()

    # =========================================================================================== #
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
    im = Image.open("images/record.jpg")
    print(im.mode)
    gui = GUI()
    gui.open_icon()
    import time

    time.sleep(5)
    gui.icon_display_watching()
    time.sleep(5)
