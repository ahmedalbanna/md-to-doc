import os
import sys
import click
from .converter import MarkdownToDocxConverter
from .models import ConvertOptions
from .styles import CoverStyles, Fonts, NumberFormats


@click.group()
def cli():
    pass


@cli.command()
@click.argument("input", type=click.Path(exists=True))
@click.option("-o", "--output", default=None, help="Output DOCX file path")
@click.option("--dir", default="rtl", type=click.Choice(["rtl", "ltr"]),
              help="Document direction")
@click.option("--lang", default="ar", type=click.Choice(["ar", "en"]),
              help="Document language")
@click.option("--cover-style", default="classic",
              type=click.Choice(CoverStyles.ALL), help="Cover page style")
@click.option("--font-arabic", default=Fonts.ARABIC_DEFAULT, help="Arabic font name")
@click.option("--font-latin", default=Fonts.LATIN_DEFAULT, help="Latin font name")
@click.option("--page-number", default=NumberFormats.ARABIC_INDIC,
              type=click.Choice(NumberFormats.ALL), help="Page number format")
@click.option("--heading-numbering/--no-heading-numbering", default=True,
              help="Enable heading numbering")
@click.option("--toc/--no-toc", default=True, help="Include table of contents")
@click.option("--lof/--no-lof", default=True, help="Include list of figures")
@click.option("--lot/--no-lot", default=True, help="Include list of tables")
@click.option("--diagrams/--no-diagrams", default=True,
              help="Render PlantUML/Mermaid diagrams")
@click.option("--from-frontmatter/--no-frontmatter", default=True,
              help="Parse YAML front matter")
def convert(input, output, dir, lang, cover_style, font_arabic, font_latin,
           page_number, heading_numbering, toc, lof, lot, diagrams,
           from_frontmatter):
    """Convert Markdown file to DOCX."""
    with open(input, "r", encoding="utf-8") as f:
        markdown_text = f.read()

    if not output:
        base = os.path.splitext(input)[0]
        output = f"{base}.docx"

    options = ConvertOptions(
        dir=dir,
        lang=lang,
        font_arabic=font_arabic,
        font_latin=font_latin,
        cover_style=cover_style,
        page_number_format=page_number,
        heading_numbering=heading_numbering,
        toc=toc,
        lof=lof,
        lot=lot,
        diagrams=diagrams,
    )

    converter = MarkdownToDocxConverter(options=options)
    base_path = os.path.dirname(os.path.abspath(input))
    result = converter.convert(markdown_text, base_path=base_path)

    with open(output, "wb") as f:
        f.write(result)

    click.echo(f"✓ Converted: {input} → {output}")


@cli.command()
@click.option("--port", default=8000, help="Port to serve on")
@click.option("--host", default="0.0.0.0", help="Host to bind to")
def serve(port, host):
    """Start the web interface server."""
    from .web import start_server
    click.echo(f"Starting web interface at http://{host}:{port}")
    start_server(host=host, port=port)


if __name__ == "__main__":
    cli()