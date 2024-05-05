import pygame, math
from pygame.locals import *
import data.engine as e


class Bullet:
    def __init__(self, main, pos, movement, rotate_amt, exceptions=[]):
        self.m = main
        self.exceptions = exceptions

        self.bulletImg = pygame.image.load('data/ASSETS/bullet.png').convert_alpha()
        self.bulletImg = pygame.transform.scale(self.bulletImg, (8,12))
        self.rotate_amt = rotate_amt

        self.speed = 10
        self.movement = [axis*self.speed for axis in movement]
        self.rect = pygame.Rect(pos, [self.bulletImg.get_width(), self.bulletImg.get_height()])

    def update(self, display):
        self.rect.x += self.movement[0]
        self.rect.y += self.movement[1]

        hit_blocks = e.collision_test(self.rect,self.m.tile_rects.copy())
        hit_entities = self.ent_collision_test(self.rect, self.m.shootable_entities)
        if hit_blocks != []:
            self.kill()
        for entity in hit_entities:
            exception_rects = [ent.rect for ent in self.exceptions]
            try:
                rect = entity.rect
            except:
                rect = entity.player_rect
            if rect not in exception_rects:
                entity.hit(self)
                try:
                    self.kill()
                except:
                    pass


        display.blit(e.circle_surf(20, (35, 35, 0)), [self.rect.x-(20*2-self.bulletImg.get_width())/2-self.m.main.scroll[0], self.rect.y-(20*2-self.bulletImg.get_width())/2-self.m.main.scroll[1]], special_flags=BLEND_RGB_ADD)
        e.perfect_outline(pygame.transform.rotate(self.bulletImg, self.rotate_amt), display, [self.rect.x-self.m.main.scroll[0], self.rect.y-self.m.main.scroll[1]], color=(255,255,255))
        display.blit(pygame.transform.rotate(self.bulletImg, self.rotate_amt), [self.rect.x-self.m.main.scroll[0], self.rect.y-self.m.main.scroll[1]])


    def kill(self):
        try:
            self.m.entities.remove(self)
        except:
            pass

    def ent_collision_test(self, rect, ents):
        hit_list = []
        for ent in ents:
            try:
                if rect.colliderect(ent.rect):
                    hit_list.append(ent)
            except: #excpetion for player since im too lazy to change all the player_rect references
                if rect.colliderect(ent.player_rect):
                        hit_list.append(ent)
        return hit_list

