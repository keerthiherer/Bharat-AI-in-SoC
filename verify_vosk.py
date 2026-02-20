from wake_vosk import listen_loop
import sys

print("Verifying Vosk Audio Integration...")
print("Please speak the wake word 'जार्विस' (Jarvis) or any sentence...")

try:
    result = listen_loop()
    if result:
        print(f"Success! Received: {result}")
    else:
        print("Failed: listen_loop returned None")
except KeyboardInterrupt:
    print("\nTest cancelled by user.")
except Exception as e:
    print(f"\nError during test: {e}")
