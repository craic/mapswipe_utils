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

If you are not familar with the MapSwipe mobile app then I recommend you install that and spend a bit of
time using it on a current project. That will help you understand some of the concepts described below.

This project is very much a **work in progress** and things will change without notice.

## MapSwipe Machine Learning

These utilities were written to support work on machine learning with the MapSwipe data.

That repository is [mapswipe_convnet](https://github.com/craic/mapswipe_convnet)


## MapSwipe Resources

Here are the main MapSwipe resources:

[MapSwipe web site](http://mapswipe.org/)

[MapSwipe Github repository](https://github.com/mapswipe)

[MapSwipe Analytics](http://mapswipe.geog.uni-heidelberg.de/) at Heidelberg University in Germany

[MapSwipe API document](https://docs.google.com/document/d/1RwN4BNhgMT5Nj9EWYRBWxIZck5iaawg9i_5FdAAderw/edit#heading=h.wp1a8ue6nwhv)


## MapSwipe Data Concepts

The basic idea behind MapSwipe is straightforward. A project defines a geographic region, typically a rural area in a eveloping country,
that needs mapping. Specifically a project will aim to identify buildings and/or roads. Most projects aim to identify buildings.

Tile images from Bing Maps that lie in this region are presented by the mobile app to the user who is tasked with making one of three
assignments for each tile. These are:
- Yes/Positive - the tile contains one or more buildings
- Maybe/Ambiguous - the tile contains something that might be a building
- Bad Imagery - the image is obscured by cloud or the image is missing

Note that the system does not explicitly track images that do not contain a building. The fact that a set of tiles was presented to the user who
did not tag them is an implicit negative assignment.

A given set of tiles is typically presented to multiple users. The same assignment for a tile from multiple users adds confidence in that assignment.

The MapSwipe server collects the assignments and makes them available to downstream map creators as part of the Missing Maps project.

MapSwipe also makes these assignments publicly available as JSON files as described in the
[MapSwipe API document](https://docs.google.com/document/d/1RwN4BNhgMT5Nj9EWYRBWxIZck5iaawg9i_5FdAAderw/edit#heading=h.wp1a8ue6nwhv).

The JSON record for a given tile looks like this:

```json
  {
    "bad_imagery_count": 0,
    "maybe_count": 0,
    "yes_count": 3,
    "id": "18-134732-123781",
    "user_id": "eaJS1LL3nUVftxLC7iltRh5be493",
    "project": 7260,
    "timestamp": 1499342969729,
    "task_x": "134732",
    "task_y": "123781",
    "task_z": "18",
    "decision": 1
  },
```
The terms task_x and task_y define the Bing Maps tile at a given zoom level (task z).
Taken together these create a unique tile ID

```json
    "task_x": "134732",
    "task_y": "123781",
    "task_z": "18",

    ...become...

    "id": "18-134732-123781"
```

The terms yes_count, maybe_count and bad_imagery_count represent the assignments for this tile and these are evaluated to produce an
aggregate decision, where 1 is a positive/yes call, 2 is maybe/ambiguous and 3 is a bad image
```json
    "bad_imagery_count": 0,
    "maybe_count": 0,
    "yes_count": 3,

    ...become...

    "decision": 1
```


Publicly available MapSwipe data can be found at two locations:

[MapSwipe Analytics](http://mapswipe.geog.uni-heidelberg.de/) provides a map of locations of MapSwipe projects around the world and offers
several types of data for each project.

[http://api.mapswipe.org](http://api.mapswipe.org) provides JSON formatted data on specific projects. Note that this site does not provide an
index of its resources.


## Project Directory Structure

The directory structure that I use for a single MapSwipe project is as follows:

```
./projects/<project_id>
    README
    project.json
    all_positive_tiles.lst
    all_ambiguous_tiles.lst
    all_bad_image_tiles.lst
    selected_positive_tiles.lst
    selected_negative_tiles.lst
    positive_tiles    - directory
    negative_tiles    - directory
    [...]
```


## Utility Scripts

todo - add list of modules that need to be installed...

### mapswipe_fetch_project_json.py

```
$ ./mapswipe_fetch_project_json.py --help
usage: mapswipe_fetch_project_json.py [-h] --project <project_id>
                                      [--outdir <output_directory>]

Fetch the JSON file for a MapSwipe Project

optional arguments:
  -h, --help            show this help message and exit
  --project <project_id>, -p <project_id>
                        MapSwipe Project ID to retrieve
  --outdir <output_directory>, -o <output_directory>
                        Output directory in which to store downloaded data.
                        Default: "."
```

For example:

```
$ ./mapswipe_fetch_project_json.py --project 7260 --outdir .
```

### mapswipe_filter_tile_list.py

```
$ ./mapswipe_filter_tile_list.py --help
usage: mapswipe_filter_tile_list.py [-h] --jsonfile <project_json_file>
                                    --tilelist <tile_list_file>
                                    --attribute <json_attribute>
                                    --value <value>
                                    --operator <operator>

Filter a list of MapSwipe Tile IDs using user-supplied criteria

optional arguments:
  -h, --help            show this help message and exit
  --jsonfile <project_json_file>, -j <project_json_file>
                        MapSwipe Project JSON file
  --tilelist <tile_list_file>, -t <tile_list_file>
                        Output directory in which to store downloaded data.
                        Default: "."
  --attribute <json_attribute>, -a <json_attribute>
                        Name of JSON attribute to filter on
  --value <value>, -v <value>
                        value
  --operator <operator>, -o <operator>
                        Operator [lt, le, eq, ge, gt]
```

For example:

```
$ ./mapswipe_filter_tile_list.py --json project.json \
         --tilelist all_positive_tiles.lst \
         --operator gt --attr yes_count --value 2 > selected_positive_tiles.lst
```

### mapswipe_fetch_tiles.py

To access Bing Maps image tiles you will need a Bing Maps API key which you can create, for free, at the
[Bing Maps Developer Site](https://www.bingmapsportal.com/). This allows you to access up to 50,000 tiles
per day - which is easy to exceed.

```
$ ./mapswipe_fetch_tiles.py --help
usage: mapswipe_fetch_tiles.py [-h] --tilelist <tile_list_file>
                               [--outdir <output_directory>]
                               --keyfile <bing maps key file>

Fetch a list of Bing Maps image tiles

optional arguments:
  -h, --help            show this help message and exit
  --tilelist <tile_list_file>, -t <tile_list_file>
                        MapSwipe Project Tile List file
  --outdir <output_directory>, -o <output_directory>
                        Output directory to download to. Default: "."
  --keyfile <bing maps key file>, -k <bing maps key file>
                        File containing the Bing maps API key
```

For example:

```
$ ./mapswipe_fetch_tiles.py --keyfile maps_api_key --outdir positive_tiles --tilelist positive_tile.lst
```

### mapswipe_fetch_tile_block.py

Fetch a rectangular block of Bing Maps image tiles

```
$ ./mapswipe_fetch_tile_block.py --help
usage: mapswipe_fetch_tile_block.py [-h] [--outdir <output_directory>]
                                    --keyfile <bing maps key file>
                                    --x <x dimension low bound tile id>
                                    --y <y dimension low bound tile id>
                                    --nx <number of tiles in x dimension>
                                    --ny <number of tiles in y dimension>
                                    [--zoom <bing maps zoom level>]

Fetch a block of Bing Maps image tiles

optional arguments:
  -h, --help            show this help message and exit
  --outdir <output_directory>, -o <output_directory>
                        Output directory to download to. Default: "."
  --keyfile <bing maps key file>, -k <bing maps key file>
                        File containing the Bing maps API key
  --x <x dimension low bound tile id>
                        X dimension lower bound
  --y <y dimension low bound tile id>
                        Y dimension lower bound
  --nx <number of tiles in x dimension>
                        number of tiles in X dimension
  --ny <number of tiles in y dimension>
                        number of tiles in Y dimension
  --zoom <bing maps zoom level>
                        Bing Maps zoom level - default 18
```




### mapswipe_find_negative_neighbors.py

For machine learning we need a set of negative image tiles as well as the positives.
The MapSwipe API does not explicitly list negative tiles so we need to look for them
and this script tries to find them in the immediate vicinity of each positive tile.

The rationale behind this is that nearby tiles should have similar terrain.

```
$ ./mapswipe_find_negative_neighbors.py --help
usage: mapswipe_find_negative_neighbors.py [-h] --jsonfile <json_file>
                                           --tilelist <tile_id_file>

Identify negative MapSwipe tiles near to positive tiles

optional arguments:
  -h, --help            show this help message and exit
  --jsonfile <json_file>, -f <json_file>
                        MapSwipe Project JSON file
  --tilelist <tile_id_file>, -p <tile_id_file>
                        File of positive tile IDs
```

For example:

```
$ ./mapswipe_find_negative_neighbors.py --jsonfile project.json --tilelist positive_tiles.lst > negative_tiles.lst
```

### mapswipe_display_grid_random_tiles.py

This displays a grid of image tiles selected at random from a file of tile IDs.
I use it to get a sense of the images in a particular set.

```
$ ./mapswipe_display_grid_random_tiles.py --help
usage: mapswipe_display_grid_random_tiles.py [-h] --tile_list_file <tile_list_file>
                                     --tile_dir <tile_directory> --width
                                     <width> --height <height>

optional arguments:
  -h, --help            show this help message and exit
  --tile_list_file <tile_list_file>, -f <tile_list_file>
                        MapSwipe Project Tile List file
  --tile_dir <tile_directory>, -d <tile_directory>
                        Directory of tile images
  --nx <nx>, -x <nx>    Number of tiles in X dimension
  --ny <ny>, -y <ny>    Number of tiles in Y dimension
```

For example:

```
$ ./mapswipe_display_grid_random_tiles.py --tiledir positive_tiles  --tilelist all_positive_tiles.lst --nx 4 --ny 2
```

### mapswipe_partition_tiles.py

Given directories of positive and negative image tiles, partition these into training, validation and test directories
for use as input for machine learning code. The user can specify the fraction of each input set that goes to each target set.

The test set can be empty. It is simply the remainder after the training and validation sets are assigned.

```
./mapswipe_partition_tiles.py --help
usage: mapswipe_partition_tiles.py [-h] --positives <directory_of_positives>
                                   --negatives <directory_of_negatives>
                                   --outdir <output_directory>
                                   [--train_frac <fraction for training>]
                                   [--validation_frac <fraction for validation>]

optional arguments:
  -h, --help            show this help message and exit
  --positives <directory_of_positives>, -p <directory_of_positives>
                        Directory of Positive images
  --negatives <directory_of_negatives>, -n <directory_of_negatives>
                        Directory of Negative images
  --outdir <output_directory>, -o <output_directory>
                        Output Directory
  --train_frac <fraction for training>, -t <fraction for training>
                        Fraction of images to use for training
  --validation_frac <fraction for validation>, -v <fraction for validation>
                        Fraction of images to use for validation
```

For example:

```
$ ./mapswipe_partition_tiles.py --positives positive_tiles --negative negative_tiles \
     --outdir test --train_frac 0.8 --validation_frac 0.2
```
