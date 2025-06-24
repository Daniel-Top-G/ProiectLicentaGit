from cnn_model_radiografii import create_cnn_radiografii
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping

datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

train_gen = datagen.flow_from_directory(
    'dataset_radiografii/',
    target_size=(256, 256),
    batch_size=32,
    class_mode='categorical',
    subset='training'
)

val_gen = datagen.flow_from_directory(
    'dataset_radiografii/',
    target_size=(256, 256),
    batch_size=32,
    class_mode='categorical',
    subset='validation'
)

model = create_cnn_radiografii()


model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])


early_stop = EarlyStopping(
    monitor='val_loss',
    patience=5,
    restore_best_weights=True
)

model.fit(train_gen, validation_data=val_gen, epochs=20, callbacks=[early_stop])

model.save("model_radiografii.h5")
