from cnn_model_creier import create_cnn_creier
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping


datagen = ImageDataGenerator(rescale=1./255, validation_split=0.3)
train_gen = datagen.flow_from_directory(
    'dataset_MRI_Creier/',
    target_size=(256, 256),
    batch_size=32,
    class_mode='categorical',
    subset='training'
)

val_gen = datagen.flow_from_directory(
    'dataset_MRI_Creier/',
    target_size=(256, 256),
    batch_size=32,
    class_mode='categorical',
    subset='validation'
)

model = create_cnn_creier()

print(train_gen.class_indices)

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])


early_stop = EarlyStopping(
    monitor='val_loss',
    patience=5,
    restore_best_weights=True
)

model.fit(train_gen, validation_data=val_gen, epochs=10, callbacks=[early_stop])

model.save("model_MRI_creier.h5")



