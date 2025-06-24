import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator



model = load_model("model.h5")

test_gen = ImageDataGenerator(rescale=1./255)
test_data = test_gen.flow_from_directory(
    'dataset/',
    target_size=(256, 256),
    batch_size=32,
    class_mode='binary',
    shuffle=False
)

predictions = model.predict(test_data)
y_pred = (predictions > 0.6).astype(int)
y_true = test_data.classes

print(confusion_matrix(y_true, y_pred))
print(classification_report(y_true, y_pred))

