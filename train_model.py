import os
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

from feature_extraction import extract_features

import joblib

# DATA STORAGE
X = []
y = []

dataset_path = "dataset"

# READ FILES
for file in os.listdir(dataset_path):

    if file.endswith(".wav"):

        # GET EMOTION CODE
        emotion_code = file.split("-")[2]

        label = None

        # TRUTH LABELS
        if emotion_code in ["01", "02"]:
            label = "Truth"

        # LIE LABELS
        elif emotion_code in ["05", "06"]:
            label = "Lie"

        # PROCESS FILE
        if label:

            file_path = os.path.join(
                dataset_path,
                file
            )

            features = extract_features(
                file_path
            )

            # SAFE CHECK
            if features is not None:

                X.append(features)

                y.append(label)

# CONVERT TO ARRAY
X = np.vstack(X)
y = np.array(y)

# TRAIN TEST SPLIT
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# CREATE MODEL
model = SVC(probability=True)

# TRAIN MODEL
model.fit(X_train, y_train)

# PREDICT
predictions = model.predict(X_test)

# ACCURACY
accuracy = accuracy_score(
    y_test,
    predictions
)

print("Model Accuracy:", accuracy)

# SAVE MODEL
joblib.dump(
    model,
    "models/svm_model.pkl"
)

print("Model Saved Successfully")