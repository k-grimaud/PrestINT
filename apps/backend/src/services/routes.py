import os
import uuid
from typing import Annotated

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Cookie,
    Depends,
    HTTPException,
    Request,
    Response,
)
from pydantic import BaseModel, StringConstraints
from sqlalchemy.orm import Session


@router.get("/me")
async def get_similar_vector(body: RequestText, db: AsyncSession = Depends(get_rls_db)):
    embedding = generate_embedding(body.text)

    result = await db.execute(
        select(
            DocumentChunksModel,
            DocumentChunksModel.embedding_vector.op("<=>")(embedding).label("distance"),
        )
        .order_by(DocumentChunksModel.embedding_vector.op("<=>")(embedding)).limit(10)
    )
    chunks = [
        row[0] for row in result.all()
    ]  # ← extrait uniquement le modèle, pas la distance
    return chunks
