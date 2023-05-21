import pygame
import time
import random
from classes import Ship

pygame.init()
width = 600
height = 800
wind = pygame.display.set_mode((width,height))
pygame.display.set_caption("Space Shooter")

# Loading Images
background = pygame.transform.scale(pygame.image.load("background.png"), (width,height))
player = pygame.image.load("player.png")
met1 = pygame.image.load("met1.png")
met2 = pygame.image.load("met2.png")
met3 = pygame.image.load("met3.png")
met4 = pygame.image.load("met4.png")
shield = pygame.image.load("shield.png")
laser = pygame.image.load("laser.png")
gun = pygame.image.load("gun.png")
barrier = pygame.image.load("barrier.png")
icon = pygame.image.load("logo.png")

pygame.display.set_icon(icon)

#wind.blit(background, (0,0))
#wind.blit(player, (250,700))

def main():
    
    FPS = 60
    clock = pygame.time.Clock()
    
    r = True
    lives = 3
    
    sh = Ship(250,700)
    main_font = pygame.font.SysFont("centurygothic", 20)

    bg_y = 0
    bg_y2 = -height

    up_pressed = False
    down_pressed = False
    left_pressed = False
    right_pressed = False

    while r:
        clock.tick(FPS)
        
        def redraw():
            wind.blit(background, (0,bg_y))
            wind.blit(background, (0, bg_y2))
            lve = "*"
            life = main_font.render(f"Lives: {lve*lives}", 1 ,(255,255,255))
            wind.blit(life, (10,10))
            wind.blit(player, (250,700))

            sh.draw(wind)

            pygame.display.update()

        redraw()
        bg_y += 1
        bg_y2 += 1
        if bg_y > height:
            bg_y = -height
        
        if bg_y2 > height:
            bg_y2 = -height

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                r = False
            elif event.type==pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    up_pressed = True
                elif event.key == pygame.K_s:
                    down_pressed = True
                elif event.key == pygame.K_a:
                    left_pressed = True
                elif event.key == pygame.K_d:
                    right_pressed = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    up_pressed = False
                elif event.key == pygame.K_s:
                    down_pressed = False
                elif event.key == pygame.K_a:
                    left_pressed = False
                elif event.key == pygame.K_d:
                    right_pressed = False
        if up_pressed:
            sh.y -= 3
        if down_pressed:
            sh.y += 3
        if left_pressed:
            sh.x -= 3
        if right_pressed:
            sh.x += 3
        # MAKE SURE TO MAKE IT SO THE RECT DOES NOT MOVE OUT OF THE SCREEN DIMENSIONS


        if sh.y > height:
            sh.y = 700

main()