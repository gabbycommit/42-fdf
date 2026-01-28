import os
import sys
import math


def get_files_list(map_dir):
    map_files = [f for f in os.listdir(map_dir) if f.endswith(".fdf")]
    if not map_files:
        print("Error: maps directory is empty")
        sys.exit(1)

    return map_files


def get_heightmap(fdf_path, config):
    config.heightmap = []

    try:
        with open(fdf_path, "r") as file:
            for y, row in enumerate(file):
                line = row.strip().split()

                z_row = []
                for z in line:
                    if "," in z: # whether contain ","
                        token = z.split(",") # [3, color]
                        try:
                            z_row.append(int(token[0]))
                        except ValueError:
                            print(f"Error: invalid input in row {y}: {token}")
                            sys.exit(1)
                    else:
                        try:
                            z_row.append(int(z))
                        except ValueError:
                            print(f"Error: invalid input in row {y}: {z}")
                            sys.exit(1)

                config.heightmap.append(z_row)
        
        # empty height
        if not config.heightmap:
            print("Error: file is empty")
            sys.exit(1)
    
    except FileNotFoundError:
        print("Error: file not found")
        sys.exit(1)


def is_valid_shape(heightmap):
    width = len(heightmap[0])

    for y, row in enumerate(heightmap):
        if len(row) != width:
            print(f"Error: lenght must be {width} but found {len(row)} in row{y}")
            return False

    return True


def get_model_verteces(config):
    config.model_verteces = []

    for y, row in enumerate(config.heightmap):
        vertex_row = []
        for x, z in enumerate(row):
            vertex_row.append((x, y, z))
        config.model_verteces.append(vertex_row)


def isometric_projection(config):
    config.isometric_projection = []

    cx, sx = math.cos(config.angle_x), math.sin(config.angle_x)
    cy, sy = math.cos(config.angle_y), math.sin(config.angle_y)
    cz, sz = math.cos(config.angle_z), math.sin(config.angle_z)

    center_x3d = (config.map_w - 1) / 2
    center_y3d = (config.map_h - 1) / 2
    center_z3d = (config.min_z + config.max_z) / 2

    for row in config.model_verteces:
        projection_row = []
        for vertex in row:
            x, y, z = vertex

            curr_x = x - center_x3d
            curr_y = y - center_y3d
            curr_z = (z - center_z3d) * config.z_multiplier 

            # z-axis rotate
            x_z = (curr_x * cz) - (curr_y * sz)
            y_z = (curr_x * sz) + (curr_y * cz)
            z_z = curr_z

            # y-axis rotate
            x_y = (x_z * cy) + (z_z * sy)
            y_y = y_z
            z_y = (-x_z * sy) - (z_z * cy)

            # x-axis rotate
            final_x = x_y
            final_y = (y_y * cx) - (z_y * sx)

            # projection
            nx = final_x
            ny = final_y

            projection_row.append((nx, ny))
        
        config.isometric_projection.append(projection_row)
