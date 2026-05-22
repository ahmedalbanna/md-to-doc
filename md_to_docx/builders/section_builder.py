from docx import Document
from docx.enum.section import WD_ORIENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm
from ..models import DocumentMetadata
from ..styles import PageSetup


class SectionBuilder:
    def __init__(self, doc: Document, metadata: DocumentMetadata):
        self.doc = doc
        self.metadata = metadata
        self.section_count = 0

    def add_new_section(self, start_type: int = 2) -> "SectionBuilder":
        from docx.enum.section import WD_SECTION
        section = self.doc.add_section()
        self._configure_section(section)
        self.section_count += 1
        return self

    def _configure_section(self, section):
        section.page_width = PageSetup.PAGE_WIDTH
        section.page_height = PageSetup.PAGE_HEIGHT
        section.top_margin = PageSetup.MARGIN_TOP
        section.bottom_margin = PageSetup.MARGIN_BOTTOM
        section.left_margin = PageSetup.MARGIN_LEFT
        section.right_margin = PageSetup.MARGIN_RIGHT

        is_cover = self.section_count == 0
        if is_cover and self.metadata.cover_style:
            section.top_margin = PageSetup.COVER_MARGIN_TOP

        if self.metadata.dir == "rtl":
            self._set_section_rtl(section)

    def _set_section_rtl(self, section):
        sect_pr = section._sectPr
        bidi = OxmlElement("w:bidi")
        bidi.set(qn("w:val"), "1")
        sect_pr.append(bidi)

    def get_section(self, index: int = 0):
        sections = self.doc.sections
        if index < len(sections):
            return sections[index]
        return None

    def configure_page_number_format(self, section, num_format: str):
        sect_pr = section._sectPr
        pgNumType = sect_pr.find(qn("w:pgNumType"))
        if pgNumType is None:
            pgNumType = OxmlElement("w:pgNumType")
            sect_pr.append(pgNumType)

        fmt_map = {
            "western": "decimal",
            "arabic-indic": "decimal",
            "roman": "lowerRoman",
            "roman-upper": "upperRoman",
        }
        fmt = fmt_map.get(num_format, "decimal")
        pgNumType.set(qn("w:fmt"), fmt)

    def configure_cover_section(self, section):
        section.top_margin = PageSetup.COVER_MARGIN_TOP

    @property
    def current_section(self):
        return self.doc.sections[-1]