"""FastAPI application for the Unit Converter service."""

from __future__ import annotations

import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.models import CategoryInfo, ConversionRequest, ConversionResponse
from app.converter import get_categories, convert_units

app = FastAPI(title="Spec-Driven Unit Converter", version="0.1.0")

# API Endpoints

@app.get("/health")
def health() -> dict[str, str]:
    """Liveness probe returning operational status."""
    return {"status": "ok", "app": "Spec-Driven Unit Converter"}


@app.get("/api/categories", response_model=list[CategoryInfo])
def list_categories() -> list[CategoryInfo]:
    """Retrieve the set of supported unit categories and their available units."""
    return get_categories()


@app.post("/api/convert", response_model=ConversionResponse)
def convert(request: ConversionRequest) -> ConversionResponse:
    """Calculate and return the conversion from one unit to another."""
    try:
        response = convert_units(
            category=request.category,
            from_unit=request.from_unit,
            to_unit=request.to_unit,
            value=request.value,
        )
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


# Serve HTML static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
def get_index() -> FileResponse:
    """Default landing page serving the premium conversion web interface."""
    index_path = os.path.join(static_dir, "index.html")
    if not os.path.exists(index_path):
        raise HTTPException(status_code=404, detail="Frontend index.html not found.")
    return FileResponse(index_path)
