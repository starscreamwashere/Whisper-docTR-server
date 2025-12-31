from flask import request, jsonify
from app.services.whisper_service import process_audio
from app.services.doctr_service import process_ocr
from app.services.gemini_service import analyze_text

def init_routes(app):
    @app.route('/process', methods=['POST'])
    def handle_pipeline():
        # 1. Validation Logic
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
            
        file = request.files['file']
        filename = file.filename.lower()

        try:
            # 2. Branching Logic
            if filename.endswith(('.mp3', '.wav', '.m4a')):
                print("Using Whisper Branch...")
                extracted_text = process_audio(file)
                
            elif filename.endswith(('.pdf', '.png', '.jpg', '.jpeg')):
                print("Using docTR Branch...")
                extracted_text = process_ocr(file)
                
            else:
                return jsonify({"error": "Unsupported file format"}), 400

            # 3. Pipeline Logic (The hand-off to Gemini)
            if not extracted_text:
                return jsonify({"error": "No text could be extracted"}), 500
                
            print("Sending to Gemini...")
            ai_analysis = analyze_text(extracted_text)

            # 4. Response Logic
            return jsonify({
                "status": "success",
                "filename": filename,
                "raw_text": extracted_text,
                "gemini_analysis": ai_analysis
            })

        except Exception as e:
            return jsonify({"error": str(e)}), 500