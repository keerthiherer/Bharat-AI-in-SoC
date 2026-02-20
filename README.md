# BHARAT Hackathon - Version 4

## Overview
This project is a voice assistant application designed to understand and respond to user commands in Hindi. It integrates various components such as Natural Language Understanding (NLU), a knowledge base, and a text-to-speech system to provide a seamless user experience.

## Features
- **Voice Activation**: Detects wake words to start listening for commands.
- **Intent Recognition**: Uses deterministic and machine learning models to predict user intent.
- **Knowledge Base Integration**: Provides answers to queries related to history, politics, and general knowledge.
- **System Information**: Retrieves system details like time, date, CPU usage, and more.
- **Device Control**: Handles commands for volume, brightness, and other device settings.
- **Fallback Responses**: Uses a language model for generating fallback responses.

## Components
- **`main.py`**: The entry point of the application.
- **`nlu.py`**: Handles deterministic intent recognition.
- **`knowledge_base.py`**: Manages the knowledge base for answering queries.
- **`tts_piper.py`**: Converts text to speech for voice responses.
- **`wake_vosk.py` and `wake_fast.py`**: Modules for wake word detection.
- **`system_info.py`**: Retrieves system-related information.

## Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd BHARAT_Hackathon/version_4
   ```
3. Create and activate a virtual environment:
   ```bash
   python -m venv env
   source env/Scripts/activate  # On Windows
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Download the LLaMA model manually:
   The LLaMA model("Llama-3.2-1B-Instruct-Q4_K_M.gguf
") is large and cannot be downloaded automatically with `git clone`. Please download it manually from the official source and place it in the appropriate directory.

## Usage
Run the application:
```bash
python main.py
```

## File Structure
```
version_4/
├── main.py
├── nlu.py
├── knowledge_base.py
├── tts_piper.py
├── wake_vosk.py
├── wake_fast.py
├── system_info.py
├── requirements.txt
├── intent_model.pkl
├── vectorizer.pkl
├── intent.json
├── rag.jsonl
└── README.md
```

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
- [Vosk](https://alphacephei.com/vosk/) for speech recognition.
- [Llama.cpp](https://github.com/ggerganov/llama.cpp) for the language model.
- [Piper](https://github.com/rhasspy/piper) for text-to-speech.

## Available Intents
The following intents are supported by the assistant:
- Time now
- Date today
- Day today
- Uptime
- CPU
- RAM
- Disk
- Battery
- Temperature
- Network
- IP
- Hostname
- Exit
- Assistant name


- [YouTube Video](https://youtu.be/9GAmdWQPYAs?si=LrKyObqjtNqTr6r1)
- [Google Docs](https://docs.google.com/document/d/1eTeMM_WQV1RSw3g_AJOOADFR9tMXSNfenoZrmbFVsgM/edit?tab=t.0#heading=h.21j944wawsvl)
