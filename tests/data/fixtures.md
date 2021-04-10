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
\| - |
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
