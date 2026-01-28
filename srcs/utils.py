import math
import pygame as pg


def get_max_z(config):
    config.max_z = config.heightmap[0][0]

    for row in config.heightmap:
        for z in row:
            if z > config.max_z:
                config.max_z = z


def get_min_z(config):
    config.min_z = config.heightmap[0][0]

    for row in config.heightmap:
        for z in row:
            if z < config.min_z:
                config.min_z = z


def auto_calculate_z_multiplier(config):
    x_range = config.map_w
    y_range = config.map_h

    z_range = abs(config.max_z - config.min_z)

    if z_range == 0:
        return 0.1

    config.z_multiplier = (max(x_range, y_range) * 0.15) / z_range


def draw_line(window, p0, p1, c0, c1):
    x0, y0 = p0
    x1, y1 = p1

    dx = x1 - x0
    dy = y1 - y0
    dist = math.hypot(dx, dy)

    if dist == 0:
        return

    steps = int(dist)
    if steps == 0:
        return

    r0, g0, b0 = c0
    dr = (c1[0] - r0) / steps
    dg = (c1[1] - g0) / steps
    db = (c1[2] - b0) / steps

    ux = dx / steps
    uy = dy / steps

    for i in range(steps):
        curr_r = int(r0 + dr * i)
        curr_g = int(g0 + dg * i)
        curr_b = int(b0 + db * i)

        start_pos = (x0 + ux * i, y0 + uy * i)
        end_pos = (x0 + ux * (i + 1), y0 + uy * (i + 1))

        pg.draw.line(window, (curr_r, curr_g, curr_b), start_pos, end_pos, 1)


def get_projection_bounds(config):
    first_point = config.isometric_projection[0][0]
    min_x = max_x = first_point[0]
    min_y = max_y = first_point[1]

    for row in config.isometric_projection:
        for nx, ny in row:
            if nx < min_x:
                min_x = nx
            if nx > max_x:
                max_x = nx
            if ny < min_y:
                min_y = ny
            if ny > max_y:
                max_y = ny

    config.projection_bounds = min_x, max_x, min_y, max_y

    config.proj_center_x = (min_x + max_x) / 2
    config.proj_center_y = (min_y + max_y) / 2


def update_scale(config):
    min_x, max_x, min_y, max_y = config.projection_bounds

    available_space_x = (
        config.window_w
        - (2 * config.padding)
        - config.dashboard_w
    )
    available_space_y = config.window_h - (2 * config.padding)

    map_x = max_x - min_x
    map_y = max_y - min_y

    scale_x = available_space_x / map_x
    scale_y = available_space_y / map_y

    config.scale = min(scale_x, scale_y)
