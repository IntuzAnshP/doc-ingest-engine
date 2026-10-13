from typing import List, Optional
from doc_ingest.chunking.base import AbstractChunker
from doc_ingest.schemas.normalized_document import NormalizedDocument, TextSection
from doc_ingest.schemas.chunk import DocumentChunkSchema, ChunkMetadata

class NotionChunker(AbstractChunker):
    def chunk(self, doc: NormalizedDocument) -> List[DocumentChunkSchema]:
        chunks: List[DocumentChunkSchema] = []
        chunk_index = 0

        current_h1: Optional[str] = None
        current_h2: Optional[str] = None
        body_lines: List[str] = []

        def _breadcrumb() -> str:
            parts = [p for p in [current_h1, current_h2] if p]
            return " > ".join(parts)

        def _emit_chunks(body: str, h1: Optional[str], h2: Optional[str]) -> None:
            nonlocal chunk_index

            if not body.strip():
                return

            parts = [p for p in [h1, h2] if p]
            section_ctx = " > ".join(parts) if parts else None
            preamble = f"[Context: {section_ctx}]\n\n" if section_ctx else ""

            full_content = preamble + body

            max_chars = self.chunk_size * 4
            if len(full_content) <= max_chars:
                chunks.append(_make_chunk(full_content, chunk_index, section_ctx))
                chunk_index += 1
            else:
                overlap_chars = self.chunk_overlap * 4
                start = 0
                while start < len(full_content):
                    end = start + max_chars
                    piece = full_content[start:end].strip()
                    if piece:
                        if preamble and not piece.startswith("[Context:"):
                            piece = preamble + piece
                        chunks.append(_make_chunk(piece, chunk_index, section_ctx))
                        chunk_index += 1
                    start += max_chars - overlap_chars

        def _flush(h1: Optional[str], h2: Optional[str]) -> None:
            nonlocal body_lines
            if not body_lines:
                return
            body = "\n\n".join(body_lines).strip()
            body_lines = []
            _emit_chunks(body, h1, h2)

        def _make_chunk(content: str, idx: int, section: Optional[str]) -> DocumentChunkSchema:
            return DocumentChunkSchema(
                content=content,
                metadata=ChunkMetadata(
                    document_id=doc.source_id,
                    chunk_index=idx,
                    chunk_type="section",
                    source_type=doc.source_type,
                    source_url=doc.source_url,
                    title=doc.title,
                    section_context=section,
                ),
            )

        for section in doc.structured_sections:
            text = section.content.strip()
            if not text:
                continue

            stype = section.section_type
            level = section.metadata.get("level") if stype == "heading" else None

            if stype == "heading" and level == 1:
                _flush(current_h1, current_h2)
                current_h1 = text
                current_h2 = None

            elif stype == "heading" and level == 2:
                if current_h2 is not None:
                    _flush(current_h1, current_h2)
                current_h2 = text

            else:
                body_lines.append(text)

        _flush(current_h1, current_h2)
        return chunks
