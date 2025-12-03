"""
Email preview component
"""

import streamlit as st

def render_email_preview(email_data, template_name):
    """
    Render email preview section
    
    Args:
        email_data (dict): Email data with to, subject, body
        template_name (str): Name of selected template
    """
    
    st.markdown('<div class="step-header">📧 Step 4: Email Preview & Send</div>', unsafe_allow_html=True)
    
    # Email details
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("📨 To:", value=email_data['to'], disabled=True)
    with col2:
        st.text_input("📌 Subject:", value=email_data['subject'], disabled=True)
    
    # Email body
    st.text_area(
        "📄 Email Body:",
        value=email_data['body'],
        height=300,
        disabled=True
    )
    
    # Template info
    st.info(f"📋 Using template: **{template_name}**")