from typing import List
from doc_ingest.chunking.base import AbstractChunker
from doc_ingest.schemas.normalized_document import NormalizedDocument
from doc_ingest.schemas.chunk import DocumentChunkSchema, ChunkMetadata

class XLSXChunker(AbstractChunker):
    def chunk(self, doc: NormalizedDocument) -> List[DocumentChunkSchema]:
        chunks = []
        text = doc.full_text
        
        char_size = self.chunk_size * 4
        char_overlap = self.chunk_overlap * 4
        
        start = 0
        chunk_index = 0
        
        while start < len(text):
            end = start + char_size
            chunk_content = text[start:end]
            
            metadata = ChunkMetadata(
                document_id=doc.source_id,
                chunk_index=chunk_index,
                chunk_type="text",
                source_type=doc.source_type,
                source_url=doc.source_url,
                title=doc.title
            )
            
            chunks.append(DocumentChunkSchema(
                content=chunk_content.strip(),
                metadata=metadata
            ))
            
            start += (char_size - char_overlap)
            chunk_index += 1
            
        return chunks
