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

MyST LineComment - multiline
.
a line
% a multiline
%comment
%      yep

% another comment
.
a line

% a multiline
%comment
%      yep

% another comment
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

MyST BlockBreak: empty content
.
a line
+++ 
another line
.
a line

+++

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
That's a myst target^
The escape has no effect
.
(myst_target\)=

That's a myst target^
The escape has no effect
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
Escaped inline math: \$a=1\$
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
$\$
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
lastname: Blorothy
firstname: Dorothy
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

Move footnote definitions to the end (but before link ref defs)
.
[link]: https://www.python.org
[^1]: Here is the footnote.

# Now we reference them
Here is a footnote reference[^1]
Here is a [link]

.
# Now we reference them

Here is a footnote reference[^1]
Here is a [link]

[^1]: Here is the footnote.

[link]: https://www.python.org
.

footnote-indentation
.
[^a]

[^a]: first paragraph with
unindented next line.

    paragraph with
    indented next line

    paragraph with
unindented next line

    ```
    content
    ```
.
[^a]

[^a]: first paragraph with
    unindented next line.

    paragraph with
    indented next line

    paragraph with
    unindented next line

    ```
    content
    ```
.


MyST directive YAML
.
``` {some-directive} args
  :option1:  1
  :option2:   hello
Content
```

``` {some-directive} args
  :option1:  1
  :option2:   hello

Content
```

``` {some-directive} args
---
option1:  1
option2:   hello
---
Content
```

``` {some-directive} args
---
  option1:  1
  option2:   hello
---

Content
```
.
```{some-directive} args
---
option1: 1
option2: hello
---
Content
```

```{some-directive} args
---
option1: 1
option2: hello
---
Content
```

```{some-directive} args
---
option1: 1
option2: hello
---
Content
```

```{some-directive} args
---
option1: 1
option2: hello
---
Content
```
.


MyST directive empty YAML
.
``` {some-directive} args
  :
Content
```
.
```{some-directive} args
---
---
Content
```
.

MyST directive no content
.
``` {some-directive} args
  :letter: a

```
.
```{some-directive} args
---
letter: a
---
```
.

MyST directive, no opts or content
.
``` {some-directive} args
```
.
```{some-directive} args
```
.
