from datetime import datetime, timezone
from doc_ingest.schemas.normalized_document import NormalizedDocument, TextSection
from doc_ingest.chunking.docx_chunker import DOCXChunker
from doc_ingest.chunking.pdf_chunker import PDFChunker
from doc_ingest.chunking.notion_chunker import NotionChunker

def test_docx_chunker():
    chunker = DOCXChunker()
    doc = NormalizedDocument(
        source_type="local",
        source_id="doc-test",
        title="Test Doc",
        content_type="docx",
        raw_text="Heading\n\nBody content.",
        full_text="Heading\n\nBody content.",
        content_hash="abc123hash",
        source_url="/path/to/test.docx",
        source_updated_at=datetime.now(timezone.utc),
        metadata={},
        structured_sections=[
            TextSection(section_type="heading", content="Section 1", metadata={"section_path": ["Section 1"]}),
            TextSection(section_type="paragraph", content="This is content inside section 1.", metadata={})
        ]
    )

    chunks = chunker.chunk(doc)
    assert len(chunks) == 1
    assert "Section 1" in chunks[0].content
    assert "This is content inside section 1." in chunks[0].content
    assert chunks[0].metadata.section_context == "Section 1"

def test_notion_chunker_breadcrumb():
    chunker = NotionChunker()
    doc = NormalizedDocument(
        source_type="notion",
        source_id="notion-123",
        title="Notion Page",
        content_type="notion",
        raw_text="",
        full_text="",
        content_hash="hash",
        source_url="https://notion.so/test",
        source_updated_at=datetime.now(timezone.utc),
        metadata={},
        structured_sections=[
            TextSection(section_type="heading", content="Phase 1", metadata={"level": 1}),
            TextSection(section_type="heading", content="Setup", metadata={"level": 2}),
            TextSection(section_type="paragraph", content="Follow these setup steps.", metadata={})
        ]
    )

    chunks = chunker.chunk(doc)
    assert len(chunks) == 1
    assert "[Context: Phase 1 > Setup]" in chunks[0].content
    assert "Follow these setup steps." in chunks[0].content
