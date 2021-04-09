from __future__ import annotations

from collections.abc import Mapping, MutableMapping
from typing import Any

from markdown_it import MarkdownIt
import mdformat.plugins
from mdformat.renderer import RenderTreeNode
from mdformat.renderer.typing import RendererFunc
from mdit_py_plugins.myst_role import myst_role_plugin


def update_mdit(mdit: MarkdownIt) -> None:
    # Enable mdformat-tables plugin
    tables_plugin = mdformat.plugins.PARSER_EXTENSIONS["tables"]
    if tables_plugin not in mdit.options["parser_extension"]:
        mdit.options["parser_extension"].append(tables_plugin)
        tables_plugin.update_mdit(mdit)

    # Enable MyST role markdown-it extension
    mdit.use(myst_role_plugin)


def _role_renderer(
    node: RenderTreeNode,
    renderer_funcs: Mapping[str, RendererFunc],
    options: Mapping[str, Any],
    env: MutableMapping,
) -> str:
    role_name = "{" + node.meta["name"] + "}"
    role_content = f"`{node.content}`"
    return role_name + role_content


RENDERER_FUNCS = {"myst_role": _role_renderer}
