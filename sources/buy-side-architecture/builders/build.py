import json, html, sys
SPEC='/home/claude/am-arch/spec.json'
OUT='/home/claude/am-arch-canvas/project/Main.dc.html'
CANVAS='/home/claude/am-arch-canvas/project/canvas.json'
d=json.load(open(SPEC,encoding='utf-8'))
esc=lambda s: html.escape(s,quote=True)

# ---------- text height estimation (conservative) ----------
CW,CWB=0.57,0.62
def nlines(text,width,fs,bold=False):
    cw=(CWB if bold else CW)*fs; n=1; cur=0.0
    for w in text.split():
        wl=len(w)*cw; add=wl if cur==0 else wl+cw
        if cur>0 and cur+add>width: n+=1; cur=wl
        else: cur+=add
    return n
def ev(x): return int(x)+(int(x)%2)

NAVY='#0B1F3A'; TEAL='#0F8B8D'; AMBER='#C27C00'
INK='#17202E'; MUTED='#445066'; LINE='#C3CBD8'
SEGC={'A':'#1F4E8C','P':'#0B6E70','L':'#8A5700','ALL':'#3A4556'}
CARDT={'A':'#DCE8F7','P':'#D9F0EC','L':'#FAE8C6'}
GRPT={'A':'#C5D8F0','P':'#BFE3DD','L':'#F2D9A6'}
SEGNAME={'A':'Active','P':'Passive and ETF','L':'Alternatives','ALL':'All segments'}
FONT="'DM Sans',system-ui,sans-serif"

def chip(s,label=None):
    return ('<span style="display:inline-block;font-size:12px;line-height:16px;font-weight:700;padding:1px 7px;'
            f'border-radius:3px;color:#FFFFFF;background:{SEGC[s]};margin-right:4px">{label or s}</span>')

els=[]   # (html) in paint order: bands, cards, labels
bands=[]; cards=[]; labels=[]

# ---------- geometry ----------
W=2400; M=64
Y0=196; YC=Y0+52
SX,SW=336,1728        # centre stack
HCW=190               # layer header cell
GX0=SX+HCW+10; GAVAIL=SX+SW-10-GX0
STRIP_W=240; LX=M; RX=W-M-STRIP_W
GGAP=10

comp_name={}
cur_y=YC
band_tops={}; layer_bounds=[]
for li,L in enumerate(d['layers']):
    n=len(L['groups']); colw=(GAVAIL-(n-1)*GGAP)//n; cardw=colw-16
    iw=cardw-23
    gdata=[]
    for g in L['groups']:
        segs=set(s for c in g['components'] for s in c['seg'])
        homo = segs if len(segs)==1 and list(segs)[0] in CARDT else None
        glines=nlines(('P  ' if homo else '')+g['name'],colw-16,12,True)
        ch=[]
        for c in g['components']:
            comp_name[c['id']]=c['name']
            role=f"{c['sor']} · {c['calm']}"+(' · third party' if c['external'] else '')
            h=18+22+nlines(c['name'],iw,13,True)*17+2+nlines(c['does'],iw,12)*16
            if c['bian']: h+=4+nlines('BIAN: '+c['bian'],iw,12)*15
            h+=4+nlines(role,iw,12)*15+6
            ch.append((c,role,ev(h)))
        gdata.append((g,homo,glines,ch))
    ghl=max(x[2] for x in gdata)*15+12
    stack=max(sum(h for _,_,h in x[3])+6*(len(x[3])-1) for x in gdata)
    bandh=10+ghl+stack+8+10
    top=cur_y
    bands.append(f'<div style="position:absolute;left:{SX}px;top:{top}px;width:{SW}px;height:{bandh}px;box-sizing:border-box;background:#FFFFFF;border:1px solid #CBD3DF;border-radius:8px"></div>')
    bands.append(f'<div style="position:absolute;left:{SX}px;top:{top}px;width:{HCW}px;height:{bandh}px;box-sizing:border-box;background:{NAVY};border-radius:8px 0 0 8px"></div>')
    # layer header text
    nm=L['name']; nl=nlines(nm,HCW-28,19,True)
    h2h=16+nl*24
    labels.append(f'<h2 style="position:absolute;left:{SX+14}px;top:{top+14}px;width:{HCW-28}px;height:{h2h}px;margin:0;font-family:Fraunces,Georgia,serif;font-weight:600;font-size:19px;line-height:24px;color:#FFFFFF"><span style="display:block;font-family:{FONT};font-size:12px;line-height:16px;font-weight:700;color:#7FD6D8">Layer {li+1}</span>{esc(nm)}</h2>')
    pl=nlines(L['purpose'],HCW-28,12)
    labels.append(f'<p style="position:absolute;left:{SX+14}px;top:{top+14+h2h+8}px;width:{HCW-28}px;height:{pl*16}px;margin:0;font-size:12px;line-height:16px;color:#DDE5F0">{esc(L["purpose"])}</p>')
    # groups
    for gi,(g,homo,glines,ch) in enumerate(gdata):
        gx=GX0+gi*(colw+GGAP); gy=top+10; gh=bandh-20
        bg=GRPT[list(homo)[0]] if homo else '#E9EEF5'
        bands.append(f'<div style="position:absolute;left:{gx}px;top:{gy}px;width:{colw}px;height:{gh}px;box-sizing:border-box;background:{bg};border-radius:6px"></div>')
        pre=chip(list(homo)[0]) if homo else ''
        labels.append(f'<h3 style="position:absolute;left:{gx+8}px;top:{gy+6}px;width:{colw-16}px;height:{ghl-6}px;margin:0;font-size:12px;line-height:15px;font-weight:700;color:{NAVY}">{pre}{esc(g["name"])}</h3>')
        y=gy+ghl
        for c,role,h in ch:
            seg=c['seg']
            tint=CARDT[seg[0]] if len(seg)==1 and seg[0] in CARDT else '#FFFFFF'
            border='1.5px dashed #4A5568' if c['external'] else f'1px solid {LINE}'
            chips=chip('ALL','All') if seg==['ALL'] else ''.join(chip(s) for s in seg)
            sr='<span style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap">Segments: </span>'
            body=(f'<span style="display:block;line-height:20px;margin-bottom:2px">{sr}{chips}</span>'
                  f'<b style="display:block;font-size:13px;line-height:17px;color:{INK}">{esc(c["name"])}</b>'
                  f'<span style="display:block;margin-top:2px;color:{INK}">{esc(c["does"])}</span>')
            if c['bian']: body+=f'<span style="display:block;margin-top:4px;line-height:15px;color:{MUTED}">BIAN: {esc(c["bian"])}</span>'
            body+=f'<span style="display:block;margin-top:4px;line-height:15px;font-style:italic;color:{MUTED}">{esc(role)}</span>'
            cards.append(f'<article style="position:absolute;left:{gx+8}px;top:{y}px;width:{cardw}px;height:{h}px;box-sizing:border-box;padding:8px 10px;background:{tint};border:{border};border-radius:6px;font-size:12px;line-height:16px;color:{INK}">{body}</article>')
            y+=h+6
    band_tops[L['id']]=(top,bandh)
    cur_y=top+bandh+10
STACK_BOTTOM=cur_y-10

# ---------- externals ----------
ext={x['id']:x for x in d['externals']}
LEFT=[('X01','L1'),('X02','L1'),('X03','L1'),('X13','L2'),('X04','L3'),('X05','L3'),('X12','L3'),('X18','L3'),('X11','L3')]
RIGHT=[('X08','L2'),('X10','L2'),('X06','L4'),('X16','L4'),('X07','L4'),('X17','L4'),('X14','L5'),('X19','L5'),('X15','L5'),('X09','L6')]
assert sorted(i for i,_ in LEFT+RIGHT)==sorted(ext)
def strip(lst,x):
    y=YC
    for xid,lay in lst:
        e=ext[xid]; iw=STRIP_W-23
        h=ev(18+nlines(e['name'],iw,13,True)*17+4+nlines(e['role'],iw,12)*16+4)
        y=max(y,band_tops[lay][0])
        cards.append(f'<article style="position:absolute;left:{x}px;top:{y}px;width:{STRIP_W}px;height:{h}px;box-sizing:border-box;padding:8px 10px;background:#FFFFFF;border:1px solid #7C889B;border-radius:6px;font-size:12px;line-height:16px;color:{INK}"><b style="display:block;font-size:13px;line-height:17px;margin-bottom:4px">{esc(e["name"])}</b><span style="display:block;color:{MUTED}">{esc(e["role"])}</span></article>')
        y+=h+10
    return y-10
lb=strip(LEFT,LX); rb=strip(RIGHT,RX)
assert max(lb,rb)<=STACK_BOTTOM+0, (lb,rb,STACK_BOTTOM)
def heading(x,w,text):
    labels.append(f'<h2 style="position:absolute;left:{x}px;top:{Y0}px;width:{w}px;height:44px;margin:0;font-size:14px;line-height:18px;font-weight:700;color:{NAVY}">{esc(text)}</h2>')
heading(LX,STRIP_W,'External parties: clients, markets and counterparties')
heading(RX,STRIP_W,'External parties: service providers and oversight')
heading(SX,SW,'Functional layers, top to bottom. Each layer groups system components; standards are inputs, not the structure.')

# ---------- panels ----------
YB=STACK_BOTTOM+48
PSTYLE='position:absolute;box-sizing:border-box;padding:20px;background:#FFFFFF;border:1px solid #CBD3DF;border-radius:8px;'
def h2s(t): return f'<h2 style="margin:0 0 6px;font-family:Fraunces,Georgia,serif;font-weight:600;font-size:22px;line-height:28px;color:{NAVY}">{esc(t)}</h2>'
def note(t): return f'<p style="margin:0 0 10px;font-size:13px;line-height:18px;color:{MUTED}">{esc(t)}</p>'
def h3s(t): return f'<h3 style="margin:14px 0 4px;font-size:13px;line-height:18px;font-weight:700;color:{NAVY}">{esc(t)}</h3>'

# -- flows (data driven, grouped under three headings)
FW=960; FI=FW-40
fc=(32,442,240,170); gap=12
def name_of(i): return comp_name.get(i) or ext[i]['name']
FLOWHEADS=[('T','Life of a listed trade'),('F','Life of a fund deal'),('C','Life of a capital call')]
assert set(l['flow'] for l in d['links'])==set(k for k,_ in FLOWHEADS)
fh=0
for l in d['links']:
    a=nlines(f"{name_of(l['from'])} to {name_of(l['to'])}",fc[1],13,True)*18
    b=nlines(l['label'],fc[2],13)*18
    c=nlines(l['std'] or 'no standard named',fc[3],12)*16
    fh+=14+max(a,b,c,18)+1
fh+=len(FLOWHEADS)*(14+18+4)
FLOW_H=20+28+6+nlines('x'*210,FI,13)*18+10+26+fh+20+8
def flowlist(listname):
    return ('<ol style="list-style:none;margin:0;padding:0">'
     f'<sc-for list="{{{{{listname}}}}}" as="f" hint-placeholder-count="3">'
     f'<li style="display:grid;grid-template-columns:{fc[0]}px {fc[1]}px {fc[2]}px {fc[3]}px;column-gap:{gap}px;padding:7px 0;border-bottom:1px solid #E1E6EE;font-size:13px;line-height:18px;color:{INK}">'
     f'<span style="font-weight:700;color:{NAVY}">{{{{f.n}}}}</span>'
     '<span><b>{{f.from}}</b> to <b>{{f.to}}</b></span>'
     '<span>{{f.label}}</span>'
     '<span style="font-size:12px;line-height:16px;color:#445066">'
     '<sc-if value="{{f.hasStd}}" hint-placeholder-val="{{true}}">{{f.std}}</sc-if>'
     '<sc-if value="{{f.noStd}}" hint-placeholder-val="{{false}}"><i>no standard named</i></sc-if>'
     '</span></li></sc-for></ol>')
flows_html=(f'<section style="{PSTYLE}left:{M}px;top:{YB}px;width:{FW}px;height:{{H}}px" aria-labelledby="flows-h">'
 +h2s('Key flows').replace('<h2 ','<h2 id="flows-h" ')
 +note('Illustrative only. A selection of representative flows between components and external parties, not the integration estate. The diagram has no connector arrows by design; read these rows instead.')
 +f'<div aria-hidden="true" style="display:grid;grid-template-columns:{fc[0]}px {fc[1]}px {fc[2]}px {fc[3]}px;column-gap:{gap}px;padding:4px 0;font-size:12px;line-height:18px;font-weight:700;color:{NAVY};border-bottom:2px solid {NAVY}"><span>No.</span><span>From and to</span><span>What moves</span><span>Standard</span></div>'
 +''.join(h3s(title)+flowlist('flows'+k) for k,title in FLOWHEADS)
 +'</section>')

# -- legend (literal)
LW=600; LI=LW-40
def lrow(sample,sh,sw,text,bold_first=None):
    tw=LI-sw-12
    th=nlines(text,tw,13)*18
    h=max(sh,th)+8
    return (f'<li style="display:flex;gap:12px;align-items:flex-start;padding:4px 0;font-size:13px;line-height:18px;color:{INK}"><span style="flex:0 0 {sw}px;width:{sw}px">{sample}</span><span>{esc(text)}</span></li>'),h
def lsection(title,rows):
    h=14+18+4+sum(r[1] for r in rows)
    return h3s(title)+'<ul style="list-style:none;margin:0;padding:0">'+''.join(r[0] for r in rows)+'</ul>',h
def swatch(bg,border,inner):
    return f'<span style="display:block;width:96px;height:26px;box-sizing:border-box;padding:3px 6px;background:{bg};border:{border};border-radius:5px;font-size:12px;line-height:18px;color:{INK}">{inner}</span>'
secs=[]
secs.append(lsection('Segments',[
 lrow(chip('A'),24,96,'Active long-only listed funds and mandates'),
 lrow(chip('P'),24,96,'Passive and ETF'),
 lrow(chip('L'),24,96,'Alternatives: private equity, private credit, real assets'),
 lrow(chip('ALL','All'),24,96,'Shared by all three segments. Components for Active and Passive together show A and P.')]))
secs.append(lsection('Card edge and tint',[
 lrow(swatch('#FFFFFF','1px solid '+LINE,'Solid'),26,96,'Solid edge: the manager usually runs it'),
 lrow(swatch('#FFFFFF','1.5px dashed #4A5568','Dashed'),26,96,'Dashed edge: a third party usually runs it. The manager keeps oversight and data ownership.'),
 lrow(swatch(CARDT['A'],'1px solid '+LINE,chip('A')),26,96,'Pale blue fill: Active-only component. A deeper blue behind a whole group means every component in it is Active only.'),
 lrow(swatch(CARDT['P'],'1px solid '+LINE,chip('P')),26,96,'Pale teal fill: Passive and ETF only. A deeper teal behind a whole group means every component in it is Passive only.'),
 lrow(swatch(CARDT['L'],'1px solid '+LINE,chip('L')),26,96,'Pale amber fill: Alternatives only. A deeper amber behind a group means the same. Letters carry the meaning; colour only reinforces it.'),
 lrow(swatch('#E9EEF5','1px solid '+LINE,'Shared'),26,96,'Grey group backing: shared components')]))
roles=[('system of record','holds the authoritative copy of the data it manages'),('engagement','where clients, advisers or staff interact with the firm'),('calculation','derives values, risk, performance or analytics from data'),('data','supplies or stores reference and market data'),('integration','moves and translates data between systems'),('control','enforces limits, rules, checks and oversight')]
secs.append(lsection('Role line on each card (analyst glossary)',[lrow(f'<b>{esc(a)}</b>',20,120,b) for a,b in roles]))
calm=[('actor','a person or role that uses the architecture'),('ecosystem','a wider set of parties and systems'),('system','a deployable application or platform'),('service','a capability offered through an interface'),('database','a store of records'),('network','a network or messaging fabric'),('ldap','a directory used for identity'),('webclient','a browser or app front end'),('data-asset','a managed dataset')]
secs.append(lsection('CALM 1.1 node-type vocabulary (second word on the role line; glosses are the analyst\'s)',[lrow(f'<b>{esc(a)}</b>',20,120,b) for a,b in calm]))
LEG_H=20+28+6+nlines('x'*60,LI,13)*18+10+sum(s[1] for s in secs)+20+8
legend_html=(f'<section style="{PSTYLE}left:{M+FW+32}px;top:{YB}px;width:{LW}px;height:{{H}}px" aria-labelledby="legend-h">'
  +h2s('Legend').replace('<h2 ','<h2 id="legend-h" ')
  +note('How to read the cards. CALM terms are vocabulary only: this is not a CALM document, and flows and controls are not modelled.')+''.join(s[0] for s in secs)+'</section>')

# -- honesty (literal)
HW=W-2*M-FW-LW-64; HI=HW-40
lims=[
 'BIAN was checked against the version 10 service landscape only. It is oriented to banks and has no buy-side or private-markets coverage, so the layering is the analyst\'s own and BIAN names are labels, not structure. A card with no BIAN line had no matching domain.',
 'UK rules are named as in the FCA Handbook. Those marked not verified were not checked against the source for this draft; validate before external use.',
 'ISO 20022 business areas are verified. Message-level mappings (for example setr for fund orders, seev for proxy voting, camt for cash statements, acmt for accounts) come from analyst knowledge and need confirming.',
 'The key flows are illustrative. The real integration estate is far denser, and most components also read from the platform layer.',
 'This is an archetype, not a client estate. It assumes one manager acting as both UK UCITS manager and AIFM, and it leaves out hedge funds, synthetic ETFs and advice.',
 'Status: draft analyst design, AI-reviewed, not practitioner-validated. It has no agentic AI layer, no vendor names and no market statistics.']
hh=sum(nlines(t,HI-22,13)*18+10 for t in lims)
HON_H=20+28+6+nlines('x'*50,HI,13)*18+10+hh+20+8
lis=''.join(f'<li style="margin:0 0 10px;padding:0 0 0 0;font-size:13px;line-height:18px;color:{INK}">{esc(t)}</li>' for t in lims)
honesty_html=(f'<section style="{PSTYLE}left:{M+FW+32+LW+32}px;top:{YB}px;width:{HW}px;height:{{H}}px;background:#FFF6E3;border-color:{AMBER}" aria-labelledby="hon-h">'
  +h2s('Limitations and honesty').replace('<h2 ','<h2 id="hon-h" ')
  +note('What this diagram does not establish.')
  +f'<ul style="margin:0;padding:0 0 0 22px">{lis}</ul></section>')
ROW1=ev(max(FLOW_H,LEG_H,HON_H))+0
flows_html=flows_html.replace('{H}',str(ROW1)); legend_html=legend_html.replace('{H}',str(ROW1)); honesty_html=honesty_html.replace('{H}',str(ROW1))

# -- standards + assumptions (data driven)
YB2=YB+ROW1+32
SW2=1500; AW=W-2*M-SW2-32
sci=SW2-40; colw2=(sci-32)//2; txtw=colw2-96-12
std=d['standards']; half=(len(std)+1)//2
def sh(items):
    t=0
    for s in items:
        t+=ev(max(24,nlines(s['name'],txtw,13,True)*18+nlines(s['used_for'],txtw,12)*16))+16+1
    return t
STD_H=20+28+6+nlines('x'*200,sci,13)*18+10+max(sh(std[:half]),sh(std[half:]))+20+8
ai=AW-40-30
ah=sum(nlines(a,ai,13)*18+10 for a in d['assumptions'])
ASM_H=20+28+6+nlines('x'*60,AW-40,13)*18+10+ah+20+8
ROW2=ev(max(STD_H,ASM_H))
def stdcol(listname):
    return ('<ul style="list-style:none;margin:0;padding:0">'
     f'<sc-for list="{{{{{listname}}}}}" as="s" hint-placeholder-count="3">'
     f'<li style="display:flex;gap:12px;align-items:flex-start;padding:8px 0;border-bottom:1px solid #E1E6EE;font-size:12px;line-height:16px;color:{INK}">'
     '<span style="flex:0 0 96px;width:96px">'
     f'<sc-if value="{{{{s.verified}}}}" hint-placeholder-val="{{{{true}}}}"><span style="display:block;box-sizing:border-box;width:96px;text-align:center;padding:3px 0;background:{NAVY};color:#FFFFFF;border:2px solid {NAVY};border-radius:4px;font-size:12px;line-height:16px;font-weight:700">Verified</span></sc-if>'
     f'<sc-if value="{{{{s.unverified}}}}" hint-placeholder-val="{{{{false}}}}"><span style="display:block;box-sizing:border-box;width:96px;text-align:center;padding:3px 0;background:#FFFFFF;color:#6B4200;border:2px solid #8A5700;border-radius:4px;font-size:12px;line-height:16px;font-weight:700">Not verified</span></sc-if>'
     '</span>'
     '<span style="flex:1 1 auto"><b style="display:block;font-size:13px;line-height:18px">{{s.name}}</b>{{s.usedFor}}</span></li></sc-for></ul>')
std_html=(f'<section style="{PSTYLE}left:{M}px;top:{YB2}px;width:{SW2}px;height:{ROW2}px" aria-labelledby="std-h">'
  +h2s('Standards used as inputs').replace('<h2 ','<h2 id="std-h" ')
  +note('Each standard informed a component name, an identifier, a message or a report. None of them defines the structure. Verified means the source was read in this work; not verified means the name is used from analyst knowledge and must be checked.')
  +f'<div style="display:grid;grid-template-columns:{colw2}px {colw2}px;column-gap:32px">'+stdcol('stdA')+stdcol('stdB')+'</div></section>')
asm_html=(f'<section style="{PSTYLE}left:{M+SW2+32}px;top:{YB2}px;width:{AW}px;height:{ROW2}px" aria-labelledby="asm-h">'
  +h2s('Assumptions').replace('<h2 ','<h2 id="asm-h" ')
  +note('Choices made to draw one archetype.')
  +'<ol style="list-style:none;margin:0;padding:0">'
  '<sc-for list="{{assumptions}}" as="a" hint-placeholder-count="3">'
  f'<li style="display:flex;gap:8px;margin:0 0 10px;font-size:13px;line-height:18px;color:{INK}"><b style="flex:0 0 22px;width:22px;color:{NAVY}">{{{{a.n}}}}</b><span>{{{{a.text}}}}</span></li></sc-for></ol></section>')

H_TOTAL=YB2+ROW2+64
footer=f'<p style="position:absolute;left:{M}px;top:{YB2+ROW2+24}px;width:{W-2*M}px;height:20px;margin:0;font-size:14px;line-height:20px;color:{MUTED}">Detailed reference view; see the one-page view for presentation</p>'

# ---------- header ----------
chip_txt='Draft · analyst design · AI-reviewed, not practitioner-validated'
chip_w=int(len(chip_txt)*8.2)+40
header=(f'<header style="position:absolute;left:0;top:0;width:{W}px;height:160px;background:{NAVY}"></header>'
 f'<div style="position:absolute;left:0;top:160px;width:{W}px;height:6px;background:{TEAL}"></div>'
 f'<h1 style="position:absolute;left:{M}px;top:34px;width:1500px;height:56px;margin:0;font-family:Fraunces,Georgia,serif;font-weight:600;font-size:46px;line-height:56px;color:#FFFFFF">UK buy-side asset manager: functional architecture</h1>'
 f'<p style="position:absolute;left:{M}px;top:100px;width:1500px;height:28px;margin:0;font-size:19px;line-height:28px;color:#DDE5F0">One architecture for Active, Passive/ETF and Alternatives. Standards used as inputs, not as the structure.</p>'
 f'<p style="position:absolute;left:{W-M-chip_w}px;top:48px;width:{chip_w}px;height:36px;box-sizing:border-box;margin:0;padding:0 18px;border-radius:18px;background:#FFF1CF;color:#4A2F00;border:2px solid {AMBER};font-size:14px;line-height:32px;font-weight:700;text-align:center;white-space:nowrap">{chip_txt}</p>')

# ---------- data constant ----------
DATA={'comps':comp_name,'externals':{k:v['name'] for k,v in ext.items()},'links':[{k:l.get(k,'') for k in ('from','to','label','std','flow')} for l in d['links']],
      'standards':[{'name':s['name'],'used_for':s['used_for'],'verified':s['verified']} for s in std],
      'assumptions':d['assumptions']}
data_js=json.dumps(DATA,ensure_ascii=False,separators=(',',':'))
assert '</' not in data_js
script=("class Component extends DCLogic {\n  renderVals() {\n    const D = DATA;\n"
"    const nm = (id) => D.comps[id] || D.externals[id] || id;\n"
"    const flows = D.links.map((l, i) => ({ n: i + 1, flow: l.flow, from: nm(l.from), to: nm(l.to), label: l.label, std: l.std, hasStd: !!l.std, noStd: !l.std }));\n"
"    const mk = (s) => ({ name: s.name, usedFor: s.used_for, verified: !!s.verified, unverified: !s.verified });\n"
"    const half = Math.ceil(D.standards.length / 2);\n"
"    return {\n      flowsT: flows.filter((f) => f.flow === 'T'),\n      flowsF: flows.filter((f) => f.flow === 'F'),\n      flowsC: flows.filter((f) => f.flow === 'C'),\n      stdA: D.standards.slice(0, half).map(mk),\n      stdB: D.standards.slice(half).map(mk),\n"
"      assumptions: D.assumptions.map((t, i) => ({ n: i + 1, text: t }))\n    };\n  }\n}")
script="const DATA = "+data_js+";\n"+script

page=f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<title>UK buy-side asset manager functional architecture</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,700;1,400&amp;family=Fraunces:wght@600&amp;display=swap">
<style>
body{{margin:0}}
</style>
</helmet>
<div style="position:relative;width:{W}px;height:{H_TOTAL}px;background:#F4F6F9;font-family:{FONT};color:{INK}">
{header}
{chr(10).join(bands)}
{chr(10).join(cards)}
{chr(10).join(labels)}
{flows_html}
{legend_html}
{honesty_html}
{std_html}
{asm_html}
{footer}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{W},"height":{H_TOTAL}}}}}'>
{script}
</script>
</body>
</html>
'''
open(OUT,'w',encoding='utf-8').write(page)
NCOMP=sum(len(g['components']) for L in d['layers'] for g in L['groups'])
SUM_BOARD={"x":2480,"y":0,"w":1920,"h":1080,"title":"One-page client view"}
canvas={"v":3,"createdOnFiles":{"v":1,"at":"2026-11-01T12:00:00Z"},"title":"UK buy-side asset manager functional architecture","launch":{"view":"canvas"},"pages":[],"boards":{"Main.dc.html":{"x":0,"y":0,"w":W,"h":H_TOTAL,"title":f"Detailed view ({NCOMP} components)"},"Summary.dc.html":SUM_BOARD},"order":["Main.dc.html","Summary.dc.html"],"notes":{},"designSystems":[]}
open(CANVAS,'w').write(json.dumps(canvas,separators=(',',':')))
print('counts: layers',len(d['layers']),'groups',sum(len(L['groups']) for L in d['layers']),'comps',NCOMP,'externals',len(ext),'links',len(d['links']),'standards',len(std))
print('size',W,H_TOTAL,'stack bottom',STACK_BOTTOM,'row1',ROW1,'row2',ROW2,'strips',lb,rb)
