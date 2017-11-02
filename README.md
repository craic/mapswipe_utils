# Mapswipe Tools

A collection of python scripts for working with Mapswipe project files and Bing Maps image tiles




## Background

The [MapSwipe](http://mapswipe.org/) project uses a community of volunteers to tag
satellite imagery displayed in a mobile phone app with features such as buildings and roads.

This human annotation of map image tiles, from Microsoft's [Bing Maps](https://www.bingmapsportal.com/),
helps other volunteers in the [Missing Maps](http://www.missingmaps.org/) project
to create maps of parts of the world where these are missing. In doing so they help humanitarian groups
working in the field deliver humanitarian aid.

I am interested in using machine learning and image processing techniques to help the MapSwipe project, perhaps through
validation and/or augmentation of the existing approach.

Automated annotation of satellite image tiles is an interesting application of machine learning. The large datasets
of annotations by MapSwipe volunteers combined with the image tiles, from Bing Maps, form a rich basis for this type
of application.

This repository contains a number of utility functions that can be used to prepare and analyze MapSwipe datasets.

I am also a user of the MapSwipe mobile app.

This project is very much a **work in progress**


## MapSwipe Resources

Here are some other MapSwipe resources:

[MapSwipe web site](http://mapswipe.org/)

[MapSwipe Github repository](https://github.com/mapswipe)

[MapSwipe API document](https://docs.google.com/document/d/1RwN4BNhgMT5Nj9EWYRBWxIZck5iaawg9i_5FdAAderw/edit#heading=h.wp1a8ue6nwhv)

[MapSwipe Analytics](http://mapswipe.geog.uni-heidelberg.de/) at Heidelberg University in Germany


## Code design

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

