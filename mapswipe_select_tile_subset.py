#!/usr/local/bin/python3

# mapswipe_select_tile_subset.py

# Copyright 2017  Robert Jones  jones@craic.com

# Project repo: https://github.com/craic/mapswipe_utils

# Released under the terms of the MIT License

# Given a directory of bing tile images and a file of tile ids,
# Copy selected tiles to the output directory
# includes an --action arg to include or exclude the list

# tilelist can be a list of :
#  tile_IDs     e.g. 18-146363-145067
#  file names   e.g. 18-146363-145067.jpg
#  CSV lines where the ID is the first field
#     e.g. 18-147207-144806,positive

import argparse
import sys
import os
import shutil
import re


def main():
    parser = argparse.ArgumentParser(description="Select a subset of map tiles based on a file of tile IDs")

    parser.add_argument('--tilelist', '-t', metavar='<tile_list_file>', required=True,
                        help='File of tile IDs')


    parser.add_argument('--indir', '-i', metavar='<input_directory>', required=True,
                        help='Input Directory')
    parser.add_argument('--outdir', '-o', metavar='<output_directory>', required=True,
                        help='Output Directory')

    parser.add_argument('--action', '-a', metavar='<action>', default='include',
                        help='action is to include (default) or exclude the supplied tile IDs')


    args = parser.parse_args()


    tile_list_file = args.tilelist
    input_dir      = args.indir
    output_dir     = args.outdir
    action         = args.action


    # Load the tile IDs
    # tile ID is the first field
    tile_ids = []
    lines = []
    with open(tile_list_file, 'rt') as f:
        lines = f.read().splitlines()

    # Handle various inputs - extract IDs like 18-147209-144812
    tile_id_pattern = re.compile(r'^(\d+-\d+-\d+)')
    for line in lines:
        m = tile_id_pattern.search(line)
        if m:
            tile_ids.append(m.group(0))

    tile_hash = {}
    for tile_id in tile_ids:
        tile_hash[tile_id] = 1

    # create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # List the input directory and copy files if appropriate

    for filename in os.listdir(input_dir):
        if filename.endswith(".jpg"):
            input_id = filename.replace('.jpg', '')
            if input_id in tile_hash:
                if action == 'include':
                    src = os.path.join(input_dir,  filename)
                    dst = os.path.join(output_dir, filename)
                    shutil.copyfile(src, dst)
            else:
                if action == 'exclude':
                    src = os.path.join(input_dir,  filename)
                    dst = os.path.join(output_dir, filename)
                    shutil.copyfile(src, dst)


main()
