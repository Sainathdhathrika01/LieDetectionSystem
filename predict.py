import joblib
import numpy as np

from feature_extraction import extract_features

# LOAD MODEL
model = joblib.load(
    "models/svm_model.pkl"
)

# PREDICTION FUNCTION
def predict_voice(audio_path):

    # EXTRACT FEATURES
    features = extract_features(audio_path)

    # RESHAPE
    features = features.reshape(1, -1)

    # PREDICTION
    prediction = model.predict(features)[0]

    # PROBABILITIES
    probabilities = model.predict_proba(features)[0]

    # CLASS NAMES
    classes = model.classes_

    # CREATE SCORE DICTIONARY
    scores = {}

    for i, label in enumerate(classes):

        scores[label] = round(
            probabilities[i] * 100,
            2
        )

    return prediction, scores