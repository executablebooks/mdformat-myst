from __future__ import annotations

import re
import textwrap
from typing import Dict

from markdown_it import MarkdownIt
from markdown_it.rules_core.state_core import StateCore
import mdformat.plugins
from mdformat.renderer import RenderContext, RenderTreeNode
from mdit_py_plugins.attrs import attrs_block_plugin
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

    # Enable mdformat-front-matters plugin
    front_matters_plugin = mdformat.plugins.PARSER_EXTENSIONS["front_matters"]
    if front_matters_plugin not in mdit.options["parser_extension"]:
        mdit.options["parser_extension"].append(front_matters_plugin)
        front_matters_plugin.update_mdit(mdit)

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

    # Enable support for attribute tagging for paragraphs and other "blocks"
    mdit.use(attrs_block_plugin)

    # Trick `mdformat`s AST validation by removing HTML rendering of code
    # blocks and fences. Directives are parsed as code fences and we
    # modify them in ways that don't break MyST AST but do break
    # CommonMark AST, so we need to do this to make validation pass.
    mdit.add_render_rule("fence", render_fence_html)
    mdit.add_render_rule("code_block", render_fence_html)

    # Force `mdformat` to treat "equivalent" attribute sets in a given HTML element
    # (e.g., `<p id="a" key1="value1">` as equivalent to `<p key1="value1" id="a">` by
    # just sorting all such key/value groups.
    #
    # Multiple block attributes that are stacked on top of each other can create output
    # HTML attribute orderings (from mdit_py_plugins.attrs's parsing logic) that cannot
    # be replicated if we (nicely, for a formatter) collapse those blocks into a single
    # nicely-ordered attr dict. Therefore, there is no way to avoid doing this sorting,
    # i.e., we cannot just "preserve" the input ordering.
    mdit.core.ruler.push("sort_attrs", _sort_attrs)


def _sort_attrs(state: StateCore) -> None:
    """Sort attributes in all tokens to ensure deterministic HTML rendering.

    This fixes validation errors where `mdformat` thinks the HTML has changed
    simply because the attribute order flipped (e.g. `id="..." class="..."`
    vs `class="..." id="..."`).
    """
    for token in state.tokens:
        if token.attrs:
            token.attrs = dict(sorted(token.attrs.items()))


def _reconstruct_attrs(attrs: Dict[str, str | int | float]) -> str:
    if not attrs:
        return ""

    parts = []
    if "id" in attrs:
        parts.append(f"#{attrs['id']}")
    if "class" in attrs:
        assert isinstance(attrs["class"], str), (
            "mdit_py_plugins.attrs guarantees a string here."
        )
        for cls in attrs["class"].split():
            parts.append(f".{cls}")
    for k, v in attrs.items():
        if k in {"id", "class"}:
            continue
        parts.append(f'{k}="{v}"')

    if not parts:
        return ""
    return "{" + " ".join(parts) + "}"


def _append_attrs_postprocessor(
    text: str, node: RenderTreeNode, context: RenderContext
) -> str:
    """Prepend MyST attributes to the already-rendered text."""
    attrs_str = _reconstruct_attrs(node.attrs)
    if attrs_str:
        return f"{attrs_str}\n{text}"
    return text


def _paragraph_postprocessor(
    text: str, node: RenderTreeNode, context: RenderContext
) -> str:
    """Encapsulate all paragraph post-processing."""
    text = _escape_paragraph(text, node, context)
    return _append_attrs_postprocessor(text, node, context)


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
    indent_width = context.env.get("indent_width", 0)
    if indent_width > 0:
        return f"$${textwrap.dedent(node.content)}$$"
    return f"$${node.content}$$"


def _math_block_label_renderer(node: RenderTreeNode, context: RenderContext) -> str:
    return f"{_math_block_renderer(node, context)} ({node.info})"


def _math_block_safe_blockquote_renderer(
    node: RenderTreeNode, context: RenderContext
) -> str:
    marker = "> "
    with context.indented(len(marker)):
        lines = []
        for i, child in enumerate(node.children):
            if child.type in ("math_block", "math_block_label"):
                lines.append(child.render(context))
            else:
                lines.extend(child.render(context).splitlines())
            if i < (len(node.children) - 1):
                lines.append("")
        if not lines:
            return ">"
        quoted_lines = (f"{marker}{line}" if line else ">" for line in lines)
        quoted_str = "\n".join(quoted_lines)
        return quoted_str


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
    "blockquote": _math_block_safe_blockquote_renderer,
    "myst_role": _role_renderer,
    "myst_line_comment": _comment_renderer,
    "myst_block_break": _blockbreak_renderer,
    "myst_target": _target_renderer,
    "math_inline": _math_inline_renderer,
    "math_block_label": _math_block_label_renderer,
    "math_block": _math_block_renderer,
    "fence": fence,
}
POSTPROCESSORS = {
    "blockquote": _append_attrs_postprocessor,
    "colon_fence": _append_attrs_postprocessor,
    "fence": _append_attrs_postprocessor,
    "heading": _append_attrs_postprocessor,
    "table": _append_attrs_postprocessor,
    # Paragraphs require special handling to escape strings like "++", but also need to
    # be able to have attrs added.
    "paragraph": _paragraph_postprocessor,
    "text": _escape_text,
}
