import pyaudio
import json
import numpy as np
from vosk import Model, KaldiRecognizer

# =========================================
# CONFIG
# =========================================
WAKE_WORDS = ["इवा", "iva", "kira", "ava", "hyva", "hey nova", "hey"]  # check multiple
MODEL_PATH = "vosk-model-small-hi-0.22"
SAMPLE_RATE = 16000
BLOCK_SIZE = 1024   # fast

# =========================================
# Load Vosk model
# =========================================
try:
    model = Model(MODEL_PATH)
    rec = KaldiRecognizer(model, SAMPLE_RATE)
    print("✅ Vosk (Fast) model loaded")
except Exception as e:
    print("❌ Failed to load Vosk model:", e)
    model = None
    rec = None

# =========================================
# Helper: Detect Wake from Partial Result
# =========================================
def detect_wake(recognizer, data):
    # Accept returns True if a full silence/end of utterance is reached
    # but we are interested in partials for speed
    if recognizer.AcceptWaveform(data):
        result = json.loads(recognizer.Result())
        text = result.get("text", "")
    else:
        # PartialResult gives us real-time hypothesis
        partial = recognizer.PartialResult()
        text = json.loads(partial).get("partial", "")

    # Check against all wake words
    if any(w in text for w in WAKE_WORDS):
        recognizer.Reset() # Reset immediately after detection
        return True, text
    
    return False, text

# =========================================
# Listen Loop
# =========================================
def listen_for_wake():
    if not rec:
        return False

    p = pyaudio.PyAudio()

    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=BLOCK_SIZE
    )

    print(f"⚡ Fast Listening for: {WAKE_WORDS}...")
    
    while True:
        data = stream.read(BLOCK_SIZE, exception_on_overflow=False)
        data_bytes = bytes(data)

        wake_detected, text = detect_wake(rec, data_bytes)
        
        if wake_detected:
            print(f"🔥 Wake Word Detected! ({text})")
            return True

    stream.stop_stream()
    stream.close()
    p.terminate()
