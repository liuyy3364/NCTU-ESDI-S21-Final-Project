from gtts import gTTS
from pydub import AudioSegment
import os

class TTS:
    
    def say(self, sentence, lang='zh-tw', file_name="audio_o",non_block = False):
        speech = gTTS(text=sentence, lang=lang)
        speech.save(file_name+'.mp3')
        sound = AudioSegment.from_mp3(file_name+'.mp3')
        sound.export(file_name+'.wav', format="wav")
        os.system('rm ' + file_name + '.mp3')
        if(non_block):
            os.system(f'aplay -D plughw:1 -t wav "/home/pi/ESDI_FP/{file_name}.wav" &')
        else:
            os.system(f'aplay -D plughw:1 -t wav "/home/pi/ESDI_FP/{file_name}.wav"')
        # os.system(f'aplay -D default -t wav "/home/pi/ESDI_FP/{file_name}.wav"')
        # #DEBUG BEGIN
        # self.ssh.exec_command(f'aplay -t wav "/home/pi/ESDI_FP/{file_name}.wav"')
        # #DEBUG END
    
    # def __del__(self):
    #     self.ssh.close()
