import pygame
from pygame.locals import *


class Villager:
    def __init__(self, tileSize, main,data):
        self.tileSize = tileSize
        self.main = main

        self.rect = pygame.Rect(data['px'], (data['width'], data['height']))
        self.movement = [1,1]

        for field in data['fieldInstances']:
            if field['__identifier'] == 'Name':
                self.name = field['__value']
            if field['__identifier'] == 'Path':
                self.path = field['__value']

        self.target_point = (self.path[0],0)

    def update(self, display):
        ## changing points on path
        if int(self.rect.x/self.tileSize) == self.target_point[0]['cx'] and int(self.rect.y/self.tileSize) == self.target_point[0]['cy']:
            self.target_point = (self.path[self.target_point[1]+1],self.target_point[1]+1) if self.target_point[1]<len(self.path)-1 else (self.path[0],0)

        ## move towards point
        if not int(self.rect.x/self.tileSize) == self.target_point[0]['cx']:
            if self.target_point[0]['cx']*self.tileSize > self.rect.x:
                self.rect.x += self.movement[0]
            elif self.target_point[0]['cx']*self.tileSize < self.rect.x:
                self.rect.x -= self.movement[0]
        if not int(self.rect.y/self.tileSize) == self.target_point[0]['cy']:
            if self.target_point[0]['cy']*self.tileSize > self.rect.y:
                self.rect.y += self.movement[1]
            elif self.target_point[0]['cy']*self.tileSize < self.rect.y:
                self.rect.y -= self.movement[1] 

        pygame.draw.rect(display, (100,0,0), pygame.Rect(self.rect.x-self.main.main.scroll[0], self.rect.y-self.main.main.scroll[1], self.rect.w, self.rect.h))




