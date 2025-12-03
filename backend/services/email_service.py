import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from config import Config

logger = logging.getLogger(__name__)

def send_email(to_email, subject, body):
    """
    Send email using SMTP
    
    Args:
        to_email (str): Recipient email address
        subject (str): Email subject
        body (str): Email body text
        
    Returns:
        bool: True if sent successfully, False otherwise
    """
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = Config.EMAIL_ADDRESS
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Attach body
        msg.attach(MIMEText(body, 'plain'))
        
        # Connect to SMTP server
        server = smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT)
        server.starttls()
        
        # Login
        server.login(Config.EMAIL_ADDRESS, Config.EMAIL_PASSWORD)
        
        # Send email
        server.send_message(msg)
        
        # Close connection
        server.quit()
        
        logger.info(f"Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return False

def send_bulk_emails(email_list):
    """
    Send emails to multiple recipients
    
    Args:
        email_list (list): List of dicts with 'to', 'subject', 'body'
        
    Returns:
        dict: Results with success/failure counts
    """
    results = {
        'sent': 0,
        'failed': 0,
        'errors': []
    }
    
    for email_data in email_list:
        success = send_email(
            email_data['to'],
            email_data['subject'],
            email_data['body']
        )
        
        if success:
            results['sent'] += 1
        else:
            results['failed'] += 1
            results['errors'].append(email_data['to'])
    
    return results