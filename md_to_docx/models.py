from dataclasses import dataclass, field
from typing import Optional
from .styles import Fonts, CoverStyles, NumberFormats


@dataclass
class PageNumberConfig:
    enabled: bool = True
    front_matter: str = NumberFormats.ROMAN
    body: str = NumberFormats.ARABIC_INDIC

    def __post_init__(self):
        if self.front_matter not in NumberFormats.ALL:
            self.front_matter = NumberFormats.ROMAN
        if self.body not in NumberFormats.ALL:
            self.body = NumberFormats.ARABIC_INDIC


@dataclass
class FontConfig:
    arabic: str = Fonts.ARABIC_DEFAULT
    latin: str = Fonts.LATIN_DEFAULT
    code: str = Fonts.CODE_DEFAULT
    heading: str = Fonts.HEADING_DEFAULT
    size: int = 12


@dataclass
class HeadingNumberingConfig:
    enabled: bool = True
    start_level: int = 1
    separator: str = "."
    include_chapter: bool = True


@dataclass
class TocConfig:
    enabled: bool = True
    title: str = "المحتويات"
    max_level: int = 3


@dataclass
class LofConfig:
    enabled: bool = True
    title: str = "قائمة الأشكال"


@dataclass
class LotConfig:
    enabled: bool = True
    title: str = "قائمة الجداول"


@dataclass
class CaptionsConfig:
    table_prefix: str = "جدول"
    figure_prefix: str = "شكل"
    by_chapter: bool = True


@dataclass
class DiagramConfig:
    plantuml: bool = True
    mermaid: bool = True
    render_engine: str = "local"


@dataclass
class DocumentMetadata:
    title: str = ""
    subtitle: str = ""
    author: str = ""
    date: str = ""
    version: str = ""
    logo: str = ""
    dir: str = "rtl"
    lang: str = "ar"
    cover_style: str = CoverStyles.CLASSIC
    page_numbers: PageNumberConfig = field(default_factory=PageNumberConfig)
    fonts: FontConfig = field(default_factory=FontConfig)
    heading_numbering: HeadingNumberingConfig = field(default_factory=HeadingNumberingConfig)
    toc: TocConfig = field(default_factory=TocConfig)
    lof: LofConfig = field(default_factory=LofConfig)
    lot: LotConfig = field(default_factory=LotConfig)
    captions: CaptionsConfig = field(default_factory=CaptionsConfig)
    diagrams: DiagramConfig = field(default_factory=DiagramConfig)

    def __post_init__(self):
        if isinstance(self.page_numbers, dict):
            self.page_numbers = PageNumberConfig(**self.page_numbers)
        if isinstance(self.fonts, dict):
            self.fonts = FontConfig(**self.fonts)
        if isinstance(self.heading_numbering, dict):
            self.heading_numbering = HeadingNumberingConfig(**self.heading_numbering)
        if isinstance(self.toc, dict):
            self.toc = TocConfig(**self.toc)
        if isinstance(self.lof, dict):
            self.lof = LofConfig(**self.lof)
        if isinstance(self.lot, dict):
            self.lot = LotConfig(**self.lot)
        if isinstance(self.captions, dict):
            self.captions = CaptionsConfig(**self.captions)
        if isinstance(self.diagrams, dict):
            self.diagrams = DiagramConfig(**self.diagrams)


@dataclass
class ConvertOptions:
    text: str = ""
    dir: str = ""
    lang: str = ""
    font_arabic: str = ""
    font_latin: str = ""
    cover_style: str = ""
    page_number_format: str = ""
    heading_numbering: bool = True
    toc: bool = True
    lof: bool = True
    lot: bool = True
    diagrams: bool = True


YAML_FRONT_MATTER_TEMPLATE = """---
title: "عنوان المستند"
subtitle: "العنوان الفرعي"
author: "اسم المؤلف"
date: "2024-01-15"
version: "1.0"
logo: ""
dir: rtl
lang: ar
cover_style: classic
page_numbers:
  enabled: true
  front_matter: roman
  body: arabic-indic
fonts:
  arabic: "Amiri"
  latin: "Times New Roman"
  code: "Consolas"
  heading: "Amiri"
  size: 12
heading_numbering:
  enabled: true
  start_level: 1
  separator: "."
  include_chapter: true
toc:
  enabled: true
  title: "المحتويات"
  max_level: 3
lof:
  enabled: true
  title: "قائمة الأشكال"
lot:
  enabled: true
  title: "قائمة الجداول"
captions:
  table_prefix: "جدول"
  figure_prefix: "شكل"
  by_chapter: true
diagrams:
  plantuml: true
  mermaid: true
  render_engine: local
---"""