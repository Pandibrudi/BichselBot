import os
from bichsel_classifier import ask_bichsel
from werkzeug.utils import secure_filename
from flask import Flask, render_template, send_file, request, redirect, url_for, send_from_directory

app = Flask(__name__)

#Verzeichnissse
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Erlaubte Uploadformate
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Überprüfung der Dateiendung
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Lösche alle Bilder aus dem Upload

def delete_uploaded_images():
    upload_folder = 'uploads'
    for filename in os.listdir(upload_folder):
        file_path = os.path.join(upload_folder, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Fehler beim Löschen von {filename}: {e}")

# Routing

@app.route('/')
def index():
    return render_template('/index.html')

@app.route('/ask')
def execute_function():
    
    result = ask_bichsel()
    delete_uploaded_images()

    return result

#funktion für das Darstellen von Bildern aus dem static Ordner
@app.route('/load_image')
def load_image():
    image_path = os.path.join(app.root_path, 'static', 'Stuhl.jpg') # Pfad zum Bild
    return send_file(image_path, mimetype='image/jpg')

#Funktion zum Upload
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return render_template('index.html', message='Keine Datei ausgewählt')
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', message='Keine Datei ausgewählt')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template('index.html', message='Bild erfolgreich hochgeladen', filename=filename)
    else:
        return render_template('index.html', message='Uploadfehler')

    
# Routenfunktion zum Anzeigen des hochgeladenen Bildes
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)



if __name__ == '__main__':
    app.run(debug=True)