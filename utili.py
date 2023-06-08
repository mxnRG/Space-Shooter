import pygame
import os
import random
import time 
import sys


# CLASSES

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
        window.blit(self.img, ((self.x,self.y)))
    def get_width(self):
        return self.img.get_width()
    def get_height(self):
        return self.img.get_height()

class Player(Ship):
    def __init__(self, x,y, img, laser_img, snd,lives = 3):
        super().__init__(x,y,lives)
        self.img = img
        self.laser_img = laser_img
        self.mask = pygame.mask.from_surface(self.img)
        self.lives = lives
        self.laser_cooldown = 0
        self.snd = snd
        self.coins = 0

    def shoot_laser(self, lasers):
        if self.laser_cooldown == 0:
            laser = Laser(self.x + self.get_width() // 2 - self.laser_img.get_width() // 2, self.y, self.laser_img)
            pygame.mixer.Sound.play(self.snd)
            lasers.append(laser)
            self.laser_cooldown = 30

    def cooldown_laser(self):
        if self.laser_cooldown > 0:
            self.laser_cooldown -= 1


class Asteroid(Ship):
    def __init__(self,x,y, health = 30):
        super().__init__(x,y,health)
        self.x = 0
        self.y = 0

    def createobj(self, img1, img2, img3, img4):
        r = random.randint(1,100)
        self.x = random.randint(40,540)
        self.y = random.randint(-1000,-100)
        if r > 0 and r <= 25:
            self.img = img1
        if r>25 and r <= 50:
            self.img = img2
        if r>50 and r <= 75:
            self.img = img3
        if r>75:
            self.img = img4
        self.mask = pygame.mask.from_surface(self.img)
    def move(self, y):
        self.y += y


class Enemy(Ship):
    def __init__(self, x, img, laser_img, snd, speed=4):
        super().__init__(x, -100)
        self.img = img
        self.laser_img = laser_img
        self.mask = pygame.mask.from_surface(self.img)
        self.speed = speed
        self.cd_count = 0
        self.vel = 4
        self.snd = snd

    def movee(self):
        self.y += self.speed

    def shoot_laser(self, lasers):
        if self.cd_count == 0:
            laser = Laser(self.x + self.get_width() // 2 - self.laser_img.get_width() // 2, self.y + self.get_height(), self.laser_img)
            pygame.mixer.Sound.play(self.snd)
            lasers.append(laser)
            self.cd_count = 30  

    def update(self, player, lasers):
        self.movee()

        if self.y >= 100:  
            self.shoot_laser(lasers)
            self.y = 100
            if self.x <= 0 or self.x >= 600:
                self.vel = -self.vel 
            self.x += self.vel

        self.cooldown()

        if self.collision(player):
            player.lives -= 1
        
    
    def collision(self, obj):
        return collide(self, obj)

    def cooldown(self):
        if self.cd_count > 0:
            self.cd_count -= 1



class Score:
    def __init__(self):
        self.score = 0
        self.highscore = 0
        self.file_path = "highscores.txt"

    def increase_score(self, points):
        self.score += points
        if self.score > self.highscore:
            self.highscore = self.score

    def reset_score(self):
        self.score = 0

    def save_score(self):
        with open(self.file_path, "a") as file:
            file.write(str(self.score) + "\n")

    def load_highscore(self):
        try:
            with open(self.file_path, "r") as file:
                scores = [int(score.strip()) for score in file.readlines()]
                if scores:
                    self.highscore = max(scores)
                else:
                    self.highscore = 0
        except FileNotFoundError:
            self.highscore = 0

    def get_highscore(self):
        return self.highscore

    def get_score(self):
        return self.score


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def move(self):
        self.y -= 5

    def emove(self):
        self.y += 5  

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def collision(self, obj):
        return collide(self, obj)


class Heart(Player):
    def __init__(self, x,y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self):
        self.y += 3

    def collision(self,obj):
        return collide(self,obj)
    

class Coin(Player):
    def __init__(self,x,y,img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self,window):
        window.blit(self.img, (self.x,self.y))
    
    def move(self):
        self.y += 3
    
    def collision(self,obj):
        return collide(self,obj)


# HELPING FUNCTIONS



def collide(obj1, obj2):
    offset_x = int(obj2.x - obj1.x)
    offset_y = int(obj2.y - obj1.y)
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None

def check_collision(player, enemies, snd):
    for asteroid in enemies:
        if player.mask.overlap(asteroid.mask, (asteroid.x - player.x, asteroid.y - player.y)):
            pygame.mixer.Sound.play(snd)
            player.lives -= 1 
            enemies.remove(asteroid)  

def main_menu(wind, font, background, width, height, high_score,r,lost):
    menu_font = pygame.font.Font(font, 40)
    title_label = menu_font.render("Astro Blast", 1, (255, 255, 255))
    start_label = menu_font.render("Press [Enter] to Start", 1, (255, 255, 255))
    high_score_label = menu_font.render("Press [H] to View High Score", 1, (255, 255, 255))
    exit_label = menu_font.render("Press [E] to exit", 1, (255,255,255))
    menu_running = True
    while menu_running:
        wind.blit(background, (0, 0))
        wind.blit(title_label, (width/2 - title_label.get_width()/2, 300))
        wind.blit(start_label, (width/2 - start_label.get_width()/2, 400))
        wind.blit(high_score_label, (width/2 - high_score_label.get_width()/2, 450))
        wind.blit(exit_label, (width/2 - exit_label.get_width()/2, 500))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    menu_running = False
                    r = True
                    lost = False
                elif event.key == pygame.K_h:
                    high_score_text = menu_font.render(f"High Score: {high_score}", 1, (255, 255, 255))
                    wind.blit(high_score_text, (width/2 - high_score_text.get_width()/2, 550))
                    pygame.display.update()
                    pygame.time.delay(3000) 
                    
                elif event.key == pygame.K_e:
                    sys.exit()