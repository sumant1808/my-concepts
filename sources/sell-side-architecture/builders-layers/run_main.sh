set -e
cd /home/claude/sell-func-canvas
MODE=${1:-check}
rm -f heights.json
KEYS=1 python3 build.py >/dev/null
node /home/claude/build/dc2html.js project/Main.dc.html html/detailed.html "Sell-side markets functional architecture: detailed view" >/dev/null
python3 -I measure.py $PWD/html/detailed.html measure
KEYS=1 python3 build.py
node /home/claude/build/dc2html.js project/Main.dc.html html/detailed.html "Sell-side markets functional architecture: detailed view" >/dev/null
python3 -I measure.py $PWD/html/detailed.html measure
KEYS=1 python3 build.py
