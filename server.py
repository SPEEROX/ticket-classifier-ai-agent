"""
FastAPI REST server wrapping the support ticket classifier.
Run with: uvicorn server:app --reload
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from classifier import classify_messages
import openai

app = FastAPI(
    title="Support Ticket Classifier API",
    description="AI-powered classification and prioritization of customer support messages.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ClassifyRequest(BaseModel):
    messages: list[str]

    model_config = {
        "json_schema_extra": {
            "example": {
                "messages": [
                    "My payment got deducted but service is not activated",
                    "App crashes every time I login",
                    "How to change my email address?",
                ]
            }
        }
    }


class ClassifiedMessage(BaseModel):
    message: str
    category: str
    priority: str
    error: str | None = None


@app.post("/classify", response_model=list[ClassifiedMessage])
async def classify(request: ClassifyRequest):
    """Classify a list of support messages."""
    if not request.messages:
        raise HTTPException(status_code=400, detail="messages list cannot be empty.")
    if len(request.messages) > 50:
        raise HTTPException(status_code=400, detail="Maximum 50 messages per request.")

    try:
        results = classify_messages(request.messages)
        return results
    except openai.AuthenticationError:
        raise HTTPException(status_code=401, detail="Invalid OpenAI API key.")
    except openai.RateLimitError:
        raise HTTPException(status_code=429, detail="OpenAI rate limit exceeded.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    return {"status": "ok"}
