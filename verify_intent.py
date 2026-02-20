from intent_predict import get_intent

test_phrases = [
    "aiva",
    "hey aiva",
    "hello aiva",
    "what is time",
    "open camera",
    "random noise",
    "aiva listen"
]

print("Testing Intent Model Prediction:\n")
for phrase in test_phrases:
    intent, conf = get_intent(phrase)
    print(f"Phrase: '{phrase}' -> Intent: {intent}, Confidence: {conf:.2f}")

print("\nVerification Complete.")
