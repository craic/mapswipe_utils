# Mapswipe Tools

A collection of python scripts for working with Mapswipe project files and Bing Maps image tiles


- Download a project JSON file and create a local project directory
  select positive tiles based on a cutoff

- project stats

- select positive tiles
- select negative tiles
- fetch tiles using a list file

- grid and display a random set of tile images

- convert from lat long to tile id
- convert from tile_id to lat long


-- partition images tiles for a machine learning expt

? split image tiles into multiple subdirectories ?
keep it simple - 10 subdirs
18-135203-123552.jpg
        ^----------------> /3/
               ^---------> /2/

Project directory structure

<project id>
  README
  project.json

  positive_tiles
  negative_tiles

  positive_tiles.lst
  negative_tiles.lst
  ambiguous_tiles.lst
  bad_imagery_tiles.lst

... OR ...

/projects/<project id>

  README
  project.json

  all_positive_tiles.lst ... ALL positive tiles
  all_ambiguous_tiles.lst
  all_bad_image_tiles.lst

  .... after applying a filter
  selected_positive_tiles.lst
  selected_negative_tiles.lst ... based on selected_positive_tiles.lst

  selected_positive_tiles ... just download the selected tiles
  selected_negative_tiles

