from pydantic import BaseModel, Field


# ─── Essay ────────────────────────────────────────────────────────────────────

class EssayRequest(BaseModel):
    text: str = Field(..., max_length=2000, description="Student essay text")
    perfect_answer: str = Field(..., max_length=2000, description="Model answer")
    max_points: int = Field(..., ge=1, le=100, description="Maximum score")


class EssayResponse(BaseModel):
    score: float
    accuracy_percentage: str = ""
    feedback_ar: str
    strengths: list[str] = []
    weak_sentences: list[str]
    suggestions: list[str]


# ─── Translation ──────────────────────────────────────────────────────────────

class TranslationRequest(BaseModel):
    english_text: str = Field(..., max_length=4000, description="text to translate")


class TranslationResponse(BaseModel):
    translated_text: str


# ─── Document Generation ──────────────────────────────────────────────────────

class DocumentRequest(BaseModel):
    document_type: str = Field(..., max_length=200)
    tone: str = Field(..., max_length=200)
    recipient: str = Field(..., max_length=200)
    main_points: str = Field(..., max_length=2000)


class DocumentResponse(BaseModel):
    generated_text: str
