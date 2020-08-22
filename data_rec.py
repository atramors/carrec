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
        layers.experimental.preprocessing.RandomFlip(
            "horizontal_and_vertical", input_shape=(img_height, img_width, 3)
        ),
        layers.experimental.preprocessing.RandomRotation(0.1),
        layers.experimental.preprocessing.RandomZoom(0.1),
        layers.experimental.preprocessing.Rescaling(1.0 / 255),
        layers.Conv2D(16, 3, padding="same", activation="relu"),
        layers.MaxPooling2D(), 
        layers.Conv2D(32, 3, padding="same", activation="relu"),
        layers.MaxPooling2D(),
        layers.Conv2D(64, 3, padding="same", activation="relu"),
        layers.MaxPooling2D(),
        
        layers.Dropout(0.2),
       
        layers.Flatten(),
 
        layers.Dense(
            128, activation="relu"
        ),  # with 128 units on top by a relu activation function
        layers.Dense(
            num_classes, activation="relu"
        ),  # with 196 units on top by a relu activation function
    ]
)

# Compile the model

model.compile(
    optimizer="adam", 
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
  
    metrics=["accuracy"],
)
# View all the layers of the network using the model's summary method:
model.summary()
# Trains the model for a fixed number of epochs (iterations on a dataset).
epochs = 10
history = model.fit(train_dataset, validation_data=valid_dataset, epochs=epochs)

# Visualize training results

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
