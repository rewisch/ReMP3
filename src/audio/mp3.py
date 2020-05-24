import pygame

class MP3():

    def __init__(self):
        self.currentSong = ''
        self.is_paused = False
        pygame.mixer.init()

    def load(self, file_name):
        self.soundObj = pygame.mixer.Sound(file_name)

    def play(self, file_name):
        if self.currentSong == file_name:
            if self.is_paused:
                self.pause()
            else:
                self.soundObj.play()
        else:
            self.currentSong = file_name
            self.load(file_name)
            self.soundObj.play()

    def stop(self):
        self.soundObj.stop()

    def pause(self):
        if self.is_paused:
            pygame.mixer.unpause()
            self.is_paused = False
        else:
            pygame.mixer.pause()
            self.is_paused = True
