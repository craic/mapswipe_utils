#!/usr/local/bin/python3

# mapswipe_display_grid_random_tiles.py

# Copyright 2017  Robert Jones  jones@craic.com

# Project repo: https://github.com/craic/mapswipe_utils

# Released under the terms of the MIT License


# Simple script that generates a grid image made up of x * y image tiles selected at random
# Handy for getting a quick overview of a directory of image tiles

import argparse
import sys
import os
import json
import random
from PIL import Image



def main():
    parser = argparse.ArgumentParser(description="Display a grid of image tiles")
    parser.add_argument('--tilelist', '-f', metavar='<tile_list_file>', required=True,
                        help='MapSwipe Project Tile List file')
    parser.add_argument('--tiledir', '-d', metavar='<tile_directory>', required=True,
                        help='Directory of tile images')
    parser.add_argument('--nx', '-x', metavar='<nx>', type=int, required=True,
                        help='Number of tiles in X dimension')
    parser.add_argument('--ny', '-y', metavar='<ny>', type=int, required=True,
                        help='Number of tiles in Y dimension')
    args = parser.parse_args()


    nx = int(args.nx)
    ny = int(args.ny)

    tile_list_file = args.tilelist
    tile_dir  = args.tiledir

    # create the base image
    # Bing maps tiles are 256 x 256 pixels
    tile_size = 256

    image_width  = nx * (tile_size + 1) + 1
    image_height = ny * (tile_size + 1) + 1

    base_image = Image.new('RGBA', (image_width, image_height), (0,0,0))

    selected_tiles = {}

    # Load the tile_ids into a list
    with open(tile_list_file, 'rt') as f:
        tile_ids = f.read().splitlines()


    used_ints = {}

    n_tiles = len(tile_ids)
    print(n_tiles)

    x = 0
    y = 1
    for i in range(ny):
      x = 1
      for j in range(nx):
        k = random.randint(0, n_tiles-1)
        while k in used_ints:
          k = random.randint(0, n_tiles-1)

        used_ints[k] = 1
        tile_id = tile_ids[k]
        print(tile_id)

        img_path = os.path.join(tile_dir, "{}.jpg".format(tile_id))
        img = Image.open(img_path)
        img = img.resize((tile_size, tile_size), Image.ANTIALIAS)


        base_image.paste(img, (x, y))
        x += tile_size + 1
      print('')
      y += tile_size + 1

    base_image.show()


main()
