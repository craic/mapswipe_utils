#!/usr/local/bin/python3

# Copyright 2017  Robert Jones  jones@craic.com

# Project repo: https://github.com/craic/mapswipe_utils

# Released under the terms of the MIT License

# mapswipe_fetch_single_tile.py

#Fetch a single Bing maps tile

import argparse
import sys
import os
import urllib.request



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
    parser = argparse.ArgumentParser()
    parser.add_argument('--tileid', '-f', metavar='<tile_id>', required=True,
                        help='Tile ID')
    parser.add_argument('--outdir', '-o', metavar='<output_directory>', default='tiles',
                        help='Output directory to download to. Default: "."')
    parser.add_argument('--keyfile', '-k', metavar='<bing maps key file>', required=True,
                        help='File containing the Bing maps API key')
    args = parser.parse_args()

    # get the bing maps api key
    try:
        f = open(args.keyfile)
        bing_maps_api_key = f.read()
    except:
        print ("Problem reading Bing Maps API key")

    #create output directory if it doesn't exist
    output_dir = args.outdir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    tile_id = args.tileid

    a = tile_id.split('-')
    zoom   = int(a[0])
    tile_x = int(a[1])
    tile_y = int(a[2])
    quadkey = tile_coords_and_zoom_to_quadkey(tile_x, tile_y, zoom)

    tile_url = "http://t0.tiles.virtualearth.net/tiles/a{}.jpeg?g=854&mkt=en-US&token={}".format(quadkey, bing_maps_api_key)

    output_file_path = os.path.join(output_dir, "{}.jpg".format(tile_id))

    # Do we already have this file ?
    if not os.path.exists(output_file_path):
        local_filename, headers = urllib.request.urlretrieve(tile_url, output_file_path)


main()
