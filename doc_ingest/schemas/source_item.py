from pydantic import BaseModel
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

class SourceItem(BaseModel):
    source_type: str                  # e.g., 'local', 'google_drive', 'notion'
    source_id: str                    # file path or generated UUID
    content_type: str                 # 'pdf', 'docx', 'xlsx', 'notion'
    raw_path: Path                    # absolute path to stored file
    source_url: Optional[str] = None  # original URL if from a cloud source
    original_filename: str
    file_size: int
    uploaded_at: datetime
    metadata: Dict[str, Any] = {}
