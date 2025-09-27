import numpy as np
from numpy.typing import NDArray
import random
from noise import pnoise2
import math

TILE_SIZE = 32
BLANK = (0,0,0,0)
GRASS_PRIMARY = (88, 143, 61,255)
GRASS_BORDER = (54, 99, 61, 255)
GRASS_HIGHLIGHT = (170, 191, 64, 255)
HALF_TILE = TILE_SIZE // 2
BLANK_IMG = np.zeros((TILE_SIZE, TILE_SIZE, 4), dtype=np.uint8)

def map_value(value, start1, stop1, start2, stop2):
    """Map value from one range to another."""
    return start2 + (float(value - start1) / (stop1 - start1)) * (stop2 - start2)

# values = [pnoise1(i * 0.05, octaves=4) for i in range(200)]
# print(values) // -1 to 1
# x_noise = pnoise1(200 + i * 0.05, octaves=4)
# x = int(map_value(x_noise, -1, 1, 0, TILE_SIZE - 1))
# y_noise = pnoise1(100 + (i*0.001), octaves=8)
# y = int(map_value(y_noise, -1, 1, 0, TILE_SIZE - 1))


def random_grass(w:int, h:int, max_spot_percentage:float, grass_img: NDArray):
    number_of_spots_max = int(w * h * max_spot_percentage)
    for _ in range(random.randint(0, number_of_spots_max)):
        x = random.randint(0, w -1)
        y = random.randint(0, h - 1)
        # TODO: Draw pixel only if it is below the other line using cross product method.
        grass_img[y][x] = GRASS_BORDER if (random.randint(1, 100) < 65) else GRASS_HIGHLIGHT
    


def create_middle_grass(tile_size, max_spot_percentage=0.05):
    grass_middle = np.zeros((tile_size, tile_size, 4), dtype=np.uint8)
    grass_middle[:] = GRASS_PRIMARY
    random_grass(tile_size, tile_size, max_spot_percentage, grass_middle)
    return grass_middle


def create_half_filled(tile_size, rotation, max_spot_percentage=0.05):
    if rotation%90 != 0:
        raise RuntimeError("Can be rotated only in multiple of 90 Degrees")
    w,h = tile_size, tile_size//2
    grass_img = np.zeros((tile_size, tile_size, 4), dtype=np.uint8)
    grass_img[:h, :] = GRASS_PRIMARY
    
    random_grass(w,h,max_spot_percentage, grass_img)
    
    grass_img[h][0] = GRASS_BORDER
    grass_img[h-1][0] = GRASS_HIGHLIGHT
    
    grass_img[h][w-1] = GRASS_BORDER
    grass_img[h-1][w-1] = GRASS_HIGHLIGHT

    offset = random.randint(0, 100057)
    for i in range(1, w-1):
        x = int(1 + 4*pnoise2(offset + i / 4.0 , offset + h / 4.0, octaves=4))
        grass_img[h+x][i] = GRASS_BORDER
        # Fill White space
        grass_img[h+x-1][i] = GRASS_HIGHLIGHT
        if (h + x - 1) > h:
            for j in range(h, h + x -1):
                grass_img[j][i] = GRASS_PRIMARY
    
    
    for x in range(rotation // 90):
        grass_img = np.rot90(grass_img)
    
    return grass_img


def create_half_circle(tile_size, rotation, max_spot_percentage=0.05):
    grass_img = np.zeros((tile_size, tile_size, 4), dtype=np.uint8)
    r = tile_size // 2
    offset = random.randint(0, 100019)
    for ang in range(0, 90):
        x = int(r*math.cos(math.radians(ang)))
        y = int(r*math.sin(math.radians(ang)))
        val = int(1 + 2 * pnoise2(offset +x / 4.0 , offset + y / 4.0, octaves=4))
        r_dash = r + val
        x_dash = int(r_dash * math.cos(math.radians(ang)))
        y_dash = int(r_dash * math.sin(math.radians(ang)))
        grass_img[y,:x_dash] = GRASS_HIGHLIGHT
        grass_img[:y,:x] = GRASS_PRIMARY
        grass_img[y_dash][x_dash] = GRASS_BORDER
        
    random_grass(r,r,max_spot_percentage,grass_img)
    
    for x in range(rotation // 90):
        grass_img = np.rot90(grass_img)
    return grass_img
    

def create_from_to(tile_size, rotation, hflip = 0, vflip = 0, max_spot_percentage=0.125):
    grass_img = np.zeros((tile_size, tile_size, 4), dtype=np.uint8)
    r = tile_size // 2
    grass_img[:] = GRASS_PRIMARY

    random_grass(tile_size, tile_size, max_spot_percentage, grass_img)
    offset = random.randint(0, 100019)
    for ang in range(0, 90):
        x = int(+r*math.cos(math.radians(ang)))
        y = int(+r*math.sin(math.radians(ang)))
        grass_img[:y,:x] = BLANK
        val = int(1 + 2 * pnoise2(offset +x / 4.0 , offset + y / 4.0, octaves=4))
        r_dash = r - val
        x_dash = int(r_dash * math.cos(math.radians(ang)))
        y_dash = int(r_dash * math.sin(math.radians(ang)))
        # grass_img[y,:x_dash] = GRASS_HIGHLIGHT
        # grass_img[:y,:x] = GRASS_PRIMARY
        grass_img[y_dash][x_dash] = GRASS_BORDER

    for x in range(rotation // 90):
        grass_img = np.rot90(grass_img)

    if hflip == 1:
        grass_img = np.fliplr(grass_img)
    
    if vflip == 1:
        grass_img = np.flipud(grass_img)
    
    return grass_img

def create_diagonal(tile_size, hflip = False, max_spot_percentage=0.05):
    grass_img = np.zeros((tile_size, tile_size, 4), dtype=np.uint8)
    r = tile_size // 2
    grass_img[:] = GRASS_PRIMARY
    random_grass(tile_size, tile_size, max_spot_percentage, grass_img)

    offset = random.randint(0,  103091)
    for ang in range(0, 90):
        x = int(+r*math.cos(math.radians(ang)))
        y = int(+r*math.sin(math.radians(ang)))
        grass_img[:y,:x] = BLANK
        val = int(1 + 2 * pnoise2(offset +x / 4.0 , offset + y / 4.0, octaves=4))
        r_dash = r - val
        x_dash = int(r_dash * math.cos(math.radians(ang)))
        y_dash = int(r_dash * math.sin(math.radians(ang)))
        grass_img[y_dash][x_dash] = GRASS_BORDER

    offset = random.randint(0,  104959)
    for ang in range(90, 180):
        x = int(tile_size-1+r*math.cos(math.radians(ang)))
        y = int(tile_size-1-r*math.sin(math.radians(ang)))
        grass_img[y:,x:] = BLANK
        val = int(1 + 2 * pnoise2(offset +x / 4.0 , offset + y / 4.0, octaves=4))
        r_dash = r - val
        x_dash = int(r_dash * math.cos(math.radians(ang)))
        y_dash = int(r_dash * math.sin(math.radians(ang)))
        grass_img[y_dash][x_dash] = GRASS_BORDER

    if hflip:
        grass_img = np.fliplr(grass_img)
    
    return grass_img

def create_blank(tile_size):
    grass_img = np.zeros((tile_size, tile_size, 4), dtype=np.uint8)
    return grass_img



def create_2d_grass_tileset():
    row1 = np.hstack([
        create_half_circle(TILE_SIZE, 90),
        create_half_filled(TILE_SIZE, 270),
        create_from_to(TILE_SIZE, 0, 1),
        create_half_filled(TILE_SIZE, 180)
    ])

    row2 = np.hstack([
        create_diagonal(TILE_SIZE, hflip=True),
        create_from_to(TILE_SIZE, 0),
        create_middle_grass(TILE_SIZE),
        create_from_to(TILE_SIZE, 0, vflip=1, hflip=1),
    ])

    row3 = np.hstack([
        create_half_circle(TILE_SIZE, 270),
        create_half_filled(TILE_SIZE, 0),
        create_from_to(TILE_SIZE, 0, vflip=1),
        create_half_filled(TILE_SIZE, 90)
    ])

    row4 = np.hstack([
        create_blank(TILE_SIZE),
        create_half_circle(TILE_SIZE, 180),
        create_diagonal(TILE_SIZE),
        create_half_circle(TILE_SIZE, 0)
    ])


    return np.vstack((
        row1,
        row2,
        row3,
        row4,
    ))