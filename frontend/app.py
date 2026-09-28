import html
import os
from pathlib import Path

import requests
import streamlit as st

from backend.services.document_service import export_document

BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_LOGO = BASE_DIR / "assets" / "logo.png"
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")

st.set_page_config(page_title="LegalEase", page_icon="⚖️", layout="wide")

st.markdown("""
<style>
.block-container {max-width: 1200px; padding-top: 2rem;}
.legal-card {background:#111827; color:#f9fafb; padding:24px; border-radius:16px; max-height:600px; overflow:auto; white-space:pre-wrap; line-height:1.65;}
.notice {background:#fff7ed; border-left:5px solid #f97316; padding:12px 16px; border-radius:8px;}
.small-muted {color:#6b7280; font-size:0.9rem;}
</style>
""", unsafe_allow_html=True)

if "document" not in st.session_state:
    st.session_state.document = ""
if "document_type" not in st.session_state:
    st.session_state.document_type = ""
if "terms" not in st.session_state:
    st.session_state.terms = ""

left, center, right = st.columns([1, 2, 1])
with center:
    if DEFAULT_LOGO.exists():
        st.image(str(DEFAULT_LOGO), width=90)
    st.title("LegalEase")
    st.caption("AI-Powered Legal Document Generator")

st.markdown("### Create your document")
col1, col2 = st.columns(2)
with col1:
    document_type = st.text_input("Document Type", placeholder="e.g., Freelance Work Contract", value=st.session_state.document_type)
    parties = st.text_area("Parties Involved", placeholder="Jane Doe (Service Provider), TechNova Inc. (Client)", height=120)
    dates = st.text_input("Effective Date / Dates", placeholder="April 15, 2026")
with col2:
    terms = st.text_area("Terms & Conditions", placeholder="Use semicolons for separate terms; Payment within 30 days; Confidentiality must be maintained", height=170, value=st.session_state.terms)
    jurisdiction = st.text_input("Jurisdiction (optional)", placeholder="e.g., Tamil Nadu, India")
    language = st.selectbox("Output Language", ["English", "Tamil", "Hindi", "Malayalam", "Telugu", "Kannada"])

additional = st.text_area("Additional Instructions (optional)", placeholder="Any specific clauses, tone, placeholders, or formatting requirements.", height=90)

if st.button("Generate Document", type="primary", use_container_width=True):
    if not all([document_type.strip(), parties.strip(), terms.strip(), dates.strip()]):
        st.error("Please fill Document Type, Parties, Terms & Conditions, and Effective Date / Dates.")
    else:
        payload = {
            "document_type": document_type,
            "parties": parties,
            "terms": terms,
            "dates": dates,
            "jurisdiction": jurisdiction,
            "language": language,
            "additional_instructions": additional,
        }
        try:
            with st.spinner("Generating your legal draft..."):
                response = requests.post(f"{BACKEND_URL}/generate", json=payload, timeout=120)
            if response.ok:
                data = response.json()
                st.session_state.document = data["content"]
                st.session_state.document_type = document_type
                st.session_state.terms = terms
                st.success(f"Document generated using {data.get('model', 'Gemini')}.")
            else:
                try:
                    detail = response.json().get("detail", response.text)
                except Exception:
                    detail = response.text
                st.error(f"Backend error: {detail}")
        except requests.RequestException as exc:
            st.error(f"Could not reach FastAPI at {BACKEND_URL}. Start the backend first. Details: {exc}")

if st.session_state.document:
    st.divider()
    st.markdown("### Document Preview")
    st.markdown(f'<div class="legal-card">{html.escape(st.session_state.document)}</div>', unsafe_allow_html=True)

    st.markdown("### Edit Document")
    edited = st.text_area("Click here to edit the generated document", value=st.session_state.document, height=500, label_visibility="collapsed")
    st.session_state.document = edited

    st.markdown("### Branding")
    b1, b2 = st.columns(2)
    with b1:
        company_name = st.text_input("Company / Brand Name", value="LegalEase")
    with b2:
        footer_text = st.text_input("Footer Text", value="Generated with LegalEase")
    uploaded_logo = st.file_uploader("Optional custom logo (PNG/JPG)", type=["png", "jpg", "jpeg"])

    logo_path = DEFAULT_LOGO
    temp_logo = None
    if uploaded_logo:
        import tempfile
        suffix = Path(uploaded_logo.name).suffix.lower() or ".png"
        temp_logo = Path(tempfile.gettempdir()) / f"legalease_logo{suffix}"
        temp_logo.write_bytes(uploaded_logo.getvalue())
        logo_path = temp_logo

    st.markdown("### Download")
    d1, d2, d3 = st.columns(3)
    txt_bytes, _, txt_name = export_document("txt", st.session_state.document, document_type, terms, company_name, footer_text, logo_path)
    docx_bytes, _, docx_name = export_document("docx", st.session_state.document, document_type, terms, company_name, footer_text, logo_path)
    pdf_bytes, _, pdf_name = export_document("pdf", st.session_state.document, document_type, terms, company_name, footer_text, logo_path)
    with d1:
        st.download_button("Download TXT", txt_bytes, file_name=txt_name, mime="text/plain", use_container_width=True)
    with d2:
        st.download_button("Download DOCX", docx_bytes, file_name=docx_name, mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)
    with d3:
        st.download_button("Download PDF", pdf_bytes, file_name=pdf_name, mime="application/pdf", use_container_width=True)

    st.markdown('<div class="notice"><strong>Important:</strong> LegalEase creates AI-generated drafts for informational and drafting assistance. Review the document with a qualified legal professional before relying on it.</div>', unsafe_allow_html=True)

st.divider()
st.markdown('<div class="small-muted">LegalEase • FastAPI + Streamlit + Gemini • Keep your API key private and never commit .env to source control.</div>', unsafe_allow_html=True)
