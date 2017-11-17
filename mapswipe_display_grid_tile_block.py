#!/usr/local/bin/python3

# mapswipe_display_grid_tile_block.py

# Copyright 2017  Robert Jones  jones@craic.com

# Project repo: https://github.com/craic/mapswipe_utils

# Released under the terms of the MIT License


# Simple script that generates a grid image made up of the image tiles
# in a directory - this expects those to be a contiguous tile block

# It is up the user to ensure the block is not too large to display
# Use the imagesize argument to display smaller tiles

import argparse
import sys
import os
import json
import re
from PIL import Image



def main():
    parser = argparse.ArgumentParser(description="Display an image tile block")
    parser.add_argument('--tiledir', '-d', metavar='<tile_directory>', required=True,
                        help='Directory of tile images')
    parser.add_argument('--imagesize', '-s', metavar='<image size>', type=int, default=256,
                        help='Display size for each image')
    args = parser.parse_args()

    tile_dir  = args.tiledir
    image_size = int(args.imagesize)

    # Read the tiles from the directory and get the bounds

    filenames = [x for x in os.listdir(tile_dir) if x.endswith(".jpg")]

    min_x = 99999999999999
    max_x = 0
    min_y = 99999999999999
    max_y = 0
    zoom = 0
    for filename in filenames:
        filename = re.sub(r"\.jpg", "", filename)
        a = filename.split('-')
        zoom = int(a[0])
        x = int(a[1])
        y = int(a[2])
        if x < min_x:
            min_x = x
        elif x > max_x:
            max_x = x
        if y < min_y:
            min_y = y
        elif y > max_y:
            max_y = y


    nx = max_x - min_x + 1
    ny = max_y - min_y + 1

    # create the base image for the composite
    # this allows for a 1px gap between tiles

    image_width  = nx * (image_size + 1) + 1
    image_height = ny * (image_size + 1) + 1

    base_image = Image.new('RGBA', (image_width, image_height), (0,0,0))

    y = 1
    tile_y = min_y
    for i in range(ny):
      x = 1
      tile_x = min_x
      for j in range(nx):
        tile_id = "{}-{}-{}".format(zoom, tile_x, tile_y)
        img_path = os.path.join(tile_dir, "{}.jpg".format(tile_id))
        img = Image.open(img_path)
        img = img.resize((image_size, image_size), Image.ANTIALIAS)
        base_image.paste(img, (x, y))
        x += image_size + 1
        tile_x += 1

      y += image_size + 1
      tile_y += 1

    base_image.show()


main()
