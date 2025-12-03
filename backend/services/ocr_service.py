import pytesseract
from PIL import Image
import io
import base64
import logging

logger = logging.getLogger(__name__)

def extract_text_from_image(image_data):
    """
    Extract text from image using Tesseract OCR
    
    Args:
        image_data (str): Base64 encoded image data
        
    Returns:
        str: Extracted text or None if failed
    """
    try:
        # Remove data URL prefix if present
        if 'base64,' in image_data:
            image_data = image_data.split('base64,')[1]
        
        # Decode base64 image
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Perform OCR with custom config for better accuracy
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(image, config=custom_config)
        
        logger.info(f"Extracted text length: {len(text)} characters")
        return text.strip()
        
    except Exception as e:
        logger.error(f"Error in OCR extraction: {e}")
        return None