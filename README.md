# Spectrum

A sophisticated phone call analysis tool that leverages AI for transcription, speaker recognition, content analysis, and relationship visualization.

## Features

- 🎙️ Automatic audio transcription with multi-accent support
- 👥 Speaker recognition and voice identification
- 🔍 Content analysis with keyword and pattern extraction
- 📊 Interactive relationship network visualization
- 🔔 Real-time suspicious activity alerts
- 💾 Secure and scalable data management

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Unix/macOS
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Project Structure

```
spectrum/
├── api/            # FastAPI routes and endpoints
├── core/           # Core business logic
│   ├── audio/      # Audio processing and transcription
│   ├── speakers/   # Speaker recognition
│   ├── analysis/   # Content analysis
│   └── alerts/     # Real-time alert system
├── models/         # Database models and schemas
├── services/       # External service integrations
├── utils/          # Utility functions
└── web/           # Web interface
```

## Security Note

This tool handles sensitive audio data. Ensure proper security measures are in place and comply with relevant privacy regulations.
