Table
.
a | b | c
:- | -: | :-:
1 | 2 | 3
xxxxxx | yyyyyy | zzzzzz
.
| a      |      b |   c    |
| :----- | -----: | :----: |
| 1      |      2 |   3    |
| xxxxxx | yyyyyy | zzzzzz |
.

Table escape
.
| a |
\| - |
.
| a |
| \- |
.

MyST Role
.
Euler's identity, equation {math:numref}`euler`, was elected one of the
most beautiful mathematical formulas.
.
Euler's identity, equation {math:numref}`euler`, was elected one of the
most beautiful mathematical formulas.
.

MyST Role escape
.
Escaped role {math:numref\}`euler`, right there
.
Escaped role \{math:numref}`euler`, right there
.

MyST LineComment
.
a line
% a comment
another line
.
a line

% a comment

another line
.

MyST LineComment escape
.
a line
\% a comment
another line
.
a line
\% a comment
another line
.

MyST BlockBreak
.
a line
+++ a block break
another line
.
a line

+++ a block break

another line
.

MyST BlockBreak escape
.
a line
++\+ NOT a block break
another line
.
a line
\+++ NOT a block break
another line
.

MyST Target
.
(myst_target)=
That's a myst target^
.
(myst_target)=

That's a myst target^
.

MyST Target escape
.
(myst_target\)=
That's NOT a myst target^
.
\(myst_target)=
That's NOT a myst target^
.

Dollarmath inline
.
Inline math: $a=1$
.
Inline math: $a=1$
.

Dollarmath inline escape
.
Escaped inline math: $a=1\$
.
Escaped inline math: \$a=1$
.

Dollarmath block
.
Block math:

$$
a=1
$$
.
Block math:

$$
a=1
$$
.

Dollarmath block escape
.
$$
a=1
$\$
.
\$$
a=1
\$$
.

Dollarmath block labeled
.
Labeled block math:

$$
a=1
$$ (eq1)
.
Labeled block math:

$$
a=1
$$ (eq1)
.

Frontmatter
.
---
lastname: Blorothy
firstname: Dorothy
---
Thats YAML front matter^
.
---
firstname: Dorothy
lastname: Blorothy
---

Thats YAML front matter^
.

Frontmatter escape
.
--\-
not frontmatter
-\--

Thats not YAML front matter^
.
\---
not frontmatter
\---

Thats not YAML front matter^
.


Footnotes
.
# Now some markdown
Here is a footnote reference,[^1] and another.[^longnote]
[^1]: Here is the footnote.
[^longnote]: Here's one with multiple blocks.

    Subsequent paragraphs are indented to show that they
belong to the previous footnote.

    Third paragraph here.
.
# Now some markdown

Here is a footnote reference,[^1] and another.[^longnote]

[^1]: Here is the footnote.

[^longnote]: Here's one with multiple blocks.

    Subsequent paragraphs are indented to show that they
belong to the previous footnote.

    Third paragraph here.
.
