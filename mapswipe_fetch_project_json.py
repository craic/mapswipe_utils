#!/usr/local/bin/python3

# Copyright 2017  Robert Jones  jones@craic.com

# Project repo: https://github.com/craic/mapswipe_utils

# Released under the terms of the MIT License

# Fetch a project JSON file and write list files for
# positive, ambiguous and bad tiles

# Fetch JSON file from api.mapswipe.org  e.g. http://api.mapswipe.org/projects/4877.json

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



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--project', '-p', metavar='<project_id>', type=int, required=True,
                        help='MapSwipe Project ID to retrieve')

    parser.add_argument('--outdir', '-o', metavar='<output_directory>', default='.',
                        help='Output directory in which to store downloaded data. Default: "."')


    args = parser.parse_args()

    project_id = str(args.project)
    output_dir = args.outdir

    # does projects_dir exist?
    if not os.path.isdir(output_dir):
      print("Error: output_dir does not exist")
      exit()

    # does project subdirectory exist? if not then create it
    project_path = os.path.join(output_dir, project_id)
    if not os.path.isdir(project_path):
        os.makedirs(project_path)


    categories = ['positive', 'ambiguous', 'bad']
    tile_category = {}
    for category in categories:
      tile_category[category] = []

    # construct the URL
    api_url = "http://api.mapswipe.org/projects/"
    url_string = "{}{}.json".format(api_url, project_id)

    # fetch the JSON file and partition the tile_ids into 3 arrays
    with urllib.request.urlopen(url_string) as url:
      json_text = url.read().decode()

      # dump the raw json to a file
      json_out_path = os.path.join(project_path, "project.json".format(project_id))
      with open(json_out_path, 'wt') as f:
        f.write(json_text)

      # partition tile ids into positive, ambiguous, bad categories
      tiles = json.loads(json_text)
      for tile in tiles:
        decision = float(tile['decision'])
        if decision <= 1.0:
          tile_category['positive'].append(tile['id'])
        elif decision <= 2.0:
          tile_category['ambiguous'].append(tile['id'])
        else:
          tile_category['bad'].append(tile['id'])

    # write the tile ids to files
    for category in categories:
      tile_out_path = os.path.join(project_path, "all_{}_tiles.lst".format(category))
      with open(tile_out_path, 'wt') as f:
        for tile_id in sorted(tile_category[category]):
          f.write(tile_id + '\n')

    # write a basic README file
    readme_path = os.path.join(project_path, "README")
    text = "MapSwipe Project {}\n\nproject JSON file downloaded from {}\n\n".format(project_id, url_string)
    with open(readme_path, 'wt') as f:
      f.write(text)


main()
