from gtts import gTTS
from playsound import playsound
  

def play(text, lng='en'):
    # generate speech from text and save to speech.mp3
    gTTS(text=text, lang=lng, slow=False).save('speech.mp3')
    # play the text
    playsound('speech.mp3')