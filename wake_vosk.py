import pyaudio
import json
import numpy as np
from vosk import Model, KaldiRecognizer
import re

# =========================================
# CONFIG
# =========================================

WAKE_WORDS = ["इवा", "iva", "kira", "ava", "hyva", "hey nova", "hey"]  # check multiple
MODEL_PATH = "vosk-model-small-hi-0.22"

SAMPLE_RATE = 16000
BLOCK_SIZE = 4000          # 0.5 sec
RMS_THRESHOLD = 30         # VERY LOW (important)
MIN_TOKENS = 1             # allow even 1-word speech


# =========================================
# Load Vosk model ONCE
# =========================================
try:
    model = Model(MODEL_PATH)
    rec = KaldiRecognizer(model, SAMPLE_RATE)
    rec.SetWords(False)
    rec.SetPartialWords(False)
    print("✅ Vosk model loaded")
except Exception as e:
    print("❌ Failed to load Vosk model:", e)
    model = None
    rec = None


# =========================================
# Tokenizer
# =========================================
"""def tokenize(text):
    text = re.sub(r"[^\w\s\u0900-\u097F]", "", text)
    return text.strip().split()
"""
def tokenize(text):
    return text.strip().split()



# =========================================
# Audio device helper
# =========================================
def get_input_device_index():
    # IMPORTANT:
    # If mic does not work, replace None with the correct mic index
    return None


# =========================================
# Listen loop
# =========================================
import time  # [NEW]

def listen_loop(timeout=None):  # [NEW] timeout support
    if not rec:
        print("❌ Vosk not ready")
        return None

    rec.Reset()

    try:
        p = pyaudio.PyAudio()

        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=SAMPLE_RATE,
            input=True,
            frames_per_buffer=BLOCK_SIZE,
            stream_callback=None
        )

        print("🎤 Listening...")
        start_time = time.time()  # [NEW]

        while True:
            # [NEW] Check timeout
            if timeout and (time.time() - start_time > timeout):
                print("⏰ Timeout reached")
                
                # Try to get partial result!
                partial = rec.PartialResult()
                p_text = json.loads(partial).get("partial", "").strip()
                
                if p_text:
                    print(f"⚠️ Recovered partial command: {p_text}")
                    tokens = tokenize(p_text)
                    wake = any(t in WAKE_WORDS for t in tokens)
                    return {
                        "wake": wake,
                        "text": p_text,
                        "tokens": tokens
                    }
                
                return None

            data = stream.read(BLOCK_SIZE, exception_on_overflow=False)

            audio_np = np.frombuffer(data, dtype=np.int16)

            # ---------------------------------
            # Light noise gate
            # ---------------------------------
            rms = np.sqrt(np.mean(audio_np.astype(np.float32) ** 2))
            if rms < RMS_THRESHOLD:
                continue

            # ---------------------------------
            # Speech recognition
            # ---------------------------------
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "").strip()

                if not text:
                    continue

                tokens = tokenize(text)

                if len(tokens) < MIN_TOKENS:
                    continue

                # [NEW] Check against list
                wake = any(t in WAKE_WORDS for t in tokens)

                print("\n🗣 Recognized:", text)
                print("🔹 Tokens:", tokens)
                print("🔔 Wake:", wake)

                return {
                    "wake": wake,
                    "text": text,
                    "tokens": tokens
                }

    except Exception as e:
        print("❌ Audio error:", e)
        return None