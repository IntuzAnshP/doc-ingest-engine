"""
doc-ingest-engine
-----------------
Enterprise document parsing, normalization, and structure-aware chunking engine for RAG systems.
"""

__version__ = "0.1.0"

from doc_ingest.pipeline import DocumentIngestionPipeline
from doc_ingest.parsers.router import ParserRouter
from doc_ingest.normalizer.normalizer import NormalizationService
from doc_ingest.chunking.router import ChunkingRouter
from doc_ingest.schemas.source_item import SourceItem
from doc_ingest.schemas.extracted_document import ExtractedDocument
from doc_ingest.schemas.normalized_document import NormalizedDocument, TextSection
from doc_ingest.schemas.chunk import DocumentChunkSchema, ChunkMetadata

__all__ = [
    "DocumentIngestionPipeline",
    "ParserRouter",
    "NormalizationService",
    "ChunkingRouter",
    "SourceItem",
    "ExtractedDocument",
    "NormalizedDocument",
    "TextSection",
    "DocumentChunkSchema",
    "ChunkMetadata",
]
