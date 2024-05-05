import pygame
import math, random
from time import time
from pygame.locals import *
import data.engine as e

class Player:
    def __init__(self, main):
        self.main = main

        self.rect = pygame.Rect(0,0,26,26)
        self.health = 100
        self.max_health = 100

        self.action = 'player_idle'
        self.frame = 0

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        self.friction = 0.8
        self.player_movement = [0,0]
        self.vertical_momentum = 0
        self.air_timer = 0

        self.hit_time = None

    def update(self):
        self.movement()
        self.animations()
        self.draw()


    def draw(self):
        rot = -math.degrees(math.atan2(self.main.my+self.main.cursorImg.get_height()/2 - (int(self.rect.centery) - self.main.scroll[1]), self.main.mx+self.main.cursorImg.get_width()/2 - (int(self.rect.centerx - self.main.scroll[0]))))-90
        rotated_img, rotated_rect = e.rotate_img(self.player_img, rot, [self.rect.centerx, self.rect.centery])

        if not self.hit_time:
            e.perfect_outline(rotated_img, self.main.display, [rotated_rect.x-self.main.scroll[0], rotated_rect.y-self.main.scroll[1]], color=(255,255,255))
        else:
            time_elapsed = time()-self.hit_time
            if time_elapsed > 1:
                self.hit_time = None
            else:
                e.perfect_outline(rotated_img, self.main.display, [rotated_rect.x-self.main.scroll[0], rotated_rect.y-self.main.scroll[1]], color=(255-(255*time_elapsed),0,0))
        self.main.display.blit(rotated_img, [rotated_rect.x-self.main.scroll[0], rotated_rect.y-self.main.scroll[1]])
        # pygame.draw.rect(self.main.display, (255,0,0), pygame.Rect(self.rect.x-self.main.scroll[0], self.rect.y-self.main.scroll[1], self.rect.w, self.rect.h))


    def movement(self):
        self.player_movement = [axis*self.friction if abs(axis)<16 else 14 for axis in self.player_movement]
        self.player_movement = [axis if abs(axis)>0.01 else 0 for axis in self.player_movement]

        if self.moving_right:
            self.player_movement[0] += 1
        if self.moving_left:
            self.player_movement[0] -= 1
        if self.moving_down:
            self.player_movement[1] += 1 
        if self.moving_up:
            self.player_movement[1] -= 1 

        self.rect,self.collisions = e.move(self.rect,self.player_movement,self.main.level.tile_rects)

    def animations(self):
        if self.moving_up or self.moving_down:
            self.action,self.frame = e.change_action(self.action,self.frame,'player_charge')
        if self.player_movement == [0,0]:
            self.action,self.frame = e.change_action(self.action,self.frame,'player_idle')


        self.frame += 1
        if self.frame >= len(self.main.anim_data[self.action]):
            self.frame = 0
        self.player_img_id = self.main.anim_data[self.action][self.frame]
        self.player_img = self.main.anim_frames[self.player_img_id]


    def stop_movement(self):
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False


    def hit(self, projectile):
        projectile.kill()
        self.main.hitSound.play()
        self.health -= 1
        if self.health <= 0:
            self.kill()
        self.hit_time = time()

    def kill(self):
        self.main.level.currentLevel = 1
        self.main.level.change_level(self.main.level.currentLevel)
        self.health = self.max_health