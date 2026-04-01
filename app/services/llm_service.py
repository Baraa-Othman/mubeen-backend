import json
import logging
import re

import google.generativeai as genai
from fastapi import HTTPException

from app.core.config import settings
from app.services.prompts import ESSAY_PROMPT, TRANSLATION_PROMPT, DOCUMENT_PROMPT

logger = logging.getLogger(__name__)

# Configure Gemini once at module load
genai.configure(api_key=settings.GEMINI_API_KEY)


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _build_model(temperature: float) -> genai.GenerativeModel:
    return genai.GenerativeModel(
        model_name=settings.GEMINI_MODEL,
        generation_config=genai.GenerationConfig(temperature=temperature),
    )


def _clean_and_parse_json(raw: str) -> dict:
    """Strip markdown fences and parse JSON safely."""
    # Remove ```json ... ``` or ``` ... ``` wrappers
    cleaned = re.sub(r"```(?:json)?\s*", "", raw).replace("```", "").strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as exc:
        logger.error("JSON parse error: %s | raw (first 500 chars): %s", exc, cleaned[:500])
        raise HTTPException(status_code=502, detail="فشل تحليل استجابة الذكاء الاصطناعي")


async def _call_gemini(prompt: str, temperature: float) -> str:
    """Send prompt to Gemini and return raw text, with error handling."""
    model = _build_model(temperature)
    try:
        response = await model.generate_content_async(prompt)
        # Check if the response was blocked by safety filters
        if not response.candidates:
            logger.warning("Gemini response blocked or empty. Candidates: %s", response.candidates)
            raise HTTPException(status_code=502, detail="تم حظر الاستجابة بواسطة فلاتر الأمان")
            
        return response.text.strip()
    except Exception as exc:
        logger.error("Gemini API error (Type: %s): %s", type(exc).__name__, exc)
        if "rate limit" in str(exc).lower():
            raise HTTPException(status_code=429, detail="لقد تجاوزت حد الطلبات، حاول لاحقاً")
        raise HTTPException(status_code=502, detail="حدث خطأ أثناء الاتصال بالذكاء الاصطناعي")


# ─── Essay Evaluation ─────────────────────────────────────────────────────────

async def evaluate_essay(text: str, perfect_answer: str, max_points: int) -> dict:
    prompt = ESSAY_PROMPT.format(
        text=text,
        perfect_answer=perfect_answer,
        max_points=max_points,
    )
    logger.info("Calling Gemini for essay evaluation")
    raw = await _call_gemini(prompt, settings.ESSAY_TEMPERATURE)
    data = _clean_and_parse_json(raw)

    # Validate required keys
    required = {"score", "feedback_ar", "weak_sentences", "suggestions"}
    if not required.issubset(data.keys()):
        logger.error("Unexpected essay response keys: %s", data.keys())
        raise HTTPException(status_code=502, detail="استجابة غير مكتملة من الذكاء الاصطناعي")

    return data


# ─── Translation ──────────────────────────────────────────────────────────────

async def translate_text(english_text: str) -> str:
    prompt = TRANSLATION_PROMPT.format(text=english_text)
    logger.info("Calling Gemini for translation")
    return await _call_gemini(prompt, settings.TRANSLATION_TEMPERATURE)


# ─── Document Generation ──────────────────────────────────────────────────────

async def generate_document(document_type: str, tone: str, recipient: str, main_points: str) -> str:
    prompt = DOCUMENT_PROMPT.format(
        document_type=document_type,
        tone=tone,
        recipient=recipient,
        main_points=main_points,
    )
    logger.info("Calling Gemini for document generation")
    return await _call_gemini(prompt, settings.DOCUMENT_TEMPERATURE)
