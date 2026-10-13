from pathlib import Path
from doc_ingest.pipeline import DocumentIngestionPipeline

def test_pipeline_on_real_docx():
    docx_path = Path(__file__).resolve().parent.parent.parent.parent / "FTX Scandal.docx"
    if not docx_path.exists():
        return

    pipeline = DocumentIngestionPipeline()
    chunks = pipeline.process_file(docx_path)
    
    assert len(chunks) > 0
    assert chunks[0].metadata.title == "FTX Scandal.docx"
    assert chunks[0].content is not None
