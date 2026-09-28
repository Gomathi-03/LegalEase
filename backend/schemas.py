from pydantic import BaseModel, Field, field_validator


class DocumentRequest(BaseModel):
    document_type: str = Field(..., min_length=2, max_length=120)
    parties: str = Field(..., min_length=2, max_length=4000)
    terms: str = Field(..., min_length=2, max_length=8000)
    dates: str = Field(..., min_length=2, max_length=200)
    jurisdiction: str = Field(default="", max_length=200)
    language: str = Field(default="English", max_length=80)
    additional_instructions: str = Field(default="", max_length=4000)

    @field_validator("document_type", "parties", "terms", "dates", "jurisdiction", "language", "additional_instructions", mode="before")
    @classmethod
    def strip_strings(cls, value):
        return value.strip() if isinstance(value, str) else value


class DocumentResponse(BaseModel):
    document_type: str
    content: str
    model: str
    disclaimer: str


class ExportRequest(BaseModel):
    document_type: str = Field(..., min_length=2, max_length=120)
    content: str = Field(..., min_length=1, max_length=50000)
    terms: str = Field(default="", max_length=8000)
    company_name: str = Field(default="LegalEase", max_length=120)
    footer_text: str = Field(default="Generated with LegalEase", max_length=300)
