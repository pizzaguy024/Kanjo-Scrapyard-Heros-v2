import pygame


class AudioManager:
    def __init__(self, resource_path_func):
        self.resource_path = resource_path_func
        self.music_volume = 0.45
        self.music_loaded = False

        try:
            pygame.mixer.init()
        except Exception:
            pass

    def play_music(self, music_path):
        try:
            pygame.mixer.music.load(self.resource_path(music_path))
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(-1)
            self.music_loaded = True
        except Exception as error:
            print(f"Music failed to load: {error}")

    def stop_music(self):
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass

    def set_volume(self, volume):
        self.music_volume = max(0.0, min(1.0, volume))
        try:
            pygame.mixer.music.set_volume(self.music_volume)
        except Exception:
            pass
