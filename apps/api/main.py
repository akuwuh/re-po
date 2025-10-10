from __future__ import annotations

import os
from typing import Literal, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import PlainTextResponse, Response

from re_po.cli import render_card

app = FastAPI(title="re-po API", version="0.1.0")


@app.get("/v1/card")
def get_card(
    user: str = Query(..., description="GitHub username"),
    format: Literal["txt", "svg"] = Query("svg", description="Output format"),
    theme: Optional[str] = Query(None, description="Theme identifier"),
    width: Optional[int] = Query(None, ge=200, le=2000, description="Optional width for SVG output"),
):
    try:
        result = render_card(user=user, format=format, theme=theme, width=width)
    except Exception as exc:  # noqa: BLE001 - return HTTP error
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    cache_control = "public, s-maxage=3600, stale-while-revalidate=86400"
    headers = {
        "Cache-Control": cache_control,
        "ETag": result.etag,
        "Vary": "Accept",
    }

    media_type = result.content_type
    if format == "txt":
        return PlainTextResponse(result.content, media_type=media_type, headers=headers)
    return Response(result.content, media_type=media_type, headers=headers)


@app.get("/")
def root() -> dict[str, str]:
    base_url = os.getenv("RE_PO_API_BASE", "http://localhost:8000")
    return {
        "message": "re-po API",
        "docs": f"{base_url}/docs",
    }
