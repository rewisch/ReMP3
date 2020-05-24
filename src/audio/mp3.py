import pygame
from pydub import AudioSegment
import os


class MP3():
    def __init__(self):
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

    def play(self, blob):
        self.soundObj = pygame.mixer.Sound(blob)
        self.soundObj.play()

    def stop(self):
        self.soundObj.stop()

    def pause(self):
        pass

    def mp3_to_wav(self, file_name : str):
        name, extension = file_name.split('.')
        if not extension == 'mp3':
            return None
        else:
            dst = "converted.wav"
            sound = AudioSegment.from_mp3(file_name)
            sound.export(dst, format="wav")
            return dst
