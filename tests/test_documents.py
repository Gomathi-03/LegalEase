from backend.services.document_service import format_docx, format_pdf, format_txt


def test_txt_export():
    result = format_txt("Hello — world")
    assert result == b"Hello - world"


def test_docx_export():
    result = format_docx("1. Parties\nJane Doe and ABC Corp", "NDA", "Confidentiality;Payment")
    assert result[:2] == b"PK"


def test_pdf_export():
    result = format_pdf("1. Parties\nJane Doe and ABC Corp", "NDA")
    assert result.startswith(b"%PDF")
