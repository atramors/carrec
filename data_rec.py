#%%
import mlflow
import mlflow.tensorflow
import matplotlib.pyplot as plt
import numpy as np
import os
import tensorflow as tf
from pathlib import Path
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential


mlflow.tensorflow.autolog()

# Path to images
DATA_DIR = Path(
    "/Users/atramors/desktop/My_Projects/datasets/car_DS/car_data/\
car_data/train"
)

# Create a dataset
# Parameters
batch_size = 200
img_height = 200
img_width = 200
num_classes = 196

train_dataset = keras.preprocessing.image_dataset_from_directory(
    DATA_DIR,
    labels="inferred",  # labels are generated from the directory structure
    validation_split=0.2,  # fraction of data to reserve for validation
    subset="training",
    seed=123,  # Optional random seed for shuffling and transformations
    color_mode="rgb",
    batch_size=batch_size,
    image_size=(img_height, img_height),
)
valid_dataset = keras.preprocessing.image_dataset_from_directory(
    DATA_DIR,
    labels="inferred",
    validation_split=0.2,
    subset="validation",
    seed=123,
    color_mode="rgb",
    batch_size=batch_size,
    image_size=(img_height, img_height),
)
# labels of cars acording the directory structure
class_names = train_dataset.class_names

# Configure the dataset for performance

AUTOTUNE = tf.data.experimental.AUTOTUNE
train_dataset = train_dataset.cache().shuffle(2700).prefetch(buffer_size=AUTOTUNE)
valid_dataset = valid_dataset.cache().prefetch(buffer_size=AUTOTUNE)

# Create the model

model = Sequential(
    [
        # Data augmentation:
        # Generating additional training data from our existing examples by augmenting
        # then using random transformations that yield believable-looking images.
        # This helps expose the model to more aspects of the data and generalize better.
        layers.experimental.preprocessing.RandomFlip(
            "horizontal_and_vertical", input_shape=(img_height, img_width, 3)
        ),
        layers.experimental.preprocessing.RandomRotation(0.1),
        layers.experimental.preprocessing.RandomZoom(0.1),
        # Standardize values to be in the [0, 1] by using a Rescaling layer
        # (RGB channel values are in the [0, 255] range)
        layers.experimental.preprocessing.Rescaling(1.0 / 255),
        # The model consists of three convolution blocks with a max pool layer in each of them:
        # Creates a convolution kernel that is convolved with the layer input to produce a tensor of outputs.
        layers.Conv2D(16, 3, padding="same", activation="relu"),
        # Downsamples the input representation by taking the maximum value over the window defined by
        # pool_size for each dimension along the features axis
        layers.MaxPooling2D(),  # Max pooling operation for 2D spatial data
        layers.Conv2D(32, 3, padding="same", activation="relu"),
        layers.MaxPooling2D(),
        layers.Conv2D(64, 3, padding="same", activation="relu"),
        layers.MaxPooling2D(),
        # Technique to reduce overfitting to the network, a form of regularization.
        layers.Dropout(0.2),
        # Flattens the input. Does not affect the batch size.
        layers.Flatten(),
        # Regular densely-connected NN layer:
        layers.Dense(
            128, activation="relu"
        ),  # with 128 units on top by a relu activation function
        layers.Dense(
            num_classes, activation="relu"
        ),  # with 196 units on top by a relu activation function
    ]
)

# Compile the model
# Configures the model for training.
model.compile(
    optimizer="adam",  # Optimizer that implements the Adam algorithm
    # Computes the crossentropy loss between the labels and predictions
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    # To view training and validation accuracy for each training epoch,
    # pass the metrics argument.
    metrics=["accuracy"],
)
# View all the layers of the network using the model's summary method:
model.summary()
# Trains the model for a fixed number of epochs (iterations on a dataset).
epochs = 10
history = model.fit(train_dataset, validation_data=valid_dataset, epochs=epochs)

# Visualize training results
# Create plots of loss and accuracy on the training and validation sets.
acc = history.history["accuracy"]
val_acc = history.history["val_accuracy"]
loss = history.history["loss"]
val_loss = history.history["val_loss"]
epochs_range = range(epochs)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label="Training Accuracy")
plt.plot(epochs_range, val_acc, label="Validation Accuracy")
plt.legend(loc="upper left")
plt.title("Training and Validation Accuracy")

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label="Training Loss")
plt.plot(epochs_range, val_loss, label="Validation Loss")
plt.legend(loc="upper right")
plt.title("Training and Validation Loss")
plt.show()
