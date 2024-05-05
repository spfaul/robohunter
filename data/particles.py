import pygame


class Particles():
    def __init__(self):
        self.TILE_SIZE = 16
        self.obstacles = []
        self.circle_particles = [] #ex [[x,y], [move_x, move_y], size, color]

    def update(self, display, scroll):
        # print(self.obstacles)
        for particle in self.circle_particles:
            particle[0][0] += particle[1][0]
            loc = (int(particle[0][0] / self.TILE_SIZE),int(particle[0][1] / self.TILE_SIZE))
            if loc in self.obstacles:
                particle[1][0] = -0.7 * particle[1][0]
                particle[1][1] *= 0.95
                particle[0][0] += particle[1][0] * 2
            particle[0][1] += particle[1][1]
            loc = (int(particle[0][0] / self.TILE_SIZE),int(particle[0][1] / self.TILE_SIZE))
            if loc in self.obstacles:
                particle[1][1] = -0.7 * particle[1][1]
                particle[1][0] *= 0.95
                particle[0][1] += particle[1][1] * 2
            particle[2] -= 0.035
            # particle[1][1] += 0.15
            pygame.draw.circle(display, particle[3], [int(particle[0][0])-scroll[0], int(particle[0][1])-scroll[1]], int(particle[2]))
            if particle[2] <= 0:
                self.circle_particles.remove(particle)

    def create_particle(self, startPos, movement, size, color):
        self.circle_particles.append([startPos, movement, size, color])


    def rect_to_tile(self, rects):
        tiles = []
        for rect in rects:
            tiles.append((int(rect[0].x/self.TILE_SIZE), int(rect[0].y/self.TILE_SIZE)))
        return tiles