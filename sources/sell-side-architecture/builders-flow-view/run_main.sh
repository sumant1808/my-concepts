set -e
cd /home/claude/sell-arch-canvas
python3 build.py
node /home/claude/build/dc2html.js project/Main.dc.html html/detailed.html "Sell-side markets functional architecture: detailed view" >/dev/null
python3 -I measure.py $PWD/html/detailed.html check $PWD/shots/detailed-top.png
