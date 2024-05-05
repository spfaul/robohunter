import pygame
from pygame.locals import *
import json


def parse_json(path, levelNum, collidable_tiles):
    tiles = []
    tile_rects = []
    entities = []
    with open(path) as json_data:
        data = json.load(json_data)

    TILE_SIZE = data["defaultGridSize"]

    level_width = data['levels'][levelNum]['pxWid']
    level_height = data['levels'][levelNum]['pxHei']

    for layer in data['levels'][levelNum]["layerInstances"]:
        ## autotiling layer
        if layer['__identifier'].startswith('AutoLayer'):
            tiles.append([layer["autoLayerTiles"], layer['__tilesetRelPath']])

        ## normal tile layer
        if layer['__identifier'].startswith('Tiles'):
            tiles.append([layer['gridTiles'], layer['__tilesetRelPath']])

        ## entities
        if layer['__identifier'] == 'Entities':
            entities = [e for e in layer["entityInstances"]]

        ## use this for collisions
        if layer['__identifier'] == 'IntGrid':
            grid_size = layer['__gridSize']
            for l in tiles:
                for tile in l[0]:
                    grid_x = int(tile['px'][0] / grid_size)
                    grid_y = int(tile['px'][1] / grid_size)
                    tileType = layer['intGridCsv'][grid_x + grid_y * int(level_width / grid_size)]
                    if tileType in collidable_tiles:
                        tile_rects.append(pygame.Rect(tile['px'][0],tile['px'][1],grid_size,grid_size))

    levelInfo = [TILE_SIZE,tiles,tile_rects,entities]

    return levelInfo

def collision_test(rect,tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect,movement,tiles):
    collision_types = {'top':False,'bottom':False,'right':False,'left':False}
    rect.x += movement[0]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

def load_animation(path, frame_durations, animation_frames):
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        # player_animations/idle/idle_0.png
        animation_image = pygame.image.load(img_loc).convert_alpha()
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data

def change_action(action_var,frame,new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var,frame


def clip(surf,x,y,x_size,y_size):
    handle_surf = surf.copy()
    clipR = pygame.Rect(x,y,x_size,y_size)
    handle_surf.set_clip(clipR)
    image = surf.subsurface(handle_surf.get_clip())
    return image.copy()

def perfect_outline(img, display, loc, color):
    mask = pygame.mask.from_surface(img)
    mask_surf = mask.to_surface(setcolor=color)
    mask_surf.set_colorkey((0,0,0))
    display.blit(mask_surf,(loc[0]-1,loc[1]))
    display.blit(mask_surf,(loc[0]+1,loc[1]))
    display.blit(mask_surf,(loc[0],loc[1]-1))
    display.blit(mask_surf,(loc[0],loc[1]+1))
    

def load_tilemap(path, tile_size):
    tileset_img = pygame.image.load(path).convert_alpha()
    # tileset_img.set_colorkey((0, 0, 0))
    width = tileset_img.get_width()
    height = tileset_img.get_height()

    images = []
    for y in range(int(height / tile_size[1])):
        for x in range(int(width / tile_size[0])):
            tile_img = clip(tileset_img, x*tile_size[0], y*tile_size[1],tile_size[0],tile_size[1])
            images.append([tile_img, x*tile_size[0], y*tile_size[1]])

    tilemap = {}
    for img in images:
        tilemap[(img[1],img[2])] = img[0]
    return tilemap

def rotate_img(img, angle, center_coords):
    rotated_img = pygame.transform.rotozoom(img, angle, 1)
    rotated_rect = rotated_img.get_rect(center=center_coords)

    return rotated_img, rotated_rect


def collision_test(rect,tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def circle_surf(radius, color):
    surf = pygame.Surface((radius * 2, radius * 2))
    surf.set_alpha(128)
    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey((0, 0, 0))
    return surf