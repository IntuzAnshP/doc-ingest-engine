from pathlib import Path
from datetime import datetime, timezone
from doc_ingest.schemas.source_item import SourceItem
from doc_ingest.schemas.extracted_document import ExtractedDocument, DocumentMetadata
from doc_ingest.schemas.document_elements import HeadingElement, ParagraphElement
from doc_ingest.normalizer.normalizer import NormalizationService

def test_normalization_service():
    normalizer = NormalizationService()
    source_item = SourceItem(
        source_type="local",
        source_id="doc-123",
        content_type="docx",
        raw_path=Path("/fake/path.docx"),
        original_filename="Important Document.docx",
        file_size=1024,
        uploaded_at=datetime.now(timezone.utc)
    )

    metadata = DocumentMetadata(
        title="Important Document",
        author="Test Author",
        modified_at="2026-01-01T10:00:00Z"
    )

    elements = [
        HeadingElement(index=0, text="Introduction", level=1, section_path=["Introduction"]),
        ParagraphElement(index=1, text="This is the first paragraph.", style="Normal", section_path=["Introduction"])
    ]

    extracted = ExtractedDocument(
        source_item=source_item,
        raw_text="Introduction\n\nThis is the first paragraph.",
        metadata=metadata,
        elements=elements
    )

    normalized = normalizer.normalize(extracted)
    assert normalized.title == "Important Document.docx"
    assert len(normalized.structured_sections) == 2
    assert normalized.structured_sections[0].section_type == "heading"
    assert normalized.content_hash is not None
