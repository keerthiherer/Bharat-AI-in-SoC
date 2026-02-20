import nlu
import json

# Setup
print("Loading intents...")
intent_map = nlu.load_intents("intent.json")
print(f"Loaded {len(intent_map)} keywords.")

# Test inputs (Romanized examples from user + Devanagari actuals)
test_inputs = [
    ("asdh din", None),          # mismatch (Roman 'din' vs Devanagari 'दिन')
    ("asdh दिन", "day"),         # Correct Hindi input
    ("दिन बताओ", "day"),         # "batao" is stopword, "din" matches
    ("random noise", None),
    ("kuchhsh din", None),       # Roman mismatch
    ("कुछश दिन", "day"),         # Devanagari noise + match
    ("समय", "time"),
    ("बंद करो", "exit"),         # "karo" stopword, "band" (बंद) matches
]

print("\n--- Testing Intent Detection ---")
for text, expected in test_inputs:
    intent = nlu.detect_intent(text, intent_map)
    status = "✅" if intent == expected else f"❌ (Expected {expected})"
    print(f"Input: '{text}' -> Intent: {intent} {status}")

print("\n--- Test Complete ---")
