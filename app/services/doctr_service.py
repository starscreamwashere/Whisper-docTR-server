import io
import numpy as np
from PIL import Image
from app.core.models import DOCTR_MODEL

def process_ocr(file_storage):
    """
    Logic: Converts raw bytes into a 'Pixel Array' so docTR can see it.
    """
    # 1. Logic: Read the raw bytes from the upload
    file_bytes = file_storage.read()

    # 2. Logic: The 'Unwrapper' 
    # We turn the bytes into an Image object, and then into a Numpy Array
    image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
    image_array = np.array(image)

    # 3. Logic: Feed the array (which now has 'ndim'!) to the model
    # Note: docTR expects a list of images, so we put it in brackets [ ]
    result = DOCTR_MODEL([image_array])

    # 4. Logic: Extract text from the result
    extracted_text = ""
    json_output = result.export()

    for page in json_output['pages']:
        for block in page['blocks']:
            for line in block['lines']:
                for word in line['words']:
                    extracted_text += word['value'] + " "
                    
    return extracted_text.strip()