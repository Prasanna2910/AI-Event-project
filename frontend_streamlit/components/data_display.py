"""
Data display component
"""

import streamlit as st

def render_data_display(data):
    """
    Render extracted data display
    
    Args:
        data (dict): Extracted event data
    """
    
    st.markdown('<div class="step-header">📋 Step 2: Extracted Details</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("🎪 Event Name", value=data.get('event_name', ''), disabled=True)
        st.text_input("🏛️ Venue Name", value=data.get('venue_name', ''), disabled=True)
        st.text_input("📅 Date", value=data.get('date', ''), disabled=True)
        st.text_input("📧 Artist Email", value=data.get('artist_email', ''), disabled=True)
    
    with col2:
        st.text_input("🎤 Artist Name", value=data.get('artist_name', ''), disabled=True)
        st.text_input("👤 Venue Owner", value=data.get('venue_owner', ''), disabled=True)
        st.text_input("⏰ Time", value=data.get('time', ''), disabled=True)
        st.text_input("📧 Venue Email", value=data.get('venue_email', ''), disabled=True)
    
    st.text_input("📍 Location", value=data.get('location', ''), disabled=True)
    
    st.markdown('<div class="success-box">✅ Data automatically saved to Google Sheets</div>', unsafe_allow_html=True)