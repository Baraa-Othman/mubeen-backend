import logging

from fastapi import APIRouter, Depends, Request

from app.models.schemas import (
    EssayRequest, EssayResponse,
    TranslationRequest, TranslationResponse,
    DocumentRequest, DocumentResponse,
)
from app.services.auth_service import verify_firebase_token
from app.services import llm_service

logger = logging.getLogger(__name__)
router = APIRouter()


# ─── Essay ────────────────────────────────────────────────────────────────────

@router.post("/essay/evaluate", response_model=EssayResponse)
async def evaluate_essay(
    body: EssayRequest,
    request: Request,
    uid: str = Depends(verify_firebase_token),
):
    logger.info("[essay/evaluate] uid=%s", uid)
    result = await llm_service.evaluate_essay(
        text=body.text,
        perfect_answer=body.perfect_answer,
        max_points=body.max_points,
    )
    return EssayResponse(**result)


# ─── Translation ──────────────────────────────────────────────────────────────

@router.post("/translation/translate", response_model=TranslationResponse)
async def translate(
    body: TranslationRequest,
    request: Request,
    uid: str = Depends(verify_firebase_token),
):
    logger.info("[translation/translate] uid=%s", uid)
    translated = await llm_service.translate_text(body.english_text)
    return TranslationResponse(translated_text=translated)


# ─── Document Generation ──────────────────────────────────────────────────────

@router.post("/document/generate", response_model=DocumentResponse)
async def generate_document(
    body: DocumentRequest,
    request: Request,
    uid: str = Depends(verify_firebase_token),
):
    logger.info("[document/generate] uid=%s", uid)
    text = await llm_service.generate_document(
        document_type=body.document_type,
        tone=body.tone,
        recipient=body.recipient,
        main_points=body.main_points,
    )
    return DocumentResponse(generated_text=text)
