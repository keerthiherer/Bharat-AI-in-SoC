# =========================================
# Imports
# =========================================
import json
import re
import pickle

from wake_vosk import listen_loop
from wake_fast import listen_for_wake  # [NEW]
import system_info as sys
from tts_piper import speak
from llama_cpp import Llama
import nlu  # [NEW] Deterministic NLU
from knowledge_base import KnowledgeBase  # [NEW] Knowledge Base

#from rag import SimpleRAG   # your rag.py


# =========================================
# Load INTENT MODEL (ML)
# =========================================
intent_model = pickle.load(open("intent_model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# [NEW] Load Deterministic Intents
intent_map = nlu.load_intents("intent.json")
print(f"Loaded {len(intent_map)} deterministic keywords")

# [NEW] Load Knowledge Base
kb = KnowledgeBase()
print("✅ Knowledge Base loaded")


def predict_intent(text):
    X = vectorizer.transform([text])
    intent = intent_model.predict(X)[0]
    confidence = max(intent_model.predict_proba(X)[0])
    return intent, confidence


# =========================================
# Load RAG
# =========================================
#rag = SimpleRAG("rag.jsonl")


# =========================================
# Load Qwen ONCE
# =========================================
MODEL_PATH = "Llama-3.2-1B-Instruct-Q4_K_M.gguf"

print("Loading llama model...")

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=128,
    n_threads=4,
    n_batch=64,
    verbose=False
)

print("Qwen ready ✅")


# =========================================
# Qwen fallback
# =========================================
def qwen_reply(hindi_text):

    prompt = f"""आप एक हिंदी वॉयस असिस्टेंट हैं।
संक्षेप में उत्तर दें।

User: {hindi_text}
Assistant:"""

    result = llm(
        prompt=prompt,
        max_tokens=64,
        temperature=0.6,
        top_p=0.9,
        repeat_penalty=1.15
    )

    return result["choices"][0]["text"].strip()


# =========================================
# Start program
# =========================================
print("Program started")
speak("मैं तैयार हूँ")


# =========================================
# Main loop
# =========================================
while True:

    print("\nWaiting for Wake Word (Fast)...")
    
    # 1. Block until wake word detected (Fast Mode)
    if listen_for_wake():
        speak("हाँ बताइए")  # [ENABLED] Acknowledge wake word
        print("⚡ Listening for query ......")
        print("ask me anything about system info such as time, date, cpu, ram, disk, battery, temperature, network, ip, hostname or general knowledge questions about history, Indian history, politics, world GK and India GK")
        
        # 2. Listen for Command (Standard Mode with Timeout)
        # We still use the standard listen_loop for command capture as it handles full sentences better
    
    # 3. Listen for Command (Standard Mode with Timeout)
    # We still use the standard listen_loop for command capture as it handles full sentences better
    result = listen_loop(timeout=4.5)
    
    if not result:
        print("❌ Command timeout")
        continue

    text = result["text"]
    tokens = result["tokens"]

    print("Heard Command:", text)
    print("Tokens:", tokens)

    response = None

    try:
        # =====================================
        # INTENT (Deterministic + ML)
        # =====================================
        
        # 1. Deterministic Check
        intent = nlu.detect_intent(text, intent_map)
        if intent:
            conf = 1.0
            print(f"Deterministic Match: {intent}")
        else:
            # 2. ML Fallback
            intent, conf = predict_intent(text)
        
        print("Intent:", intent, "Confidence:", round(conf, 2))

        if conf > 0.65:   # confidence gate (VERY important)

            if intent == "time":
                response = f"अभी समय है {sys.time_now()}"

            elif intent == "date":
                response = f"आज की तारीख है {sys.date_today()}"

            elif intent == "day":
                response = f"आज {sys.day_today()} है"

            elif intent == "uptime":
                response = f"सिस्टम {sys.uptime()} से चालू है"

            elif intent == "cpu":
                response = f"सीपीयू उपयोग {sys.cpu()} है"

            elif intent == "ram":
                response = f"रैम उपयोग {sys.ram()} है"

            elif intent == "disk":
                response = f"डिस्क उपयोग {sys.disk()} है"

            elif intent == "battery":
                response = f"बैटरी {sys.battery()}"

            elif intent == "temperature":
                response = f"तापमान {sys.temp()}"

            elif intent == "network":
                response = sys.network()

            elif intent == "ip":
                response = f"आईपी एड्रेस है {sys.ip()}"

            elif intent == "hostname":
                response = f"कंप्यूटर का नाम है {sys.hostname()}"

            elif intent == "volume_up":
                response = "वॉल्यूम बढ़ा रहा हूँ"
                # Add volume up command here

            elif intent == "volume_down":
                response = "वॉल्यूम कम कर रहा हूँ"
                # Add volume down command here

            elif intent == "mute":
                response = "म्यूट कर रहा हूँ"
                # Add mute command here

            elif intent == "brightness_up":
                response = "स्क्रीन की चमक बढ़ा रहा हूँ"
                # Add brightness up command here

            elif intent == "brightness_down":
                response = "स्क्रीन की चमक कम कर रहा हूँ"
                # Add brightness down command here

            elif intent == "open_camera":
                response = "कैमरा खोल रहा हूँ"
                # Add open camera command here

            elif intent == "take_photo":
                response = "फोटो ले रहा हूँ"
                # Add take photo command here

            elif intent == "record_video":
                response = "वीडियो रिकॉर्ड कर रहा हूँ"
                # Add record video command here

            elif intent == "record_audio":
                response = "ऑडियो रिकॉर्ड कर रहा हूँ"
                # Add record audio command here

            elif intent == "open_browser":
                response = "ब्राउज़र खोल रहा हूँ"
                # Add open browser command here

            elif intent == "shutdown":
                response = "सिस्टम बंद कर रहा हूँ"
                # Add shutdown command here
                break

            elif intent == "restart":
                response = "सिस्टम रीस्टार्ट कर रहा हूँ"
                # Add restart command here
                break

            elif intent == "assistant_name":
                response = "मेरा नाम नोवा है"

            elif intent == "assistant_status":
                response = "मैं तैयार हूँ"

            elif intent == "history":
                # Search in history knowledge base
                answer = kb.get_history(text)
                if answer:
                    response = answer
                else:
                    response = "मुझे इस बारे में पूरी जानकारी नहीं है"

            elif intent == "indian_history":
                # Search in Indian history knowledge base
                answer = kb.get_indian_history(text)
                if answer:
                    response = answer
                else:
                    response = "मुझे इस बारे में पूरी जानकारी नहीं है"

            elif intent == "politics":
                # Search in politics knowledge base
                answer = kb.get_politics(text)
                if answer:
                    response = answer
                else:
                    response = "मुझे इस बारे में पूरी जानकारी नहीं है"

            elif intent == "world_gk":
                # Search in world general knowledge base
                answer = kb.get_world_gk(text)
                if answer:
                    response = answer
                else:
                    response = "मुझे इस बारे में पूरी जानकारी नहीं है"

            elif intent == "india_gk":
                # Search in India general knowledge base
                answer = kb.get_india_gk(text)
                if answer:
                    response = answer
                else:
                    response = "मुझे इस बारे में पूरी जानकारी नहीं है"

            elif intent == "exit":
                speak("अलविदा")
                break

        if not response:
            print("Using llama fallback")
            response = qwen_reply(text)

        # =====================================
        # SPEAK ONCE
        # =====================================
        if response:
            print("Reply:", response)
            speak(response)

    except KeyboardInterrupt:
        print("\nStopping...")
        break
    except Exception as e:
        print("Error:", e)
        speak("क्षमा करें, कुछ गलत हो गया")
