# MapSwipe Tools

A collection of python scripts for working with MapSwipe project files and Bing Maps image tiles




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

This project is very much a **work in progress** and things will change without notice.


## MapSwipe Resources

Here are some other MapSwipe resources:

[MapSwipe web site](http://mapswipe.org/)

[MapSwipe Github repository](https://github.com/mapswipe)

[MapSwipe Analytics](http://mapswipe.geog.uni-heidelberg.de/) at Heidelberg University in Germany

[MapSwipe API document](https://docs.google.com/document/d/1RwN4BNhgMT5Nj9EWYRBWxIZck5iaawg9i_5FdAAderw/edit#heading=h.wp1a8ue6nwhv)


## MapSwipe Data

Publicly available MapSwipe data can be found at two locations:

[MapSwipe Analytics](http://mapswipe.geog.uni-heidelberg.de/) provides a map of locations of MapSwipe projects around the world and offers
several types of data for each project.

[http://api.mapswipe.org](http://api.mapswipe.org) provides JSON formatted data on specific projects. Note that this site does not provide an
index of its resources. Look at the
[MapSwipe API document](https://docs.google.com/document/d/1RwN4BNhgMT5Nj9EWYRBWxIZck5iaawg9i_5FdAAderw/edit#heading=h.wp1a8ue6nwhv)
for URLs to specific files.


## Data Concepts

[...]

## Project Directory Structure

The directory structure for a single MapSwipe project that I use is as follows:

```
./projects/<project_id>
    README
    project.json
    all_positive_tiles.lst
    all_ambiguous_tiles.lst
    all_bad_image_tiles.lst

```

[...]

## Utility Scripts

[...]

