import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import logging
from config import Config

logger = logging.getLogger(__name__)

def init_google_sheets():
    """
    Initialize Google Sheets connection
    
    Returns:
        gspread.Worksheet: The worksheet object or None if failed
    """
    try:
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            Config.GOOGLE_CREDENTIALS_FILE,
            scope
        )
        client = gspread.authorize(creds)
        
        try:
            sheet = client.open(Config.SPREADSHEET_NAME).sheet1
            logger.info(f"Connected to existing sheet: {Config.SPREADSHEET_NAME}")
        except gspread.SpreadsheetNotFound:
            spreadsheet = client.create(Config.SPREADSHEET_NAME)
            sheet = spreadsheet.sheet1
            
            # Set headers
            headers = [
                'Timestamp',
                'Event Name',
                'Artist Name',
                'Venue Name',
                'Venue Owner',
                'Date',
                'Time',
                'Location',
                'Artist Email',
                'Venue Email'
            ]
            sheet.insert_row(headers, 1)
            
            # Format header row
            sheet.format('A1:J1', {
                'textFormat': {'bold': True},
                'backgroundColor': {'red': 0.2, 'green': 0.6, 'blue': 0.9}
            })
            
            logger.info(f"Created new sheet: {Config.SPREADSHEET_NAME}")
        
        return sheet
        
    except Exception as e:
        logger.error(f"Error initializing Google Sheets: {e}")
        return None

def save_to_google_sheets(data, sheet):
    """
    Save extracted data to Google Sheets
    
    Args:
        data (dict): Extracted event data
        sheet (gspread.Worksheet): The worksheet object
        
    Returns:
        bool: True if successful, False otherwise
    """
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
        logger.info("Data saved to Google Sheets successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error saving to Google Sheets: {e}")
        return False