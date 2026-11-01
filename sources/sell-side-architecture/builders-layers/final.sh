set -e
cd /home/claude/sell-func-canvas
bash run_main.sh >/dev/null          # measure passes, leaves heights.json
KEYS=0 python3 build.py
python3 build_summary.py
python3 - <<'PY'
import json
m=json.load(open('/home/claude/sell-func-canvas/main_size.json'))
c={"v":3,"createdOnFiles":{"v":1,"at":"2026-11-01T14:00:00Z"},"title":"Sell-side markets functional architecture (layers and common services)","launch":{"view":"canvas"},"pages":[],
"boards":{"Main.dc.html":{"x":0,"y":0,"w":m['w'],"h":m['h'],"title":f"Detailed view ({m['n']} components)"},"Summary.dc.html":{"x":m['w']+80,"y":0,"w":1920,"h":1080,"title":"One-page client view"}},
"order":["Main.dc.html","Summary.dc.html"],"notes":{},"designSystems":[]}
open('/home/claude/sell-func-canvas/project/canvas.json','w').write(json.dumps(c,separators=(',',':')))
PY
node /home/claude/build/dc2html.js project/Main.dc.html html/detailed.html "Sell-side markets functional architecture: detailed view"
node /home/claude/build/dc2html.js project/Summary.dc.html html/onepage.html "Sell-side markets functional architecture: one page"
python3 -I measure.py $PWD/html/detailed.html check $PWD/shots/detailed-top.png $PWD/shots/detailed-full.png
python3 -I measure.py $PWD/html/onepage.html check $PWD/shots/onepage.png
python3 check.py
