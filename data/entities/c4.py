import pygame, math, random
from data.entities.bullet import Bullet

class C4:
    def __init__(self, main, data):
        self.m = main
        self.data = data

        srcx = data['__tile']['srcRect'][0]
        srcy = data['__tile']['srcRect'][1]
        self.img = self.m.main_tilemap[(srcx, srcy)]

        self.rect = pygame.Rect(data['px'], [16,16])
        self.m.shootable_entities.append(self)

    def update(self, display):
        display.blit(self.img, [self.rect.x-self.m.main.scroll[0], self.rect.y-self.m.main.scroll[1]])


    def hit(self, projectile):
        projectile.kill()
        self.m.main.explodeSound.play()
        for i in range(10):
            radians = math.radians(random.randint(0,359))
            self.m.entities.append(Bullet(self.m, self.data['px'], [math.cos(radians),math.sin(radians)], -math.degrees(radians)-90 ))

        self.m.entities.pop(self.m.entities.index(self))
        self.m.shootable_entities.remove(self)



