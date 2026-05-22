from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE


class Fonts:
    ARABIC_DEFAULT = "Amiri"
    LATIN_DEFAULT = "Times New Roman"
    CODE_DEFAULT = "Consolas"
    HEADING_DEFAULT = "Amiri"
    SIZE_DEFAULT = Pt(12)
    SIZE_SMALL = Pt(10)
    SIZE_CODE = Pt(9)
    SIZE_H1 = Pt(26)
    SIZE_H2 = Pt(22)
    SIZE_H3 = Pt(18)
    SIZE_H4 = Pt(16)
    SIZE_H5 = Pt(14)
    SIZE_H6 = Pt(12)
    SIZE_COVER_TITLE = Pt(36)
    SIZE_COVER_SUBTITLE = Pt(20)
    SIZE_COVER_META = Pt(14)
    SIZE_CAPTION = Pt(11)
    SIZE_TOC = Pt(12)


class Colors:
    PRIMARY = RGBColor(0x1B, 0x4F, 0x72)
    SECONDARY = RGBColor(0x2C, 0x3E, 0x50)
    HEADING = RGBColor(0x1A, 0x3C, 0x6E)
    HEADING_ACCENT = RGBColor(0x2C, 0x5F, 0x8A)
    BODY = RGBColor(0x33, 0x33, 0x33)
    CODE_BG = RGBColor(0xF2, 0xF2, 0xF2)
    CODE_FG = RGBColor(0x1E, 0x1E, 0x1E)
    QUOTE_BG = RGBColor(0xF5, 0xF5, 0xF5)
    QUOTE_BAR = RGBColor(0xBB, 0xBB, 0xBB)
    TABLE_HEADER_BG = RGBColor(0x1B, 0x4F, 0x72)
    TABLE_HEADER_FG = RGBColor(0xFF, 0xFF, 0xFF)
    TABLE_BORDER = RGBColor(0xCC, 0xCC, 0xCC)
    TABLE_ALT_ROW = RGBColor(0xF8, 0xF8, 0xF8)
    LINK = RGBColor(0x05, 0x63, 0xC1)
    COVER_ACCENT = RGBColor(0xC0, 0x39, 0x2B)
    COVER_GOLD = RGBColor(0xD4, 0xA5, 0x37)
    COVER_LIGHT_BG = RGBColor(0xF8, 0xF9, 0xFA)
    STRIKETHROUGH = RGBColor(0x99, 0x99, 0x99)


class Spacing:
    PARAGRAPH_BEFORE = Pt(3)
    PARAGRAPH_AFTER = Pt(6)
    HEADING_BEFORE = Pt(18)
    HEADING_AFTER = Pt(8)
    LIST_INDENT = Cm(1.27)
    QUOTE_INDENT = Cm(1.0)
    QUOTE_LEFT = Cm(0.5)
    TABLE_CELL_PADDING = Cm(0.15)
    CAPTION_BEFORE = Pt(4)
    CAPTION_AFTER = Pt(10)
    SECTION_TOP = Cm(2.54)
    SECTION_BOTTOM = Cm(2.54)
    SECTION_LEFT = Cm(2.54)
    SECTION_RIGHT = Cm(2.54)
    COVER_TOP = Cm(4.0)
    COVER_BOTTOM = Cm(2.0)
    COVER_LEFT = Cm(3.0)
    COVER_RIGHT = Cm(3.0)
    CODE_LEFT_INDENT = Cm(0.5)
    CODE_RIGHT_INDENT = Cm(0.3)


class ListStyles:
    BULLET_CHARS = ["●", "○", "▪", "▹"]
    ARABIC_NUMBER_FORMAT = "%1.%2.%3"
    TASK_LIST_SYMBOL_CHECKED = "\u2611"
    TASK_LIST_SYMBOL_UNCHECKED = "\u2610"
    LIST_TAB_STOP = Cm(1.27)
    LIST_INDENT = Cm(1.27)
    NUMBER_INDENT_LEFT = Cm(0.63)
    BULLET_INDENT_LEFT = Cm(0.63)
    HANGING_INDENT = Cm(0.63)


class PageSetup:
    PAGE_WIDTH = Cm(21.0)
    PAGE_HEIGHT = Cm(29.7)
    MARGIN_TOP = Cm(2.54)
    MARGIN_BOTTOM = Cm(2.54)
    MARGIN_LEFT = Cm(2.54)
    MARGIN_RIGHT = Cm(2.54)
    COVER_MARGIN_TOP = Cm(4.0)
    GUTTER = Cm(0.0)
    HEADER_DISTANCE = Cm(1.25)
    FOOTER_DISTANCE = Cm(1.25)


class CoverStyles:
    CLASSIC = "classic"
    MODERN = "modern"
    MINIMAL = "minimal"
    ELEGANT = "elegant"
    ALL = [CLASSIC, MODERN, MINIMAL, ELEGANT]


class NumberFormats:
    WESTERN = "western"
    ARABIC_INDIC = "arabic-indic"
    ROMAN = "roman"
    ROMAN_UPPER = "roman-upper"
    ALL = [WESTERN, ARABIC_INDIC, ROMAN, ROMAN_UPPER]


class CaptionTypes:
    TABLE = "table"
    FIGURE = "figure"


class BidiAliases:
    ARABIC_RANGES = [
        (0x0600, 0x06FF),
        (0x0750, 0x077F),
        (0x08A0, 0x08FF),
        (0xFB50, 0xFDFF),
        (0xFE70, 0xFEFF),
        (0x1EE00, 0x1EEFF),
    ]
    URDU_RANGES = [(0x0600, 0x06FF)]
    PERSIAN_RANGES = [(0x0600, 0x06FF), (0xFB50, 0xFDFF)]
    RTL_SCRIPTS = {
        "Arabic": (0x0600, 0x06FF),
        "Arabic Supplement": (0x0750, 0x077F),
        "Arabic Extended-A": (0x08A0, 0x08FF),
        "Arabic Presentation Forms-A": (0xFB50, 0xFDFF),
        "Arabic Presentation Forms-B": (0xFE70, 0xFEFF),
        "Arabic Mathematical": (0x1EE00, 0x1EEFF),
        "Hebrew": (0x0590, 0x05FF),
        "Syriac": (0x0700, 0x074F),
        "Thaana": (0x0780, 0x07BF),
        "NKo": (0x07C0, 0x07FF),
        "Samaritan": (0x0800, 0x083F),
        "Mandaic": (0x0840, 0x085F),
    }