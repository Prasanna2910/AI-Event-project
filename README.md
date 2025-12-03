# 🎭 Event Poster Data Extractor

Automatically extract event details from posters, categorize data with AI, and send personalized emails.

## ✨ Features

- 📸 OCR text extraction from poster images
- 🤖 GPT-4 powered intelligent categorization
- 📊 Automatic Google Sheets integration
- 📧 Email scraping from Instagram/Facebook
- ✉️ Customizable email templates
- 🚀 One-click automated email sending

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Tesseract OCR installed
- OpenAI API key
- Google Cloud credentials
- Gmail account with App Password

### Installation

1. Clone the repository
```bash
git clone <your-repo-url>
cd event-poster-extractor
```

2. Set up backend
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
```

3. Set up Streamlit frontend
```bash
cd frontend-streamlit
pip install -r requirements.txt
```

4. Run the application
```bash
# Terminal 1: Backend
cd backend
python app.py

# Terminal 2: Frontend
cd frontend-streamlit
streamlit run streamlit_app.py
```

5. Open browser
- Backend: http://localhost:5000
- Frontend: http://localhost:8501

## 📖 Documentation

See `/docs` folder for detailed documentation:
- Setup Guide
- API Documentation
- User Manual

## 📝 License

MIT License - see LICENSE file for details