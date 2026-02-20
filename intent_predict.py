import pickle
import numpy as np

# Load trained model and vectorizer
try:
    model = pickle.load(open("intent_model.pkl", "rb"))
    vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
    MODEL_LOADED = True
except Exception as e:
    print(f"Warning: Intent model not found: {e}")
    MODEL_LOADED = False

def get_intent(text):
    if not MODEL_LOADED:
        return None, 0.0
        
    try:
        # Vectorize input
        Xv = vectorizer.transform([text])
        
        # Predict
        probabilities = model.predict_proba(Xv)[0]
        max_idx = np.argmax(probabilities)
        confidence = probabilities[max_idx]
        
        tag = model.classes_[max_idx]
        
        # Threshold for confidence
        if confidence < 0.3:
            return None, confidence
            
        return tag, confidence
        
    except Exception as e:
        print(f"Error predicting intent: {e}")
        return None, 0.0
