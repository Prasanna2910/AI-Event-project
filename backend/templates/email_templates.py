EMAIL_TEMPLATES = {
    'good_artist': {
        'subject': 'Exciting Opportunity: Perform at {event_name}',
        'body': '''Dear {artist_name},

We are thrilled to invite you to perform at {event_name}!

Your exceptional talent and unique style have caught our attention, and we believe your performance would make this event truly memorable for our audience.

📅 Event Details:
- Date: {date}
- Time: {time}
- Venue: {venue_name}
- Location: {location}

We would love to discuss the details further, including:
- Performance duration and set requirements
- Technical specifications
- Compensation and travel arrangements

Please let us know your availability and any requirements you may have.

Looking forward to collaborating with you!

Best regards,
Event Management Team

---
This is an automated email. Please reply to confirm your interest.'''
    },
    
    'bad_artist': {
        'subject': 'Re: {event_name} Performance Opportunity',
        'body': '''Dear {artist_name},

Thank you for your interest in performing at {event_name}.

After careful consideration of all applications, we regret to inform you that we will not be able to include you in the lineup for this particular event. We received an overwhelming number of talented applications and had to make some difficult decisions based on our event's specific requirements and theme.

We genuinely appreciate your interest and encourage you to stay connected with us for future opportunities. Your talent is valued, and we hope to find a suitable collaboration in the future.

Wishing you all the best in your artistic journey!

Warm regards,
Event Management Team

---
Please do not reply to this automated email.'''
    },
    
    'good_venue': {
        'subject': 'Partnership Confirmation: {event_name}',
        'body': '''Dear {venue_owner},

Thank you for agreeing to host {event_name} at {venue_name}!

We greatly appreciate your excellent facilities and professional service. Your venue provides the perfect setting for this event, and we're confident it will be a great success.

📅 Event Details:
- Event: {event_name}
- Date: {date}
- Time: {time}
- Featuring: {artist_name}
- Location: {location}

Next Steps:
1. Technical specifications and setup requirements
2. Capacity and seating arrangements
3. Catering and hospitality details
4. Insurance and safety protocols

We'll be in touch within the next few days to finalize the logistics and coordinate with your team.

Looking forward to a successful partnership!

Best regards,
Event Management Team

---
This is an automated confirmation. Our team will contact you shortly.'''
    },
    
    'bad_venue': {
        'subject': 'Re: Venue Inquiry for {event_name}',
        'body': '''Dear {venue_owner},

Thank you for your proposal and for taking the time to show us {venue_name}.

After evaluating all available options for {event_name}, we have decided to proceed with an alternative venue that better aligns with our specific requirements for this particular event, including capacity, technical specifications, and budget considerations.

We appreciate your professionalism and time throughout this process. Your venue has many excellent qualities, and we hope to explore opportunities for collaboration in future events.

We will keep your contact information on file and reach out when we have an event that would be a better fit for {venue_name}.

Thank you for your understanding.

Best regards,
Event Management Team

---
Please do not reply to this automated email.'''
    }
}