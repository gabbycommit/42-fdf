import pygame as pg
from srcs import parse, render, map_config, color

WINDOW_W = 1400
WINDOW_H = 800
DASHBOARD_W = 300
FPS = 60
MAP_DIR = "./maps"

ANGLE_SPEED = 0.03
USER_OFFSET_SPEED = 1


pg.init()

window = pg.display.set_mode((WINDOW_W, WINDOW_H))
pg.display.set_caption("42 FDF")
clock = pg.time.Clock()

config = map_config.FdfConfig(WINDOW_W, WINDOW_H, DASHBOARD_W)
dashboard = map_config.DashBoard(DASHBOARD_W, WINDOW_H)

map_files = parse.get_files_list(MAP_DIR)
current_idx = 0
config.load_new_map(MAP_DIR, map_files, current_idx)

running = True

while running:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False
        elif e.type == pg.KEYDOWN:
            if e.key == pg.K_ESCAPE:
                running = False
            # next map control
            elif e.key == pg.K_n:
                current_idx = (current_idx + 1) % len(map_files)
                config.load_new_map(MAP_DIR, map_files, current_idx)
            elif e.key == pg.K_b:
                current_idx = (current_idx - 1) % len(map_files)
                config.load_new_map(MAP_DIR, map_files, current_idx)
            # color theme control
            elif e.key == pg.K_1:
                config.selected_theme = "the_core"
                color.get_map_colors(config)
                config.needs_redraw = True
            elif e.key == pg.K_2:
                config.selected_theme = "cyber_punk"
                color.get_map_colors(config)
                config.needs_redraw = True
            elif e.key == pg.K_3:
                config.selected_theme = "ice_tundra"
                color.get_map_colors(config)
                config.needs_redraw = True
            elif e.key == pg.K_4:
                config.selected_theme = "desert_oasis"
                color.get_map_colors(config)
                config.needs_redraw = True

    keys = pg.key.get_pressed()
    # rotate contol
    if keys[pg.K_a]:
        config.angle_y -= ANGLE_SPEED
        config.needs_update = True
    if keys[pg.K_d]:
        config.angle_y += ANGLE_SPEED
        config.needs_update = True
    if keys[pg.K_w]:
        config.angle_x -= ANGLE_SPEED
        config.needs_update = True
    if keys[pg.K_s]:
        config.angle_x += ANGLE_SPEED
        config.needs_update = True
    if keys[pg.K_k]:
        config.angle_z -= ANGLE_SPEED
        config.needs_update = True
    if keys[pg.K_l]:
        config.angle_z += ANGLE_SPEED
        config.needs_update = True

    # z_multiplier control
    if keys[pg.K_PAGEUP]:
        if config.z_multiplier < config.z_max_limit:
            config.z_multiplier *= 1.01
            config.needs_update = True
    if keys[pg.K_PAGEDOWN]:
        if config.z_multiplier > config.z_min_limit:
            config.z_multiplier *= 0.99
            config.needs_update = True

    # scale control:
    if keys[pg.K_EQUALS]:
        if config.scale < config.init_scale * config.max_scale_limit:
            config.scale *= 1.01
            config.needs_update = True
    if keys[pg.K_MINUS]:
        if config.scale > config.init_scale * config.min_scale_limit:
            config.scale *= 0.99
            config.needs_update = True

    # offset_control
    if keys[pg.K_UP]:
        config.offset_y -= 1
        config.needs_redraw = True
    if keys[pg.K_DOWN]:
        config.offset_y += 1
        config.needs_redraw = True
    if keys[pg.K_LEFT]:
        config.offset_x -= 1
        config.needs_redraw = True
    if keys[pg.K_RIGHT]:
        config.offset_x += 1
        config.needs_redraw = True

    if config. needs_update:
        config.update_data()

    window.fill((0, 0, 0))
    render.render_map(window, config)
    render.render_dashboard(window, config, dashboard)
    pg.display.flip()
    clock.tick(FPS)

pg.quit()
