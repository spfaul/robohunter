import pygame
from pygame.locals import *
import data.engine as e
import math, random

from data.entities.sign import Sign_Manager
from data.entities.dialogue import Dialogue_Manager
from data.entities.bullet import Bullet
from data.entities.c4 import C4
from data.entities.cyborg import Cyborg
from data.entities.boss import Boss


class Level:
    def __init__(self, main):
        self.main = main

        self.main_tilemap = e.load_tilemap('data/ASSETS/CyberPunk-Tiles.png', [16,16])
        self.file_to_tilemap = {'CyberPunk-Tiles.png':self.main_tilemap}

        self.collidable_tiles = [1]

        self.signM = Sign_Manager(self)
        self.dialogueM = Dialogue_Manager(self)
        self.managers = [self.signM,self.dialogueM]

        self.played_end = False

        self.currentLevel = 0
        self.change_level(self.currentLevel)
        self.levelNames = {0:'Tutorial', 1:'The Arena',
                        2:'Bullet Hell', 3:'Training Arc',
                        4:'The Boss Battle', 5:'The End'}

    def update(self):
        # print(math.atan2(self.main.my-self.main.p.rect.centery, self.main.mx-self.main.p.rect.centerx))

        ## blit tiles
        for layer in self.tiles:
            tilesheet = self.file_to_tilemap[layer[1].split('/')[-1]]
            for tile in layer[0]:
                x,y = tile['px']
                if abs(x-self.main.p.rect.x) < 20*16 and abs(y-self.main.p.rect.y) < 20*16:
                    srcx, srcy = tile['src']
                    self.main.display.blit(tilesheet[srcx,srcy], (tile['px'][0]-self.main.scroll[0], tile['px'][1]-self.main.scroll[1]))

        self.main.pm.update(self.main.display, self.main.scroll)

        for ent in self.entities:
            ent.update(self.main.display)
        for m in self.managers:
            m.update(self.main.display)

        ## player health bar
        healthText = self.main.font.render('Health', True, (0,255,0))
        e.perfect_outline(healthText, self.main.display, (5,8), (1,1,1))
        self.main.display.blit(healthText, (5,8))
        pygame.draw.rect(self.main.display, (0,0,0), pygame.Rect(5+40,5,self.main.p.max_health+4, 16))
        pygame.draw.rect(self.main.display, (255,0,0), pygame.Rect(7+40,7,self.main.p.health, 12))

        ## level name
        levelText = self.main.font.render(f'Level: {self.levelNames[self.currentLevel]}', True, (255,50,100))
        e.perfect_outline(levelText, self.main.display, (5,25), (1,1,1))
        self.main.display.blit(levelText, (5,25))

        if self.currentLevel == 0:
            text = self.main.font.render('WASD To Move, Left Click To Shoot', True, (255,50,100))
            e.perfect_outline(text, self.main.display, (109-self.main.scroll[0],473-self.main.scroll[1]), (1,1,1))
            self.main.display.blit(text, (109-self.main.scroll[0],473-self.main.scroll[1]))

        if self.currentLevel == 5:
            if not self.played_end:
                pygame.mixer.music.fadeout(1000)
                pygame.mixer.music.load('data/ASSETS/mario_lofi.mp3')
                pygame.mixer.music.play()
                self.played_end = True
            endText = self.main.font.render(f'Thanks For Playing!', True, (255,50,100))
            e.perfect_outline(endText, self.main.display, (211-self.main.scroll[0],118-self.main.scroll[1]), (1,1,1))
            self.main.display.blit(endText, (211-self.main.scroll[0],118-self.main.scroll[1]))

        if len(self.enemies) == 0 and self.currentLevel != 5:
            self.currentLevel += 1
            self.change_level(self.currentLevel)

        for event in self.main.events:
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    random.choice(self.main.shootSounds).play()
                    radians = math.atan2(self.main.my-int(self.main.p.rect.centery-self.main.scroll[1]), self.main.mx-int(self.main.p.rect.centerx-self.main.scroll[0]))
                    rotate_amt = -math.degrees(math.atan2(self.main.my-int(self.main.p.rect.centery-self.main.scroll[1]), self.main.mx-int(self.main.p.rect.centerx-self.main.scroll[0])))-90
                    # distance = int(math.hypot(self.main.mx-self.ball_pos[0], self.main.my-self.ball_pos[1]))
                    self.entities.append(Bullet(self, [self.main.p.rect.centerx-10, self.main.p.rect.centery],[math.cos(radians), math.sin(radians)], rotate_amt, exceptions=[self.main.p]))
                    self.entities.append(Bullet(self, [self.main.p.rect.centerx+10, self.main.p.rect.centery],[math.cos(radians), math.sin(radians)], rotate_amt, exceptions=[self.main.p]))
                    

    def change_level(self, levelNum):
        data = e.parse_json('data/level_data/WORLD.json',levelNum,self.collidable_tiles)
        self.TILE_SIZE = data[0]
        self.tiles = data[1]
        self.tile_rects = data[2]
        self.shootable_entities = [self.main.p]
        self.entities, self.enemies = self.create_entities(data[3])

        self.main.cutscene_block_height = 100


    def create_entities(self, entityData):
        entities = []
        enemies = []

        for e in entityData:
            TYPE = e['__identifier']
            # if TYPE == 'Signs':
            #     self.signM.add_sign(e)
            # if TYPE == 'SignRegion':
            #     self.signM.add_region(e)
            # if TYPE == 'Dialogue_Entity':
            #     self.dialogueM.add_actor(e)
            # if TYPE == 'DialogueRegion':
            #     self.dialogueM.add_region(e)
            if TYPE == 'Player_Spawn':
                self.main.p.rect.x = e['px'][0];self.main.p.rect.y = e['px'][1]
            elif TYPE == 'C4':
                entities.append(C4(self, e))
            elif TYPE == 'Cyborg_Enemy':
                c = Cyborg(self, e)
                entities.append(c); enemies.append(c)
            elif TYPE == 'Boss':
                boss = Boss(self, e)
                entities.append(boss); enemies.append(boss)

        return entities, enemies




