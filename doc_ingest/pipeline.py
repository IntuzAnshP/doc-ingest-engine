from pathlib import Path
from datetime import datetime, timezone
from typing import List, Optional, Union
import uuid

from doc_ingest.schemas.source_item import SourceItem
from doc_ingest.schemas.extracted_document import ExtractedDocument
from doc_ingest.schemas.normalized_document import NormalizedDocument
from doc_ingest.schemas.chunk import DocumentChunkSchema
from doc_ingest.parsers.router import ParserRouter
from doc_ingest.normalizer.normalizer import NormalizationService
from doc_ingest.chunking.router import ChunkingRouter

class DocumentIngestionPipeline:
    """
    Unified end-to-end ingestion pipeline.
    Connects parsing -> normalization -> structure-aware chunking.
    """
    def __init__(self):
        self.parser_router = ParserRouter()
        self.normalizer = NormalizationService()
        self.chunking_router = ChunkingRouter()

    def process_file(
        self,
        file_path: Union[str, Path],
        source_type: str = "local",
        document_id: Optional[str] = None,
        source_url: Optional[str] = None,
        content_type: Optional[str] = None,
    ) -> List[DocumentChunkSchema]:
        """
        Process a single file directly from disk into structure-aware chunks.
        """
        path = Path(file_path).resolve()
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        # Detect content type if not explicitly provided
        if not content_type:
            content_type = self.parser_router.detect_content_type(str(path))

        source_id = document_id or str(uuid.uuid4())
        source_item = SourceItem(
            source_type=source_type,
            source_id=source_id,
            content_type=content_type,
            raw_path=path,
            source_url=source_url or str(path),
            original_filename=path.name,
            file_size=path.stat().st_size,
            uploaded_at=datetime.now(timezone.utc),
            metadata={}
        )

        return self.process_source_item(source_item)

    def process_source_item(self, source_item: SourceItem) -> List[DocumentChunkSchema]:
        """
        Run a SourceItem through parse -> normalize -> chunk.
        """
        # 1. Parse
        parser = self.parser_router.route(source_item)
        extracted: ExtractedDocument = parser.parse(source_item)

        # 2. Normalize
        normalized: NormalizedDocument = self.normalizer.normalize(extracted)

        # 3. Chunk
        chunker = self.chunking_router.route(normalized)
        chunks: List[DocumentChunkSchema] = chunker.chunk(normalized)

        return chunks

    def extract_and_normalize(self, source_item: SourceItem) -> NormalizedDocument:
        """
        Run parsing and normalization only (without chunking).
        """
        parser = self.parser_router.route(source_item)
        extracted = parser.parse(source_item)
        return self.normalizer.normalize(extracted)
