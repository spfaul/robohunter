import pygame
from pygame.locals import *
import textwrap


class Dialogue_Manager:
    def __init__(self, main):
        self.m = main

        self.font = pygame.font.Font('data/ASSETS/pixel_font.ttf',9)
        self.wrapper = textwrap.TextWrapper(width=50) 

        self.actors = []
        self.regions = []


    def update(self, display):

        for r in self.regions:
            if self.m.main.p.player_rect.colliderect(r[0]):
                for actor in self.actors:
                    if actor[0] == r[1]:
                        # start dialogue
                        if actor[4] == -1:
                            actor[4] = 0
                            self.m.main.scroll_lock = [(actor[2].x-self.m.main.p.player_rect.x)/2+self.m.main.p.player_rect.x,(actor[2].y-self.m.main.p.player_rect.y)/2+self.m.main.p.player_rect.y]
                            self.m.main.input = 'DISABLED'
                            self.m.main.p.stop_movement()
                        # end dialogue
                        if actor[4] == len(actor[1]):
                            actor[4] = -2
                            self.m.main.scroll_lock = None
                            self.m.main.input = 'ENABLED'

                        if actor[4] >= 0 and actor[4] < len(actor[1]):
                            if actor[1][actor[4]].startswith('e: '):
                                text_surf = self.font.render(actor[1][actor[4]][3:],True,(0,0,0))
                                display.blit(text_surf, (actor[2].x+16/2-(text_surf.get_width()/2)-self.m.main.scroll[0],actor[2].y-25-self.m.main.scroll[1]))
                            elif actor[1][actor[4]].startswith('p: '):
                                text_surf = self.font.render(actor[1][actor[4]][3:],True,(0,0,0))
                                display.blit(text_surf, (self.m.main.p.player_rect.x+16/2-(text_surf.get_width()/2)-self.m.main.scroll[0],self.m.main.p.player_rect.y-25-self.m.main.scroll[1]))

        for event in self.m.main.events:
            if event.type == KEYDOWN and event.key == K_SPACE:
                for actor in self.actors:
                    if actor[4] != -1 and actor[4] != -2:
                        actor[4] += 1

        for s in self.actors:
            display.blit(self.m.main_tilemap[s[3][0],s[3][1]], (s[2].x-self.m.main.scroll[0], s[2].y-self.m.main.scroll[1]))
            # pygame.draw.rect(display, (100,50,230), pygame.Rect(s[2].x-self.m.main.scroll[0], s[2].y-self.m.main.scroll[1], s[2].w, s[2].h))


    def add_actor(self, actor):
        srcTile = actor['__tile']['srcRect']

        for field in actor['fieldInstances']:
            if field['__identifier'] == 'Dialogue':
                dialogue = field['__value']
            if field['__identifier'] == 'Name':
                name = field['__value']

        rect = pygame.Rect(actor['px'], [actor['width'], actor['height']])
        currentDialogue = -1

        self.actors.append([name,dialogue,rect,srcTile,currentDialogue])



    def add_region(self, region):
        for field in region['fieldInstances']:
            if field['__identifier'] == 'TriggerEntity':
                triggerActor = field['__value']

        rect = pygame.Rect(region['px'], [region['width'], region['height']])

        self.regions.append([rect, triggerActor])