import uuid
from flask import Flask, render_template, request, redirect, session, url_for
from firebase_config import firebase_config
import pyrebase
import os
import smtplib
import random
import traceback
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from email.message import EmailMessage
from firebase_database import db
from validare_cnp import validare_cnp

app = Flask(__name__)


firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

model = load_model('model.h5')
model_radiografie = load_model("model_radiografii.h5")
model_creier = load_model("model_MRI_creier.h5")

EMAIL_ADDRESS = 'daniel.sighete@gmail.com'
EMAIL_PASSWORD = 'rzrf aooo cluq npvd'

def send_otp(email, otp):
     msg = EmailMessage()
     msg['Subject'] = 'Cod OTP pentru înregistrare'
     msg['From'] = EMAIL_ADDRESS
     msg['To'] = email
     msg.set_content(f'Codul tău OTP este: {otp}', charset='utf-8')

     with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)


@app.route('/', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        try:
            user = auth.sign_in_with_email_and_password(request.form['email'], request.form['password'])
            session['user'] = user['idToken']
            session['useruid'] = user['localId']
            email = request.form['email']
            session['email'] = email
            return redirect('/home')
        except:
            error = 'Email sau parolă greșită'
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = ''
    if request.method == 'POST':
        try:
             username = request.form['username']
             email = request.form['email']
             password = request.form['password']
             otp = str(random.randint(100000, 999999))
             session['otp'] = otp
             session['username'] = username
             session['email'] = email
             session['password'] = password
             send_otp(email, otp)
             return redirect('/verify')
        except Exception as e:
            print("Eroare la înregistrare:", e)
            traceback.print_exc()  
            error = 'Eroare la înregistrare.'
    return render_template('register.html', error=error)

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        user_otp = request.form['otp']
        if user_otp == session.get('otp'):
            auth.create_user_with_email_and_password(session['email'], session['password'])
            uid = auth.sign_in_with_email_and_password(session['email'], session['password'])
            db.collection("users").document(uid['localId']).set({
                "username": session['username'],
                "email": session['email']
            })
            return render_template('success.html', email=session['email'])
        else:
            return 'OTP incorect. Încearcă din nou.'
    return render_template('verify.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


@app.route("/adauga_pacient", methods=["GET", "POST"])
def adauga_pacient():
    email_user = session.get("email")
    if not email_user:
            return redirect("/")
    
    if request.method == "POST":
        nume = request.form["nume"]
        prenume = request.form["prenume"]
        cnp = request.form["cnp"]
        diagnostic = request.form["diagnostic"]

        valid, mesaj = validare_cnp(cnp)
        if not valid:
            return render_template("adauga_pacient.html", error=mesaj)

        pacient_ref = db.collection("pacienti").document(cnp)
        if pacient_ref.get().exists:
            return render_template("adauga_pacient.html", error="Pacientul există deja!")

        pacient_ref.set({
            "nume": nume,
            "prenume": prenume,
            "diagnostic": diagnostic,
            "user": email_user 
        })

        return render_template("adauga_pacient.html", success="Pacient adăugat cu succes!")
    return render_template("adauga_pacient.html")


@app.route("/sterge_pacient", methods=["GET", "POST"])
def sterge_pacient():
    email_user = session.get("email")
    if not email_user:
        return redirect("/")

    pacient = None
    cnp_cautat = None

    if request.method == "POST":
        cnp_cautat = request.form.get("cnp")
        doc_ref = db.collection("pacienti").document(cnp_cautat)
        doc = doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            if data["user"] == email_user:
                pacient = {"cnp": cnp_cautat, **data}

    return render_template("sterge_pacient.html", pacient=pacient, cnp_cautat=cnp_cautat)


@app.route("/sterge_pacient_definitiv/<cnp>", methods=["POST"])
def sterge_pacient_definitiv(cnp):
    email_user = session.get("email")
    if not email_user:
        return redirect("/")

    pacient_ref = db.collection("pacienti").document(cnp)
    doc = pacient_ref.get()
    if doc.exists and doc.to_dict().get("user") == email_user:
        pacient_ref.delete()

    return redirect("/sterge_pacient")



@app.route("/lista_pacienti")
def lista_pacienti():
    email_user = session.get("email")
    if not email_user:
        return redirect("/")

    pacienti = db.collection("pacienti").where("user", "==", email_user).stream()

    lista = []
    for p in pacienti:
        data = p.to_dict()
        data["cnp"] = p.id 
        lista.append(data)

    return render_template("lista_pacienti.html", pacienti=lista)



@app.route('/home')
def home():
    username=''
    uid= session.get("useruid")
    if 'user' not in session:
        return redirect('/')
    doc = db.collection("users").document(uid).get()
    if doc.exists:
        username = doc.to_dict().get("username")
    return render_template("home.html",username=username)

@app.route('/home2')
def home2():
    username=''
    uid= session.get("useruid")
    if 'user' not in session:
        return redirect('/')
    doc = db.collection("users").document(uid).get()
    if doc.exists:
        username = doc.to_dict().get("username")
    return render_template("home2.html",username=username)

@app.route('/radiografii')
def radiografii():
    return render_template("radiografii.html")

@app.route('/ct')
def ct():
    return render_template("ct_scan.html")

@app.route('/MRI')
def MRI():
    return render_template("MRI_creier.html")

@app.route('/radiografii2')
def radiografii2():
    return render_template("radiografii2.html")

@app.route('/ct2')
def ct2():
    return render_template("ct_scan2.html")

@app.route('/MRI2')
def MRI2():
    return render_template("MRI_creier2.html")

@app.route('/go-back')
def go_back():
    return redirect(request.referrer or '/fallback-url')

@app.route('/predict_radiografie', methods=['POST'])
def predict_radiografie():
    file = request.files['file']
    if not file:
        return redirect('/go-back')

    filepath = os.path.join('static', file.filename)
    file.save(filepath)

    img = image.load_img(filepath, target_size=(256, 256))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model_radiografie.predict(img_array)
    predicted_class = np.argmax(prediction[0])
    if predicted_class == 2:
        result = "Normal"
        color = "text-success fs-3"
    elif predicted_class == 0:
        result = "Pneumonie bacteriană detectată"
        color = "text-danger fs-3"
    else:
        result = "Pneumonie virală detectată"
        color = "text-danger fs-3"

    return render_template('result_radiografii.html',color=color, result=result, image_path=filepath)

@app.route('/predict_radiografie2', methods=['POST'])
def predict_radiografie2():
    file = request.files['file']
    if not file:
        return redirect('/go-back')

    filepath = os.path.join('static', file.filename)
    file.save(filepath)

    img = image.load_img(filepath, target_size=(256, 256))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model_radiografie.predict(img_array)
    predicted_class = np.argmax(prediction[0])
    if predicted_class == 2:
        result = "Normal"
        color = "text-success fs-3"
    elif predicted_class == 0:
        result = "Pneumonie bacteriană detectată"
        color = "text-danger fs-3"
    else:
        result = "Pneumonie virală detectată"
        color = "text-danger fs-3"

    return render_template('result_radiografii2.html',color=color, result=result, image_path=filepath)



@app.route('/predict_ct', methods=['POST'])
def predict_ct():
    files = request.files.getlist('files')
    if not files:
        return redirect('/ct')

    tumor_count = 0
    tumor_images = []
    color = "text-success fs-3"
    upload_folder = os.path.join('static', 'uploads', 'ct')
    os.makedirs(upload_folder, exist_ok=True)

    for f in files:
        unique_filename = str(uuid.uuid4()) + "_" + f.filename
        filepath = os.path.join(upload_folder, unique_filename)
        f.save(filepath)

        img = image.load_img(filepath, target_size=(256, 256))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        prediction = model.predict(img_array)
        if prediction[0][0] > 0.37:
            tumor_count += 1
            color = "text-danger fs-3"
            relative_path = f"uploads/ct/{unique_filename}"
            tumor_images.append(relative_path)

    result = f"{tumor_count} imagini cu tumoare detectate din {len(files)}"
    return render_template('result_ct.html', color=color, result=result, tumor_images=tumor_images)

@app.route('/predict_ct2', methods=['POST'])
def predict_ct2():
    files = request.files.getlist('files')
    if not files:
        return redirect('/ct')

    tumor_count = 0
    tumor_images = []
    color = "text-success fs-3"
    upload_folder = os.path.join('static', 'uploads', 'ct')
    os.makedirs(upload_folder, exist_ok=True)

    for f in files:
        unique_filename = str(uuid.uuid4()) + "_" + f.filename
        filepath = os.path.join(upload_folder, unique_filename)
        f.save(filepath)

        img = image.load_img(filepath, target_size=(256, 256))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        prediction = model.predict(img_array)
        if prediction[0][0] > 0.37:
            tumor_count += 1
            color = "text-danger fs-3"
            relative_path = f"uploads/ct/{unique_filename}"
            tumor_images.append(relative_path)

    result = f"{tumor_count} imagini cu tumoare detectate din {len(files)}"
    return render_template('result_ct2.html', color=color, result=result, tumor_images=tumor_images)


@app.route('/predict_MRI', methods=['POST'])
def predict_MRI():
    files = request.files.getlist('files')
    if not files:
        return redirect('/MRI')

    tumor_count = 0
    tumor_glioma_count = 0
    tumor_pituitar_count = 0
    tumor_meningioma_count = 0
    color = "text-success fs-3"
    tumor_images = []
    
    upload_folder = os.path.join('static', 'uploads', 'MRI')
    os.makedirs(upload_folder, exist_ok=True)

    for f in files:
        unique_filename = str(uuid.uuid4()) + "_" + f.filename
        filepath = os.path.join(upload_folder, unique_filename)
        f.save(filepath)

        img = image.load_img(filepath, target_size=(256, 256))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        prediction = model_creier.predict(img_array)
        predicted_class = np.argmax(prediction[0])
        if predicted_class == 2:
            result = "Normal"
        elif predicted_class == 0:
            color = "text-danger fs-3"
            tumor_glioma_count += 1
            relative_path = f"uploads/MRI/{unique_filename}"
            tumor_images.append(relative_path)
        elif predicted_class == 1:
            color = "text-danger fs-3"
            tumor_meningioma_count += 1
            relative_path = f"uploads/MRI/{unique_filename}"
            tumor_images.append(relative_path)
        else:
            color = "text-danger fs-3"
            tumor_pituitar_count += 1
            relative_path = f"uploads/MRI/{unique_filename}"
            tumor_images.append(relative_path)

    tumor_count=tumor_glioma_count + tumor_pituitar_count + tumor_meningioma_count
    result = f"{tumor_count} imagini cu tumoare detectate din {len(files)}, dintre care {tumor_glioma_count} sunt Gliome, {tumor_pituitar_count} sunt pituitare, {tumor_meningioma_count} sunt meningiome"
    return render_template('result_MRI_creier.html', color=color, result=result, tumor_images=tumor_images)

@app.route('/predict_MRI2', methods=['POST'])
def predict_MRI2():
    files = request.files.getlist('files')
    if not files:
        return redirect('/MRI')

    tumor_count = 0
    tumor_glioma_count = 0
    tumor_pituitar_count = 0
    tumor_meningioma_count = 0
    color = "text-success fs-3"
    tumor_images = []
    
    upload_folder = os.path.join('static', 'uploads', 'MRI')
    os.makedirs(upload_folder, exist_ok=True)

    for f in files:
        unique_filename = str(uuid.uuid4()) + "_" + f.filename
        filepath = os.path.join(upload_folder, unique_filename)
        f.save(filepath)

        img = image.load_img(filepath, target_size=(256, 256))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        prediction = model_creier.predict(img_array)
        predicted_class = np.argmax(prediction[0])
        if predicted_class == 2:
            result = "Normal"
        elif predicted_class == 0:
            color = "text-danger fs-3"
            tumor_glioma_count += 1
            relative_path = f"uploads/MRI/{unique_filename}"
            tumor_images.append(relative_path)
        elif predicted_class == 1:
            color = "text-danger fs-3"
            tumor_meningioma_count += 1
            relative_path = f"uploads/MRI/{unique_filename}"
            tumor_images.append(relative_path)
        else:
            color = "text-danger fs-3"
            tumor_pituitar_count += 1
            relative_path = f"uploads/MRI/{unique_filename}"
            tumor_images.append(relative_path)

    tumor_count=tumor_glioma_count + tumor_pituitar_count + tumor_meningioma_count
    result = f"{tumor_count} imagini cu tumoare detectate din {len(files)}, dintre care {tumor_glioma_count} sunt Gliome, {tumor_pituitar_count} sunt pituitare, {tumor_meningioma_count} sunt meningiome"
    return render_template('result_MRI_creier2.html', color=color, result=result, tumor_images=tumor_images)

if __name__ == '__main__':
    app.run(debug=True)
