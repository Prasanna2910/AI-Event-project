import openai
import json
import logging
from config import Config

logger = logging.getLogger(__name__)
openai.api_key = Config.OPENAI_API_KEY

def categorize_with_gpt(ocr_text):
    """
    Use GPT to categorize extracted text into structured data
    
    Args:
        ocr_text (str): Raw text from OCR
        
    Returns:
        dict: Categorized data or None if failed
    """
    try:
        prompt = f"""
Extract and categorize the following event poster text into JSON format.

TEXT:
{ocr_text}

Return ONLY a valid JSON object with these exact fields:
{{
    "event_name": "name of the event",
    "artist_name": "name of the artist/performer",
    "venue_name": "name of the venue",
    "venue_owner": "name of venue owner if mentioned",
    "date": "event date in YYYY-MM-DD format",
    "time": "event time (e.g., 7:00 PM)",
    "location": "city and country"
}}

Rules:
- If any field is not found, use "Not specified"
- For dates, convert to YYYY-MM-DD format
- Extract only factual information from the text
- Do not add information that isn't in the text
"""
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a data extraction expert. Return only valid JSON without any markdown formatting or explanation."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )
        
        result = response.choices[0].message.content.strip()
        
        # Remove markdown code blocks if present
        if result.startswith('```'):
            result = result.split('```')[1]
            if result.startswith('json'):
                result = result[4:]
        
        # Parse JSON
        data = json.loads(result)
        
        logger.info(f"Successfully categorized data: {list(data.keys())}")
        return data
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse GPT response as JSON: {e}")
        return None
    except Exception as e:
        logger.error(f"Error in GPT categorization: {e}")
        return None