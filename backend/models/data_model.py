"""
Data models for event poster extraction
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class EventData:
    """Model for extracted event data"""
    event_name: str = "Not specified"
    artist_name: str = "Not specified"
    venue_name: str = "Not specified"
    venue_owner: str = "Not specified"
    date: str = "Not specified"
    time: str = "Not specified"
    location: str = "Not specified"
    artist_email: str = ""
    venue_email: str = ""
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'event_name': self.event_name,
            'artist_name': self.artist_name,
            'venue_name': self.venue_name,
            'venue_owner': self.venue_owner,
            'date': self.date,
            'time': self.time,
            'location': self.location,
            'artist_email': self.artist_email,
            'venue_email': self.venue_email
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create from dictionary"""
        return cls(
            event_name=data.get('event_name', 'Not specified'),
            artist_name=data.get('artist_name', 'Not specified'),
            venue_name=data.get('venue_name', 'Not specified'),
            venue_owner=data.get('venue_owner', 'Not specified'),
            date=data.get('date', 'Not specified'),
            time=data.get('time', 'Not specified'),
            location=data.get('location', 'Not specified'),
            artist_email=data.get('artist_email', ''),
            venue_email=data.get('venue_email', '')
        )

@dataclass
class EmailTemplate:
    """Model for email template"""
    template_id: str
    subject: str
    body: str
    recipient_type: str  # 'artist' or 'venue'
    
    def format_email(self, event_data: EventData) -> dict:
        """Format email with event data"""
        data_dict = event_data.to_dict()
        
        return {
            'subject': self.subject.format(**data_dict),
            'body': self.body.format(**data_dict),
            'to': data_dict.get('artist_email') if self.recipient_type == 'artist' else data_dict.get('venue_email')
        }