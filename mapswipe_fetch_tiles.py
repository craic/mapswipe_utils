#!/usr/local/bin/python3

# Copyright 2017  Robert Jones  jones@craic.com

# Project repo: https://github.com/craic/mapswipe_utils

# Released under the terms of the MIT License

# mapswipe_fetch_tiles.py

# Given a file of MapSwipe tile IDs, fetch them and output to a directory

# This script is based on
# https://github.com/mapswipe/tile-downloader by Ivan Gayton
# https://github.com/philiptromans/mapswipe-ml-dataset-generator by Philip Tromans

# The Bing Maps API key file contains a single line with the api key

import argparse
import sys
import os
import urllib.request
import datetime
import time
import math


# Convert Tile X and Y to a Bing Maps Quadkey which is used to retrieve a tile
def tile_coords_and_zoom_to_quadkey(x, y, zoom):
    quadkey = ''
    for i in range(zoom, 0, -1):
        digit = 0
        mask = 1 << (i - 1)
        if(x & mask) != 0:
            digit += 1
        if(y & mask) != 0:
            digit += 2
        quadkey += str(digit)
    return quadkey



def main():
    parser = argparse.ArgumentParser(description="Fetch a list of Bing Maps image tiles")
    parser.add_argument('--tilelist', '-t', metavar='<tile_list_file>', required=True,
                        help='MapSwipe Project Tile List file')
    parser.add_argument('--outdir', '-o', metavar='<output_directory>', default='.',
                        help='Output directory to download to. Default: "."')
    parser.add_argument('--keyfile', '-k', metavar='<bing maps key file>', required=True,
                        help='File containing the Bing maps API key')
    args = parser.parse_args()

    output_dir = args.outdir
    tile_id_file = args.tilelist

    # get the bing maps api key
    try:
        f = open(args.keyfile)
        bing_maps_api_key = f.read()
    except:
        print ("Problem reading Bing Maps API key")

    # Bing Maps limits access to 50,000 records per day so spread them out
    request_delay = 1 + math.ceil((24.0 * 60.0 * 60.0) / 50000)

    #create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    tile_ids = []

    with open(tile_id_file, 'rt') as f:
        # read each line and decode
        tile_ids = f.read().splitlines()

    i = 0
    for tile_id in tile_ids:
        a = tile_id.split('-')
        zoom   = int(a[0])
        tile_x = int(a[1])
        tile_y = int(a[2])
        quadkey = tile_coords_and_zoom_to_quadkey(tile_x, tile_y, zoom)

        # construct the Bing Maps URL
        tile_url = "http://t0.tiles.virtualearth.net/tiles/a{}.jpeg?g=854&mkt=en-US&token={}".format(quadkey, bing_maps_api_key)

        output_file_path = os.path.join(output_dir, "{}.jpg".format(tile_id))

        # Skip this tile if we already downloaded it
        if os.path.exists(output_file_path):
            print("skip {}".format(tile_id))
            continue

        local_filename, headers = urllib.request.urlretrieve(tile_url, output_file_path)

        # report progress every 25 tiles
        i += 1
        if i % 25 == 0:
            print("{} tiles".format(i))

        # pause before getting the next one
        time.sleep(request_delay)

main()
