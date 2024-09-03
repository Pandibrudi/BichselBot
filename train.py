import os
import pickle
import numpy as np
from skimage.io import imread
from skimage.transform import resize
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# Prepare data
input_dir = 'C:/Users/Fabia/Documents/Coding/BichselBot/data/'  # Path to folder containing the data in different folders
categories = ['chairs', 'tables']

data = []
labels = []

for category_idx, category in enumerate(categories):
    for file in os.listdir(os.path.join(input_dir, category)):
        img_path = os.path.join(input_dir, category, file)
        img = imread(img_path)

        # Convert image to grayscale or keep it in RGB
        if len(img.shape) == 3:  # If the image is RGB
            img = resize(img, (15, 15, 3))  # Resize to 15x15 with 3 color channels
        else:  # If the image is grayscale
            img = resize(img, (15, 15))  # Resize to 15x15 with 1 channel

        data.append(img.flatten())
        labels.append(category_idx)

# Convert lists to numpy arrays
data = np.array(data, dtype=np.float32)
labels = np.array(labels)

# Train / test split
x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True, stratify=labels)

# Train classifier
classifier = SVC(probability=True)

parameters = [{'gamma': [0.01, 0.001, 0.0001], 'C': [1, 10, 100, 1000]}]

grid_search = GridSearchCV(classifier, parameters)

grid_search.fit(x_train, y_train)

# Test performance
best_estimator = grid_search.best_estimator_

y_prediction = best_estimator.predict(x_test)

score = accuracy_score(y_prediction, y_test)

print('{}% of samples were, according to Peter Bichsel, correctly classified.'.format(str(score * 100)))

# Save the model
pickle.dump(best_estimator, open('./model2.p', 'wb'))
