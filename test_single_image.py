from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt

model = load_model("model.h5")

img_path = "D:\Proiect_Licenta\caz_tumoare_4.jpg" 
img = image.load_img(img_path, target_size=(256, 256))
img_array = image.img_to_array(img) / 255.0
img_array = np.expand_dims(img_array, axis=0)

prediction = model.predict(img_array)
print("Predicție:", prediction[0][0])

if prediction[0][0] > 0.6:
    print("Rezultat: TUMORĂ")
else:
    print("Rezultat: NORMAL")

plt.imshow(img)
plt.title("Predicție: Tumoră" if prediction[0][0] > 0.6 else "Predicție: Normal")
plt.axis('off')
plt.show()