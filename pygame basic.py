import pygame
pygame.init()

width = 600
height = 600
background = pygame.image.load("background.png")
bg_x = 0
bg_y = 0
bg_speed = 5
ch = "y"
wind = pygame.display.set_mode((width,height))
pygame.display.set_caption("Space Shooter")
wind.blit(background, (bg_x,bg_y))

clock = pygame.time.Clock()
while ch == "y":
    pass