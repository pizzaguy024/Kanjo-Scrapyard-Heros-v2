import pygame


class AudioManager:
    def __init__(self, resource_path_func):
        self.resource_path = resource_path_func
        self.music_volume = 0.45
        self.sfx_volume = 0.65
        self.music_loaded = False
        self.sounds = {}

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

    def set_music_volume(self, volume):
        self.music_volume = max(0.0, min(1.0, volume))
        try:
            pygame.mixer.music.set_volume(self.music_volume)
        except Exception:
            pass

    def load_sound(self, name, sound_path):
        try:
            sound = pygame.mixer.Sound(self.resource_path(sound_path))
            sound.set_volume(self.sfx_volume)
            self.sounds[name] = sound
        except Exception as error:
            print(f"Sound failed to load: {sound_path} - {error}")

    def play_sound(self, name):
        try:
            sound = self.sounds.get(name)
            if sound:
                sound.play()
        except Exception:
            pass

    def set_sfx_volume(self, volume):
        self.sfx_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)
