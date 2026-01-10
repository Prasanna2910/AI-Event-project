"""
Upload section component
"""

import streamlit as st
from PIL import Image
import io
from ._compat import safe_image

def render_upload_section():
    """Render the image upload section"""
    
    st.markdown('<div class="step-header">📤 Step 1: Upload Event Poster</div>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose a poster image",
        type=['jpg', 'jpeg', 'png', 'pdf'],
        help="Upload a clear image of the event poster for best results"
    )
    
    if uploaded_file is not None:
        # Display image
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            image = Image.open(uploaded_file)
            safe_image(image, caption="Uploaded Poster", use_container_width=True)
        
        return uploaded_file, image
    
    return None, None