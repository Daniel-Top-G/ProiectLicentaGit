# MEDISCAN AI - Platformă inteligentă pentru analiză radiologică

Aplicație web pentru analiza automată a imaginilor medicale (radiografii, CT, RMN) folosind modele AI, destinată atât utilizatorilor obișnuiți, cât și cadrelor medicale.

Conținut livrabil

- Cod sursă complet al aplicației (fără fișiere binare sau cache).
- Arhitectura aplicației (imagini + descriere).
- Modelele antrenate (.h5 sau .tflite).
- Documentația proiectului (PDF sau DOCX).
- Fișierul `requirements.txt` cu toate pachetele necesare.
- Fisiere HTML/CSS/JS pentru interfață și Flask pentru backend.

# Link Git repository

Codul sursă complet este disponibil la adresa:
https://github.com/Daniel-Top-G/ProiectLicentaGit.git

Pașii de Compilare
1. Clonare - git clone https://github.com/Daniel-Top-G/ProiectLicentaGit.git
2. Instalare requirements - pip install flask
                          - pip install firebase-admin
                          - pip install pyrebase4
                          - pip install tensorflow
                          - pip install waitress
                          - pip install pyngrok

3. Lansare Aplicație -python create_cnn.py
                     -python train_cnn.py
                     -python evaluate_cnn.py
                     -python app_flask.py

