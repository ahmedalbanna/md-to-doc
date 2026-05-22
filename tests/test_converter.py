import os
import sys
import tempfile
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from md_to_docx.converter import MarkdownToDocxConverter
from md_to_docx.models import ConvertOptions
from md_to_docx.parsers.frontmatter import parse_front_matter, metadata_to_yaml
from md_to_docx.parsers.markdown_parser import MarkdownParser
from md_to_docx.builders.paragraph_builder import detect_text_direction, segment_by_direction, convert_to_arabic_indic
from md_to_docx.styles import Fonts, Colors, CoverStyles, NumberFormats


FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")


def load_fixture(name: str) -> str:
    path = os.path.join(FIXTURES_DIR, name)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


class TestConverter:
    def test_arabic_conversion(self):
        text = load_fixture("sample-arabic.md")
        options = ConvertOptions(dir="rtl", lang="ar")
        converter = MarkdownToDocxConverter(options=options)
        result = converter.convert(text)
        assert len(result) > 5000
        assert result[:2] == b"PK"

    def test_english_conversion(self):
        text = """# Hello\nThis is **bold** text."""
        options = ConvertOptions(dir="ltr", lang="en", cover_style="")
        converter = MarkdownToDocxConverter(options=options)
        result = converter.convert(text)
        assert len(result) > 3000

    def test_mixed_conversion(self):
        text = load_fixture("sample-mixed.md")
        options = ConvertOptions(dir="rtl", lang="ar")
        converter = MarkdownToDocxConverter(options=options)
        result = converter.convert(text)
        assert len(result) > 5000

    def test_minimal_content(self):
        text = "Just a simple paragraph."
        options = ConvertOptions(dir="ltr", lang="en", cover_style="",
                                 toc=False, lof=False, lot=False)
        converter = MarkdownToDocxConverter(options=options)
        result = converter.convert(text)
        assert len(result) > 2000

    def test_empty_paragraph(self):
        text = "# Title\n\n\n\nSome text."
        options = ConvertOptions(dir="rtl", lang="ar", cover_style="minimal")
        converter = MarkdownToDocxConverter(options=options)
        result = converter.convert(text)
        assert len(result) > 3000

    def test_heading_numbering(self):
        text = "# Chapter 1\n## Section 1.1\n### Subsection"
        options = ConvertOptions(dir="ltr", lang="en", cover_style="",
                                 toc=False, lof=False, lot=False,
                                 heading_numbering=True)
        converter = MarkdownToDocxConverter(options=options)
        result = converter.convert(text)
        assert len(result) > 3000

    def test_tables(self):
        text = "| A | B |\n|---|---|\n| 1 | 2 |\n| 3 | 4 |"
        options = ConvertOptions(dir="ltr", lang="en", cover_style="",
                                 toc=False, lof=False, lot=False)
        converter = MarkdownToDocxConverter(options=options)
        result = converter.convert(text)
        assert len(result) > 3000

    def test_lists(self):
        text = "- Item 1\n- Item 2\n  - Nested\n\n1. First\n2. Second"
        options = ConvertOptions(dir="ltr", lang="en", cover_style="",
                                 toc=False, lof=False, lot=False)
        converter = MarkdownToDocxConverter(options=options)
        result = converter.convert(text)
        assert len(result) > 3000

    def test_code_block(self):
        text = "```python\nprint('hello')\n```"
        options = ConvertOptions(dir="ltr", lang="en", cover_style="",
                                 toc=False, lof=False, lot=False)
        converter = MarkdownToDocxConverter(options=options)
        result = converter.convert(text)
        assert len(result) > 3000

    def test_blockquote(self):
        text = "> This is a quote."
        options = ConvertOptions(dir="ltr", lang="en", cover_style="",
                                 toc=False, lof=False, lot=False)
        converter = MarkdownToDocxConverter(options=options)
        result = converter.convert(text)
        assert len(result) > 2000

    def test_cover_styles(self):
        for style in CoverStyles.ALL:
            text = f"""---
title: "Test {style}"
cover_style: {style}
---
# Content"""
            options = ConvertOptions(dir="rtl", lang="ar")
            converter = MarkdownToDocxConverter(options=options)
            result = converter.convert(text)
            assert len(result) > 4000, f"Failed for style: {style}"

    def test_output_to_file(self):
        text = "# Test\nContent"
        options = ConvertOptions(dir="ltr", lang="en", cover_style="",
                                 toc=False, lof=False, lot=False)
        converter = MarkdownToDocxConverter(options=options)
        result = converter.convert(text)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            tmp.write(result)
            path = tmp.name
        assert os.path.exists(path)
        assert os.path.getsize(path) > 2000
        os.unlink(path)


class TestFrontMatter:
    def test_parse_full(self):
        text = """---
title: "Test"
author: "Me"
---
# Hello"""
        metadata, body = parse_front_matter(text)
        assert metadata is not None
        assert metadata.title == "Test"
        assert metadata.author == "Me"
        assert "# Hello" in body

    def test_parse_no_frontmatter(self):
        text = "# Just content"
        metadata, body = parse_front_matter(text)
        assert metadata is None
        assert body == text

    def test_parse_empty(self):
        text = ""
        metadata, body = parse_front_matter(text)
        assert metadata is None
        assert body == ""

    def test_metadata_to_yaml_roundtrip(self):
        from md_to_docx.models import DocumentMetadata
        meta = DocumentMetadata(title="Test", author="Me")
        yaml_text = metadata_to_yaml(meta)
        assert "title" in yaml_text
        assert "Test" in yaml_text
        metadata2, _ = parse_front_matter(yaml_text + "\n\n# Content")
        assert metadata2 is not None
        assert metadata2.title == "Test"
        assert metadata2.author == "Me"


class TestTextDirection:
    def test_arabic_detection(self):
        assert detect_text_direction("مرحباً بالعالم") == "rtl"

    def test_english_detection(self):
        assert detect_text_direction("Hello World") == "ltr"

    def test_mixed_detection(self):
        assert detect_text_direction("Hello مرحباً") == "rtl"

    def test_numbers_only(self):
        assert detect_text_direction("12345") == "ltr"

    def test_empty_string(self):
        assert detect_text_direction("") == "ltr"

    def test_segment_arabic(self):
        segs = segment_by_direction("Hello مرحباً World")
        assert len(segs) >= 2

    def test_convert_to_arabic_indic(self):
        assert convert_to_arabic_indic("123") == "١٢٣"
        assert convert_to_arabic_indic("0") == "٠"
        assert convert_to_arabic_indic("") == ""


class TestMarkdownParser:
    def test_parse_headings(self):
        parser = MarkdownParser()
        tokens = parser.parse("# H1\n## H2\n### H3")
        types = [t.type for t in tokens]
        assert "heading_open" in types
        assert types.count("heading_open") == 3

    def test_parse_table(self):
        parser = MarkdownParser()
        tokens = parser.parse("| A | B |\n|---|---|\n| 1 | 2 |")
        types = [t.type for t in tokens]
        assert "table_open" in types

    def test_parse_code_block(self):
        parser = MarkdownParser()
        tokens = parser.parse("```python\nprint('hi')\n```")
        types = [t.type for t in tokens]
        assert "fence" in types
        fence = [t for t in tokens if t.type == "fence"][0]
        assert fence.info.strip() == "python"

    def test_parse_list(self):
        parser = MarkdownParser()
        tokens = parser.parse("- Item 1\n- Item 2")
        types = [t.type for t in tokens]
        assert "bullet_list_open" in types

    def test_pagebreak_detection(self):
        from md_to_docx.builders.page_break import is_page_break_token
        parser = MarkdownParser()
        tokens = parser.parse("Text\n<!-- pagebreak -->\nMore")
        # Should find a pagebreak
        found = any(is_page_break_token(t) for t in tokens)
        assert found


class TestStyles:
    def test_fonts_defaults(self):
        assert Fonts.ARABIC_DEFAULT == "Amiri"
        assert Fonts.LATIN_DEFAULT == "Times New Roman"

    def test_colors_defined(self):
        assert Colors.PRIMARY is not None
        assert Colors.HEADING is not None

    def test_cover_styles(self):
        assert CoverStyles.CLASSIC in CoverStyles.ALL
        assert CoverStyles.MODERN in CoverStyles.ALL
        assert CoverStyles.MINIMAL in CoverStyles.ALL
        assert CoverStyles.ELEGANT in CoverStyles.ALL
        assert len(CoverStyles.ALL) == 4

    def test_number_formats(self):
        assert NumberFormats.WESTERN in NumberFormats.ALL
        assert NumberFormats.ARABIC_INDIC in NumberFormats.ALL
        assert NumberFormats.ROMAN in NumberFormats.ALL
        assert NumberFormats.ROMAN_UPPER in NumberFormats.ALL


if __name__ == "__main__":
    pytest.main([__file__, "-v"])