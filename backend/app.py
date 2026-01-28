# app.py - Flask Backend with Google Gemini
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import pytesseract
from PIL import Image
import io
import base64
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Initialize model lazily (only when needed)
model = None

def get_gemini_model():
    """Get or initialize Gemini model"""
    global model
    if model is None:
        if not GEMINI_API_KEY or len(GEMINI_API_KEY) < 20:
            raise ValueError("GEMINI_API_KEY not configured. Please set your real API key in .env file")
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-2.5-flash")
    return model

# Google Sheets Configuration
SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
CREDENTIALS_FILE = 'credentials.json'
SPREADSHEET_NAME = 'Event Poster Data'

# Email Configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

# Email Templates
EMAIL_TEMPLATES = {
    'good_artist': {
        'subject': 'Exciting Opportunity: {event_name}',
        'body': '''Dear {artist_name},

We are thrilled to invite you to perform at {event_name} on {date} at {venue_name}.

Your exceptional talent and unique style have caught our attention, and we believe your performance would make this event truly memorable for our audience.

Event Details:
- Date: {date}
- Time: {time}
- Venue: {venue_name}
- Location: {location}

We would love to discuss the details further. Please let us know your availability and requirements.

Looking forward to collaborating with you!

Best regards,
Event Management Team'''
    },
    'bad_artist': {
        'subject': 'Re: {event_name} Performance Opportunity',
        'body': '''Dear {artist_name},

Thank you for your interest in performing at {event_name}.

After careful consideration of all applicants, we regret to inform you that we will not be able to include you in the lineup for this particular event. We received an overwhelming number of talented applications and had to make some difficult decisions.

We appreciate your understanding and encourage you to stay connected with us for future opportunities.

Wishing you all the best in your artistic journey!

Regards,
Event Management Team'''
    },
    'good_venue': {
        'subject': 'Partnership Confirmation: {event_name}',
        'body': '''Dear {venue_owner},

Thank you for agreeing to host {event_name} at {venue_name} on {date}.

We greatly appreciate your excellent facilities and professional service. Your venue provides the perfect setting for this event, and we're confident it will be a great success.

Event Details:
- Date: {date}
- Time: {time}
- Expected Attendance: TBD
- Setup Requirements: TBD

We'll be in touch soon to finalize the logistics and technical requirements.

Looking forward to a successful partnership!

Best regards,
Event Management Team'''
    },
    'bad_venue': {
        'subject': 'Re: Venue Inquiry for {event_name}',
        'body': '''Dear {venue_owner},

Thank you for your proposal and for taking the time to show us {venue_name}.

After evaluating all available options, we have decided to proceed with an alternative venue that better aligns with our specific requirements for {event_name}.

We appreciate your professionalism and time, and we hope to explore opportunities for collaboration in the future.

Thank you for your understanding.

Regards,
Event Management Team'''
    }
}


def init_google_sheets():
    """Initialize Google Sheets connection"""
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPE)
        client = gspread.authorize(creds)
        
        try:
            sheet = client.open(SPREADSHEET_NAME).sheet1
        except gspread.SpreadsheetNotFound:
            spreadsheet = client.create(SPREADSHEET_NAME)
            sheet = spreadsheet.sheet1
            # Set headers
            headers = ['Timestamp', 'Event Name', 'Artist Name', 'Venue Name', 
                      'Venue Owner', 'Date', 'Time', 'Location', 
                      'Artist Email', 'Venue Email']
            sheet.insert_row(headers, 1)
        
        return sheet
    except Exception as e:
        print(f"Error initializing Google Sheets: {e}")
        return None


def extract_text_from_image(image_data):
    """Extract text from image using OCR"""
    try:
        # Decode base64 image
        if 'base64,' in image_data:
            image_data = image_data.split('base64,')[1]
        
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        
        # Perform OCR
        text = pytesseract.image_to_string(image)
        print(f"OCR extracted text: {text[:200]}...")
        return text
    except Exception as e:
        print(f"Error in OCR: {e}")
        return None


def categorize_with_gemini(ocr_text):
    """Use Google Gemini to categorize extracted text into structured data"""
    try:
        model = get_gemini_model()
            
        prompt = f"""
Extract and categorize the following event poster text into JSON format.

TEXT:
{ocr_text}

Return ONLY a valid JSON object (no markdown, no code blocks) with these exact fields:
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
- Return ONLY the JSON object, no explanation
"""
        
        print("Calling Google Gemini API...")
        response = model.generate_content(prompt)
        result = response.text.strip()
        
        print(f"Gemini response: {result[:200]}...")
        
        # Remove markdown code blocks if present
        if result.startswith('```'):
            result = result.split('```')[1]
            if result.startswith('json'):
                result = result[4:]
            result = result.strip()
        
        # Parse JSON
        data = json.loads(result)
        print(f"Successfully parsed data: {list(data.keys())}")
        return data
        
    except json.JSONDecodeError as e:
        print(f"JSON Parse Error: {e}")
        print(f"Response was: {result}")
        # Return default structure
        return {
            "event_name": "Not specified",
            "artist_name": "Not specified",
            "venue_name": "Not specified",
            "venue_owner": "Not specified",
            "date": "Not specified",
            "time": "Not specified",
            "location": "Not specified"
        }
    except Exception as e:
        print(f"Error in Gemini categorization: {e}")
        raise


def scrape_email_from_social(name, platform='instagram'):
    """
    Scrape email from Instagram/Facebook
    Note: This is a simplified version.
    """
    try:
        # Placeholder for actual scraping logic
        clean_name = name.lower().replace(' ', '').replace('the', '')
        return f"contact@{clean_name}.com"
        
    except Exception as e:
        print(f"Error scraping email: {e}")
        return "email@example.com"


def save_to_google_sheets(data, sheet):
    """Save extracted data to Google Sheets"""
    try:
        row = [
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            data.get('event_name', ''),
            data.get('artist_name', ''),
            data.get('venue_name', ''),
            data.get('venue_owner', ''),
            data.get('date', ''),
            data.get('time', ''),
            data.get('location', ''),
            data.get('artist_email', ''),
            data.get('venue_email', '')
        ]
        sheet.append_row(row)
        return True
    except Exception as e:
        print(f"Error saving to Google Sheets: {e}")
        return False


def send_email(to_email, subject, body):
    """Send email using SMTP"""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)  # Connect to SMTP server
        server.starttls() #encrypting the connection
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD) 
        server.send_message(msg)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Backend is running with Google Gemini'
    })


@app.route('/api/extract', methods=['POST'])
def extract_poster_data():
    """Main endpoint to extract data from poster"""
    try:
        data = request.json
        print("Received request to /api/extract")
        
        image_data = data.get('image')
        
        if not image_data:
            return jsonify({'success': False, 'error': 'No image provided'}), 400
        
        print("Step 1: Extracting text with OCR...")
        ocr_text = extract_text_from_image(image_data)
        if not ocr_text:
            return jsonify({'success': False, 'error': 'Failed to extract text from image'}), 500
        
        print("Step 2: Categorizing with Gemini...")
        categorized_data = categorize_with_gemini(ocr_text)
        if not categorized_data:
            return jsonify({'success': False, 'error': 'Failed to categorize data'}), 500
        
        print("Step 3: Scraping emails...")
        artist_email = scrape_email_from_social(
            categorized_data.get('artist_name', ''),
            platform='instagram'
        )
        venue_email = scrape_email_from_social(
            categorized_data.get('venue_name', ''),
            platform='facebook'
        )
        
        categorized_data['artist_email'] = artist_email
        categorized_data['venue_email'] = venue_email
        
        print("Step 4: Saving to Google Sheets...")
        sheet = init_google_sheets()
        if sheet:
            save_to_google_sheets(categorized_data, sheet)
        
        print("Success! Returning data...")
        return jsonify({
            'success': True,
            'data': categorized_data
        })
        
    except Exception as e:
        print(f"Error in extract endpoint: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/generate-email', methods=['POST'])
def generate_email():
    """Generate email from template"""
    try:
        data = request.json
        template_type = data.get('template_type')
        event_data = data.get('event_data')
        
        if template_type not in EMAIL_TEMPLATES:
            return jsonify({'error': 'Invalid template type'}), 400
        
        template = EMAIL_TEMPLATES[template_type]
        
        # Format email with event data
        subject = template['subject'].format(**event_data)
        body = template['body'].format(**event_data)
        
        # Determine recipient
        if 'artist' in template_type:
            recipient = event_data.get('artist_email')
        else:
            recipient = event_data.get('venue_email')
        
        return jsonify({
            'success': True,
            'email': {
                'to': recipient,
                'subject': subject,
                'body': body
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/send-email', methods=['POST'])
def send_email_endpoint():
    """Send the generated email"""
    try:
        data = request.json
        to_email = data.get('to')
        subject = data.get('subject')
        body = data.get('body')
        
        success = send_email(to_email, subject, body)
        
        if success:
            return jsonify({'success': True, 'message': 'Email sent successfully'})
        else:
            return jsonify({'error': 'Failed to send email'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/templates', methods=['GET'])
def get_templates():
    """Get all available email templates"""
    templates = []
    for key, value in EMAIL_TEMPLATES.items():
        templates.append({
            'id': key,
            'name': key.replace('_', ' ').title()
        })
    return jsonify(templates)


if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Starting Event Poster Extractor Backend")
    print("Using Google Gemini for AI processing")
    print("Backend will run on: http://localhost:5000")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=6100)