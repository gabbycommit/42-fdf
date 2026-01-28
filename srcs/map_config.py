import math
import os
import sys
import pygame as pg

from srcs import parse, utils, color

class FdfConfig:
    def __init__(self, window_w, window_h, dashboard_w):
        self.window_w = window_w
        self.window_h = window_h
        self.dashboard_w = dashboard_w

        self.map_surface = pg.Surface((window_w, window_h))

        self.file_name = ""

        self.heightmap = None
        self.model_verteces = None
        
        self.z_multiplier = 0.2
        self.z_min_limit = 0.001
        self.z_max_limit = 5
        self.z_multi_default = {
            "10-2": 0.3,
            "10-70": 0.017,
            "20-60": 0.03,
            "42": 0.1,
            "50-4": 1,
            "100-6": 0.3,
            "basictest": 0.3,
            "elem": 0.2,
            "elem2": 0.5,
            "mars": 0.4, 
            "WEST_COAST_USA_OCEAN": 0.016,
            "LOS_ANDES_OCEAN": 0.016, 
            "CALIFORNIA_OCEAN": 0.016, 
            "HIMALAYA_OCEAN": 0.08,
            "WHOLE_WORLD_OCEAN": 0.016,
            "pentenegpos": 0.2,
            "plat": 0.2, 
            "pnp_flat": 0.2,
            "pylone": 2.2,
            "pyra": 0.7,
            "t1": 0.2,
            "t2": 0.2,
        }
        self.isometric_projection = []

        self.map_w = 0
        self.map_h = 0

        self.min_z = 0
        self.max_z = 0

        self.angle_x = -1.05
        self.angle_y = 0.0
        self.angle_z = 0.75

        self.padding = 50

        self.projection_bounds = 0, 0, 0, 0
        
        self.map_center_x = 0
        self.map_center_y = 0

        self.proj_center_x = 0
        self.proj_center_y = 0

        self.scale = 1
        self.init_scale = 1
        self.max_scale_limit = 2.0
        self.min_scale_limit = 0.4

        self.theme = {
            "the_core": {
                "water1": (0, 119, 190),
                "water2": (0, 31, 63),
                "ground": (255, 255, 255),
                "land1": (88, 214, 141),
                "land2": (163, 152, 93),
                "land3": (255, 69, 0),
            },
            "cyber_punk": {
                "water1": (44, 62, 80),
                "water2": (48, 25, 52),
                "ground": (255, 255, 255),
                "land1": (191, 0, 255),
                "land2": (255, 105, 180),
                "land3": (255, 255, 51),
            },
            "ice_tundra": {
                "water1": (0, 128, 128),
                "water2": (5, 55, 66),
                "ground": (173, 216, 230),
                "land1": (112, 128, 144),
                "land2": (214, 211, 193),
                "land3": (250, 250, 250),
            },
            "desert_oasis": {
                "water1": (102, 204, 255),
                "water2": (0, 51, 102),
                "ground": (244, 164, 96),
                "land1": (226, 114, 91),
                "land2": (204, 85, 0),
                "land3": (255, 215, 0)
            }
        }
        self.selected_theme = "the_core"
        self.colors = []

        self.offset_x = 0
        self.offset_y = 0

        self.needs_update = False
        self.needs_redraw = True

    def load_new_map(self, map_dir, map_files, map_idx):
        map_path = os.path.join(map_dir, map_files[map_idx])
        print(f"loading map: {map_files[map_idx]}")

        parse.get_heightmap(map_path, self)
        if not parse.is_valid_shape(self.heightmap):
            sys.exit(1)

        self.map_w = len(self.heightmap[0])
        self.map_h = len(self.heightmap)

        utils.get_min_z(self)
        utils.get_max_z(self)
        
        parse.get_model_verteces(self)
        
        map_key = os.path.splitext(map_files[map_idx])[0]
        self.file_name = map_key
        self.z_multiplier = self.z_multi_default.get(map_key, self.z_multiplier)

        self.angle_x = -1.05
        self.angle_y = 0.0
        self.angle_z = 0.75

        parse.isometric_projection(self)

        color.get_map_colors(self)

        utils.get_projection_bounds(self)
        min_x, max_x, min_y, max_y = self.projection_bounds
        self.map_center_x = (min_x + max_x) / 2
        self.map_center_y = (min_y + max_y) / 2

        utils.update_scale(self)
        self.init_scale = self.scale

        self.offset_x = 0
        self.offset_y = 0

        self.needs_redraw = True

    def update_data(self):
        parse.isometric_projection(self)

        self.needs_update = False
        self.needs_redraw = True


class DashBoard:
    def __init__(self, dashboard_w, window_h):
        self.dashboard_w = dashboard_w
        self.window_h = window_h

        self.dashboard_surface = pg.Surface(
            (self.dashboard_w,self.window_h),
            pg.SRCALPHA
        )
 
        self.font_small = pg.font.SysFont("consolas", 14)
        self.font_medium = pg.font.SysFont("consolas", 18)
        self.font_big = pg.font.SysFont("consolas", 24)
