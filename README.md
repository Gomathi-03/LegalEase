
## 🚀 Live Demo

[**Open LegalEase**](https://legalease-frontend-l6a6.onrender.com)

# LegalEase — AI-Powered Legal Document Generator

LegalEase is a complete local application based on the supplied project specification. It uses:

- **Streamlit** for the frontend, editable preview, branding, and downloads.

- **FastAPI** for the backend `/generate` API and health checks.

- **Gemini** for AI-assisted legal-document drafting.

- **python-docx** for editable Word documents.

- **FPDF2** for branded PDF output.

- **TXT** export for plain text.

The supplied specification explicitly names Gemini 1.5 Pro and the legacy `google-generativeai` package. The implementation uses Google's current `google-genai` SDK instead, because Google currently recommends that SDK and lists the older Python package as a legacy/deprecated library. Set `GEMINI_MODEL` to a model available to your API account. See Google's official SDK guidance: https://ai.google.dev/gemini-api/docs/libraries

## 📄 Project Documentation

https://drive.google.com/file/d/1k4gbSH0Xc3bqtmkkGyCoEzDohpOYy96C/view?usp=drivesdk

## 1. Project structure


```text

LegalEase/

├── assets/

│   └── logo.png

├── backend/

│   ├── __init__.py

│   ├── ai_core/

│   │   ├── __init__.py

│   │   └── gemini_generator.py

│   ├── config.py

│   ├── main.py

│   ├── routes.py

│   ├── schemas.py

│   ├── services/

│   │   ├── __init__.py

│   │   └── document_service.py

│   └── utils/

│       ├── __init__.py

│       └── sanitize.py

├── frontend/

│   └── app.py

├── tests/

│   ├── test_api.py

│   └── test_documents.py

├── .env.example

├── .gitignore

├── Dockerfile

├── Procfile

├── docker-compose.yml

├── README.md

└── requirements.txt

```

## 2. VS Code setup

### Windows PowerShell

```powershell

cd LegalEase

py -3.12 -m venv .venv

.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip

pip install -r requirements.txt

copy .env.example .env

```

### Linux / macOS

```bash

cd LegalEase

python3 -m venv .venv

source .venv/bin/activate

python -m pip install --upgrade pip

pip install -r requirements.txt

cp .env.example .env

```

Open the folder in VS Code:

```bash

code .

```

Choose the `.venv` Python interpreter from **Ctrl+Shift+P → Python: Select Interpreter**.

## 3. Configure Gemini

Open `.env` and set:

```env

GEMINI_API_KEY=your_real_key

GEMINI_MODEL=gemini-3.8-flash

```

Create/manage the API key in Google AI Studio. Never commit `.env` to Git.

If the model name above is unavailable to your account, change `GEMINI_MODEL` to a currently available text-generation model in your Gemini API account.

## 4. Run the backend

Open VS Code terminal 1:

```bash

source .venv/bin/activate

uvicorn backend.main:app --reload --port 8000

```

Windows PowerShell after activation uses the same command:

```powershell

uvicorn backend.main:app --reload --port 8000

```

Check:

- API: http://127.0.0.1:8000

- Swagger: http://127.0.0.1:8000/docs

- Health: http://127.0.0.1:8000/health

## 5. Run Streamlit

Open VS Code terminal 2:

```bash

source .venv/bin/activate

streamlit run frontend/app.py

```

Open the URL Streamlit prints, normally http://localhost:8501.

## 6. Test the complete flow

Use these sample inputs:

**Document Type**

```text

Freelance Work Contract

```

**Parties**

```text

Jane Doe (Service Provider), TechNova Inc. (Client)

```

**Terms**

```text

Payment to be made within 30 days of invoice; The provider agrees to deliver work by the agreed deadline; Confidentiality must be maintained; Either party may terminate with 15 days notice

```

**Effective Date**

```text

April 15, 2026

```

Then:

1. Click **Generate Document**.

2. Review the AI draft.

3. Edit it in the editable text area.

4. Optionally upload a PNG/JPG logo.

5. Download TXT, DOCX, and PDF.

6. Open the DOCX and PDF to verify headings, terms table, logo, and footer.

## 7. Run automated tests

```bash

pytest -q

```

These tests verify the API health/root endpoints and the local TXT/DOCX/PDF exporters without making an AI request.

## 8. API example

```bash

curl -X POST "http://127.0.0.1:8000/generate" \

-H "Content-Type: application/json" \

-d '{

"document_type": "Non-Disclosure Agreement",  

"parties": "Jane Doe (Disclosing Party), TechNova Inc. (Receiving Party)",  

"terms": "Confidential information must not be disclosed; Confidentiality lasts 2 years; Either party may terminate with 15 days notice",  

"dates": "April 15, 2026",  

"jurisdiction": "Tamil Nadu, India",  

"language": "English",  

"additional_instructions": "Use clear section headings."

}'

```

## 9. Docker

Create `.env` first, then:

```bash

docker compose up --build

```

Frontend: http://localhost:8501

Backend: http://localhost:8000/docs

## 10. Important implementation notes

- The Gemini API key stays on the backend; Streamlit does not send the key to the browser.

- User-entered legal facts are passed to Gemini only for the generation request.

- The AI prompt explicitly instructs the model not to fabricate missing facts or legal citations.

- Export formatting is deterministic and does not require another AI call.

- The application is a drafting aid, not a substitute for legal advice or attorney review.




