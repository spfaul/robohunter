import pygame, math, random
import data.engine as e
from time import time
from data.entities.bullet import Bullet


class Cyborg:
    def __init__(self, main, data):
        self.m = main
        self.data = data

        self.rect = pygame.Rect(data['px'][0], data['px'][1], data['width'], data['height'])
        self.health = 20

        for i in data['fieldInstances']:
            if i['__identifier'] == 'Difficulty':
                self.mode = i['__value']

        self.action = 'cyborg_left'
        self.frame = 0
        self.hit_time = None

        self.modeReference = {
                            'Easy': {'moveRange': [-1,1], 'shootCD': 60},
                            'Medium': {'moveRange': [-2,2], 'shootCD': 40},
                            'Hard': {'moveRange': [-3,3], 'shootCD': 20}
                            }

        self.move = [random.randint(self.modeReference[self.mode]['moveRange'][0],self.modeReference[self.mode]['moveRange'][1]), random.randint(self.modeReference[self.mode]['moveRange'][0],self.modeReference[self.mode]['moveRange'][1])]
        self.last_shoot = 0
        self.shoot_cooldown = 30

        self.m.shootable_entities.append(self)

    def update(self, display):
        self.movement()
        self.animations()

        # cyborg
        if not self.hit_time:
            e.perfect_outline(self.img, display, [self.rect.x-self.m.main.scroll[0], self.rect.y-self.m.main.scroll[1]], (200,0,0))
        else:
            time_elapsed = time() - self.hit_time
            if math.ceil(time_elapsed) > 1:
                self.hit_time = None
            else:
                e.perfect_outline(self.img, display, [self.rect.x-self.m.main.scroll[0], self.rect.y-self.m.main.scroll[1]], (int(255-255*time_elapsed),int(255-255*time_elapsed),0))
        display.blit(self.img, [self.rect.x-self.m.main.scroll[0], self.rect.y-self.m.main.scroll[1]])


        # gun
        rot = -math.degrees(math.atan2(self.m.main.p.rect.centery - int(self.rect.centery), self.m.main.p.rect.centerx - int(self.rect.centerx)))
        gun_offset = [0,5]
        if abs(int(rot)) > 90: # mirror image calculations
            self.action = 'cyborg_left'
            gun_offset[0] -= 5
            if rot > 0: #positive
                rot = 90-(rot-90)
            else: #negative
                rot = -90+(-90-rot)
            rotated_img, rotated_rect = e.rotate_img(self.m.main.gunImg, rot, [self.rect.centerx, self.rect.centery])
            rotated_img = pygame.transform.flip(rotated_img, True, False)
        else:
            rotated_img, rotated_rect = e.rotate_img(self.m.main.gunImg, rot, [self.rect.centerx, self.rect.centery])
            self.action = 'cyborg_right'
            gun_offset[0] += 5
 

        e.perfect_outline(rotated_img, display, [rotated_rect.centerx-rotated_img.get_width()/2-self.m.main.scroll[0]+gun_offset[0], rotated_rect.centery-rotated_img.get_height()/2-self.m.main.scroll[1]+gun_offset[1]], (255,50,50))
        display.blit(rotated_img, [rotated_rect.centerx-rotated_img.get_width()/2-self.m.main.scroll[0]+gun_offset[0], rotated_rect.centery-rotated_img.get_height()/2-self.m.main.scroll[1]+gun_offset[1]])


    def animations(self):
        self.frame += 1
        if self.frame >= len(self.m.main.anim_data[self.action]):
            self.frame = 0
        self.img_id = self.m.main.anim_data[self.action][self.frame]
        self.img = self.m.main.anim_frames[self.img_id]

        self.img = pygame.transform.scale(self.img, (self.data['width'], self.data['height']))

    def movement(self):
        dist = self.dist_to([self.m.main.p.rect.centerx, self.m.main.p.rect.centery])

        SeesPlayer = self.raytrace_to_target([self.rect.centerx, self.rect.centery], [self.m.main.p.rect.centerx,self.m.main.p.rect.centery], self.m.tile_rects)
        # print(SeesPlayer)
        if SeesPlayer:
            if self.m.main.frame-self.last_shoot>self.modeReference[self.mode]['shootCD']:
                self.shoot([self.m.main.p.rect.centerx,self.m.main.p.rect.centery])
                self.last_shoot = self.m.main.frame

            if random.randint(0,60) == 1 or self.move == [0,0]:
                self.move = [random.randint(self.modeReference[self.mode]['moveRange'][0],self.modeReference[self.mode]['moveRange'][1]), random.randint(self.modeReference[self.mode]['moveRange'][0],self.modeReference[self.mode]['moveRange'][1])]
            self.rect, collisions = e.move(self.rect, self.move, self.m.tile_rects)
            if collisions['top'] or collisions['bottom']:
                self.move[1] *= -1
            if collisions['left'] or collisions['right']:
                self.move[0] *= -1


    def shoot(self, targetPos):
        startPos = [self.rect.centerx, self.rect.centery]
        radians = math.atan2(targetPos[1]-self.rect.centery,targetPos[0]-self.rect.centerx)
        rot = -math.degrees(radians)-90
        self.m.entities.append(Bullet(self.m, startPos, [math.cos(radians), math.sin(radians)], rot, exceptions=[self]))
        self.m.main.roboShootSound.play()



    def raytrace_to_target(self, startPos, targetPos, tiles):
        targetVec = pygame.math.Vector2(targetPos)
        startVec = pygame.math.Vector2(startPos)
        ray = pygame.math.Vector2(startPos)

        try:
            move = pygame.math.Vector2(targetVec.x-startVec.x, targetVec.y-startVec.y).normalize()
        except:
            return True
        # print(move)
        loopCount = 0
        while True:
            # print(f'[{int(ray.x)},{int(ray.y)}]   {targetVec}')
            ray.x += move.x
            ray.y += move.y

            for t in tiles:
                if t.collidepoint(ray):
                    return False
            if move.x < 0:
                finalx = math.ceil(ray.x)
            else:
                finalx = int(ray.x)
            if move.y < 0:
                finaly = math.ceil(ray.y)
            else:
                finaly = int(ray.y)

            if finalx == targetVec.x and finaly == targetVec.y:
                return True

            # pygame.draw.circle(self.m.main.display, (255,0,0), [ray.x-self.m.main.scroll[0],ray.y-self.m.main.scroll[1]], 1)
            loopCount += 1
            if loopCount > 2000:
                print('loop count reached')
                return False

    def hit(self, projectile):
        vel = pygame.math.Vector2(projectile.movement).normalize()
        self.move[0] += vel.x
        self.move[1] += vel.y
        projectile.kill()
        self.health -= 2
        if self.health <= 0:
            self.kill()
        self.hit_time = time()

    def dist_to(self, point): # point: [x,y]
        x = abs(self.rect.centerx); y = abs(self.rect.centery)
        px = abs(point[0]) ; py = abs(point[1])

        dist = math.sqrt( (px-x)**2 + (py-y)**2 )
        return dist


    def kill(self):
        self.m.entities.remove(self)
        self.m.enemies.remove(self)
        self.m.shootable_entities.remove(self)

