#!/usr/local/bin/python3

# Fetch a project JSON file and write list files for
# positive, ambiguous and bad tiles

# change it to read from a downloaded json file...

import argparse
import sys
import os
import json
import urllib.request

# Uses the mapswipe API as defined in: https://docs.google.com/document/d/1RwN4BNhgMT5Nj9EWYRBWxIZck5iaawg9i_5FdAAderw/

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


mapswipe_project_url = ''

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--project-id', metavar='<project_id>', type=int, required=True,
                        help='MapSwipe Project ID to retrieve')
    parser.add_argument('--min-positive', metavar='<min_positive>', type=int, default=1,
                        help='Minimum count of positives')

    parser.add_argument('--output-dir', '-p', metavar='<output_directory>', default='projects',
                        help='Output directory in which to store downloaded data. Default: "projects".')


    args = parser.parse_args()

    min_positive_count = int(args.min_positive)

    # does projects_dir exist?
    if not os.path.isdir(args.output_dir):
      print("Error: output_dir does not exist")
      exit()

    # does project subdirectory exist? if not then create it
    project_path = os.path.join(args.output_dir, str(args.project_id))
    if not os.path.isdir(project_path):
        os.makedirs(project_path)

    # target URL
    url_string = "http://api.mapswipe.org/projects/{}.json".format(args.project_id)

    # print(url_string)

    categories = ['positive', 'ambiguous', 'bad']
    tile_category = {}
    for category in categories:
      tile_category[category] = []


    with urllib.request.urlopen(url_string) as url:
      json_text = url.read().decode()

      # dump the raw json to a file
      json_out_path = os.path.join(project_path, "project_{}.json".format(args.project_id))
      with open(json_out_path, 'wt') as f:
        f.write(json_text)

      # partition tiles into positive, ambiguous, bad categories
      # - and require a yes_count of at least 2...
      tiles = json.loads(json_text)
      for tile in tiles:
        decision = float(tile['decision'])
        if decision <= 1.0:
          # ----------------------------------->>>>
          if int(tile['yes_count']) >= min_positive_count:
            tile_category['positive'].append(tile['id'])
          else:
            tile_category['ambiguous'].append(tile['id'])
        elif decision <= 2.0:
          tile_category['ambiguous'].append(tile['id'])
        else:
          tile_category['bad'].append(tile['id'])

    # write the tile ids to files
    for category in categories:
      tile_out_path = os.path.join(project_path, "{}_tiles.lst".format(category))
      with open(tile_out_path, 'wt') as f:
        for tile_id in sorted(tile_category[category]):
          f.write(tile_id + '\n')

    # write a basic README file
    readme_path = os.path.join(project_path, "README")
    text = "Project JSON file downloaded from {}\n\n".format(url_string)
    with open(readme_path, 'wt') as f:
      f.write(text)


main()
