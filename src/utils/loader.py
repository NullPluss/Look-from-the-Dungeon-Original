import pygame
import os

_image_cache = {}
_sound_cache = {}

def load_image(path):
    if path not in _image_cache:
        _image_cache[path] = pygame.image.load(path).convert_alpha()
    return _image_cache[path]

def load_sound(path):
    if path not in _sound_cache:
        _sound_cache[path] = pygame.mixer.Sound(path)
    return _sound_cache[path]