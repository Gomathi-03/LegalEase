import time

from backend.config import Settings


class GeminiDocumentGenerator:
    """Generate structured legal-document drafts with Gemini.

    The model is configurable so the application can track current Gemini model
    availability without changing application code.
    """

    def __init__(self, settings: Settings):
        self.settings = settings
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is not configured. Add it to the .env file.")
        from google import genai
        self.client = genai.Client(api_key=settings.gemini_api_key)

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        dates: str,
        jurisdiction: str = "",
        language: str = "English",
        additional_instructions: str = "",
    ) -> str:
        system_instruction = """
You are LegalEase's legal-document drafting assistant. Create a clear, professional
DRAFT legal document from the user's supplied facts. Do not invent names, dates,
amounts, addresses, obligations, or legal citations. If information is missing,
use a clearly marked placeholder such as [NOT PROVIDED] instead of guessing.

Output only the document draft, with a title and useful section headings.
Use plain text formatting that converts cleanly to DOCX and PDF. Keep clauses
specific to the supplied inputs. Do not claim that the draft is legally valid,
legally sound, attorney-reviewed, or suitable for a particular jurisdiction.
End with a short "Important Notice" section stating that the document is an
AI-generated draft and should be reviewed by a qualified legal professional.
""".strip()

        user_prompt = f"""
Create a {document_type}.

Parties:
{parties}

Terms and conditions (semicolon-separated where applicable):
{terms}

Effective date / dates:
{dates}

Jurisdiction (if provided):
{jurisdiction or '[NOT PROVIDED]'}

Output language:
{language}

Additional instructions:
{additional_instructions or '[NONE]'}

Requirements:
- Use the supplied facts faithfully.
- Include appropriate sections for this document type.
- Include party details, dates, definitions where useful, obligations, payment/termination/confidentiality provisions only when supported by the inputs or clearly necessary as standard placeholders.
- Never fabricate legal authority or citations.
- Return only the draft document.
""".strip()

        from google.genai import types

        import time

        for attempt in range(3):
            try:
                response = self.client.models.generate_content(
                    model=self.settings.gemini_model,
                    contents=user_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.2,
                        max_output_tokens=7000,
                    ),
                )
                break
            except Exception as e:
                if "503" in str(e) and attempt < 2:
                    time.sleep(5 * (attempt + 1))
                else:
                    raise
        text = (response.text or "").strip()
        if not text:
            raise RuntimeError("Gemini returned an empty response.")
        return text
