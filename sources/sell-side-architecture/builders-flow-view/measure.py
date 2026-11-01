import sys,json,subprocess
from playwright.sync_api import sync_playwright
ROOT='/home/claude/sell-arch-canvas'
page_path=sys.argv[1]; mode=sys.argv[2]  # measure | check
with sync_playwright() as p:
    b=p.chromium.launch(); 
    size=json.load(open(ROOT+'/main_size.json')) if 'detailed' in page_path else {'w':1920,'h':1080}
    pg=b.new_page(viewport={'width':size['w'],'height':min(size['h'],4000)})
    errs=[]
    pg.on('console',lambda m: errs.append(m.text) if m.type=='error' else None)
    pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.goto('file://'+page_path); pg.wait_for_timeout(1500)
    if mode=='measure':
        hs=pg.evaluate("""()=>{const o={};document.querySelectorAll('[data-k]').forEach(e=>{e.style.height='auto'});
          document.querySelectorAll('[data-k]').forEach(e=>{o[e.dataset.k]=Math.ceil(e.getBoundingClientRect().height)});return o}""")
        # keep original if smaller? use measured + small pad for cards
        out={k:(v+3 if k[0] in 'cx' else v+ (4 if k[0] in 'gv' else 2)) for k,v in hs.items()}
        out={k:(v if k[:2]!='p:' else v+8) for k,v in out.items()}
        json.dump(out,open(ROOT+'/heights.json','w'))
        print('measured',len(out))
    else:
        r=pg.evaluate("""()=>{const bad=[];document.querySelectorAll('#wrap *').forEach(e=>{
          if(e.closest('svg'))return; const cs=getComputedStyle(e);
          if(cs.display==='inline'||e.clientWidth<=1)return;
          if(e.scrollHeight>e.clientHeight+1||e.scrollWidth>e.clientWidth+1){bad.push([e.tagName,(e.dataset.k||''),e.className||'',e.scrollWidth+'x'+e.scrollHeight,e.clientWidth+'x'+e.clientHeight,(e.textContent||'').slice(0,50)])}});
          return {bad:bad,sw:document.documentElement.scrollWidth,iw:innerWidth,fonts:[...document.fonts].map(f=>f.family+':'+f.status)}}""")
        print('overflow elements',len(r['bad']));
        for x in r['bad'][:40]: print(x)
        print('hscroll',r['sw'],r['iw'],'fonts',r['fonts'][:4])
        print('console errors',errs)
        if len(sys.argv)>3:
            pg.screenshot(path=sys.argv[3],full_page=False)
        if len(sys.argv)>4:
            pg.screenshot(path=sys.argv[4],full_page=True)
    b.close()
