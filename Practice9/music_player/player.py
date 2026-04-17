import pygame
import os

BASE_DIR = os.path.dirname(__file__)

playlist = [
    os.path.join(BASE_DIR, "music", "track1.wav"),
    os.path.join(BASE_DIR, "music", "track2.wav")
]

current = 0

def play():
    pygame.mixer.music.load(playlist[current])
    pygame.mixer.music.play()

def stop():
    pygame.mixer.music.stop()

def next_track():
    global current
    current = (current + 1) % len(playlist)
    play()

def prev_track():
    global current
    current = (current - 1) % len(playlist)
    play()