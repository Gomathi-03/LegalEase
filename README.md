LegalEase — AI-Powered Legal Document Generator

LegalEase is a local AI-powered application that helps users draft, edit, and export legal documents in multiple formats.

✨ Features

- 🤖 AI-assisted drafting using Google Gemini
- 🖥️ Streamlit frontend with editable document preview
- ⚡ FastAPI backend with "/generate" API and health checks
- 📝 DOCX export using "python-docx"
- 📄 PDF export using "FPDF2"
- 📃 TXT export for plain text
- 🖼️ Custom logo support for generated documents
- 🧪 Automated API and document-export tests
- 🐳 Docker support

«Note: The original specification mentioned Gemini 1.5 Pro and the legacy "google-generativeai" package. LegalEase uses Google's current "google-genai" SDK instead. Set "GEMINI_MODEL" to a model available to your API account.»

📁 Project Structure

LegalEase/
├── assets/                 # Project assets and logo
├── backend/                # FastAPI backend
│   ├── ai_core/            # Gemini integration
│   ├── services/           # Document generation
│   ├── config.py
│   ├── main.py
│   ├── routes.py
│   └── schemas.py
├── frontend/
│   └── app.py              # Streamlit application
├── tests/                  # Automated tests
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── Procfile
├── requirements.txt
└── README.md

🚀 Installation

Windows

cd LegalEase
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env

Linux / macOS

cd LegalEase
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env

Open the project in VS Code:

code .

Select the ".venv" interpreter from Python: Select Interpreter.

🔑 Configure Gemini

Add your API key to ".env":

GEMINI_API_KEY=your_real_key
GEMINI_MODEL=gemini-3.8-flash

Create/manage your API key through "Google AI Studio" (https://aistudio.google.com/?utm_source=chatgpt.com).

Never commit ".env" to Git.

If the configured model is unavailable for your account, replace "GEMINI_MODEL" with a currently available Gemini text-generation model.

▶️ Run the Application

Terminal 1 — Backend

source .venv/bin/activate
uvicorn backend.main:app --reload --port 8000

Windows PowerShell uses the same "uvicorn" command after activating the environment.

Backend:

http://127.0.0.1:8000

Swagger API documentation:

http://127.0.0.1:8000/docs

Health check:

http://127.0.0.1:8000/health

Terminal 2 — Frontend

source .venv/bin/activate
streamlit run frontend/app.py

Open:

http://localhost:8501

🔄 How It Works

User Input
    ↓
Streamlit Frontend
    ↓
FastAPI Backend
    ↓
Google Gemini
    ↓
AI-Generated Legal Draft
    ↓
Edit & Review
    ↓
TXT / DOCX / PDF

🧪 Run Tests

pytest -q

Tests cover API health/root endpoints and local TXT, DOCX, and PDF generation without making an AI request.

🐳 Docker

Create ".env" first, then run:

docker compose up --build

- Frontend: "http://localhost:8501"
- Backend: "http://localhost:8000/docs"

🔐 Important Notes

- The Gemini API key remains on the backend and is never exposed to the browser.
- User-provided legal information is sent to Gemini only during the document-generation request.
- The AI prompt instructs Gemini not to invent missing facts or legal citations.
- Document exports use deterministic formatting and do not require additional AI calls.
- LegalEase is a drafting and information tool, not a substitute for professional legal advice or attorney review.

📌 Disclaimer

LegalEase helps users create and understand draft legal documents. Users should have important documents reviewed by a qualified legal professional before relying on them.

---

Built with

Python • Streamlit • FastAPI • Google Gemini • python-docx • FPDF2