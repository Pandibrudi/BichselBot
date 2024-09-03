import pickle
import os
import numpy as np
from skimage.io import imread
from skimage.transform import resize

def ask_bichsel():
    # Laden des Modells
    loaded_model = pickle.load(open('./model2.p', 'rb'))

    # Funktion zum Laden und Vorbereiten eines Bildes
    def preprocess_image(image_path):
        img = imread(image_path)
        img = resize(img, (15, 15))
        img = img.flatten()
        return img

    # Beispielbilder für Testzwecke
    image_folder = 'uploads'
    image_paths = os.listdir(image_folder)

    # Vorhersage für jedes Bild
    for image_name in image_paths:
        image_path = os.path.join(image_folder, image_name)
        # Laden und Vorbereiten des Bildes
        img = preprocess_image(image_path)
        # Vorhersage des geladenen Modells
        prediction = loaded_model.predict([img])
        # Wahrscheinlichkeiten des geladenen Modells
        proba = loaded_model.predict_proba([img])
        confidence = np.max(proba) * 100  # Convert to percentage
        # Ausgabe der Vorhersage und Konfidenz
        if prediction[0] == 0:
            return "Bei {} handelt es sich mit einer Konfidenz von {:.2f}% um einen Stuhl.".format(image_name, confidence)

        elif prediction[0] == 1:
            return "Bei {} handelt es sich mit einer Konfidenz von {:.2f}% um einen Tisch.".format(image_name, confidence)
