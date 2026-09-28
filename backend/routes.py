from fastapi import APIRouter, HTTPException

from backend.ai_core.gemini_generator import GeminiDocumentGenerator
from backend.config import get_settings
from backend.schemas import DocumentRequest, DocumentResponse
from backend.utils.sanitize import sanitize_text

router = APIRouter()

DISCLAIMER = "LegalEase produces AI-generated drafts for informational and drafting assistance. It is not legal advice and should be reviewed by a qualified legal professional before use."


@router.post("/generate", response_model=DocumentResponse)
def generate_document(request: DocumentRequest):
    settings = get_settings()
    if len(request.parties) + len(request.terms) + len(request.additional_instructions) > settings.max_input_chars:
        raise HTTPException(status_code=413, detail="Input is too large. Please shorten the parties, terms, or instructions.")
    try:
        generator = GeminiDocumentGenerator(settings)
        content = generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            dates=request.dates,
            jurisdiction=request.jurisdiction,
            language=request.language,
            additional_instructions=request.additional_instructions,
        )
        return DocumentResponse(
            document_type=request.document_type,
            content=sanitize_text(content),
            model=settings.gemini_model,
            disclaimer=DISCLAIMER,
        )
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"AI generation failed: {exc}") from exc
