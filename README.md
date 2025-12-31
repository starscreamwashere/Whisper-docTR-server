# Whisper & docTR Multi-Modal Pipeline

A professional-grade Flask server that intelligently routes and processes multi-modal inputs. This application handles audio transcription via **OpenAI Whisper** and handwritten/printed OCR via **Mindee docTR**, finally piping the extracted text to **Google Gemini 2.5 Flash Lite** for advanced summarization and context cleaning.

## 🚀 Features
- **In-Memory Processing:** Strictly adheres to in-memory processing requirements. Files are handled as byte streams via `io.BytesIO` and `FFmpeg` pipes, never touching the hard drive.
- **Persistent Model Memory:** AI models (Whisper and docTR) are loaded once into the server's RAM during startup for high-speed inference.
- **Intelligent Branching:** Automatically detects file formats and routes `.mp3/.wav` to the Whisper pipeline and `.jpg/.png/.pdf` to the docTR pipeline.
- **Gemini 2.5 Integration:** Leverages the latest `gemini-2.5-flash-lite` model for ultra-fast and efficient text refinement.

---

## 🛠️ Prerequisites
Ensure you have **FFmpeg** installed on your system to handle audio processing:
- **Mac:** `brew install ffmpeg`
- **Ubuntu/Linux:** `sudo apt install ffmpeg`

---

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/starscreamwashere/Whisper-docTR-server.git
   cd Whisper-docTR-server


Virtual Environment setup:

python3 -m venv venv
source venv/bin/activate

Dependency Installation

pip install -r requirements.txt

🔑 Environment Variables
Create a .env file in the root directory to store your Google AI credentials. This file is excluded from GitHub via .gitignore.

code
Text
GEMINI_API_KEY=your_gemini_api_key_here
🏃 How to Run
Launch the server on port 9000:

code
Bash
python run.py
Wait for the "Models Loaded" confirmation message before sending requests.

🧪 How to Test
You can use cURL to test the two pipeline branches directly from your terminal.

1. Test Audio (Whisper Branch)
code
Bash
curl -X POST -F "file=@/path/to/your/audio.mp3" http://localhost:9000/process | json_pp
2. Test Image/Handwriting (docTR Branch)
code
Bash
curl -X POST -F "file=@/path/to/your/handwritten_note.jpg" http://localhost:9000/process | json_pp
📁 Project Structure
code
Text
├── run.py              # Main entrance (Ignition)
├── .env                # API Keys (Protected)
├── requirements.txt    # Project dependencies
└── app/
    ├── routes.py       # API Endpoint & Routing logic
    ├── core/
        └── models.py   # Global model initialization (RAM persistence)
    └── services/
        ├── whisper_service.py # Audio-to-Text specialist
        ├── doctr_service.py   # Image-to-Text specialist
        └── gemini_service.py  # Gemini 2.5 Flash Lite pipeline