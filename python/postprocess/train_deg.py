"""
Train classifier from multiple images for degradation classification
Usage:
    train_eg.py <train_data_dir> <train_data_path> <output_fname> [--verbose] [--bands=<bands>]

The <train_data_dir> must be a path to the location containing the maps for training
The <train_data_path> argument must be a path to a directory with vector data files
The <train_data_path> must be a shapefile with attributes containing class and file name
(in shapefile format). These vectors must specify the target class of the training pixels. One file
per class. The base filename (without extension) is taken as class name.
The <output_fname> argument must be af ilename where the trained XY data can be stored
Options:
  -h --help  Show this screen.
  --verbose                             If given, debug output is writen to stdout.
  --bands=<bands>			A list of bands to use for training and classification
"""

import logging
import numpy as np
import os

import pandas as pd

from docopt import docopt
from osgeo import gdal, ogr
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.externals import joblib


logger = logging.getLogger(__name__)



def make_class_dict(path):
    # Set up dict to save Xs and Ys
    driver = ogr.GetDriverByName('ESRI Shapefile')
#    data_source = gdal.OpenEx(vector_data_path, gdal.OF_VECTOR)
    data_source = driver.Open(path, 0)
    if data_source is None:
        report_and_exit("File read failed: %s", path)

    layer = data_source.GetLayer(0)
    class_labels = []
    data = []

    for feature in layer:
        try:
            var1 = float(feature.GetField('NFDI_mag')) 
#   	    var2 = float(feature.GetField('NFDI_rmse'))
	    var3 = float(feature.GetField('NFDI_sin')) 
	    var4 = float(feature.GetField('NFDI_cos')) 
	    var5 = float(feature.GetField('Gv_mag')) 
	    var6 = float(feature.GetField('Shade_mag'))
	    var7 = float(feature.GetField('NPV_mag')) 
	    var8 = float(feature.GetField('Soil_mag')) 
	    label = feature.GetField('class')
        except:
            continue 
        class_labels.append(label)
        #data.append([var1, var2, var3, var4, var5, var6, var7, var8])
        data.append([var1, var3, var4, var5, var6, var7, var8])

    return class_labels, data




if __name__ == "__main__":
    opts = docopt(__doc__)

    train_data_dir = opts["<train_data_dir>"]
    train_data_path = opts["<train_data_path>"]
    labels, data = make_class_dict(train_data_path)

    output_fname = opts["<output_fname>"]



    # Perform classification
    #
    classifier = RandomForestClassifier(n_jobs=4, n_estimators=10, class_weight='balanced')
    logger.debug("Train the classifier: %s", str(classifier))
    classifier.fit(data, labels)
    joblib.dump(classifier, output_fname, compress=3)

