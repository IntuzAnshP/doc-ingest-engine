from doc_ingest.schemas.normalized_document import NormalizedDocument
from doc_ingest.chunking.base import AbstractChunker
from doc_ingest.chunking.docx_chunker import DOCXChunker
from doc_ingest.chunking.pdf_chunker import PDFChunker
from doc_ingest.chunking.xlsx_chunker import XLSXChunker
from doc_ingest.chunking.notion_chunker import NotionChunker

class UnsupportedContentTypeError(Exception):
    pass

class ChunkingRouter:
    def __init__(self):
        self.chunkers = {
            "docx": DOCXChunker(),
            "pdf": PDFChunker(),
            "xlsx": XLSXChunker(),
            "notion": NotionChunker()
        }

    def route(self, doc: NormalizedDocument) -> AbstractChunker:
        chunker = self.chunkers.get(doc.content_type)
        if not chunker:
            raise UnsupportedContentTypeError(f"No chunker found for content type: {doc.content_type}")
        return chunker
