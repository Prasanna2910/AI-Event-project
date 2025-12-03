"""
Helper utility functions
"""

import re
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def clean_text(text):
    """
    Clean and normalize text
    
    Args:
        text (str): Raw text
        
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s\-.,!?@]', '', text)
    
    return text.strip()

def validate_email(email):
    """
    Validate email format
    
    Args:
        email (str): Email address
        
    Returns:
        bool: True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def format_date(date_string):
    """
    Convert various date formats to YYYY-MM-DD
    
    Args:
        date_string (str): Date in any format
        
    Returns:
        str: Date in YYYY-MM-DD format or original string
    """
    date_formats = [
        '%Y-%m-%d',
        '%d-%m-%Y',
        '%m-%d-%Y',
        '%d/%m/%Y',
        '%m/%d/%Y',
        '%B %d, %Y',
        '%b %d, %Y',
        '%d %B %Y',
        '%d %b %Y'
    ]
    
    for fmt in date_formats:
        try:
            date_obj = datetime.strptime(date_string.strip(), fmt)
            return date_obj.strftime('%Y-%m-%d')
        except ValueError:
            continue
    
    return date_string

def extract_emails_from_text(text):
    """
    Extract email addresses from text
    
    Args:
        text (str): Text containing emails
        
    Returns:
        list: List of email addresses
    """
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(pattern, text)

def save_uploaded_file(file, upload_folder):
    """
    Save uploaded file to upload folder
    
    Args:
        file: File object
        upload_folder (str): Path to upload folder
        
    Returns:
        str: Path to saved file
    """
    import os
    from werkzeug.utils import secure_filename
    
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    filename = secure_filename(file.filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{timestamp}_{filename}"
    filepath = os.path.join(upload_folder, filename)
    
    file.save(filepath)
    logger.info(f"File saved: {filepath}")
    
    return filepath

def log_api_call(endpoint, data, response):
    """
    Log API call details
    
    Args:
        endpoint (str): API endpoint
        data (dict): Request data
        response (dict): Response data
    """
    logger.info(f"API Call: {endpoint}")
    logger.debug(f"Request: {data}")
    logger.debug(f"Response: {response}")