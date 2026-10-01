import os
from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy import text


from authentification.routes import router as auth_router
from authentification.session import get_current_user
from infra.database import engine
from infra.models.identity import Users


app = FastAPI(openapi_url="/openapi.json" if os.getenv("DEV_DOCS") else None)
app.include_router(auth_router)


@app.get("/api/health")
def health():
    """
    Minimal script to test the app
    """

    with engine.connect() as conn:
        return {"db": conn.execute(text("SELECT 1")).scalar()}

@app.get("/items")
async def read_items(user: Annotated[Users, Depends(get_current_user)]):
    return {"user": user}
