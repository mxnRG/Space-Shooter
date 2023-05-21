    #CLASSES
import pygame
import os
import random
import time 
class Ship:
    def __init__(self, x, y, health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.img = None
        self.laser_img = None
        self.lasers = []
        self.cd_count = 0
    def draw(self, window):
        pygame.draw.rect(window, (0,0,0), (self.x,self.y, 93,84), 1)