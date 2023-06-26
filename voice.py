import pyttsx3,os
import speech_recognition as sr
# imgModeList = []
engine = pyttsx3.init()
from gtts import gTTS
# # import os
import playsound

# # wait for the sound to finish playing?
# blocking = True

# playsound.playsound("audio.mp3", block=blocking)
# cwd = os.getcwd()  # Get the current working directory (c  



# import pyttsx3,os
# import speech_recognition as sr
# # # imgModeList = []
# # engine = pyttsx3.init()
# from gtts import gTTS
# # import os
# import playsound

# # wait for the sound to finish playing?
# blocking = True

# playsound.playsound("audio.mp3", block=blocking)
# cwd = os.getcwd()  # Get the current working directory (cwd)
# files = os.listdir(cwd)  # Get all the files in that directory
# print("Files in %r: %s" % (cwd, files))
def speak(a):
    tts = gTTS(text=a, lang='en')
    tts.save("audio.mp3")
    blocking = True

    playsound.playsound("audio.mp3", block=blocking)
# # speak("Hello, how are you")


# import pyttsx3
# import speech_recognition as sr


# engine = pyttsx3.init()
# def speak(audio):
#     audio = str(audio)
#     engine.say(audio)
#     engine.runAndWait()
    
# speak("who are you")