#!/usr/local/bin/python3

# mapswipe_filter_tile_list.py

# Copyright 2017  Robert Jones  jones@craic.com

# Project repo: https://github.com/craic/mapswipe_utils

# Released under the terms of the MIT License

# Given a list of bing map tiles and a mapswipe project JSON file
# output those that match the supplied constraints
# For example: yes_count >= 3
#              task_y eq 123699

# It's primary use is to filter a list of tiles based on the yes_count
# but the other modea might be useful at times


# --attribute
# --value
# --operator   lt, le, eq, ge, gt

# Can only be applied to numeric attributes
#   bad_imagery_count
#   maybe_count
#   yes_count
#   task_x
#   task_y
#   task_z

# This could be done using 'jq' but the syntax of that is realtively complex

# The mapswipe API is defined in:
# https://docs.google.com/document/d/1RwN4BNhgMT5Nj9EWYRBWxIZck5iaawg9i_5FdAAderw/

# example record
# {
#   "bad_imagery_count": 0,
#   "maybe_count": 0,
#   "yes_count": 8,
#   "id": "18-86142-119266",
#   "user_id": "3tE8WVBSUoOImzL1fDZVsSBOoSH2",
#   "project": 8210,
#   "timestamp": 1505686483197,
#   "task_x": "86142",
#   "task_y": "119266",
#   "task_z": "18",
#   "decision": 1
# },

import argparse
import sys
import os
import json
import urllib.request


def check_tile_info(tile, attribute_name, operator, value):
    result = False
    if operator == 'lt':
      if int(tile[attribute_name]) < value:
        result = True
    elif operator == 'le':
      if int(tile[attribute_name]) <= value:
        result = True
    elif operator == 'eq':
      if int(tile[attribute_name]) == value:
        result = True
    elif operator == 'ge':
      if int(tile[attribute_name]) >= value:
        result = True
    elif operator == 'gt':
      if int(tile[attribute_name]) > value:
        result = True

    return result



def main():
    parser = argparse.ArgumentParser(description="Filter a list of MapSwipe Tile IDs using user-supplied criteria")
    parser.add_argument('--jsonfile', '-j', metavar='<project_json_file>', required=True,
                        help='MapSwipe Project JSON file')

# need this ? - yes
    parser.add_argument('--tilelist', '-t', metavar='<tile_list_file>', required=True,
                        help='Output directory in which to store downloaded data. Default: "."')

    parser.add_argument('--attribute', '-a', metavar='<json_attribute>', required=True,
                        help='Name of JSON attribute to filter on')
    parser.add_argument('--value', '-v', metavar='<value>', type=int, required=True,
                        help='value')
    parser.add_argument('--operator', '-o', metavar='<operator>', required=True,
                        help='Operator [lt, le, eq, ge, gt]')


    args = parser.parse_args()

    valid_attributes = [ 'bad_imagery_count', 'maybe_count', 'yes_count', 'task_x', 'task_y', 'task_z' ]
    valid_operators  = [ 'lt', 'le', 'eq', 'ge', 'gt' ]


    tile_list_file = args.tilelist
    json_file      = args.jsonfile
    attribute_name = args.attribute
    value          = int(args.value)
    operator       = args.operator

    # check for valid attributes and operators
    if not attribute_name in valid_attributes:
        sys.stderr.write("ERROR: invalid attribute: {}\n".attribute_name)
        exit()
    if not operator in valid_operators:
        sys.stderr.write("ERROR: invalid operators: {}\n".operator)
        exit()

    output_tile_ids = []

    # Load the tile IDs
    tile_ids = []
    with open(tile_list_file, 'rt') as f:
        tile_ids = f.read().splitlines()

    # Load in the project JSON
    with open(json_file, 'rt') as f:
      json_text = f.read()

      tiles = json.loads(json_text)

      for tile in tiles:
          if tile['id'] in tile_ids:
              result = check_tile_info(tile, attribute_name, operator, value)
              if result is True:
                output_tile_ids.append(tile['id'])

    # output the tile_ids
    for tile_id in output_tile_ids:
        print(tile_id)

main()
