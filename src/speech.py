from gtts import gTTS
from playsound import playsound
  
mytext = 'Welcome!'
language = 'en'

# generate speech from text and save to speech.mp3
gTTS(text=mytext, lang=language, slow=False).save('speech.mp3')

# play the text
playsound('speech.mp3')