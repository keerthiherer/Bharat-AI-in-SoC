import os
import platform
import subprocess
import tempfile
import wave
from piper import PiperVoice
from piper.voice import SynthesisConfig

PIPER_MODEL = "piper/hi_IN-priyamvada-medium.onnx"

# Load the voice model once at module level for better performance
try:
    voice = PiperVoice.load(PIPER_MODEL)
    print("Piper voice model loaded successfully")
except Exception as e:
    print(f"Error loading Piper voice model: {e}")
    voice = None


def speak(text):
    if not text or not text.strip():
        return
    
    if voice is None:
        print("ERROR: Piper voice model not loaded")
        return

    try:
        print("Speaking text...")
    except UnicodeEncodeError:
        print("Speaking text (Unicode)")

    clean_text = text.strip()

    # Create temporary WAV file
    wav_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    wav_path = wav_file.name
    wav_file.close()

    try:
        # Configure synthesis (optional - adjust speed, etc.)
        config = SynthesisConfig()
        config.length_scale = 1.2  # Slightly slower speech
        
        # Synthesize the text - returns iterable of audio chunks
        audio_chunks = voice.synthesize(clean_text, syn_config=config)
        
        # Get sample rate from voice config
        sample_rate = voice.config.sample_rate
        
        # Write audio chunks to WAV file
        with wave.open(wav_path, "wb") as wav:
            # Set WAV file parameters
            wav.setnchannels(1)  # Mono audio
            wav.setsampwidth(2)  # 16-bit audio (2 bytes per sample)
            wav.setframerate(sample_rate)
            
            # Write all audio chunks
            for audio_chunk in audio_chunks:
                wav.writeframes(audio_chunk.audio_int16_bytes)

        # Check if file was created and has content
        if not os.path.exists(wav_path) or os.path.getsize(wav_path) == 0:
            print("ERROR: WAV file was not created or is empty")
            return

        # Play the audio file
        if platform.system() == "Windows":
            subprocess.run([
                "powershell",
                "-c",
                f'(New-Object Media.SoundPlayer "{wav_path}").PlaySync();'
            ], check=False)
        else:
            subprocess.run(["aplay", wav_path], check=False)

    except Exception as e:
        print(f"ERROR during speech synthesis or playback: {e}")
    finally:
        # Clean up temporary file
        try:
            if os.path.exists(wav_path):
                os.remove(wav_path)
        except:
            pass
