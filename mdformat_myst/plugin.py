from __future__ import annotations

from markdown_it import MarkdownIt
import mdformat.plugins
from mdformat.renderer import RenderContext, RenderTreeNode
from mdit_py_plugins.dollarmath import dollarmath_plugin
from mdit_py_plugins.myst_blocks import myst_block_plugin
from mdit_py_plugins.myst_role import myst_role_plugin


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


def _role_renderer(node: RenderTreeNode, context: RenderContext) -> str:
    role_name = "{" + node.meta["name"] + "}"
    role_content = f"`{node.content}`"
    return role_name + role_content


def _comment_renderer(node: RenderTreeNode, context: RenderContext) -> str:
    return "% " + node.content


def _blockbreak_renderer(node: RenderTreeNode, context: RenderContext) -> str:
    return "+++ " + node.content


def _target_renderer(node: RenderTreeNode, context: RenderContext) -> str:
    return f"({node.content})="


def _math_inline_renderer(node: RenderTreeNode, context: RenderContext) -> str:
    return f"${node.content}$"


def _math_block_renderer(node: RenderTreeNode, context: RenderContext) -> str:
    return f"$${node.content}$$"


def _math_block_eqno_renderer(node: RenderTreeNode, context: RenderContext) -> str:
    return f"$${node.content}$$ ({node.info})"


RENDERERS = {
    "myst_role": _role_renderer,
    "myst_line_comment": _comment_renderer,
    "myst_block_break": _blockbreak_renderer,
    "myst_target": _target_renderer,
    "math_inline": _math_inline_renderer,
    "math_block_eqno": _math_block_eqno_renderer,
    "math_block": _math_block_renderer,
}
