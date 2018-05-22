#import tensorflow as tf
#import tensorflow_hub as hub
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re
import seaborn as sns
import csv

#code modified from code taken from TensorFlow website
#load all files from a directory in a DataFrame
def load_data(file):
	data = {}
	data["sentence"] = []
	data["sentiment"] = []
	with open(file, newline='') as csvFile:
		dataReader = csv.reader(csvFile)
		for row in dataReader:
			data["sentence"].append(row[0])
			data["sentiment"].append(float(row[1]))
	return pd.DataFrame.from_dict(data)

#build one training and one testing dataset

def 