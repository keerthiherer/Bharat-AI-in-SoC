import json, pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

data = json.load(open("intent.json", encoding="utf-8"))

X, y = [], []
for intent in data["intents"]:
    for p in intent["patterns"]:
        X.append(p)
        y.append(intent["tag"])

vectorizer = TfidfVectorizer()
Xv = vectorizer.fit_transform(X)

model = LogisticRegression()
model.fit(Xv, y)

pickle.dump(model, open("intent_model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("✅ Intent model trained")

