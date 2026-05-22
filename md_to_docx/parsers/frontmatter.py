import re
import yaml
from typing import Optional
from ..models import DocumentMetadata, PageNumberConfig, FontConfig, HeadingNumberingConfig
from ..models import TocConfig, LofConfig, LotConfig, CaptionsConfig, DiagramConfig
from ..styles import Fonts


FRONT_MATTER_PATTERN = re.compile(
    r'^\s*---\s*\n(.*?)\n---\s*\n',
    re.DOTALL
)


def parse_front_matter(text: str) -> tuple[Optional[DocumentMetadata], str]:
    match = FRONT_MATTER_PATTERN.match(text)
    if not match:
        return None, text

    yaml_content = match.group(1)
    body = text[match.end():]

    try:
        data = yaml.safe_load(yaml_content)
        if not isinstance(data, dict):
            return None, text
    except yaml.YAMLError:
        return None, text

    metadata = _dict_to_metadata(data)
    return metadata, body


def _dict_to_metadata(data: dict) -> DocumentMetadata:
    fonts_data = data.get("fonts", {})
    if isinstance(fonts_data, dict):
        fonts = FontConfig(
            arabic=fonts_data.get("arabic", Fonts.ARABIC_DEFAULT),
            latin=fonts_data.get("latin", Fonts.LATIN_DEFAULT),
            code=fonts_data.get("code", Fonts.CODE_DEFAULT),
            heading=fonts_data.get("heading", Fonts.HEADING_DEFAULT),
            size=fonts_data.get("size", 12),
        )
    else:
        fonts = FontConfig()

    pn_data = data.get("page_numbers", {})
    if isinstance(pn_data, dict):
        page_numbers = PageNumberConfig(
            enabled=pn_data.get("enabled", True),
            front_matter=pn_data.get("front_matter", "roman"),
            body=pn_data.get("body", "arabic-indic"),
        )
    else:
        page_numbers = PageNumberConfig()

    hn_data = data.get("heading_numbering", {})
    if isinstance(hn_data, dict):
        heading_numbering = HeadingNumberingConfig(
            enabled=hn_data.get("enabled", True),
            start_level=hn_data.get("start_level", 1),
            separator=hn_data.get("separator", "."),
            include_chapter=hn_data.get("include_chapter", True),
        )
    else:
        heading_numbering = HeadingNumberingConfig()

    toc_data = data.get("toc", {})
    if isinstance(toc_data, dict):
        toc = TocConfig(
            enabled=toc_data.get("enabled", True),
            title=toc_data.get("title", "المحتويات"),
            max_level=toc_data.get("max_level", 3),
        )
    else:
        toc = TocConfig()

    lof_data = data.get("lof", {})
    if isinstance(lof_data, dict):
        lof = LofConfig(
            enabled=lof_data.get("enabled", True),
            title=lof_data.get("title", "قائمة الأشكال"),
        )
    else:
        lof = LofConfig()

    lot_data = data.get("lot", {})
    if isinstance(lot_data, dict):
        lot = LotConfig(
            enabled=lot_data.get("enabled", True),
            title=lot_data.get("title", "قائمة الجداول"),
        )
    else:
        lot = LotConfig()

    cap_data = data.get("captions", {})
    if isinstance(cap_data, dict):
        captions = CaptionsConfig(
            table_prefix=cap_data.get("table_prefix", "جدول"),
            figure_prefix=cap_data.get("figure_prefix", "شكل"),
            by_chapter=cap_data.get("by_chapter", True),
        )
    else:
        captions = CaptionsConfig()

    diag_data = data.get("diagrams", {})
    if isinstance(diag_data, dict):
        diagrams = DiagramConfig(
            plantuml=diag_data.get("plantuml", True),
            mermaid=diag_data.get("mermaid", True),
            render_engine=diag_data.get("render_engine", "local"),
        )
    else:
        diagrams = DiagramConfig()

    return DocumentMetadata(
        title=data.get("title", ""),
        subtitle=data.get("subtitle", ""),
        author=data.get("author", ""),
        date=data.get("date", ""),
        version=data.get("version", ""),
        logo=data.get("logo", ""),
        dir=data.get("dir", "rtl"),
        lang=data.get("lang", "ar"),
        cover_style=data.get("cover_style", "classic"),
        page_numbers=page_numbers,
        fonts=fonts,
        heading_numbering=heading_numbering,
        toc=toc,
        lof=lof,
        lot=lot,
        captions=captions,
        diagrams=diagrams,
    )


def metadata_to_yaml(metadata: DocumentMetadata) -> str:
    data = {
        "title": metadata.title,
        "subtitle": metadata.subtitle,
        "author": metadata.author,
        "date": metadata.date,
        "version": metadata.version,
        "logo": metadata.logo,
        "dir": metadata.dir,
        "lang": metadata.lang,
        "cover_style": metadata.cover_style,
        "page_numbers": {
            "enabled": metadata.page_numbers.enabled,
            "front_matter": metadata.page_numbers.front_matter,
            "body": metadata.page_numbers.body,
        },
        "fonts": {
            "arabic": metadata.fonts.arabic,
            "latin": metadata.fonts.latin,
            "code": metadata.fonts.code,
            "heading": metadata.fonts.heading,
            "size": metadata.fonts.size,
        },
        "heading_numbering": {
            "enabled": metadata.heading_numbering.enabled,
            "start_level": metadata.heading_numbering.start_level,
            "separator": metadata.heading_numbering.separator,
            "include_chapter": metadata.heading_numbering.include_chapter,
        },
        "toc": {
            "enabled": metadata.toc.enabled,
            "title": metadata.toc.title,
            "max_level": metadata.toc.max_level,
        },
        "lof": {
            "enabled": metadata.lof.enabled,
            "title": metadata.lof.title,
        },
        "lot": {
            "enabled": metadata.lot.enabled,
            "title": metadata.lot.title,
        },
        "captions": {
            "table_prefix": metadata.captions.table_prefix,
            "figure_prefix": metadata.captions.figure_prefix,
            "by_chapter": metadata.captions.by_chapter,
        },
        "diagrams": {
            "plantuml": metadata.diagrams.plantuml,
            "mermaid": metadata.diagrams.mermaid,
            "render_engine": metadata.diagrams.render_engine,
        },
    }
    return "---\n" + yaml.dump(data, allow_unicode=True, default_flow_style=False).strip() + "\n---"