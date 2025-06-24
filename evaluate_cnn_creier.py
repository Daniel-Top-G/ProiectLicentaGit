import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator



model = load_model("model_MRI_creier.h5")

test_gen = ImageDataGenerator(rescale=1./255)
test_data = test_gen.flow_from_directory(
    'dataset_MRI_Creier/',
    target_size=(256, 256),
    batch_size=32,
    class_mode='categorical',
    shuffle=False
)

y_true = test_data.classes
predictions = model.predict(test_data)
y_pred = np.argmax(predictions, axis=1)


print(confusion_matrix(y_true, y_pred))
print(classification_report(y_true, y_pred))

