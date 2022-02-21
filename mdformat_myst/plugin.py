from __future__ import annotations

import re

from markdown_it import MarkdownIt
import mdformat.plugins
from mdformat.renderer import RenderContext, RenderTreeNode
from mdit_py_plugins.dollarmath import dollarmath_plugin
from mdit_py_plugins.myst_blocks import myst_block_plugin
from mdit_py_plugins.myst_role import myst_role_plugin

from mdformat_myst._directives import fence, render_fence_html

_TARGET_PATTERN = re.compile(r"^\s*\(.+\)=\s*$")
_ROLE_NAME_PATTERN = re.compile(r"({[a-zA-Z0-9_\-+:]+})")


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
POSTPROCESSORS = {"paragraph": _escape_paragraph, "text": _escape_text}
