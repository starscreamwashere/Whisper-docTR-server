import os
import google.generativeai as genai

def analyze_text(text):
    # Initialize inside the function to ensure it uses the latest env vars
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    
    # You chose Gemini 2.0 Flash Lite - it's fast!
    model = genai.GenerativeModel('gemini-2.5-flash-lite') 
    
    prompt = f"""
    The following text was extracted from an AI pipeline (Whisper or docTR). 
    Please clean up any typos and provide a concise summary:
    
    TEXT: {text}
    """
    
    response = model.generate_content(prompt)
    return response.text