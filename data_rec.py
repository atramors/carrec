import numpy as np
import tensorflow as tf
from tensorflow import keras

# Path to images
DATA_DIR = "/Users/atramors/desktop/My_Projects/datasets/car_DS/car_data/\
car_data/"

# Parameters
batch_size = 64
img_height = 200
img_width = 200

train_dataset = keras.preprocessing.image_dataset_from_directory(
    DATA_DIR + "train", labels="inferred",
    color_mode="rgb",
    batch_size=batch_size,
    image_size=(img_height, img_height))
test_dataset = keras.preprocessing.image_dataset_from_directory(
    DATA_DIR + "test", labels="inferred",
    color_mode="rgb",
    batch_size=batch_size,
    image_size=(img_height, img_height))

