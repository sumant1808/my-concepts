import sys,json
from playwright.sync_api import sync_playwright
ROOT='/home/claude/sell-func-canvas'
page_path=sys.argv[1]; mode=sys.argv[2]
with sync_playwright() as p:
    b=p.chromium.launch()
    size=json.load(open(ROOT+'/main_size.json')) if 'detailed' in page_path else {'w':1920,'h':1080}
    pg=b.new_page(viewport={'width':size['w'],'height':min(size['h'],4000)})
    errs=[]
    pg.on('console',lambda m: errs.append(m.text) if m.type=='error' else None)
    pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.goto('file://'+page_path); pg.wait_for_timeout(1500)
    if mode=='measure':
        hs=pg.evaluate("""()=>{const o={};document.querySelectorAll('[data-k]').forEach(e=>{e.style.height='auto'});
          document.querySelectorAll('[data-k]').forEach(e=>{o[e.dataset.k]=Math.ceil(e.getBoundingClientRect().height)});return o}""")
        pad={'c':3,'x':3,'g':2,'l':4,'p':8}
        out={k:v+pad[k[0]] for k,v in hs.items()}
        json.dump(out,open(ROOT+'/heights.json','w'))
        print('measured',len(out))
    else:
        r=pg.evaluate("""()=>{const bad=[];document.querySelectorAll('#wrap *').forEach(e=>{
          if(e.closest('svg'))return; const cs=getComputedStyle(e);
          if(cs.display==='inline'||e.clientWidth<=1)return;
          if(e.scrollHeight>e.clientHeight+1||e.scrollWidth>e.clientWidth+1){bad.push([e.tagName,(e.dataset.k||''),e.scrollWidth+'x'+e.scrollHeight,e.clientWidth+'x'+e.clientHeight,(e.textContent||'').slice(0,50)])}});
          const f=[];document.querySelectorAll('#wrap *').forEach(e=>{const fs=parseFloat(getComputedStyle(e).fontSize);if(e.childNodes.length&&[...e.childNodes].some(n=>n.nodeType==3&&n.textContent.trim())&&fs<%s)f.push([e.tagName,fs,e.textContent.slice(0,30)])});
          return {bad:bad,small:f.slice(0,10),sw:document.documentElement.scrollWidth,iw:innerWidth,fonts:[...document.fonts].map(f=>f.family+':'+f.status)}}""" % ('12' if 'detailed' in page_path else '18'))
        print('overflow elements',len(r['bad']))
        for x in r['bad'][:40]: print(x)
        print('below min font',r['small'])
        print('hscroll',r['sw'],r['iw'],'fonts',r['fonts'][:4])
        print('console errors',errs)
        if len(sys.argv)>3: pg.screenshot(path=sys.argv[3],full_page=False)
        if len(sys.argv)>4: pg.screenshot(path=sys.argv[4],full_page=True)
    b.close()
