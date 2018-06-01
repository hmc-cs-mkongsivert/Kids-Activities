import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import seaborn as sns
import csv

#code modified from code taken from TensorFlow website:
#https://www.tensorflow.org/tutorials/text_classification_with_tf_hub

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
	mid_df["polarity"] = 0.5
	old_df["polarity"] = 1
	return pd.concat([young_df, mid_df, old_df]).sample(frac=1).reset_index(drop=True)

def download_and_load_datasets(force_download=False):
	train_df = load_dataset("train")
	test_df = load_dataset("test")

	return train_df, test_df

def split_sets(filename):
	'''splits sample sets into training and testing sets'''
	with open(filename, newline='') as csvFile:
		dataReader = csv.reader(csvFile)
		with open('train-'+filename, 'w') as train:
			with open('test-'+filename, 'w') as test:
				trainFile = csv.writer(train)
				testFile = csv.writer(test)
				count = 0
				for row in dataReader:
					if count%2 == 0:
						trainFile.writerow(row)
					else:
						testFile.writerow(row)
					count += 1


# Reduce logging output.
tf.logging.set_verbosity(tf.logging.ERROR)

train_df, test_df = download_and_load_datasets()
train_df.head()

# Training input on the whole training set with no limit on training epochs.
train_input_fn = tf.estimator.inputs.pandas_input_fn(
    train_df, train_df["polarity"], num_epochs=None, shuffle=True)

# Prediction on the whole training set.
predict_train_input_fn = tf.estimator.inputs.pandas_input_fn(
    train_df, train_df["polarity"], shuffle=False)
# Prediction on the test set.
predict_test_input_fn = tf.estimator.inputs.pandas_input_fn(
    test_df, test_df["polarity"], shuffle=False)

embedded_text_feature_column = hub.text_embedding_column(
    key="sentence", 
    module_spec="https://tfhub.dev/google/nnlm-en-dim128/1")

estimator = tf.estimator.DNNClassifier(
    hidden_units=[500, 100],
    feature_columns=[embedded_text_feature_column],
    n_classes=2,
    optimizer=tf.train.AdagradOptimizer(learning_rate=0.003))

# Training for 1,000 steps means 128,000 training examples with the default
# batch size. This is roughly equivalent to 5 epochs since the training dataset
# contains 25,000 examples.
estimator.train(input_fn=train_input_fn, steps=1000);

train_eval_result = estimator.evaluate(input_fn=predict_train_input_fn)
test_eval_result = estimator.evaluate(input_fn=predict_test_input_fn)

print("Training set accuracy: {accuracy}".format(**train_eval_result))
print("Test set accuracy: {accuracy}".format(**test_eval_result))

def get_predictions(estimator, input_fn):
  return [x["class_ids"][0] for x in estimator.predict(input_fn=input_fn)]

LABELS = [
    "Young", "Middle", "Old"
]

# Create a confusion matrix on training data.
with tf.Graph().as_default():
  cm = tf.confusion_matrix(train_df["polarity"], 
                           get_predictions(estimator, predict_train_input_fn))
  with tf.Session() as session:
    cm_out = session.run(cm)

# Normalize the confusion matrix so that each row sums to 1.
cm_out = cm_out.astype(float) / cm_out.sum(axis=1)[:, np.newaxis]

sns.heatmap(cm_out, annot=True, xticklabels=LABELS, yticklabels=LABELS);
plt.xlabel("Predicted");
plt.ylabel("True");
plt.show()
