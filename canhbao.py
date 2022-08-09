

from pygame import mixer  # Load the popular external library
import speech_recognition as sr
import playsound
import os
from datetime import datetime, date
from gtts import gTTS
import glob

r = sr.Recognizer()

# AI hiểu
def minds(text):
    you = text
    if you == "":
        mind = " "
    elif "thời tiết" in you:
        mind = "bạn có thể nhìn qua cửa sổ"
    elif "bật nhạc" in you or "mở nhạc" in you: # bật nhạc
        mind ="tôi đang phát nhạc"

    elif "qua bài" in you:# điều khiển nhạc
        try:
            mixer.music.stop()
            mind = "tôi sẽ qua bài ngay"
        except:
            mind = "bạn chưa bật nhạc"
    elif "tắt nhạc" in you or"dừng nhạc" in you or"stop music" in you:
        try:
            mixer.music.stop()
            mind = "đã dừng nhạc"
        except:
            mind = "bạn chưa bật nhạc"

    elif "bye" in you:
        mind = "bye"
    elif "hôm nay là ngày" in you:
        today = date.today()
        mind = "hôm nay là ngày" + today.strftime("%Y/%m/%d")
    elif "mấy giờ" in you:
        now = datetime.now()
        mind = "bây giờ là" + now.strftime("%H:%M:%S")
    elif "buồn ngủ" in you:
        mind = "bạn có muốn bật nhạc"
    else:
        mind = "tôi không hiểu tôi sẽ học nhiều hơn để hiểu được bạn"
    return mind
# phat nhac
def playsong(path):
    mixer.init()
    mixer.music.load(path)
    mixer.music.play()
    print("alarm " + path)

def getlistMusic(path):
    music = []
    for song in glob.glob(path):
        i = 0
        music.insert(i, song)
    return music
# AI nói
def speak(mind):
    tts = gTTS(text=mind, lang='vi')
    print("AI:", mind)
    filename = 'voiceVI.mp3'
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)
# AI nghe
def listenvi():
    with sr.Microphone() as mic:
        print("recognizing VI......")
        audio_data = r.record(mic, duration=5)
        try:
            text = r.recognize_google(audio_data, language='vi')
            print("you:", text)
            return text
        except:
            text = ""
            print("you:", text)
            return text
def listenen():
    with sr.Microphone() as mic:
        print("recognizing EN......")
        audio_data = r.record(mic, duration=5)
        try:
            text = r.recognize_google(audio_data, language='en')
            print("you:", text)
            return text
        except:
            text = ""
            print("you:", text)
            return text
# kết hợp  thục hieenbj lệnh khi nói skynet
i = 0
MusicOn= False
while True:
        try:
            a = mixer.music.get_busy()
        except:
            a = False
        if a ==True:
            print("music-ON")
            pass # nhac đang bật  thi skipp
        else:
            if MusicOn == True:
                path = "D:\\music\\*.mp3"
                music = getlistMusic(path)
                playsong(music[i])
                i += 1
                a = len(music)
                if a < i + 1:
                    i = 0
        if a == False:
            print("music-OFF")


        text1= listenvi().lower()
        if "buồn ngủ" in text1:
            mind1 = minds(text1)
            while True:
                speak(mind1)
                print("có/không")
                if mind1 == "bạn có muốn bật nhạc":
                    you = listenvi().lower()
                    if "có" in you:
                        MusicOn = True
                        break
                    else:
                        break
        if text1 == "lan":
            while True:
                speak("tôi có thể giúp gì cho bạn")
                textvi = listenvi().lower()
                if textvi == "":
                    break
                else:
                    mind = minds(textvi)
                    speak(mind)
                    if mind == "tôi đang phát nhạc":
                        MusicOn = True
                        break
                    if mind == "đã dừng nhạc":
                        MusicOn = False
                        break
                    if mind == "tôi sẽ qua bài ngay":
                        path = "D:\\music\\*.mp3"
                        music = getlistMusic(path)
                        playsong(music[i])
                        break
                    if mind == "bạn có muốn bật nhạc":
                        you = listenvi().lower()
                        if "có" in you:
                            MusicOn = True
                            break
                        else:
                            break
                    break
        else:
            continue



