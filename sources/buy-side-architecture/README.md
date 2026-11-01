# UK buy-side asset manager functional architecture: sources

Working sources for the buy-side architecture views published under outputs/uk-buy-side-architecture/ (the site serves only outputs/, nothing here is deployed).

## content/
- spec.json: CURRENT content as published (6 layers, 35 groups, 90 components C01-C90, 19 externals, 32 illustrative flows in three headings, 26 standards of which 11 not verified).
- spec.pre-review.json (if present): content before the independent review fixes.
- notes.md: layer logic, where BIAN fits and where it does not, other standards used as inputs, limitations.
- review.md: the independent review (35 findings R1-R35). fixes.md: what was applied, modified or skipped.

## builders/
build.py (detailed board plus canvas.json), build_summary.py (one-page 16:9 board, functional clusters, 7-slot grid), check.py and holes.js (local checks). They read spec.json and write Main.dc.html, Summary.dc.html and canvas.json; paths assume the original working folders (/home/claude/am-arch, /home/claude/am-arch-canvas): adjust when re-running.

## tools/
dc2html.js converts a Design-canvas board into a standalone static HTML page (run with node: dc2html.js board.dc.html out.html "title"). build_spec.py is the original generator for spec.json; do not re-run it, spec.json was edited directly after the review.

Published: Design canvas https://claude.ai/artifact/BC57GYzmkSob6ngaAG6aj1 ; static pages outputs/uk-buy-side-architecture/ (commit 649fc5b, updates in 2 later commits are in the same folder). Drive state file: buy-side-functional-architecture-STATE-v1.md in my-claude-memory.
