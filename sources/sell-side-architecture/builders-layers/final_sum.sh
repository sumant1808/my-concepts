cd /home/claude/sell-func-canvas
python3 build_summary.py && node /home/claude/build/dc2html.js project/Summary.dc.html html/onepage.html "Sell-side markets functional architecture: one page" >/dev/null && python3 -I measure.py $PWD/html/onepage.html check $PWD/shots/onepage.png
