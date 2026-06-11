import os
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from research_and_analyst.api.routes import report_routes

app = FastAPI(title="ShodhAI - Research Report Generator")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="research_and_analyst/api/templates")
app.templates = templates


def basename_filter(path: str):
    return os.path.basename(path)


def filesize_filter(size: int | str | None):
    try:
        value = int(size or 0)
    except (TypeError, ValueError):
        value = 0
    if value >= 1024 * 1024:
        return f"{value / (1024 * 1024):.1f} MB"
    if value >= 1024:
        return f"{value / 1024:.1f} KB"
    return f"{value} B"


def datetime_filter(value: str | None):
    if not value:
        return ""
    try:
        normalized = value.replace("Z", "+00:00")
        parsed = datetime.fromisoformat(normalized)
        return parsed.strftime("%b %d, %Y %H:%M UTC")
    except ValueError:
        return value


templates.env.filters["basename"] = basename_filter
templates.env.filters["filesize"] = filesize_filter
templates.env.filters["datetime"] = datetime_filter

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "shodhai",
        "timestamp": datetime.now().isoformat(),
    }


app.include_router(report_routes.router)
