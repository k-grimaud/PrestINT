import os
from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy import text

from authentification.routes import router as auth_router
from authentification.session import get_current_user
from infra.database import engine
from infra.models.audit import AuditEvent, OtpCode, RateLimit, UserSession
from infra.models.identity import (
    List_Service,
    Ongoing_Service,
    Permission,
    Picture,
    Users,
)

app = FastAPI(openapi_url="/openapi.json" if os.getenv("DEV_DOCS") else None)
app.include_router(auth_router)

# If DEV_DOCS is set to 1 then a PSQL admin panel is built
if os.getenv("DEV_DOCS"):
    # sqladmin is only in dev dependancies
    # Thus if DEV_DOCS is set by error a ModuleNotFoundError is raised
    from sqladmin import Admin, ModelView

    admin = Admin(app, engine, base_url="/admin", title="PSQL Admin Panel")

    class ReadOnlyView(ModelView):
        can_create = False
        can_edit = False
        can_delete = False

    # Creating model and adding them to the admin view
    ## editable tables
    for m in [Users, Permission, Picture, Ongoing_Service, List_Service]:

        class View(ModelView, model=m):
            column_list = "__all__"

        admin.add_view(View)

    ## read-only tables
    for m in [UserSession, AuditEvent, RateLimit, OtpCode]:

        class View(ReadOnlyView, model=m):
            column_list = "__all__"

        admin.add_view(View)


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
