from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
import typing as t

from .config import settings
from .models import FeatureFlag
from .db import lifespan_engine, lifespan_session


def create_app() -> FastAPI:
    app = FastAPI(
        title="Session Arena",
        debug=settings.debug,
        lifespan=lifespan_engine,
    )

    # homepage jinja templates as static files
    app.mount("/static", StaticFiles(directory="app/static"), name="static")
    templates = Jinja2Templates(directory="app/templates")

    @app.get("/", response_class=HTMLResponse)
    async def homepage(request: Request, session: t.Annotated[AsyncSession, Depends(lifespan_session)]):
        flag = await session.get(FeatureFlag, "cool_mode")
        enabled = flag.enabled if flag is not None else None
        return templates.TemplateResponse("index.html", {"request": request, "cool_mode": enabled})

    @app.get("/favicon.ico", include_in_schema=False)
    async def get_favicon():
        return FileResponse("app/static/favicon.ico")

    # health check
    @app.get("/healthz")
    async def healthz():
        return {"ok": True, "env": settings.env}

    # toggle feature flag
    @app.post("/api/flags/{flag_name}/toggle")
    async def toggle_flag(flag_name: str, session: t.Annotated[AsyncSession, Depends(lifespan_session)]):
        flag = await session.get(FeatureFlag, flag_name)
        if flag is not None:
            flag.enabled = not flag.enabled
        else:
            flag = FeatureFlag(key=flag_name, enabled=True)
            session.add(flag)
        # commit happens during teardown
        return {"key": flag_name, "enabled": flag.enabled}

    return app

app = create_app()
