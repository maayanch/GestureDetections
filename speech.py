import speech_recognition as sr
from gtts import gTTS
import playsound

PAUSE = 4
PLAY_PREV = 3
PLAY_NEXT = 2
ASK_AGAIN = 1
ASK_WHAT = 0

""" 
working with python3.8 or python3.7, in order to install all the needed packages, do the following steps: 
- pip install SpeechRecognition
- pip install pipwin
- pipwin install pyaudio
- pip install gTTS
- pip install playsound

"""


class sounds(object):
    def __init__(self, create=True):
        self.ask_what = None
        self.play_next = None

        self.play_prev = None
        self.stop_music = None

        self.recorder = sr.Recognizer()
        self.act_dict = dict()  # each pair in the dict represent action and text
        self.update_action_dict()
        if create:
            self.create_sounds()

    def create_sounds(self):
        """
        Create basic sentences in mp3 files, the app should use that in order to communicate with the user.
        """

        self.ask_what = gTTS(text=self.act_dict[ASK_WHAT], lang='en', slow=False)
        self.ask_what.save(f"{ASK_WHAT}.mp3")

        self.ask_again = gTTS(text=self.act_dict[ASK_AGAIN], lang='en', slow=False)
        self.ask_again.save(f"{ASK_AGAIN}.mp3")

        self.play_next = gTTS(text=self.act_dict[PLAY_NEXT], lang='en', slow=False)
        self.play_next.save(f"{PLAY_NEXT}.mp3")

        self.play_prev = gTTS(text=self.act_dict[PLAY_PREV], lang='en', slow=False)
        self.play_prev.save(f"{PLAY_PREV}.mp3")

        self.stop_music = gTTS(text=self.act_dict[PAUSE], lang='en', slow=False)
        self.stop_music.save(f"{PAUSE}.mp3")

    def update_action_dict(self):
        self.act_dict[ASK_WHAT] = "What would you like to do?"
        self.act_dict.update({ASK_AGAIN: "Sorry, I didn't understand that, can you repeat yourself?"})
        self.act_dict.update({PLAY_NEXT: "Playing next song"})
        self.act_dict.update({PLAY_PREV: "Playing previous song"})
        self.act_dict.update({PAUSE: "Stopping music"})

    def ask_and_analyze(self):
        """ In this mode the app will ask the user "what would tou like to do, analyze his answer and
        return action and text represent the ans
        """
        playsound.playsound(f'{ASK_WHAT}.mp3', True)
        print("asking 'what would you like to do'")

        while True:
            with sr.Microphone() as source:
                audio_request = self.recorder.listen(source)
            try:
                text_request = self.recorder.recognize_google(audio_request)
                print(text_request)
                action = self.get_action(text_request)
                if action:
                    break
            except:
                print("The app didn't understand, asking again")
                playsound.playsound(f'{ASK_AGAIN}.mp3', True)

        print('starting analyze text')
        playsound.playsound(f'{action}.mp3', True)
        return action, self.act_dict[action]

    def get_action(self, text_request):
        if "next" in text_request:
            print('action was play next')
            return PLAY_NEXT
        elif "previous" in text_request:
            print('action was play previous')
            return PLAY_PREV
        elif "pause" in text_request or "mute" in text_request:
            print('action was pause')
            return PAUSE
        else:
            print('didnt understand your request')
            return None


if __name__ == '__main__':
    sound = sounds(create=False)
    action, text = sound.ask_and_analyze()
    print(f'the action is {action}, represented with "{text}"')
