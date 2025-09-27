from grass_2d import *
from PIL import Image

def create_shifted_half_filled(rotation=0, hflip=False, vflip=False):
    if rotation%90 != 0:
        raise RuntimeError("Can be rotated only in multiple of 90 Degrees")
    value = np.hstack([
        BLANK_IMG,
        create_half_filled(TILE_SIZE, 270),
        create_middle_grass(TILE_SIZE),        
    ])[:,(HALF_TILE):-(HALF_TILE),:]
    
    for _ in range(rotation // 90):
        value = np.rot90(value)

    if hflip:
        value = np.fliplr(value)

    if vflip == 1:
        value = np.flipud(value)

    return value
    
def create_shifted_half_circle(rotation=0, hflip=False, vflip=False):
    if rotation%90 != 0:
        raise RuntimeError("Can be rotated only in multiple of 90 Degrees")
    value = np.vstack([
        np.hstack([
            BLANK_IMG,
            BLANK_IMG,
            BLANK_IMG,
        ]),
        np.hstack([
            BLANK_IMG,
            create_half_circle(TILE_SIZE, 180),
            create_half_filled(TILE_SIZE, 180)
        ]),
        np.hstack([
            BLANK_IMG,
            create_half_filled(TILE_SIZE, 270),        
            create_middle_grass(TILE_SIZE),        
        ]),
    ])[(HALF_TILE):-(HALF_TILE),(HALF_TILE):-(HALF_TILE),:]
    
    for _ in range(rotation // 90):
        value = np.rot90(value)

    if hflip:
        value = np.fliplr(value)

    if vflip == 1:
        value = np.flipud(value)

    return value

def create_shifted_from_to(rotation=0, hflip=False, vflip=False):
    if rotation%90 != 0:
        raise RuntimeError("Can be rotated only in multiple of 90 Degrees")
    value = np.hstack([
        BLANK_IMG,
        create_half_filled(TILE_SIZE, 270),
        create_middle_grass(TILE_SIZE),        
    ])[:,(HALF_TILE):-(HALF_TILE),:]
    
    for _ in range(rotation // 90):
        value = np.rot90(value)

    if hflip:
        value = np.fliplr(value)

    if vflip == 1:
        value = np.flipud(value)

    return value

def create_2d_grass_tileset_shifted():
    row0 = np.hstack([
        create_middle_grass(TILE_SIZE),
        create_shifted_half_filled(),
        create_shifted_half_filled(hflip=True),
        BLANK_IMG,
        BLANK_IMG,
    ])
    
    top = create_shifted_half_filled(rotation=90, vflip=1)
    bottom = create_shifted_half_filled(rotation=90)
    top_to_right = create_shifted_half_circle()
    top_to_left = create_shifted_half_circle(hflip=True)
        
    row1 = np.hstack([
        top_to_right,
        top_to_left,
        bottom,
        top,
        np.zeros((64, 224 - top.shape[1] - bottom.shape[1] - top_to_right.shape[1] - top_to_left.shape[1], 4), dtype=np.uint8)
    ])

    down_to_right = create_shifted_half_circle(vflip=True)
    down_to_left = create_shifted_half_circle(vflip=True, hflip=True)
    
    # Image.fromarray(top_to_left, "RGBA").save("top_to_right.png")
    row2 = np.hstack([
        down_to_right,
        down_to_left,
        np.zeros((64, 224 - top_to_right.shape[1] - down_to_left.shape[1], 4), dtype=np.uint8)
    ])

    row3 = np.hstack([
        create_from_to(TILE_SIZE, 0, 1),
        create_from_to(TILE_SIZE, 0),
        create_from_to(TILE_SIZE, 0, vflip=1, hflip=1),
        create_from_to(TILE_SIZE, 0, vflip=1),
        BLANK_IMG,
        create_diagonal(TILE_SIZE),
        create_diagonal(TILE_SIZE, hflip=True),
    ])

    return np.vstack((
        row0,
        row1,
        row2,
        row3,
    ))

if __name__ == '__main__':
    img = create_2d_grass_tileset_shifted()
    pil_img = Image.fromarray(img, mode='RGBA')
    pil_img.save("D:\\Projects\\isekai\\resources\\grass1_.png")
