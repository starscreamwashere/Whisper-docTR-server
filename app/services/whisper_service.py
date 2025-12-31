import numpy as np
import subprocess
import io
from app.core.models import WHISPER_MODEL

def process_audio(file_storage):
    """
    Processes audio purely in memory using FFmpeg and Numpy.
    Bypasses the 'audioop' error in Python 3.13/3.14.
    """
    # 1. Logic: Read the file's raw data into memory
    file_bytes = file_storage.read()

    # 2. Logic: Run FFmpeg as a 'Sub-Process'
    # -i pipe:0 -> Take input from memory (stdin)
    # -ac 1     -> Convert to Mono
    # -ar 16000 -> Set sample rate to 16kHz (Whisper's favorite)
    # -f f32le  -> Output raw 32-bit floats
    # pipe:1    -> Send result back to memory (stdout)
    command = [
        "ffmpeg",
        "-i", "pipe:0",
        "-ac", "1",
        "-ar", "16000",
        "-f", "f32le",
        "-acodec", "pcm_f32le",
        "pipe:1"
    ]

    # Start the conversation with FFmpeg
    process = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Push the file bytes in, and catch the converted audio out
    out, err = process.communicate(input=file_bytes)

    if process.returncode != 0:
        raise Exception(f"FFmpeg error: {err.decode()}")

    # 3. Logic: Convert the binary output into a Numpy list of numbers
    audio_data = np.frombuffer(out, np.float32)

    # 4. Logic: Feed the numbers to the Whisper brain
    print("Whisper is listening to the memory buffer...")
    result = WHISPER_MODEL.transcribe(audio_data)
    
    return result['text']