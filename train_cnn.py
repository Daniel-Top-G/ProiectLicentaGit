from cnn_model import create_cnn
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping


datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)
train_gen = datagen.flow_from_directory(
    'dataset/',
    target_size=(256, 256),
    batch_size=32,
    class_mode='binary',
    subset='training'
)

val_gen = datagen.flow_from_directory(
    'dataset/',
    target_size=(256, 256),
    batch_size=32,
    class_mode='binary',
    subset='validation'
)

model = create_cnn()


model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

early_stop = EarlyStopping(
    monitor='val_loss',
    patience=7,
    restore_best_weights=True
)

model.fit(train_gen, validation_data=val_gen, epochs=20, callbacks=[early_stop])

model.save("model.h5")
