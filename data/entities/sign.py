import pygame
from pygame.locals import *


class Sign_Manager:
    def __init__(self, main):
        self.m = main
        self.font = pygame.font.Font('data/ASSETS/pixel_font.ttf',9)
        self.signs = []
        self.regions = []

    def update(self, display):
        for r in self.regions:
            if self.m.main.p.player_rect.colliderect(r[0]):
                for sign in self.signs:
                    if sign[0] == r[1]:
                        if sign[4] >= 2:
                            sign[4] -= 2
                        else:
                             sign[4] = 0
                        text = self.font.render(sign[1],True,(0,0,0))
                        display.blit(text, (sign[2].x+16/2-(text.get_width()/2)-self.m.main.scroll[0],sign[2].y-25+sign[4]-self.m.main.scroll[1]))


        for s in self.signs:
            display.blit(self.m.main_tilemap[s[3][0],s[3][1]], (s[2].x-self.m.main.scroll[0], s[2].y-self.m.main.scroll[1]))
            # pygame.draw.rect(display, (100,50,230), pygame.Rect(s[2].x-self.m.main.scroll[0], s[2].y-self.m.main.scroll[1], s[2].w, s[2].h))


    def add_sign(self, sign):
        srcTile = sign['__tile']['srcRect']

        for field in sign['fieldInstances']:
            if field['__identifier'] == 'Message':
                message = field['__value']
            if field['__identifier'] == 'Name':
                name = field['__value']

        rect = pygame.Rect(sign['px'], [sign['width'], sign['height']])

        self.signs.append([name,message,rect,srcTile,30])



    def add_region(self, region):
        for field in region['fieldInstances']:
            if field['__identifier'] == 'TriggerSign':
                triggerSign = field['__value']

        rect = pygame.Rect(region['px'], [region['width'], region['height']])

        self.regions.append([rect, triggerSign])