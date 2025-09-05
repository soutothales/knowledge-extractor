from pydantic import BaseModel
from typing import List, Optional

class AnalyzeRequest(BaseModel):
    text: str

class AnalyzeResponse(BaseModel):
    id: str
    title: str
    summary: str
    topics: List[str]
    sentiment: str
    keywords: List[str]
    provider: Optional[str] = None
    fallback_used: Optional[bool] = False
