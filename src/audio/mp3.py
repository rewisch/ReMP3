import pygame
from pydub import AudioSegment
import os


class MP3():
    def __init__(self):
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        self.current_song = None
        self.is_paused = False
        self.songs = dict()

    def play(self, title, blob):
        if self.is_paused and title == self.current_song:
            pygame.mixer.unpause()
            self.is_paused == False
        else:
            if title not in self.songs:
                soundObj = pygame.mixer.Sound(blob)
                self.songs[title] = soundObj
            else:
                soundObj = self.songs[title]

            self.current_song = title
            pygame.mixer.Channel(0).play(soundObj)
            print(pygame.mixer.get_busy())


    def stop(self):
        self.get_playing_soundObj().stop()
        self.is_paused = False

    def pause(self):
        pygame.mixer.pause()
        self.is_paused = True

    def unpause(self):
        pygame.mixer.unpause()

    def get_playing_soundObj(self):
        return self.songs[self.current_song]

    def mp3_to_wav(self, file_name : str):
        name, extension = file_name.split('.')
        if not extension == 'mp3':
            return None
        else:
            dst = "converted.wav"
            sound = AudioSegment.from_mp3(file_name)
            sound.export(dst, format="wav")
            return dst
