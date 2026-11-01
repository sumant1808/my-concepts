# Sell-side global markets functional architecture: sources

Working sources for the sell-side architecture views published under outputs/ (not deployed from here: the site serves only outputs/).

## content/
- spec.json: CURRENT content, layered functional architecture, extended for coverage on 2026-11-01 (8 layers, 51 groups, 114 components, 60 links, 21 externals, 44 standards). Validated structurally; NOT yet rebuilt into the views, NOT yet reviewed.
- spec.published-layers-v1.json: the layered content as PUBLISHED (8 layers, 33 groups, 100 components).
- spec.flow-view.json: the stage-by-stage flow view content as PUBLISHED (10 stages, 100 components).
- notes.md / notes.published-layers-v1.md, coverage.md (what the coverage extension added), restructure.md (stage view to layers mapping), review.md and fixes.md (independent review of the flow view and the fixes applied).

## builders-layers/ and builders-flow-view/
Python builders that read spec.json and write the two Design-canvas boards (Main.dc.html detailed, Summary.dc.html one-page) and canvas.json; final.sh runs the full rebuild plus conversion to static pages and checks. Paths inside assume the original working folders (/home/claude/sell-func-canvas, /home/claude/sell-arch); adjust when re-running.

## tools/
dc2html.js converts a Design-canvas board to a standalone static HTML page (expands sc-for and sc-if from renderVals). Other scripts were used for the restructure.
