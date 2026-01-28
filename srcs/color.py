def get_t(z, config):
    if z < 0:
        return abs(z) / abs(config.min_z)
    elif z > 0:
        return abs(z) / abs(config.max_z)
    else:
        return 0


def lerp_color(c0, c1, t):
    r = int(c0[0] + (c1[0] - c0[0]) * t)
    g = int(c0[1] + (c1[1] - c0[1]) * t)
    b = int(c0[2] + (c1[2] - c0[2]) * t)

    return r, g, b


def get_color(t, z, config):
    theme_data = config.theme[config.selected_theme]

    if z < 0:
        return lerp_color(theme_data["water1"], theme_data["water2"], t)
    elif z == 0:
        return theme_data["ground"]
    else:
        if t <= 0.7:
            return lerp_color(
                theme_data["land1"],
                theme_data["land2"],
                t / 0.7
            )
        else:
            return lerp_color(
                theme_data["land2"],
                theme_data["land3"],
                (t - 0.7) / 0.3
            )


def get_map_colors(config):
    config.colors = []

    for row in config.heightmap:
        colors_row = []
        for z in row:
            t = get_t(z, config)
            color = get_color(t, z, config)
            colors_row.append(color)

        config.colors.append(colors_row)
