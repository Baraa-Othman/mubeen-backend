import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.routes import router

# ─── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

# ─── App ──────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Mubeen AI Proxy",
    description="Secure AI backend for the Mubeen Flutter app – auth verification + Gemini proxy.",
    version="1.0.0",
)

# ─── CORS ─────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Routes ───────────────────────────────────────────────────────────────────
app.include_router(router, prefix="/api/v1")


@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to Mubeen Backend. The API is running."}


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok"}
