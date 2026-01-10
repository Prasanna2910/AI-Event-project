"""
Sidebar component
"""

import streamlit as st
from ._compat import safe_button

def render_sidebar(api_client):
    """
    Render sidebar with instructions and configuration
    
    Args:
        api_client: API client instance
    """
    
    with st.sidebar:
        st.header("📖 Instructions")
        st.markdown("""
        ### Setup Required:
        1. **OpenAI API Key**: Set in backend/.env
        2. **Google Sheets**: Configure credentials.json
        3. **Email**: Set SMTP credentials
        4. **Tesseract OCR**: Install on system
        
        ### Features:
        - ✅ OCR text extraction
        - ✅ GPT-powered categorization
        - ✅ Google Sheets integration
        - ✅ Social media email scraping
        - ✅ Custom email templates
        - ✅ Automated sending
        
        ### Tips:
        - Use high-quality poster images
        - Ensure clear text visibility
        - Check extracted data before sending
        """)
        
        st.markdown("---")
        st.header("⚙️ Configuration")
        
        # Backend connection test
        if safe_button("🔌 Test Backend Connection", use_container_width=True):
            with st.spinner("Testing connection..."):
                if api_client.test_connection():
                    st.success("✅ Backend connected!")
                else:
                    st.error("❌ Backend not running")
        
        st.markdown("---")
        st.caption("Made with ❤️ using Streamlit")