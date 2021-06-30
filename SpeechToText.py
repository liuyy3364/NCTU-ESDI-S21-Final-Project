# from threading import Semaphore
# from typing import Union
import speech_recognition as sr

class STT:
    def __init__(self) -> None:
        self.r=sr.Recognizer()
        self.recording = False
    
    def record(self, calibarate_duration=1, timeout=5, logger=None, msg=""):
    # def record(self, calibarate_sem: Union[Semaphore, None] = None, calibarate_duration=2, timeout=5):
        with sr.Microphone() as source:
            print("Please wait. Calibrating microphone...") 
            if logger is not None:
                logger(msg+"麥克風校正中...")
                
            #listen for 1 seconds and create the ambient noise energy level 
            self.r.adjust_for_ambient_noise(source, duration=calibarate_duration) 
            self.recroding=True

            print("Say something!")
            if logger is not None:
                logger(msg+"收音中...")
            audio = self.r.listen(source,timeout=timeout)
            self.recroding=False
        return audio
    
    def from_file(self, file: str):
        audio_file = sr.AudioFile(file)
        with audio_file as source:
            audio = self.r.record(source)
        return audio

    def recognize(self, audio, lang='zh-TW'):
        # recognize speech using Google Speech Recognition 
        text = ""
        err = (0,"")
        try:
            # print("Google Speech Recognition thinks you said:")
            text = self.r.recognize_google(audio, language="zh-TW")
        except sr.UnknownValueError:
            err = (1,"Google Speech Recognition could not understand audio")
            pass
        except sr.RequestError as e:
            err = (2,"No response from Google Speech Recognition service: {0}".format(e))
            pass
        return err, text


