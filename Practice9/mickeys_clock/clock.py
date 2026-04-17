import pygame
import datetime

def get_time_angles():
    now = datetime.datetime.now()
    
    minutes = now.minute
    seconds = now.second

    minute_angle = minutes * 6
    second_angle = seconds * 6

    return minute_angle, second_angle