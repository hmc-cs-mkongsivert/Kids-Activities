import tensorflow as tf
import tensorflow_hub as hub
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
	data["age-group"] = []
	with open(file, newline='') as csvFile:
		dataReader = csv.reader(csvFile)
		for row in dataReader:
			data["sentence"].append(row[0])
			data["age-group"].append(float(row[1]))
	return pd.DataFrame.from_dict(data)

#build one training and one testing dataset
def load_dataset(filename):
	young_df = load_data(filename + "-young.csv")
	mid_df = load_data(filename + "-mid.csv")
	old_df = load_data(filename + "-old.csv")
	young_df["polarity"] = 0
	mid_df = ["polarity"] = 0.5
	old_df = ["polarity"] = 1
	return pd.concat([young_df, mid_df, old_df]).sample(frac=1).reset_index(drop=True)

def dowload_and_load_datasets(force_download=False):
	train_df = load_dataset("train")
	test_df = load_dataset("test")

	return train_df, test_df

