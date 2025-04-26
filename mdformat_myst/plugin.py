from __future__ import annotations

import re

from markdown_it import MarkdownIt
import mdformat.plugins
from mdformat.renderer import RenderContext, RenderTreeNode
from mdit_py_plugins.dollarmath import dollarmath_plugin
from mdit_py_plugins.myst_blocks import myst_block_plugin
from mdit_py_plugins.myst_role import myst_role_plugin
from mdit_py_plugins.container import container_plugin

from mdformat_myst._directives import fence, render_fence_html

_TARGET_PATTERN = re.compile(r"^\s*\(.+\)=\s*$")
_ROLE_NAME_PATTERN = re.compile(r"({[a-zA-Z0-9_\-+:]+})")
_YAML_HEADER_PATTERN = re.compile(r"(?m)(^:\w+: .*$\n?)+|^---$\n(?s:.).*\n---\n")

container_names = [
    "admonition",
    "attention",
    "caution",
    "danger",
    "div",
    "dropdown",
    "embed",
    "error",
    "exercise",
    "exercise-end",
    "exercise-start",
    "figure",
    "glossary",
    "grid",
    "grid-item",
    "grid-item-card",
    "hint",
    "image",
    "important",
    "include",
    "index",
    "literal-include",
    "margin",
    "math",
    "note",
    "prf:algorithm",
    "prf:assumption",
    "prf:axiom",
    "prf:conjecture",
    "prf:corollary",
    "prf:criterion",
    "prf:definition",
    "prf:example",
    "prf:lemma",
    "prf:observation",
    "prf:proof",
    "prf:property",
    "prf:proposition",
    "prf:remark",
    "prf:theorem",
    "seealso",
    "show-index",
    "sidebar",
    "solution",
    "solution-end",
    "solution-start",
    "span",
    "tab-item",
    "tab-set",
    "table",
    "tip",
    "topics",
    "warning",
]


def update_mdit(mdit: MarkdownIt) -> None:
    # Enable mdformat-tables plugin
    tables_plugin = mdformat.plugins.PARSER_EXTENSIONS["tables"]
    if tables_plugin not in mdit.options["parser_extension"]:
        mdit.options["parser_extension"].append(tables_plugin)
        tables_plugin.update_mdit(mdit)

    # Enable mdformat-frontmatter plugin
    frontmatter_plugin = mdformat.plugins.PARSER_EXTENSIONS["frontmatter"]
    if frontmatter_plugin not in mdit.options["parser_extension"]:
        mdit.options["parser_extension"].append(frontmatter_plugin)
        frontmatter_plugin.update_mdit(mdit)

    # Enable mdformat-footnote plugin
    footnote_plugin = mdformat.plugins.PARSER_EXTENSIONS["footnote"]
    if footnote_plugin not in mdit.options["parser_extension"]:
        mdit.options["parser_extension"].append(footnote_plugin)
        footnote_plugin.update_mdit(mdit)

    # Enable MyST role markdown-it extension
    mdit.use(myst_role_plugin)

    # Enable MyST block markdown-it extension (including "LineComment",
    # "BlockBreak" and "Target" syntaxes)
    mdit.use(myst_block_plugin)

    # Enable dollarmath markdown-it extension
    mdit.use(dollarmath_plugin)

    # Trick `mdformat`s AST validation by removing HTML rendering of code
    # blocks and fences. Directives are parsed as code fences and we
    # modify them in ways that don't break MyST AST but do break
    # CommonMark AST, so we need to do this to make validation pass.
    mdit.add_render_rule("fence", render_fence_html)
    mdit.add_render_rule("code_block", render_fence_html)

    for name in container_names:
        container_plugin(mdit, name="{" + name + "}", marker=":")


def container_renderer(
    node: RenderTreeNode, context: RenderContext, *args, **kwargs
) -> str:
    children = node.children
    paragraphs = []
    if children:
        # Look at the tokens forming the first paragraph and see if
        # they form a YAML header. This could be stricter: there
        # should be exactly three tokens: paragraph start, YAML
        # header, paragraph end.
        tokens = children[0].to_tokens()
        if all(
            not token.content or _YAML_HEADER_PATTERN.fullmatch(token.content)
            for token in tokens
        ):
            paragraphs.append('\n'.join(token.content.strip()
                                        for token in tokens
                                        if token.content))
            # and skip that first paragraph
            children = children[1:]

    paragraphs.extend(child.render(context) for child in children)

    return node.markup + node.info + "\n" + "\n\n".join(paragraphs) + "\n" + node.markup


def _role_renderer(node: RenderTreeNode, context: RenderContext) -> str:
    role_name = "{" + node.meta["name"] + "}"
    role_content = f"`{node.content}`"
    return role_name + role_content


def _comment_renderer(node: RenderTreeNode, context: RenderContext) -> str:
    return "%" + node.content.replace("\n", "\n%")


def _blockbreak_renderer(node: RenderTreeNode, context: RenderContext) -> str:
    text = "+++"
    if node.content:
        text += f" {node.content}"
    return text


def _target_renderer(node: RenderTreeNode, context: RenderContext) -> str:
    return f"({node.content})="


def _math_inline_renderer(node: RenderTreeNode, context: RenderContext) -> str:
    return f"${node.content}$"


def _math_block_renderer(node: RenderTreeNode, context: RenderContext) -> str:
    return f"$${node.content}$$"


def _math_block_label_renderer(node: RenderTreeNode, context: RenderContext) -> str:
    return f"$${node.content}$$ ({node.info})"


def _render_children(node: RenderTreeNode, context: RenderContext) -> str:
    return "\n\n".join(child.render(context) for child in node.children)


def _escape_paragraph(text: str, node: RenderTreeNode, context: RenderContext) -> str:
    lines = text.split("\n")

    for i in range(len(lines)):

        # Three or more "+" chars are interpreted as a block break. Escape them.
        space_removed = lines[i].replace(" ", "")
        if space_removed.startswith("+++"):
            lines[i] = lines[i].replace("+", "\\+", 1)

        # A line starting with "%" is a comment. Escape.
        if lines[i].startswith("%"):
            lines[i] = f"\\{lines[i]}"

        # Escape lines that look like targets
        if _TARGET_PATTERN.search(lines[i]):
            lines[i] = lines[i].replace("(", "\\(", 1)

    return "\n".join(lines)


def _escape_text(text: str, node: RenderTreeNode, context: RenderContext) -> str:
    # Escape MyST role names
    text = _ROLE_NAME_PATTERN.sub(r"\\\1", text)

    # Escape inline and block dollarmath
    text = text.replace("$", "\\$")

    return text


RENDERERS = {
    "myst_role": _role_renderer,
    "myst_line_comment": _comment_renderer,
    "myst_block_break": _blockbreak_renderer,
    "myst_target": _target_renderer,
    "math_inline": _math_inline_renderer,
    "math_block_label": _math_block_label_renderer,
    "math_block": _math_block_renderer,
    "fence": fence,
}


for name in container_names:
    RENDERERS["container_{" + name + "}"] = container_renderer

POSTPROCESSORS = {"paragraph": _escape_paragraph, "text": _escape_text}
