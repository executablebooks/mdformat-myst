---
key: value
---

(myst_target)=

# Header

% a comment
%   with indentation

+++ a block break

MyST role: {name}`content`

MyST directive:

```{name} arguments
---
option1: 1
option2: hello
---
Content
```

table:

| a      |      b |   c    |
| :----- | -----: | :----: |
| 1      |      2 |   3    |
| xxxxxx | yyyyyy | zzzzzz |

dollar math:

$$
a=1
$$

Here is a footnote reference.[^a]

[^a]: First paragraph with
    two lines.

    ```
    content
    ```
