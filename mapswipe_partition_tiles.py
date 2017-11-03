#!/usr/local/bin/python3

# mapswipe_partition_tiles.py

# Copyright 2017  Robert Jones  jones@craic.com

# Project repo: https://github.com/craic/mapswipe_utils

# Released under the terms of the MIT License

# Given two directories of positive and negative image tiles
# partition these for input to a Convolutional Nerual Network
# with three directories - train, validation and test
# User specifes the fraction of file for each of these

# This assumes that the number of positives and negatives are the same

# Output directory structure is
# /train
#    /positives
#    /negatives
# /validation
#    /positives
#    /negatives
# /test
#    /positives
#    /negatives

import argparse
import os, shutil



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--positives', '-p', metavar='<directory_of_positives>', required=True,
                        help='Directory of Positive images')
    parser.add_argument('--negatives', '-n', metavar='<directory_of_negatives>', required=True,
                        help='Directory of Negative images')
    parser.add_argument('--outdir', '-o', metavar='<output_directory>', required=True,
                        help='Output Directory')
    parser.add_argument('--train_frac', '-t', metavar='<fraction for training>', type=float,
                        help='Fraction of images to use for training', default=0.6)
    parser.add_argument('--validation_frac', '-v', metavar='<fraction for validation>', type=float,
                        help='Fraction of images to use for validation', default=0.2)


    args = parser.parse_args()

    positives_dir = args.positives
    negatives_dir = args.negatives
    output_dir = args.outdir

    positive_files = os.listdir(positives_dir)
    negative_files = os.listdir(negatives_dir)
    n_positive_files = len(positive_files)
    n_negative_files = len(negative_files)

    frac_train      = float(args.train_frac)
    frac_validation = float(args.validation_frac)
    if frac_train + frac_validation > 1.0:
        sys.stderr.write("ERROR: fraction arguments must be <= 1.0\n")
        exit()
    frac_test = 1.0 - (frac_train + frac_validation)

    #create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Directories for our training, validation and test splits

    train_dir = os.path.join(output_dir, 'train')
    if not os.path.exists(train_dir):
        os.makedirs(train_dir)

    train_positives_dir = os.path.join(train_dir, 'positives')
    if not os.path.exists(train_positives_dir):
        os.makedirs(train_positives_dir)

    train_negatives_dir = os.path.join(train_dir, 'negatives')
    if not os.path.exists(train_negatives_dir):
        os.makedirs(train_negatives_dir)


    validation_dir = os.path.join(output_dir, 'validation')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    validation_positives_dir = os.path.join(validation_dir, 'positives')
    if not os.path.exists(validation_positives_dir):
        os.makedirs(validation_positives_dir)

    validation_negatives_dir = os.path.join(validation_dir, 'negatives')
    if not os.path.exists(validation_negatives_dir):
        os.makedirs(validation_negatives_dir)


    test_dir = os.path.join(output_dir, 'test')
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

    test_positives_dir = os.path.join(test_dir, 'positives')
    if not os.path.exists(test_positives_dir):
        os.makedirs(test_positives_dir)

    test_negatives_dir = os.path.join(test_dir, 'negatives')
    if not os.path.exists(test_negatives_dir):
        os.makedirs(test_negatives_dir)


    train_n_positives      = int(n_positive_files * frac_train)
    validation_n_positives = int(n_positive_files * frac_validation)
    test_n_positives       = int(n_positive_files * frac_test)

    train_n_negatives      = int(n_negative_files * frac_train)
    validation_n_negatives = int(n_negative_files * frac_validation)
    test_n_negatives       = int(n_negative_files * frac_test)


    # Ideally this should partition files at random, using a seed for repreducibility

    for i in range(0,train_n_positives):
        filename = positive_files[i]
        src = os.path.join(positives_dir,       filename)
        dst = os.path.join(train_positives_dir, filename)
        shutil.copyfile(src, dst)

    j = train_n_positives
    k = j + validation_n_positives
    for i in range(j,k):
        filename = positive_files[i]
        src = os.path.join(positives_dir,       filename)
        dst = os.path.join(validation_positives_dir, filename)
        shutil.copyfile(src, dst)

    j = train_n_positives + validation_n_positives
    k = j + test_n_positives
    for i in range(j,k):
        filename = positive_files[i]
        src = os.path.join(positives_dir,       filename)
        dst = os.path.join(test_positives_dir, filename)
        shutil.copyfile(src, dst)


    negative_files = os.listdir(negatives_dir)

    for i in range(0,train_n_negatives):
        filename = negative_files[i]
        src = os.path.join(negatives_dir,       filename)
        dst = os.path.join(train_negatives_dir, filename)
        shutil.copyfile(src, dst)

    j = train_n_negatives
    k = j + validation_n_negatives
    for i in range(j,k):
        filename = negative_files[i]
        src = os.path.join(negatives_dir,       filename)
        dst = os.path.join(validation_negatives_dir, filename)
        shutil.copyfile(src, dst)

    j = train_n_negatives + validation_n_negatives
    k = j + test_n_negatives
    for i in range(j,k):
        filename = negative_files[i]
        src = os.path.join(negatives_dir,       filename)
        dst = os.path.join(test_negatives_dir, filename)
        shutil.copyfile(src, dst)


    print('total training positive images:', len(os.listdir(train_positives_dir)))
    print('total training negative images:', len(os.listdir(train_negatives_dir)))
    print('total validation positive images:', len(os.listdir(validation_positives_dir)))
    print('total validation negative images:', len(os.listdir(validation_negatives_dir)))
    print('total test positive images:', len(os.listdir(test_positives_dir)))
    print('total test negative images:', len(os.listdir(test_negatives_dir)))


main()
