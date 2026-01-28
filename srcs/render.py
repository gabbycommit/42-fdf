from srcs import utils, text


def render_map(window, config):
    if config.needs_redraw:
        config.map_surface.fill((0, 0, 0))

        center_x = (config.dashboard_w
                    + (config.window_w - config.dashboard_w)
                    // 2
                    )
        center_y = config.window_h // 2

        for y, row in enumerate(config.isometric_projection):
            for x, (nx, ny) in enumerate(row):
                c0 = config.colors[y][x]
                x0 = int(
                    (nx - config.proj_center_x)
                    * config.scale + center_x
                    + config.offset_x
                )
                y0 = int(
                    (ny - config.proj_center_y)
                    * config.scale
                    + center_y
                    + config.offset_y
                )

                # draw horizontal line
                if x + 1 < config.map_w:
                    hc = config.colors[y][x + 1]
                    hx, hy = config.isometric_projection[y][x + 1]
                    hx = int(
                        (hx - config.proj_center_x)
                        * config.scale
                        + center_x
                        + config.offset_x
                    )
                    hy = int(
                        (hy - config.proj_center_y)
                        * config.scale
                        + center_y
                        + config.offset_y
                    )
                    utils.draw_line(
                        config.map_surface,
                        (x0, y0),
                        (hx, hy),
                        c0,
                        hc,
                    )

                # draw verticle line
                if y + 1 < config.map_h:
                    vc = config.colors[y + 1][x]
                    vx, vy = config.isometric_projection[y + 1][x]
                    vx = int(
                        (vx - config.proj_center_x)
                        * config.scale
                        + center_x
                        + config.offset_x
                    )
                    vy = int(
                        (vy - config.proj_center_y)
                        * config.scale
                        + center_y
                        + config.offset_y
                    )
                    utils.draw_line(
                        config.map_surface,
                        (x0, y0),
                        (vx, vy),
                        c0,
                        vc
                    )

        config.needs_redraw = False

    window.blit(config.map_surface, (0, 0))


def render_dashboard(window, config, dashboard):
    dashboard.dashboard_surface.fill((30, 30, 30, 100))

    title_x = 20
    item_x = 30
    y = 30
    padding = 8

    min_x, max_x, min_y, max_y = config.projection_bounds

    header = dashboard.font_big.render("/// 42 FDF ///", True, (255, 255, 255))
    header_rect = header.get_rect(topleft=(title_x, y))
    dashboard.dashboard_surface.blit(header, header_rect)
    y += 60

    y = text.title("[ MAP INFO ]", dashboard, title_x, y)
    file_name_rect, y = text.item("Map's name:", dashboard, item_x, y)
    text.value(f"{config.file_name}", dashboard, file_name_rect, padding)
    map_size_rect, y = text.item("Map's size:", dashboard, item_x, y)
    text.value(f"{(max_x * max_y):.2f}", dashboard, map_size_rect, padding)
    max_x_rect, y = text.item("Max_x:", dashboard, item_x, y)
    text.value(f"{max_x:.2f}", dashboard, max_x_rect, padding)
    max_y_rect, y = text.item("Max_y:", dashboard, item_x, y)
    text.value(f"{max_y:.2f}", dashboard, max_y_rect, padding)
    max_z_rect, y = text.item("Max_z:", dashboard, item_x, y)
    text.value(f"{config.max_z}", dashboard, max_z_rect, padding)
    min_z_rect, y = text.item("Min_z:", dashboard, item_x, y)
    text.value(f"{config.min_z}", dashboard, min_z_rect, padding)
    y += 30

    y = text.title("[ CAMERA INFO ]", dashboard, title_x, y)
    curr_theme, y = text.item("Current Theme:", dashboard, item_x, y)
    text.value(f"{config.selected_theme}", dashboard, curr_theme, padding)
    z_multi, y = text.item("z multiplier:", dashboard, item_x, y)
    text.value(f"{config.z_multiplier:.2f}", dashboard, z_multi, padding)
    x_angle, y = text.item("angle x:", dashboard, item_x, y)
    text.value(f"{config.angle_x:.2f}", dashboard, x_angle, padding)
    y_angle, y = text.item("angle y:", dashboard, item_x, y)
    text.value(f"{config.angle_y:.2f}", dashboard, y_angle, padding)
    z_angle, y = text.item("angle z:", dashboard, item_x, y)
    text.value(f"{config.angle_z:.2f}", dashboard, z_angle, padding)
    scale, y = text.item("scale:", dashboard, item_x, y)
    text.value(f"{config.scale:.2f}", dashboard, scale, padding)
    y += 30

    y = text.title("[ CONTROLS ]", dashboard, title_x, y)
    b_n, y = text.item("B / N:", dashboard, item_x, y)
    text.value("prev map / next map", dashboard, b_n, padding)
    arrows, y = text.item("ARROWS:", dashboard, item_x, y)
    text.value("move map", dashboard, arrows, padding)
    w_s, y = text.item("W / S:", dashboard, item_x, y)
    text.value("rotate X", dashboard, w_s, padding)
    a_d, y = text.item("A / D:", dashboard, item_x, y)
    text.value("rotate Y", dashboard, a_d, padding)
    k_l, y = text.item("K / L:", dashboard, item_x, y)
    text.value("rotate z", dashboard, k_l, padding)
    page, y = text.item("PG UP / PG DN:", dashboard, item_x, y)
    text.value("z-multiplier", dashboard, page, padding)
    zoom, y = text.item("- / =:", dashboard, item_x, y)
    text.value("zoom", dashboard, zoom, padding)
    y += 30

    y = text.title("[ COLOR THEME ]", dashboard, title_x, y)
    the_core, y = text.item("1:", dashboard, item_x, y)
    text.value("The Core", dashboard, the_core, padding)
    cyber_punk, y = text.item("2:", dashboard, item_x, y)
    text.value("Cyber Punk", dashboard, cyber_punk, padding)
    ice_tundra, y = text.item("3:", dashboard, item_x, y)
    text.value("Ice Tundra", dashboard, ice_tundra, padding)
    desert_oasis, y = text.item("4:", dashboard, item_x, y)
    text.value("Dessert Oasis", dashboard, desert_oasis, padding)

    window.blit(dashboard.dashboard_surface, (0, 0))
