import os
import tempfile
import json
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse, Response, FileResponse
from fastapi.staticfiles import StaticFiles

from .converter import MarkdownToDocxConverter
from .models import ConvertOptions
from .styles import CoverStyles, Fonts, NumberFormats

app = FastAPI(title="Markdown to DOCX Converter")

STATIC_DIR = Path(__file__).parent / "static"


@app.get("/", response_class=HTMLResponse)
async def index():
    index_path = STATIC_DIR / "index.html"
    if not index_path.exists():
        return HTMLResponse("<h1>Index page not found</h1>", status_code=404)
    return HTMLResponse(index_path.read_text(encoding="utf-8"))


@app.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}


@app.get("/api/cover-styles")
async def cover_styles():
    return {"styles": CoverStyles.ALL}


@app.post("/api/convert")
async def convert_file(
    file: UploadFile = File(None),
    text: str = Form(""),
    dir: str = Form("rtl"),
    lang: str = Form("ar"),
    font_arabic: str = Form(Fonts.ARABIC_DEFAULT),
    font_latin: str = Form(Fonts.LATIN_DEFAULT),
    cover_style: str = Form("classic"),
    page_number_format: str = Form(NumberFormats.ARABIC_INDIC),
    heading_numbering: bool = Form(True),
    toc: bool = Form(True),
    lof: bool = Form(True),
    lot: bool = Form(True),
    diagrams: bool = Form(True),
):
    markdown_text = text

    if file and file.filename:
        content = await file.read()
        markdown_text = content.decode("utf-8", errors="replace")

    if not markdown_text.strip():
        raise HTTPException(status_code=400, detail="No markdown content provided")

    options = ConvertOptions(
        dir=dir,
        lang=lang,
        font_arabic=font_arabic,
        font_latin=font_latin,
        cover_style=cover_style,
        page_number_format=page_number_format,
        heading_numbering=heading_numbering,
        toc=toc,
        lof=lof,
        lot=lot,
        diagrams=diagrams,
    )

    try:
        converter = MarkdownToDocxConverter(options=options)
        result = converter.convert(markdown_text)

        return Response(
            content=result,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={
                "Content-Disposition": "attachment; filename=converted.docx"
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/convert/text")
async def convert_text(data: dict):
    markdown_text = data.get("text", "")
    if not markdown_text.strip():
        raise HTTPException(status_code=400, detail="No markdown content provided")

    options_dict = data.get("options", {})
    options = ConvertOptions(
        dir=options_dict.get("dir", "rtl"),
        lang=options_dict.get("lang", "ar"),
        font_arabic=options_dict.get("font_arabic", Fonts.ARABIC_DEFAULT),
        font_latin=options_dict.get("font_latin", Fonts.LATIN_DEFAULT),
        cover_style=options_dict.get("cover_style", "classic"),
        page_number_format=options_dict.get("page_number_format", NumberFormats.ARABIC_INDIC),
        heading_numbering=options_dict.get("heading_numbering", True),
        toc=options_dict.get("toc", True),
        lof=options_dict.get("lof", True),
        lot=options_dict.get("lot", True),
        diagrams=options_dict.get("diagrams", True),
    )

    try:
        converter = MarkdownToDocxConverter(options=options)
        result = converter.convert(markdown_text)

        return Response(
            content=result,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={
                "Content-Disposition": "attachment; filename=converted.docx"
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def start_server(host: str = "0.0.0.0", port: int = 8000):
    import uvicorn
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    start_server()