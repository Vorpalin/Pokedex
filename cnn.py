import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
import tensorflow as tf
import json
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models

image_net_model = tf.keras.applications.MobileNetV2(input_shape=(128,128, 3),include_top=False, weights='imagenet')
image_net_model.trainable = False

try:
    model = tf.keras.models.load_model("pokemon_AI.h5")
except:
    model = tf.keras.Sequential([
        image_net_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(1024, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(149, activation='softmax'),
    ])

prepocessing = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    validation_split=0.2
)

train = prepocessing.flow_from_directory(
    "dataset",
    target_size=(128, 128),
    batch_size=32,
    class_mode='sparse',
    subset='training',
    shuffle=True
)

validation = prepocessing.flow_from_directory(
    "dataset",
    target_size=(128, 128),
    batch_size=32,
    class_mode='sparse',
    subset='validation',
    shuffle=True
)

model.compile(optimizer='adam', loss="sparse_categorical_crossentropy", metrics=['accuracy'])

try:
    epochs = int(input("How many epochs do you want to train your model? : "))
except:
    epochs = 10


history = model.fit(
    train,
    validation_data=validation,
    epochs=epochs,
)

model.save("pokemon_AI.h5")
classification = train.class_indices

classification2 = {value: key for key, value in classification.items()}
with open("pokemon_AI.json", "w") as outfile:
    json.dump(classification2, outfile)

model.summary()