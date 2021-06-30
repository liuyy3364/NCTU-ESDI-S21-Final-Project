from gtts import gTTS
from pydub import AudioSegment
import os
import paramiko

class TTS:
    def __init__(self) -> None:
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect("127.0.0.1", 22, "pi", "gukc4456")
    
    def say(self, sentence, lang='zh-tw', file_name="audio_o"):
        speech = gTTS(text=sentence, lang=lang)
        speech.save(file_name+'.mp3')
        sound = AudioSegment.from_mp3(file_name+'.mp3')
        sound.export(file_name+'.wav', format="wav")
        os.system('rm ' + file_name + '.mp3')
        os.system(f'aplay -D plughw:1 -t wav "/home/pi/ESDI_FP/{file_name}.wav"')
        # os.system(f'aplay -D default -t wav "/home/pi/ESDI_FP/{file_name}.wav"')
        # #DEBUG BEGIN
        # self.ssh.exec_command(f'aplay -t wav "/home/pi/ESDI_FP/{file_name}.wav"')
        # #DEBUG END
    
    # def __del__(self):
    #     self.ssh.close()
