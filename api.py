from fastapi import APIRouter, HTTPException
from data_models import AnalyzeRequest, AnalyzeResponse
from llm import call_llm
from keyword_extract import extract_keywords
from fallback_sentiment import fallback_sentiment, fallback_topics, fallback_summary
from persistence import save_analysis, search_by_topic
import uuid

router = APIRouter()

@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_text(req: AnalyzeRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    try:
        llm_output = call_llm(req.text)
        if isinstance(llm_output, dict):
            title = llm_output.get("title")
            summary = llm_output.get("summary")
            topics = llm_output.get("topics", [])
            sentiment = llm_output.get("sentiment", "neutral")
        else:
            # fallback parse
            title = "Untitled"
            summary = fallback_summary(req.text)
            topics = fallback_topics(req.text)
            sentiment = fallback_sentiment(req.text)
    except Exception:
        title = "Untitled"
        summary = fallback_summary(req.text)
        topics = fallback_topics(req.text)
        sentiment = fallback_sentiment(req.text)

    keywords = extract_keywords(req.text)

    record = {
        "id": str(uuid.uuid4()),
        "text": req.text,
        "title": title,
        "summary": summary,
        "topics": topics,
        "sentiment": sentiment,
        "keywords": keywords,
    }
    saved = save_analysis(record)
    return AnalyzeResponse(**saved, provider="llm", fallback_used=False)


@router.get("/search")
def search(topic):
    results = search_by_topic(topic)
    return results
