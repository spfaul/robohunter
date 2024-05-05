import pygame, time
from pygame.locals import *

import data.engine as e
from data.player import Player
from data.levels.world import Level as World
from data.particles import Particles as ParticleManager

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()

pygame.display.set_caption('RoboHunter')

class Editor:
    def __init__(self, **kwargs):
        self.running = True
        self.WINDOW_SIZE = [800,800]
        self.MAIN_SCREEN = pygame.display.set_mode(self.WINDOW_SIZE)
        self.display = pygame.Surface((300,300))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('data/ASSETS/pixel_font.ttf', 10)

        self.TILE_SIZE = 16
        self.true_scroll = [0,0]
        self.scroll_lock = None
        self.events = []
        self.input = 'ENABLED'

        self.pm = ParticleManager()

        self.frame = 0
        self.cutscene_block_height = 100

        self.anim_frames = {}
        self.anim_data = {}
        self.anim_data['player_charge'] = e.load_animation('data/animations/player_charge',[7,7,7,7], self.anim_frames)
        self.anim_data['player_idle'] = e.load_animation('data/animations/player_idle',[7], self.anim_frames)
        self.anim_data['boss_charge'] = e.load_animation('data/animations/boss_charge',[7,7,7,7], self.anim_frames)
        self.anim_data['boss_idle'] = e.load_animation('data/animations/boss_idle',[7], self.anim_frames)
        self.anim_data['cyborg_left'] = e.load_animation('data/animations/cyborg_left',[7], self.anim_frames)
        self.anim_data['cyborg_right'] = e.load_animation('data/animations/cyborg_right',[7], self.anim_frames)

        self.shootSounds = [pygame.mixer.Sound(path) for path in ['data/ASSETS/shoot.wav','data/ASSETS/shoot2.wav','data/ASSETS/shoot3.wav']]
        self.explodeSound = pygame.mixer.Sound('data/ASSETS/explode.wav')
        self.hitSound = pygame.mixer.Sound('data/ASSETS/hit.wav')
        self.roboShootSound = pygame.mixer.Sound('data/ASSETS/roboshoot.wav')
        theme = pygame.mixer.music.load('data/ASSETS/theme.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

        self.gunImg = pygame.image.load('data/ASSETS/gun.png').convert_alpha()
        self.cursorImg = pygame.image.load('data/ASSETS/cursor.png').convert_alpha()
        pygame.mouse.set_visible(False)

        ## test 
        self.p = Player(self)
        self.level = World(self)

        for key, value in kwargs.items():
            setattr(self, key, value)

    def preRun(self):
        startTime = time.time()
        while self.running:
            self.display.fill((0,0,0))
            self.events = pygame.event.get()


            text = ['High Tech Robots Have Come To Life And Are',
                    'Taking Over Earth. Gun Them Down With Your Jet!',
                    'Good Luck!',
                    '','','',
                    'Sincerely,',
                    'The Army']
            for i, t in enumerate(text):
                surf = self.font.render(t, True, (230,230,230))
                self.display.blit(surf, (10,(i+1)*20))
            surf = self.font.render(f'Deployment in {round(8-(time.time()-startTime),2)}s', True, (230,230,230))
            self.display.blit(surf, (180,270))


            for event in self.events:
                if event.type == QUIT:
                    pygame.quit()
                    quit()
            if time.time()-startTime > 8:
                self.running = False

            self.MAIN_SCREEN.blit(pygame.transform.scale(self.display, self.WINDOW_SIZE), (0,0))

            pygame.display.update()
            self.clock.tick(60)

    def run(self):
        while self.running:
            self.display.fill((161,42,199))
            self.events = pygame.event.get()

            self.mx, self.my = pygame.mouse.get_pos()
            self.mx /= self.WINDOW_SIZE[0]/300
            self.my /= self.WINDOW_SIZE[1]/300

            if self.scroll_lock != None:
                self.true_scroll[0] += (self.scroll_lock[0]-self.true_scroll[0]-150)/20
                self.true_scroll[1] += (self.scroll_lock[1]-self.true_scroll[1]-150)/20
            else:
                self.true_scroll[0] += (self.p.rect.x-self.true_scroll[0]-150)/20
                self.true_scroll[1] += (self.p.rect.y-self.true_scroll[1]-150)/20
            self.scroll = self.true_scroll.copy()
            self.scroll[0] = int(self.scroll[0])
            self.scroll[1] = int(self.scroll[1])

            self.level.update()
            self.p.update()
            # self.pm.update(self.display, self.scroll)

            self.display.blit(self.cursorImg, [self.mx, self.my])

            if self.input == 'ENABLED':
                keys = pygame.key.get_pressed()
                self.p.moving_up = False;self.p.moving_down = False;self.p.moving_left = False;self.p.moving_right = False
                if keys[K_w]:
                    self.p.moving_up = True
                if keys[K_s]:
                    self.p.moving_down = True
                if keys[K_a]:
                    self.p.moving_left = True
                if keys[K_d]:
                    self.p.moving_right = True


            for event in self.events:
                if event.type == QUIT:
                    self.running = False
                if event.type == KEYDOWN:
                    if event.key == K_F1:
                        self.level.currentLevel += 1
                        self.level.change_level(self.level.currentLevel)

            self.cutscene_block_height -= 3
            if int(self.cutscene_block_height) > 0:
                cutscene_block = pygame.Surface((self.display.get_width(), int(self.cutscene_block_height)))
                cutscene_block.fill((8, 5, 8))
                self.display.blit(cutscene_block, (0, 0))
                self.display.blit(cutscene_block, (0, self.display.get_height() - int(self.cutscene_block_height)))


            self.MAIN_SCREEN.blit(pygame.transform.scale(self.display, self.WINDOW_SIZE), (0,0))

            pygame.display.update()
            self.clock.tick(60)
            self.frame += 1


if __name__ == '__main__':
    edit = Editor()
    edit.preRun()
    edit.running = True
    edit.run()

    pygame.quit()
