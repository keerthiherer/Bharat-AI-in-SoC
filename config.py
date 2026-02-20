# config.py

# Wake words list - Easy to change
WAKE_WORDS = [
    "ira", "vira", "वीरा",     # Ira (Vira)
    "aiva", "ava", "ऐवा",      # Aiva
    "ziva", "ज़ीवा",           # Ziva
    "kiva", "कीवा",            # Kiva
    "tiva", "टीवा",            # Tiva
    "reva", "रेवा",            # Reva
    "niva", "नीवा"             # Niva
]

# Audio Noise Threshold
# Adjust this based on your microphone. 
# Typical values: 500-2000 for skipping absolute silence/static.
NOISE_THRESHOLD = 800

# Messages
MSG_CAMERA_NOT_FOUND = "कौई कैमरा नहीं मिला"  # No camera found
MSG_CAMERA_OPENING = "कैमरा खोल रहा हूँ"      # Opening camera
MSG_PHOTO_MODE = "फोटो लेने के लिए कैमरा खोल रहा हूँ"
MSG_VIDEO_MODE = "वीडियो रिकॉर्डिंग के लिए कैमरा खोल रहा हूँ"
