import os
import whisper
import torch
from doctr.models import ocr_predictor, db_resnet50, crnn_vgg16_bn

# --- LOGIC: DYNAMIC BASE DIRECTORY ---
# Finds the 'WhisperDoctrServer' root folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

device = "cuda" if torch.cuda.is_available() else "cpu"

# --- WHISPER LOGIC ---
# Points to the manual weights folder
whisper_path = os.path.join(BASE_DIR, "model_weights", "whisper_tiny", "tiny.pt")

print(f"Loading Whisper from: {whisper_path}")
# Logic: Point directly to the local .pt file
WHISPER_MODEL = whisper.load_model(whisper_path, device=device)

# --- DOCTR LOGIC ---
print("Loading docTR manually from model_weights/docTR_ocr...")

# Detector
det_model = db_resnet50(pretrained=False)
det_path = os.path.join(BASE_DIR, "model_weights", "docTR_ocr", "db_resnet50.pt")
det_model.load_state_dict(torch.load(det_path, map_location="cpu"))

# Recognizer
reco_model = crnn_vgg16_bn(pretrained=False)
reco_path = os.path.join(BASE_DIR, "model_weights", "docTR_ocr", "crnn_vgg16_bn.pt")
reco_model.load_state_dict(torch.load(reco_path, map_location="cpu"))

DOCTR_MODEL = ocr_predictor(det_arch=det_model, reco_arch=reco_model)

print("Status: All models initialized locally and resident in RAM!")