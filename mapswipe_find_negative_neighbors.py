#!/usr/local/bin/python3

# mapswipe_find_negative_neighbors.py

# Copyright 2017  Robert Jones  jones@craic.com

# Project repo: https://github.com/craic/mapswipe_utils

# Released under the terms of the MIT License

# Given a mapswipe project json file and a file of positive tiles, look for
# tiles near to the positives that are not explicitly tagged as positive, ambiguous or bad imagery
# and therefore they should be negatives

# The Output is a list of tile IDs, one per line

import argparse
import sys
import os
import json
import random


# Given a tile ID find a neighbor that is not in the dict
# This searches systematically for an immediate neighbor
# if it can't find one then it searches systematically 2 tiles away
# if it can't find one then it looks at random tiles up to 5 tiles away
# if it can't find one then it looks at random tiles up to 50 tiles away
#
# The idea is that we want to select negative tiles that are likely to have
# similar terrain to the positives
#
# This approach seems to work well in practice

def find_neighbor(all_tile_ids, tile_id):
    # split the id
    fields = tile_id.split('-')
    zoom   = int(fields[0])
    tile_x = int(fields[1])
    tile_y = int(fields[2])

    # explore 1 unit away in clockwise order N, NE, E, SE etc
    x_steps_1 = [  0,  1,  1,  1,  0, -1, -1, -1 ]
    y_steps_1 = [ -1, -1,  0,  1,  1,  1,  0, -1 ]

    new_id = ''
    neighbors = []
    flag = 0
    for i in range(len(x_steps_1)):
      new_x = tile_x + x_steps_1[i]
      new_y = tile_y + y_steps_1[i]
      new_id = "{}-{}-{}".format(zoom, str(new_x), str(new_y))
      if new_id not in all_tile_ids:
        neighbors.append(new_id)

    # if one or more neighbors exists then pick one at random
    if len(neighbors) == 1:
      new_id = neighbors[0]
      all_tile_ids[new_id] = 1
      flag = 1
    elif len(neighbors) > 1:
      new_id = random.choice(neighbors)
      all_tile_ids[new_id] = 1
      flag = 1


    # if not then look for one 2 steps away
    if flag == 0:
      x_steps_2 = [  0,  1,  2,  2,  2,  2,  2,  1,  0, -1, -2, -2, -2, -2, -2, -1 ]
      y_steps_2 = [ -2, -2, -2, -1,  0,  1,  2,  2,  2,  2,  2,  1,  0, -1, -2, -2 ]

      for i in range(len(x_steps_2)):
        new_x = tile_x + x_steps_2[i]
        new_y = tile_y + y_steps_2[i]
        new_id = "{}-{}-{}".format(zoom, str(new_x), str(new_y))
        if new_id not in all_tile_ids:
          neighbors.append(new_id)

      # if one or more neighbors exists then pick one at random

      if len(neighbors) == 1:
        new_id = neighbors[0]
        all_tile_ids[new_id] = 1
        flag = 1
      elif len(neighbors) > 1:
        new_id = random.choice(neighbors)
        all_tile_ids[new_id] = 1
        flag = 1

    # generate random x and y within 5 tiles...
    if flag == 0:
      radius = 5
      for i in range(200):
        new_x = tile_x + (random.randint(-radius, radius))
        new_y = tile_y + (random.randint(-radius, radius))
        new_id = "{}-{}-{}".format(zoom, str(new_x), str(new_y))
        # pick the first one
        if new_id not in all_tile_ids:
          all_tile_ids[new_id] = 1
          flag = 1
          break

    if flag == 0:
      radius = 50
      for i in range(200):
        new_x = tile_x + (random.randint(-radius, radius))
        new_y = tile_y + (random.randint(-radius, radius))
        new_id = "{}-{}-{}".format(zoom, str(new_x), str(new_y))
        # pick the first one
        if new_id not in all_tile_ids:
          all_tile_ids[new_id] = 1
          flag = 1
          break

    # report if we can't find a neighbor
    if flag == 0:
      print("{} has no neighbor".format(tile_id), file=sys.stderr)

    return new_id



def main():
    parser = argparse.ArgumentParser(description="Identify negative MapSwipe tiles near to positive tiles")
    parser.add_argument('--jsonfile', '-f', metavar='<json_file>', required=True,
                        help='MapSwipe Project JSON file')
    parser.add_argument('--tilelist', '-p', metavar='<tile_id_file>', required=True,
                        help='File of positive tile IDs')

    args = parser.parse_args()
    json_file = args.jsonfile
    tile_list_file = args.tilelist


    all_tile_ids = {}
    positive_tile_ids = []

    # Load all the IDs from the JSON file
    with open(json_file, 'rt') as f:
      json_text = f.read()

      tiles = json.loads(json_text)
      for tile in tiles:
        all_tile_ids[tile['id']] = 1

    # Load the positive IDs
    with open(tile_list_file, 'rt') as f:
        positive_tile_ids = f.read().splitlines()

    # For each positive, calculate neighbors and pick one at random

    for tile_id in positive_tile_ids:
      # calculate a neighbor
      new_id = find_neighbor(all_tile_ids, tile_id)
      print(new_id)


main()


