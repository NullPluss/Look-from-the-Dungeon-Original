import math

def clamp(value, min_val, max_val):
    return max(min_val, min(value, max_val))

def lerp(a, b, t):
    return a + (b - a) * t

def distance(a, b):
    return math.hypot(b[0] - a[0], b[1] - a[1])

def grid_to_world(x, y, tile_size):
    return x * tile_size, y * tile_size

def world_to_grid(x, y, tile_size):
    return x // tile_size, y // tile_size