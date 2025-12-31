# app/core/models.py
import whisper
from doctr.models import ocr_predictor
import torch

# Logic: Load once, use everywhere
print("Loading models into RAM...")
device = "cuda" if torch.cuda.is_available() else "cpu"

# These variables stay in memory
WHISPER_MODEL = whisper.load_model("tiny", device=device)
DOCTR_MODEL = ocr_predictor(pretrained=True)