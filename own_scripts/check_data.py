
import os
import json
import pdal
import argparse
from tqdm import tqdm
import numpy as np
from plyfile import PlyData, PlyElement
import logging
import glob
logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Label the instances in the ply files.')
    parser.add_argument('--path', type=str, help='Path of the output')

    args = parser.parse_args()

    for file in glob.glob(args.path +"/**/*.ply", recursive=True):
        print(file)
    for file in glob.glob(args.path +"/**/*.las", recursive=True):
        print(file)


    
