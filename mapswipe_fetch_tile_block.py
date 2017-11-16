#!/usr/local/bin/python3

# Copyright 2017  Robert Jones  jones@craic.com

# Project repo: https://github.com/craic/mapswipe_utils

# Released under the terms of the MIT License

# mapswipe_fetch_tile_block.py

# Fetc a rectangular block of Bing Map image tiles given the bounds

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
    parser = argparse.ArgumentParser(description="Fetch a block of Bing Maps image tiles")
    parser.add_argument('--outdir', '-o', metavar='<output_directory>', default='.',
                        help='Output directory to download to. Default: "."')
    parser.add_argument('--keyfile', '-k', metavar='<bing maps key file>', required=True,
                        help='File containing the Bing maps API key')
    parser.add_argument('--x', metavar='<x dimension low bound tile id>', required=True,
                        help='X dimension lower bound')
    parser.add_argument('--y', metavar='<y dimension low bound tile id>', required=True,
                        help='Y dimension lower bound')

    parser.add_argument('--nx', metavar='<number of tiles in x dimension>', required=True,
                        help='number of tiles in X dimension')
    parser.add_argument('--ny', metavar='<number of tiles in y dimension>', required=True,
                        help='number of tiles in Y dimension')

    parser.add_argument('--zoom', metavar='<bing maps zoom level>', default=18, type=int,
                        help='Bing Maps zoom level - default 18')


    args = parser.parse_args()

    output_dir = args.outdir

    # tile id bounds are inclusive
    x_lo = int(args.x)
    y_lo = int(args.y)

    nx = int(args.nx)
    ny = int(args.ny)
    zoom = int(args.zoom)

    # get the bing maps api key
    try:
        f = open(args.keyfile)
        bing_maps_api_key = f.read()
    except:
        print ("Problem reading Bing Maps API key")

    # Bing Maps limits access to 50,000 records per day so spread them out
    # Not necessary for this script
    request_delay = math.ceil((24.0 * 60.0 * 60.0) / 50000)

    #create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Generate a list of the tile ids
    tile_ids = []

    for y in range(y_lo, y_lo+ny):
        for x in range(x_lo, x_lo+nx):
            tile_id = "{}-{}-{}".format(zoom, x, y)
            tile_ids.append(tile_id)
            # print(tile_id)

    # Fetch the tiles

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

        # # report progress every 25 tiles
        # i += 1
        # if i % 25 == 0:
        #     print("{} tiles".format(i))

        # pause before getting the next one
        time.sleep(request_delay)

main()
