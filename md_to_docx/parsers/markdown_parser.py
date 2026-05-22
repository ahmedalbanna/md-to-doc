from markdown_it import MarkdownIt
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.tasklists import tasklists_plugin
from mdit_py_plugins.container import container_plugin
from mdit_py_plugins.deflist import deflist_plugin
from mdit_py_plugins.amsmath import amsmath_plugin
from markdown_it.token import Token
from typing import Generator, Optional


class MarkdownParser:
    def __init__(self):
        self.md = (
            MarkdownIt("commonmark", {"breaks": True, "html": True})
            .use(front_matter_plugin)
            .use(footnote_plugin)
            .use(tasklists_plugin)
            .use(deflist_plugin)
            .use(amsmath_plugin)
            .use(container_plugin, name="pagebreak")
            .enable("table")
            .enable("strikethrough")
            .enable("linkify")
        )
        self.md = self._enable_gfm(self.md)

    def _enable_gfm(self, md: MarkdownIt) -> MarkdownIt:
        try:
            md = md.enable("tasklists")
        except Exception:
            pass
        return md

    def parse(self, text: str) -> list[Token]:
        return self.md.parse(text)

    def iter_tokens(self, tokens: list[Token]) -> Generator[Token, None, None]:
        yield from tokens

    def find_heading_level(self, tokens: list[Token], pos: int) -> Optional[int]:
        for i in range(pos, max(pos - 20, -1), -1):
            if i >= 0 and i < len(tokens):
                token = tokens[i]
                if token.type == "heading_open" and token.tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
                    return int(token.tag[1])
        return None

    def get_inline_content(self, tokens: list[Token], start: int) -> str:
        parts = []
        i = start
        while i < len(tokens):
            token = tokens[i]
            if token.type == "inline":
                parts.append(token.content)
            elif token.type in ("heading_close", "paragraph_close"):
                break
            i += 1
        return "".join(parts)

    def has_pagebreak(self, token: Token) -> bool:
        if token.type == "container_pagebreak_open":
            return True
        if token.type == "inline" and token.content.strip() in ("\\pagebreak", "\\newpage"):
            return True
        if token.type == "inline" and "<!-- pagebreak -->" in token.content:
            return True
        if token.type == "hr":
            return False
        return False

    def get_code_language(self, token: Token) -> str:
        if token.type == "fence" and token.info:
            return token.info.strip().split()[0].lower()
        return ""

    def is_diagram(self, language: str) -> bool:
        return language in ("plantuml", "puml", "mermaid", "mmd")


def parse_markdown(text: str) -> list[Token]:
    parser = MarkdownParser()
    return parser.parse(text)