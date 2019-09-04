
import tensorflow.keras
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import Dense, Activation, Flatten, Dropout
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.optimizers import SGD, Adam
from tensorflow.keras.callbacks import ModelCheckpoint

import os

TRAIN_DIR = "images"
class_sizes = {}
for d in os.listdir(TRAIN_DIR):
    p = os.path.join(TRAIN_DIR,d)
    if os.path.isdir(p):
        class_sizes[d] = len(os.listdir(p))

HEIGHT = 300
WIDTH = 300

model_name = "ResNet50"
base_model = ResNet50(weights='imagenet',
                      include_top=False,
                      input_shape=(HEIGHT, WIDTH, 3))



HEIGHT = 300
WIDTH = 300
BATCH_SIZE = 8

train_datagen =  ImageDataGenerator(
      preprocessing_function=preprocess_input,
      rotation_range=0,
      horizontal_flip=False,
      vertical_flip=False
    )

train_generator = train_datagen.flow_from_directory(TRAIN_DIR,
                                                    target_size=(HEIGHT, WIDTH),
                                                    batch_size=BATCH_SIZE)


classes = train_generator.class_indices
print("class indicies",classes)

print("class sizes",class_sizes)

class_list = ["cat", "not_cat"]
class_weight = {
    classes['cat'] : class_sizes["not_cat"] * 1.0 / class_sizes['cat'],
    classes['not_cat'] : 1.0,
}

print("class weights",class_weight)

def build_finetune_model(base_model, dropout, fc_layers, num_classes):
    for layer in base_model.layers:
        layer.trainable = False

    x = base_model.output
    x = Flatten()(x)
    for fc in fc_layers:
        # New FC layer, random init
        x = Dense(fc, activation='relu')(x)
        x = Dropout(dropout)(x)

    # New softmax layer
    predictions = Dense(num_classes, activation='softmax')(x)

    finetune_model = Model(inputs=base_model.input, outputs=predictions)

    return finetune_model

FC_LAYERS = [1024, 1024]
dropout = 0.5

finetune_model = build_finetune_model(base_model,
                                      dropout=dropout,
                                      fc_layers=FC_LAYERS,
                                      num_classes=len(class_list))


NUM_EPOCHS = 10
BATCH_SIZE = 8
num_train_images = 10000

adam = Adam(lr=0.00001)
finetune_model.compile(adam, loss='categorical_crossentropy', metrics=['accuracy'])

try:
    os.makedirs("keras2/checkpoints")
except EnvironmentError:
    pass

filepath="keras2/checkpoints/" + model_name + "_model_weights.h5"
checkpoint = ModelCheckpoint(filepath, monitor=["acc"], verbose=1, mode='max')
callbacks_list = [checkpoint]

history = finetune_model.fit_generator(train_generator, epochs=NUM_EPOCHS, workers=8,
                                       steps_per_epoch=num_train_images // BATCH_SIZE,
                                       shuffle=True, callbacks=callbacks_list,
                                       class_weight=class_weight)

finetune_model.save("keras2/cat_model_{}.h5".format(model_name))

print('history dict:', history.history)

# Plot the training and validation loss + accuracy
def plot_training(history):
    acc = history.history['acc']
    val_acc = history.history['val_acc']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    epochs = range(len(acc))

    plt.plot(epochs, acc, 'r.')
    plt.plot(epochs, val_acc, 'r')
    plt.title('Training and validation accuracy')

    # plt.figure()
    # plt.plot(epochs, loss, 'r.')
    # plt.plot(epochs, val_loss, 'r-')
    # plt.title('Training and validation loss')
    plt.show()

    plt.savefig('acc_vs_epochs.png')

# plot_training(history)

"""
cat:
t: 2100, c 0.27, n 0.72

not_cat:
t 1880, c 0.15, n 0.84

"""
