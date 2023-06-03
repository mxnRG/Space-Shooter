# Muhammad Mamoon 261938489 

# Importing modules

import pygame
import time
import random
import sys
import utili
import os
from pygame import mixer

# Loading music and setting up display

mixer.init()
pygame.init()
width = 600
height = 800
wind = pygame.display.set_mode((width,height))
pygame.display.set_caption("Space Shooter")



# Loading Images & sounds
p = 'pics'
background = pygame.transform.scale(pygame.image.load(os.path.join(p,"background.png")), (width,height))
player = pygame.image.load(os.path.join(p,"player.png"))
met1 = pygame.image.load(os.path.join(p,"met1.png"))
met2 = pygame.image.load(os.path.join(p,"met2.png"))
met3 = pygame.image.load(os.path.join(p,"met3.png"))
met4 = pygame.image.load(os.path.join(p,"met4.png"))
enemyimg = pygame.image.load(os.path.join(p,"enemy.png"))
laserimg = pygame.image.load(os.path.join(p,"laser.png"))
elaser = pygame.image.load(os.path.join(p, "elaser.png"))
icon = pygame.image.load(os.path.join(p,"logo.png"))
heart = pygame.image.load(os.path.join(p, "heart.png"))

s = 'sounds'
lasersnd = pygame.mixer.Sound(os.path.join(s, 'plaser.wav'))
elasersnd = pygame.mixer.Sound(os.path.join(s, 'elaser.wav'))
losesnd = pygame.mixer.Sound(os.path.join(s, 'lose.wav'))
destroysnd = pygame.mixer.Sound(os.path.join(s, 'destroy.wav'))

f = 'font'
font = os.path.join(f, 'font.ttf')

pygame.mixer.music.load(os.path.join(s, 'gameMusic.wav'))
pygame.mixer.music.play()

pygame.display.set_icon(icon)

# MAIN

def main():
    
    FPS = 60
    clock = pygame.time.Clock()
    

    play = utili.Player(250,700, player, laserimg, lasersnd)
    enmy = utili.Enemy(random.randint(50,550), enemyimg, elaser, elasersnd)
    main_font = pygame.font.Font(font, 20)
    pill = utili.Heart(random.randint(0,600), random.randint(-300,0), heart)

    enemies = []
    lasers = []
    enemies_ships = []
    elasers = []
    pills = []

    bg_y = 0
    bg_y2 = -height

    up_pressed = False
    down_pressed = False
    left_pressed = False
    right_pressed = False

    timer = pygame.time.get_ticks()
    timer2 = 30 * 1000
    
    score = utili.Score()
    score.load_highscore()
    highscore = score.get_highscore()

    score_increment = 500
    last_score = 0

    # Functions to handle display update

    def redraw(player, lasers):
        wind.blit(background, (0, bg_y))
        wind.blit(background, (0, bg_y2))
        lve = "*"
        life = main_font.render(f"Lives: {lve * player.lives}", 1, (255, 255, 255))
        score_label = main_font.render(f"Score: {score.get_score()}", 1, (255, 255, 255))
        pause_label = main_font.render(f"[P] - Pause", 1, (255,255,255))

        if lost:
            wind.fill((0, 0, 0))
            wind.blit(background, (0, 0))
            lost_label = main_font.render(f"YOU LOST! | GAME OVER | SCORE: {score.get_score()}", 1, (255, 255, 255))
            wind.blit(lost_label, (width / 2 - lost_label.get_width() / 2, 400))
            r = False

        player.draw(wind)

        for pil in pills:
            pil.draw(wind)

        for enemy in enemies_ships:
            wind.blit(enemy.img, (enemy.x, enemy.y))

        for laser in lasers:
            laser.draw(wind)

        for elaser in elasers:
            elaser.draw(wind)

        for enm in enemies:
            enm.draw(wind)
        wind.blit(life, (10, 10))
        wind.blit(score_label, (width - score_label.get_width() - 10, 10))
        wind.blit(pause_label, (10,30))
        pygame.display.update()

    def pausegame():
        paused = True
        pause_label = main_font.render("PAUSED", 1, (255, 255, 255))
        wind.blit(pause_label, (width / 2 - pause_label.get_width() / 2, height / 2 - pause_label.get_height() / 2))
        pygame.display.update()

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = False
    
    # Main Menu loop

    while True:
        r = True
        lost = False
        lostcount = 0

        utili.main_menu(wind, font, background, width, height, highscore,r,lost)


        # Main Game loop

        while r:
            clock.tick(FPS)

            current_time = pygame.time.get_ticks()
            if current_time - timer >= timer2:
                if play.lives < 5 and len(pills) < 1:
                    pil = utili.Heart(random.randint(50,550), random.randint(-300,-100), heart)
                    pills.append(pil)
                timer = current_time

            if play.lives == 0:
                lost = True            

            if lost:
                pygame.mixer.music.stop()
                if lostcount >= FPS * 5:
                    r = False
                    pygame.mixer.music.play()
                    main()
                else:
                    if lostcount <= 1:
                        pygame.mixer.Sound.play(losesnd)
                    lostcount += 1
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                r = False

            if len(enemies) < 10:    
                for i in range(1):
                    ast = utili.Asteroid(0,0)
                    ast.createobj(met1, met2, met3, met4)
                    enemies.append(ast)
                

            for i in enemies:
                i.move(1)
                if i.y > 800:
                    enemies.remove(i)

            for i in enemies:
                i.move(1)
                if i.y > 800:
                    enemies.remove(i)
            
            for pil in pills:
                pil.move()
                if pil.collision(play):
                    play.lives += 1
                    pills.remove(pil)
                if pil.y > 800:
                    pills.remove(pil)


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
                    elif event.key == pygame.K_SPACE:
                        play.shoot_laser(lasers)
                    elif event.key == pygame.K_p:
                        pausegame()

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        up_pressed = False
                    elif event.key == pygame.K_s:
                        down_pressed = False
                    elif event.key == pygame.K_a:
                        left_pressed = False
                    elif event.key == pygame.K_d:
                        right_pressed = False

            if up_pressed and play.y > 0:
                play.y -= 3
            if down_pressed and play.y < 714:
                play.y += 3
            if left_pressed and play.x > 0:
                play.x -= 3
            if right_pressed and play.x < 514:
                play.x += 3

            if play.y > height:
                play.y = 700
            
            play.cooldown_laser()

            if score.get_score() - last_score >= score_increment:
                enmy = utili.Enemy(random.randint(50,550), enemyimg, elaser, elasersnd)
                if len(enemies_ships) <= 0:
                    enemies_ships.append(enmy)
                last_score = score.get_score()

            for laser in lasers[:]:
                laser.move()
                if laser.y < 0:
                    lasers.remove(laser)
                else:
                    for enemy in enemies:
                        if laser.collision(enemy):
                            pygame.mixer.Sound.play(destroysnd)
                            enemies.remove(enemy)
                            lasers.remove(laser)
                            score.increase_score(30)
                            break
                    for enm in enemies_ships:
                        if laser.collision(enm):
                            pygame.mixer.Sound.play(destroysnd)
                            enemies_ships.remove(enm)
                            lasers.remove(laser)
                            score.increase_score(50)
            for elasert in elasers[:]:
                elasert.emove()
                if elasert.y > 800 or elasert.y < 0:
                    elasers.remove(elasert)
                else:
                    if elasert.collision(play):
                        play.lives -= 1
                        elasers.remove(elasert)
            
            for enm in enemies_ships:
                enm.update(play, elasers)

            utili.check_collision(play, enemies, destroysnd)
            
            redraw(play, lasers)
        score.save_score()
        score.reset_score()
main()