import streamlit as st
import requests
import base64
from PIL import Image
import io
import sys
import os

# Add components to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'components'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from utils.api_client import APIClient
from components._compat import safe_image, safe_button

# Configure Streamlit page
st.set_page_config(
    page_title="Event Poster Data Extractor",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(to right, #9333ea, #2563eb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #6b7280;
        margin-bottom: 2rem;
        font-size: 1.1rem;
    }
    .step-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #374151;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-left: 10px;
        border-left: 4px solid #9333ea;
    }
    .success-box {
        padding: 1rem;
        background-color: #d1fae5;
        border-left: 4px solid #10b981;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        background-color: #dbeafe;
        border-left: 4px solid #3b82f6;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .warning-box {
        padding: 1rem;
        background-color: #fef3c7;
        border-left: 4px solid #f59e0b;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(to right, #9333ea, #2563eb);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
        font-weight: 600;
        border-radius: 0.5rem;
        cursor: pointer;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(147, 51, 234, 0.3);
    }
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
    .main-header {
        color: #2563eb !important;
        -webkit-text-fill-color: #2563eb !important;
        background: none !important;
    }
</style>
""", unsafe_allow_html=True)


# Initialize API client
api_client = APIClient()

# Initialize session state
if 'extracted_data' not in st.session_state:
    st.session_state.extracted_data = None
if 'email_preview' not in st.session_state:
    st.session_state.email_preview = None
if 'uploaded_image' not in st.session_state:
    st.session_state.uploaded_image = None

# Header
st.markdown('<h1 class="main-header ">AI-Powered Outreach Automation Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Extract event details, scrape emails, and send automated outreach</p>', unsafe_allow_html=True)

# Sidebar
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
                st.error("❌ Backend not running. Start with: python backend/app.py")
    
    st.markdown("---")
    st.caption("Made with ❤️ using Streamlit")

# Main content
# Step 1: Upload Image
st.markdown('<div class="step-header">📤 Step 1: Upload Event Poster</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Choose a poster image",
    type=['jpg', 'jpeg', 'png', 'pdf'],
    help="Upload a clear image of the event poster for best results"
)

if uploaded_file is not None:
    # Store uploaded image
    st.session_state.uploaded_image = uploaded_file
    
    # Display uploaded image
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        image = Image.open(uploaded_file)
        safe_image(image, caption="Uploaded Poster", use_container_width=True)
    
    # Convert image to base64
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    # Extract button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if safe_button("🔍 Extract Details with OCR + GPT", type="primary", use_container_width=True):
            with st.spinner("🔄 Extracting and categorizing data..."):
                result = api_client.extract_data(img_str)

                if result['success']:
                    st.session_state.extracted_data = result['data']
                    st.success("✅ Data extracted and saved to Google Sheets!")
                    st.balloons()
                else:
                    st.error(f"❌ Error: {result.get('error', 'Unknown error')}")

# Step 2: Display Extracted Data
if st.session_state.extracted_data:
    st.markdown('<div class="step-header">📋 Step 2: Extracted Details</div>', unsafe_allow_html=True)
    
    data = st.session_state.extracted_data
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("🎪 Event Name", value=data.get('event_name', ''), disabled=True, key="event_name")
        st.text_input("🏛️ Venue Name", value=data.get('venue_name', ''), disabled=True, key="venue_name")
        st.text_input("📅 Date", value=data.get('date', ''), disabled=True, key="date")
        st.text_input("📧 Artist Email (Scraped)", value=data.get('artist_email', ''), disabled=True, key="artist_email")
    
    with col2:
        st.text_input("🎤 Artist Name", value=data.get('artist_name', ''), disabled=True, key="artist_name")
        st.text_input("👤 Venue Owner", value=data.get('venue_owner', ''), disabled=True, key="venue_owner")
        st.text_input("⏰ Time", value=data.get('time', ''), disabled=True, key="time")
        st.text_input("📧 Venue Email (Scraped)", value=data.get('venue_email', ''), disabled=True, key="venue_email")
    
    st.text_input("📍 Location", value=data.get('location', ''), disabled=True, key="location")
    
    st.markdown('<div class="success-box">✅ Data automatically saved to Google Sheets</div>', unsafe_allow_html=True)
    
    # Step 3: Select Email Template
    st.markdown('<div class="step-header">✉️ Step 3: Select Email Template</div>', unsafe_allow_html=True)
    
    template_options = {
        'good_artist': '🌟 Good Artist Template - Positive Invitation',
        'bad_artist': '❌ Bad Artist Template - Polite Rejection',
        'good_venue': '🏛️ Good Venue Owner Template - Partnership Confirmation',
        'bad_venue': '❌ Bad Venue Owner Template - Polite Decline'
    }
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        selected_template = st.selectbox(
            "Choose email template",
            options=list(template_options.keys()),
            format_func=lambda x: template_options[x],
            key="template_selector"
        )
    
    with col2:
        generate_btn = safe_button("📝 Generate Email", use_container_width=True)
    
    if generate_btn:
        with st.spinner("🔄 Generating email preview..."):
            result = api_client.generate_email(selected_template, data)
            
            if result['success']:
                st.session_state.email_preview = result['email']
                st.success("✅ Email generated successfully!")
            else:
                st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
    
    # Step 4: Email Preview and Send
    if st.session_state.email_preview:
        st.markdown('<div class="step-header">📧 Step 4: Email Preview & Send</div>', unsafe_allow_html=True)
        
        email = st.session_state.email_preview
        
        # Email details
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("📨 To:", value=email['to'], disabled=True, key="email_to")
        with col2:
            st.text_input("📌 Subject:", value=email['subject'], disabled=True, key="email_subject")
        
        # Email body preview
        st.text_area(
            "📄 Email Body:",
            value=email['body'],
            height=300,
            disabled=True,
            key="email_body"
        )
        
        # Send email button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if safe_button("📨 Send Email Now", type="primary", use_container_width=True):
                with st.spinner("📤 Sending email..."):
                    result = api_client.send_email(
                        email['to'],
                        email['subject'],
                        email['body']
                    )
                    
                    if result['success']:
                        st.success("✅ Email sent successfully!")
                        st.balloons()
                        
                        # Show success message
                        st.markdown(f"""
                        <div class="success-box">
                            <strong>✅ Email Sent!</strong><br>
                            Recipient: {email['to']}<br>
                            Template: {template_options[selected_template]}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error(f"❌ Error sending email: {result.get('error', 'Unknown error')}")

# Information Footer
st.markdown("---")
st.markdown('<div class="info-box">', unsafe_allow_html=True)
st.markdown("""
**📌 Complete Workflow:**
1. **Upload** event poster image
2. **OCR** extracts all text from image
3. **GPT-4** intelligently categorizes data
4. **Auto-save** to Google Sheets
5. **Scrape** emails from Instagram/Facebook
6. **Select** appropriate email template
7. **Generate** personalized email
8. **Send** with one click!
""")
st.markdown('</div>', unsafe_allow_html=True)

# Warning if no backend connection
if not api_client.test_connection():
    st.markdown('<div class="warning-box">', unsafe_allow_html=True)
    st.markdown("""
    ⚠️ **Backend Not Connected**
    
    Please start the Flask backend server:
```bash
    cd backend
    python app.py
```
    """)
    st.markdown('</div>', unsafe_allow_html=True)