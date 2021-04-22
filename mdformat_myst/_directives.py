from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
import io

from markdown_it import MarkdownIt
from mdformat.renderer import LOGGER, RenderContext, RenderTreeNode
import ruamel.yaml

yaml = ruamel.yaml.YAML()
yaml.indent(mapping=2, sequence=4, offset=2)


def longest_consecutive_sequence(seq: str, char: str) -> int:
    """Return length of the longest consecutive sequence of `char` characters
    in string `seq`."""
    assert len(char) == 1
    longest = 0
    current_streak = 0
    for c in seq:
        if c == char:
            current_streak += 1
        else:
            current_streak = 0
        if current_streak > longest:
            longest = current_streak
    return longest


def fence(node: "RenderTreeNode", context: "RenderContext") -> str:
    """Render fences (and directives).

    Copied from upstream `mdformat` core and should be kept up-to-date
    if upstream introduces changes. Note that only two lines are added
    to the upstream implementation, i.e. the condition that calls
    `format_directive_content` function.
    """
    info_str = node.info.strip()
    lang = info_str.split(maxsplit=1)[0] if info_str else ""
    code_block = node.content

    # Info strings of backtick code fences can not contain backticks or tildes.
    # If that is the case, we make a tilde code fence instead.
    if "`" in info_str or "~" in info_str:
        fence_char = "~"
    else:
        fence_char = "`"

    # Format the code block using enabled codeformatter funcs
    if lang in context.options.get("codeformatters", {}):
        fmt_func = context.options["codeformatters"][lang]
        try:
            code_block = fmt_func(code_block, info_str)
        except Exception:
            # Swallow exceptions so that formatter errors (e.g. due to
            # invalid code) do not crash mdformat.
            assert node.map is not None, "A fence token must have `map` attribute set"
            LOGGER.warning(
                f"Failed formatting content of a {lang} code block "
                f"(line {node.map[0] + 1} before formatting)"
            )
    # This "elif" is the *only* thing added to the upstream `fence` implementation!
    elif lang.startswith("{") and lang.endswith("}"):
        code_block = format_directive_content(code_block)

    # The code block must not include as long or longer sequence of `fence_char`s
    # as the fence string itself
    fence_len = max(3, longest_consecutive_sequence(code_block, fence_char) + 1)
    fence_str = fence_char * fence_len

    return f"{fence_str}{info_str}\n{code_block}{fence_str}"


def format_directive_content(raw_content: str) -> str:
    parse_result = parse_opts_and_content(raw_content)
    if not parse_result:
        return raw_content
    unformatted_yaml, content = parse_result
    dump_stream = io.StringIO()
    try:
        parsed = yaml.load(unformatted_yaml)
        yaml.dump(parsed, stream=dump_stream)
    except ruamel.yaml.YAMLError:
        LOGGER.warning("Invalid YAML in MyST directive options.")
        return raw_content
    formatted_yaml = dump_stream.getvalue()

    # Remove the YAML closing tag if added by `ruamel.yaml`
    if formatted_yaml.endswith("\n...\n"):
        formatted_yaml = formatted_yaml[:-4]

    # Convert empty YAML to most concise form
    if formatted_yaml == "null\n":
        formatted_yaml = ""

    formatted = "---\n" + formatted_yaml + "---\n"
    if content:
        formatted += content + "\n"
    return formatted


def parse_opts_and_content(raw_content: str) -> tuple[str, str] | None:
    lines = raw_content.splitlines()
    line = lines.pop(0)
    yaml_lines = []
    if all(c == "-" for c in line) and len(line) >= 3:
        while lines:
            line = lines.pop(0)
            if all(c == "-" for c in line) and len(line) >= 3:
                break
            yaml_lines.append(line)
    elif line.lstrip().startswith(":"):
        yaml_lines.append(line.lstrip()[1:])
        while lines:
            if not lines[0].lstrip().startswith(":"):
                break
            line = lines.pop(0).lstrip()[1:]
            yaml_lines.append(line)
    else:
        return None

    first_line_is_empty_but_second_line_isnt = (
        len(lines) >= 2 and not lines[0].strip() and lines[1].strip()
    )
    exactly_one_empty_line = len(lines) == 1 and not lines[0].strip()
    if first_line_is_empty_but_second_line_isnt or exactly_one_empty_line:
        lines.pop(0)

    unformatted_yaml = "\n".join(yaml_lines)
    content = "\n".join(lines)
    return unformatted_yaml, content


def render_fence_html(
    self: MarkdownIt, tokens: Sequence, idx: int, options: Mapping, env: MutableMapping
) -> str:
    return ""
