import json,os,sys
sys.path.insert(0,'/home/claude/sell-arch-canvas')
from common import *
KEYS=os.environ.get('KEYS','1')=='1'
HF=ROOT+'/heights.json'
HT=json.load(open(HF)) if os.path.exists(HF) else {}
def hh(k,est): return int(HT[k]) if k in HT else est
def dk(k): return f' data-k="{k}"' if KEYS else ''
OUT=ROOT+'/project/Main.dc.html'
d=spec
W=3200; M=48
STRIP_W=216; LX=M; RX=W-M-STRIP_W
SX0=LX+STRIP_W+16; SX1=RX-16
GAPC=8
COLW=(SX1-SX0-9*GAPC)//10
CGAP=GAPC
bands=[];cards=[];labels=[]
def chip(t): return (f'<span style="display:inline-block;font-size:12px;line-height:16px;font-weight:700;padding:1px 6px;border-radius:3px;color:#FFFFFF;background:{CHIPBG};margin-right:4px">{t}</span>')
def card_est(c,iw):
    h=16+nlines(c['name'],iw,13,True)*17+2+nlines(c['does'],iw,12)*16+4
    if [a for a in c['ac'] if a!='ALL']: h+=22
    role=role_line(c); h+=nlines(role,iw,12)*16+4
    for lab,k in XREF:
        if c[k]: h+=nlines(lab+' '+c[k],iw,12)*16
    return ev(h+4)
XREF=[('BIAN:','bian'),('FIX:','fix'),('FpML/CDM:','fpml_cdm'),('ISO 20022:','iso20022'),('MT:','swift_mt')]
def role_line(c):
    return f"{c['sor']} · CALM {c['calm']}"+(' · third party' if c['external'] else '')
def card_html(c,x,y,w,h):
    border='2px dashed #3A4556' if c['external'] else f'1px solid {LINE}'
    cs=[a for a in acs(c['ac'])]
    body=f'<b style="display:block;font-size:13px;line-height:17px;color:{INK}">{esc(c["name"])}</b>'
    body+=f'<span style="display:block;margin-top:2px;color:{INK}">{esc(c["does"])}</span>'
    if 'ALL' not in c['ac']:
        body+='<span style="display:block;margin-top:4px;line-height:20px"><span style="position:absolute;width:1px;height:1px;overflow:hidden;white-space:nowrap">Asset classes: </span>'+''.join(chip(a) for a in cs)+'</span>'
    body+=f'<span style="display:block;margin-top:4px;font-style:italic;color:{MUTED}">{esc(role_line(c))}</span>'
    for lab,k in XREF:
        if c[k]: body+=f'<span style="display:block;margin-top:1px;color:{MUTED}"><b style="color:{INK}">{lab}</b> {esc(c[k])}</span>'
    return f'<article{dk("c:"+c["id"])} style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;box-sizing:border-box;padding:8px 10px;background:#FFFFFF;border:{border};border-radius:6px;font-size:12px;line-height:16px;color:{INK}">{body}</article>'

Y0=200; CH=92
def hd(txt_cls): return ''
# ---- stage columns
vals_h=0
for s in d['stages']:
    vals_h=max(vals_h,hh('v:'+s['id'],ev(nlines(s['value'],COLW-20,12)*16+16)))
GY=Y0+CH+6+vals_h+12
stage_bottom=GY
for i,s in enumerate(d['stages']):
    x=SX0+i*(COLW+CGAP); fill,tc,tint,bd=OFFICE[s['office']]
    # chevron
    labels.append(f'<h2 aria-label="Stage {s["no"]}: {esc(s["name"])}, {OFFICE_LABEL[s["office"]]}" style="position:absolute;left:{x}px;top:{Y0}px;width:{COLW}px;height:{CH}px;box-sizing:border-box;margin:0;padding:10px 28px 10px 34px;display:flex;flex-direction:column;justify-content:center;background:{fill};color:{tc};clip-path:polygon(0 0,calc(100% - 22px) 0,100% 50%,calc(100% - 22px) 100%,0 100%,22px 50%)">'
      f'<span style="display:block;font-family:{FONT};font-size:12px;line-height:16px;font-weight:700">Stage {s["no"]} · {OFFICE_LABEL[s["office"]]}</span>'
      f'<span style="display:block;font-family:{SERIF};font-size:20px;line-height:24px;font-weight:600">{esc(s["name"])}</span></h2>')
    labels.append(f'<p{dk("v:"+s["id"])} style="position:absolute;left:{x}px;top:{Y0+CH+6}px;width:{COLW}px;height:{vals_h}px;box-sizing:border-box;margin:0;padding:6px 10px;background:{tint};border-radius:4px;font-size:12px;line-height:16px;color:{INK}">{esc(s["value"])}</p>')
    y=GY
    iw=COLW-16-20-2
    for g in s['groups']:
        gl=hh('g:'+g['id'],ev(nlines(g['name'],COLW-16,13,True)*17+6))
        ch=[(c,hh('c:'+c['id'],card_est(c,iw))) for c in g['components']]
        gh=8+gl+sum(h for _,h in ch)+6*(len(ch)-1)+8
        bands.append(f'<div style="position:absolute;left:{x}px;top:{y}px;width:{COLW}px;height:{gh}px;box-sizing:border-box;background:{tint};border:1px solid {bd};border-radius:6px"></div>')
        labels.append(f'<h3{dk("g:"+g["id"])} style="position:absolute;left:{x+8}px;top:{y+8}px;width:{COLW-16}px;height:{gl}px;margin:0;font-size:13px;line-height:17px;font-weight:700;color:{NAVY}">{esc(g["name"])}</h3>')
        cy=y+8+gl
        for c,h in ch:
            cards.append(card_html(c,x+8,cy,COLW-16,h)); cy+=h+6
        y+=gh+10
    stage_bottom=max(stage_bottom,y-10)
# ---- externals strips
SIDES=[('left',[('Clients',['X01','X15']),('Markets',['X02','X03','X18'])]),
       ('right',[('Infrastructure',['X04','X05','X07','X08','X09','X10','X16','X19']),('Service providers',['X06','X12','X13','X14','X17','X20']),('Regulators',['X11','X21'])])]
assert sorted(sum([i for _,gs in SIDES for _,i in gs],[]))==sorted(EXT)
sbot=0
for side,groups in SIDES:
    x=LX if side=='left' else RX
    y=GY
    hdr='Clients and markets' if side=='left' else 'Infrastructure, providers and regulators'
    labels.append(f'<h2 style="position:absolute;left:{x}px;top:{Y0}px;width:{STRIP_W}px;height:{CH}px;box-sizing:border-box;margin:0;padding:10px 0;display:flex;flex-direction:column;justify-content:center;font-family:{SERIF};font-size:20px;line-height:24px;font-weight:600;color:{NAVY}"><span style="display:block;font-family:{FONT};font-size:12px;line-height:16px;font-weight:700;color:{MUTED}">External parties</span>{hdr}</h2>')
    for gname,ids in groups:
        labels.append(f'<h3 style="position:absolute;left:{x}px;top:{y}px;width:{STRIP_W}px;height:18px;margin:0;font-size:13px;line-height:18px;font-weight:700;color:{NAVY}">{gname}</h3>'); y+=22
        for xid in ids:
            e=EXT[xid]; iw=STRIP_W-22
            h=hh('x:'+xid,ev(16+nlines(e['name'],iw,13,True)*17+4+nlines(e['role'],iw,12)*16+4))
            cards.append(f'<article{dk("x:"+xid)} style="position:absolute;left:{x}px;top:{y}px;width:{STRIP_W}px;height:{h}px;box-sizing:border-box;padding:8px 10px;background:#FFFFFF;border:1px solid #6B7A92;border-radius:6px;font-size:12px;line-height:16px;color:{INK}"><b style="display:block;font-size:13px;line-height:17px;margin-bottom:4px">{esc(e["name"])}</b><span style="display:block;color:{MUTED}">{esc(e["role"])}</span></article>')
            y+=h+8
        y+=6
    sbot=max(sbot,y-6)
stage_bottom=max(stage_bottom,sbot)
# ---- platform band
PY=stage_bottom+40
PADB=20
pg=d['platform']['groups']
NCOLS={'P1':1,'P2':1,'P3':2,'P4':1,'P5':2,'P6':1,'P7':3}
PGAP=10; GPAD=8
availw=W-2*M-2*PADB
ncol=sum(NCOLS[g['id']] for g in pg)
CARDW=(availw-PGAP*(len(pg)-1)-sum(2*GPAD+(NCOLS[g['id']]-1)*GPAD for g in pg))//ncol
PHEAD=hh('phead',64)
pfill,ptc,ptint,pbd=OFFICE['Cross-cutting']
labels.append(f'<div{dk("phead")} style="position:absolute;left:{M+PADB}px;top:{PY+14}px;width:{W-2*M-2*PADB}px;height:{PHEAD}px;margin:0"><h2 style="margin:0;font-family:{SERIF};font-size:24px;line-height:30px;font-weight:600;color:{NAVY}">{esc(d["platform"]["name"])}</h2><p style="margin:2px 0 0;font-size:13px;line-height:18px;color:{MUTED}">Shared services used by every stage: reference data, risk and limits, collateral, liquidity and cash, data and analytics, integration and messaging, conduct, surveillance and reporting oversight, and controls and resilience.</p></div>')
px=M+PADB; py0=PY+14+PHEAD+10
pcards=[];pmax=0
for g in pg:
    nc=NCOLS[g['id']]; gw=2*GPAD+nc*CARDW+(nc-1)*GPAD
    gl=hh('g:'+g['id'],ev(nlines(g['name'],gw-16,13,True)*17+6))
    comps=g['components']; per=-(-len(comps)//nc)
    colsx=[]; hmax=0
    for k in range(nc):
        part=comps[k*per:(k+1)*per]
        hs=[(c,hh('c:'+c['id'],card_est(c,CARDW-22))) for c in part]
        colsx.append(hs); hmax=max(hmax,sum(h for _,h in hs)+6*(len(hs)-1))
    gh=GPAD+gl+hmax+GPAD
    pcards.append((g,px,gw,gl,colsx,gh)); pmax=max(pmax,gh); px+=gw+PGAP
for g,gx,gw,gl,colsx,_ in pcards:
    bands.append(f'<div style="position:absolute;left:{gx}px;top:{py0}px;width:{gw}px;height:{pmax}px;box-sizing:border-box;background:#FFFFFF;border:1px solid {pbd};border-radius:6px"></div>')
    labels.append(f'<h3{dk("g:"+g["id"])} style="position:absolute;left:{gx+GPAD}px;top:{py0+GPAD}px;width:{gw-2*GPAD}px;height:{gl}px;margin:0;font-size:13px;line-height:17px;font-weight:700;color:{NAVY}">{esc(g["name"])}</h3>')
    for k,hs in enumerate(colsx):
        cy=py0+GPAD+gl
        for c,h in hs:
            cards.append(card_html(c,gx+GPAD+k*(CARDW+GPAD),cy,CARDW,h)); cy+=h+6
PBOT=py0+pmax+PADB
bands.insert(0,f'<div style="position:absolute;left:{M}px;top:{PY}px;width:{W-2*M}px;height:{PBOT-PY}px;box-sizing:border-box;background:{ptint};border:2px solid {pbd};border-radius:8px"></div>')

# ---- panels
PSTYLE=f'position:absolute;box-sizing:border-box;padding:20px;background:#FFFFFF;border:1px solid #B7C1D0;border-radius:8px;font-size:13px;line-height:18px;color:{INK};'
def h2s(t,i): return f'<h2 id="{i}" style="margin:0 0 6px;font-family:{SERIF};font-weight:600;font-size:22px;line-height:28px;color:{NAVY}">{esc(t)}</h2>'
def note(t): return f'<p style="margin:0 0 10px;font-size:13px;line-height:18px;color:{MUTED}">{esc(t)}</p>'
def h3s(t): return f'<h3 style="margin:14px 0 4px;font-size:14px;line-height:20px;font-weight:700;color:{NAVY}">{esc(t)}</h3>'
YA=PBOT+40
FW=1260; MW=W-2*M-FW-32
# flows
fc=(30,420,260,FW-42-30-420-260-36)
THREADS=[('Flow trade','Trade flow'),('Flow margin and collateral','Margin and collateral flow'),('Flow reporting','Reporting flow')]
assert set(l['thread'] for l in d['links'])==set(t for t,_ in THREADS)
def flowlist(name):
    g=' '.join(f'{c}px' for c in fc)
    return ('<ol style="list-style:none;margin:0;padding:0">'
     f'<sc-for list="{{{{{name}}}}}" as="f" hint-placeholder-count="3">'
     f'<li style="display:grid;grid-template-columns:{g};column-gap:12px;padding:6px 0;border-bottom:1px solid #E1E6EE;font-size:13px;line-height:18px;color:{INK}">'
     f'<span style="font-weight:700;color:{NAVY}">{{{{f.n}}}}</span>'
     '<span><b>{{f.from}}</b> to <b>{{f.to}}</b></span><span>{{f.label}}</span>'
     f'<span style="font-size:12px;line-height:16px;color:{MUTED}">'
     '<sc-if value="{{f.hasStd}}" hint-placeholder-val="{{true}}">{{f.std}}</sc-if>'
     '<sc-if value="{{f.noStd}}" hint-placeholder-val="{{false}}"><i>no standard named</i></sc-if></span></li></sc-for></ol>')
fh=f'<div aria-hidden="true" style="display:grid;grid-template-columns:{" ".join(f"{c}px" for c in fc)};column-gap:12px;padding:4px 0;font-size:12px;line-height:18px;font-weight:700;color:{NAVY};border-bottom:2px solid {NAVY}"><span>No.</span><span>From and to</span><span>What moves</span><span>Standard</span></div>'
flows_html=(f'<section{dk("p:flows")} style="{PSTYLE}left:{M}px;top:{YA}px;width:{FW}px;height:{{H}}px" aria-labelledby="flows-h">'
 +h2s('Key flows','flows-h')+note('Illustrative only: a selection of representative flows between components and external parties, not the integration estate. The diagram has no connector arrows by design; read these rows instead. Three headings follow the three threads of the links.')
 +fh+''.join(h3s(t)+flowlist('fl'+str(i)) for i,(_,t) in enumerate(THREADS))+'</section>')
# matrix
FAM=[('BIAN','BIAN','BIAN'),('CALM','CALM','CALM'),('FIX','FIX','FIX'),('FpML_CDM','FpML / CDM','FpML_CDM'),('ISO20022','ISO 20022','ISO20022'),('SWIFT_MT','Swift MT','SWIFT_MT'),('other','Regulation and other','regs')]
mc=[150]+[(MW-40-150-7*10-0)//7]*7
mg=' '.join(f'{c}px' for c in mc)
xm=d['xref_matrix']; cov=xm['coverage']
stage_n={s['id']:len(comps_of(s)) for s in d['stages']}; stage_n['PLATFORM']=len(comps_of(d['platform']))
STG={s['id']:s for s in d['stages']}; STG['PLATFORM']=d['platform']
# consistency check of counts vs component fields
fieldmap={'BIAN':'bian','FIX':'fix','FpML_CDM':'fpml_cdm','ISO20022':'iso20022','SWIFT_MT':'swift_mt'}
for r in xm['stages']:
    s=STG[r['stage']]
    for fk,f in fieldmap.items():
        n=sum(1 for c in comps_of(s) if c[f])
        if n!=r['counts'][fk]: print('NOTE count mismatch',r['stage'],fk,'matrix',r['counts'][fk],'fields',n)
    n=sum(1 for c in comps_of(s) if c['regs'])
    if n!=r['counts']['regs']: print('NOTE regs mismatch',r['stage'],'matrix',r['counts']['regs'],'fields',n)
mrows=[]
for r in xm['stages']:
    row={'stage':(r['name'] if r['stage']=='PLATFORM' else f"{r['stage']} {r['name']}")}
    for key,lab,ck in FAM:
        cnt=stage_n[r['stage']] if key=='CALM' else r['counts'][ck]
        row[key+'N']=f"{cnt} of {stage_n[r['stage']]}"; row[key+'T']=r['families'][key]
    mrows.append(row)
covcells=[]
for key,lab,ck in FAM:
    cv=cov[ck]
    covcells.append({'lab':lab,'n':f"{cv['matched']} of {cov['total_components']}",'ver':cv.get('verified',None),'note':cv.get('note','')})
def cell(k):
    return f'<span><b>{{{{r.{k}N}}}}</b><br>{{{{r.{k}T}}}}</span>'
mhead=''.join(f'<span>{lab}</span>' for _,lab,_ in FAM)
mat=(f'<section{dk("p:matrix")} style="{PSTYLE}left:{M+FW+32}px;top:{YA}px;width:{MW}px;height:{{H}}px" aria-labelledby="mat-h">'
 +h2s('Standards cross-reference matrix','mat-h')
 +note('Stages as rows, standards families as columns. Each cell gives the number of the stage\'s components carrying a reference in that family, then what the references are. Blank references are left blank where no honest match exists.')
 +f'<div aria-hidden="true" style="display:grid;grid-template-columns:{mg};column-gap:10px;padding:4px 0;font-size:12px;line-height:18px;font-weight:700;color:{NAVY};border-bottom:2px solid {NAVY}"><span>Stage</span>{mhead}</div>'
 +'<ol style="list-style:none;margin:0;padding:0"><sc-for list="{{matrix}}" as="r" hint-placeholder-count="3">'
 +f'<li style="display:grid;grid-template-columns:{mg};column-gap:10px;padding:6px 0;border-bottom:1px solid #E1E6EE;font-size:12px;line-height:16px;color:{INK}"><b style="font-size:13px;line-height:18px;color:{NAVY}">{{{{r.stage}}}}</b>'
 +''.join(cell(k) for k,_,_ in FAM)+'</li></sc-for></ol>'
 +h3s('Coverage summary: components carrying a reference, of all components')
 +f'<ul style="list-style:none;margin:0;padding:0;display:grid;grid-template-columns:{mg};column-gap:10px;font-size:12px;line-height:16px"><li style="font-weight:700;color:{NAVY}">All stages</li>'
 +'<sc-for list="{{coverage}}" as="v" hint-placeholder-count="7"><li><b style="font-size:13px;line-height:18px;color:'+NAVY+'">{{v.n}}</b><br>'
 +'<sc-if value="{{v.isVerified}}" hint-placeholder-val="{{true}}"><span style="display:inline-block;margin:2px 0;padding:0 6px;border-radius:3px;background:'+NAVY+';color:#FFFFFF;font-weight:700">Verified</span><br></sc-if>'
 +'<sc-if value="{{v.isUnverified}}" hint-placeholder-val="{{false}}"><span style="display:inline-block;margin:2px 0;padding:0 5px;border-radius:3px;border:2px solid '+AMBER+';color:#6B4200;font-weight:700">Not verified</span><br></sc-if>'
 +'{{v.note}}</li></sc-for></ul>'
 +h3s('Gaps: where no standard fits')
 +'<ul style="margin:0;padding:0 0 0 20px;font-size:13px;line-height:18px;column-count:2;column-gap:32px"><sc-for list="{{gaps}}" as="g" hint-placeholder-count="4"><li style="margin:0 0 4px">{{g.text}}</li></sc-for></ul></section>')
# row B
YB=YA+40  # placeholder, fixed below
# standards
std=d['standards']; half=(len(std)+1)//2
SW2=1480; LW=720; HW=W-2*M-SW2-LW-64
sci=SW2-40; colw2=(sci-2-32)//2
def stdcol(name):
    return ('<ul style="list-style:none;margin:0;padding:0">'
     f'<sc-for list="{{{{{name}}}}}" as="s" hint-placeholder-count="3">'
     f'<li style="display:flex;gap:12px;align-items:flex-start;padding:7px 0;border-bottom:1px solid #E1E6EE;font-size:12px;line-height:16px;color:{INK}">'
     '<span style="flex:0 0 96px;width:96px">'
     f'<sc-if value="{{{{s.verified}}}}" hint-placeholder-val="{{{{true}}}}"><span style="display:block;box-sizing:border-box;width:96px;text-align:center;padding:2px 0;background:{NAVY};color:#FFFFFF;border:2px solid {NAVY};border-radius:4px;font-size:12px;line-height:16px;font-weight:700">Verified</span></sc-if>'
     f'<sc-if value="{{{{s.unverified}}}}" hint-placeholder-val="{{{{false}}}}"><span style="display:block;box-sizing:border-box;width:96px;text-align:center;padding:2px 0;background:#FFFFFF;color:#6B4200;border:2px solid {AMBER};border-radius:4px;font-size:12px;line-height:16px;font-weight:700">Not verified</span></sc-if></span>'
     '<span style="flex:1 1 auto"><b style="display:block;font-size:13px;line-height:18px">{{s.name}}</b>{{s.usedFor}}</span></li></sc-for></ul>')
nunv=sum(1 for s in std if not s['verified'])
std_html=(f'<section{dk("p:std")} style="{PSTYLE}left:{M}px;top:{{Y}}px;width:{SW2}px;height:{{H}}px" aria-labelledby="std-h">'
 +h2s('Standards used as inputs','std-h')
 +note(f'{len(std)} entries, {len(std)-nunv} verified and {nunv} not verified. Each informed a component name, an identifier, a message or a report; none defines the structure. Verified means a cited source was read; not verified means not checked against the source for this draft and to be validated before external use.')
 +f'<div style="display:grid;grid-template-columns:{colw2}px {colw2}px;column-gap:32px">'+stdcol('stdA')+stdcol('stdB')+'</div></section>')
# legend
LI=LW-40
def lrow(sample,sw,text):
    return f'<li style="display:flex;gap:12px;align-items:flex-start;padding:3px 0;font-size:13px;line-height:18px;color:{INK}"><span style="flex:0 0 {sw}px;width:{sw}px">{sample}</span><span>{esc(text)}</span></li>'
def sec(title,rows): return h3s(title)+'<ul style="list-style:none;margin:0;padding:0">'+''.join(rows)+'</ul>'
def osw(o):
    f,t,ti,b=OFFICE[o]
    return f'<span style="display:block;width:112px;height:26px;box-sizing:border-box;padding:3px 6px;background:{f};color:{t};border:1px solid {b};border-radius:4px;font-size:12px;line-height:18px;font-weight:700;text-align:center">{o}</span>'
OFFDESC={'Front':'Revenue-generating client and trading activity: stages 1, 2 and 8',
 'Middle':'Onboarding, confirmation, and independent risk and reporting: stages 0, 3 and 4',
 'Back':'Operations that move securities, cash and margin: stages 5, 6 and 7',
 'Cross-cutting':'Market data (stage 9) and the platform, which serve every stage'}
roles=[('system of record','holds the authoritative copy of its data'),('engagement','where clients, traders or staff interact with the bank'),('calculation','derives values, risk or analytics'),('data','supplies or stores reference and market data'),('integration','moves and translates data between systems'),('control','enforces limits, rules, checks and oversight')]
calm=[('actor','a person or role'),('ecosystem','a wider set of parties and systems'),('system','a deployable application or platform'),('service','a capability offered through an interface'),('database','a store of records'),('network','a network or messaging fabric'),('ldap','a directory used for identity'),('webclient','a browser or app front end'),('data-asset','a managed dataset')]
used_calm={c['calm'] for c in ALLC.values()}; assert used_calm<={a for a,_ in calm},used_calm
dash='<span style="display:block;width:96px;height:26px;box-sizing:border-box;padding:3px 6px;background:#FFFFFF;border:2px dashed #3A4556;border-radius:6px;font-size:12px;line-height:18px;text-align:center">third party</span>'
solid=f'<span style="display:block;width:96px;height:26px;box-sizing:border-box;padding:3px 6px;background:#FFFFFF;border:1px solid {LINE};border-radius:6px;font-size:12px;line-height:18px;text-align:center">solid</span>'
legend_html=(f'<section{dk("p:legend")} style="{PSTYLE}left:{M+SW2+32}px;top:{{Y}}px;width:{LW}px;height:{{H}}px" aria-labelledby="leg-h">'
 +h2s('Legend','leg-h')+note('How to read the cards. CALM terms are vocabulary only.')
 +sec('Office, shown on stage chevrons',[lrow(osw(o),112,OFFDESC[o]) for o in OFFICE])
 +sec('Asset classes',[lrow(''.join(chip(a) for a in ['EQ','FI']),96,'EQ equities, FI fixed income (rates and credit), FX foreign exchange, DR derivatives (OTC and listed). A chip means the component is specific to those classes.'),
    lrow('<span style="display:block;width:96px;font-size:12px;line-height:18px;font-weight:700">No chip</span>',96,'No chip means the component applies to all four asset classes (ALL).')])
 +sec('Card edge',[lrow(solid,96,'Solid edge: the bank runs it'),lrow(dash,96,'Dashed edge and the words third party: usually run by a third party; the bank keeps oversight')])
 +sec('Cross-reference lines on cards',[lrow('<b>BIAN:</b>',96,'closest-fit service domain label'),lrow('<b>FIX:</b>',96,'FIX message types'),lrow('<b>FpML/CDM:</b>',96,'FpML or CDM model family'),lrow('<b>ISO 20022:</b>',96,'business area codes only'),lrow('<b>MT:</b>',96,'Swift MT numbers, unverified'),lrow('<i>role line</i>',96,'role, then the CALM node type, for example system of record · CALM database')])
 +sec('Role, as the first word of the role line',[lrow(f'<b>{esc(a)}</b>',96,b) for a,b in roles])
 +sec('CALM 1.1 node types (glosses are the analyst\'s)',[lrow(f'<b>{esc(a)}</b>',96,b) for a,b in calm])+'</section>')
# honesty
verified_regs=[s['name'] for s in std if not s['verified']]
lims=[
 'CALM is vocabulary only. Every component carries a CALM 1.1 node type as a label, but this is not a CALM document: no relationships, flows or controls are modelled.',
 'BIAN names are closest-fit labels, checked against the version 10 service landscape only. BIAN is oriented to banks and has no lifecycle view of capital markets, so the structure is the analyst\'s own. A card with no BIAN line had no matching domain. Later releases may rename domains.',
 'ISO 20022 is shown at business area level only (for example secl, sese, colr, auth). Message identifiers were not checked, and sell-side use of setr and fxtr was not checked.',
 'Swift MT numbers are analyst knowledge and are not verified. Verified: the coexistence of ISO 15022 and ISO 20022 for securities (MT to ISO 20022 is coexistence, not a forced cut-over), and the end of MT/MX coexistence for cross-border payments on 22 November 2025 (MT103/202 retired).',
 f'{nunv} of {len(std)} standards entries are marked not verified. They were not checked against the source for this draft and should be validated before external use. They include UK MiFIR, best execution, pre- and post-trade transparency, EMIR risk-mitigation and clearing duties, CFTC Part 43, SEC SBSR, UMR phase-in and CCP margin models, CASS and 15c3-3, Reg SHO, 15c3-5 and RTS 6, KYC and AML, MiFID categorisation and suitability, ISDA, GMRA and GMSLA, LEI, ISIN, CFI and FIGI, FRTB, SA-CCR and BCBS 239, ISDA DRR, US broker-dealer regimes, MiFID II recording of communications, UK MAR Articles 11 and 18, and the Swift MT numbers. Mapping to components is indicative, not legal or regulatory advice.',
 'FIX names were checked against a third-party FIX Latest dictionary. CDM was checked at model level, not function level. FpML and CDM references are family level.',
 'The key flows are illustrative; the real integration estate is far denser and most components also read from the platform.',
 'This is an archetype, not a client estate. Office assignment is a convention and banks differ. Status: AI-reviewed, not practitioner-validated. It has no vendor names, no statistics and no agentic AI layer.']
asm=d['assumptions']
HI=HW-40
lis=''.join(f'<li style="margin:0 0 8px;font-size:13px;line-height:18px;color:{INK}">{esc(t)}</li>' for t in lims)
alis=''.join(f'<li style="margin:0 0 6px;font-size:13px;line-height:18px;color:{INK}">{esc(t)}</li>' for t in asm)
hon_html=(f'<section{dk("p:hon")} style="{PSTYLE}left:{M+SW2+LW+64}px;top:{{Y}}px;width:{HW}px;height:{{H}}px;background:#FFF6E3;border-color:{AMBER}" aria-labelledby="hon-h">'
 +h2s('Limitations and assumptions','hon-h')+note('What this diagram does not establish, and the choices made to draw one archetype.')
 +h3s('Limitations')+f'<ul style="margin:0;padding:0 0 0 20px">{lis}</ul>'+h3s('Assumptions')+f'<ol style="margin:0;padding:0 0 0 22px">{alis}</ol></section>')
# row heights
def est_panel(k,e): return hh(k,e)
HA=max(hh('p:flows',2300),hh('p:matrix',2300))
flows_html=flows_html.replace('{H}',str(HA)); mat=mat.replace('{H}',str(HA))
YB=YA+HA+32
HB=max(hh('p:std',1500),hh('p:legend',1500),hh('p:hon',1500))
parts=[]
for h in (std_html,legend_html,hon_html): parts.append(h.replace('{H}',str(HB)).replace('{Y}',str(YB)))
std_html,legend_html,hon_html=parts
H_TOTAL=YB+HB+64
footer=f'<p style="position:absolute;left:{M}px;top:{YB+HB+24}px;width:{W-2*M}px;height:20px;margin:0;font-size:14px;line-height:20px;color:{MUTED}">Detailed reference view; see the one-page view for presentation.</p>'
# ---- header
chip_txt='Illustrative archetype · AI-reviewed, not practitioner-validated · Nov 2026'
chip_w=int(len(chip_txt)*8.2)+44
header=(f'<header style="position:absolute;left:0;top:0;width:{W}px;height:160px;background:{NAVY}"></header>'
 f'<div style="position:absolute;left:0;top:160px;width:{W}px;height:6px;background:{TEAL}"></div>'
 f'<h1 style="position:absolute;left:{M}px;top:34px;width:2200px;height:56px;margin:0;font-family:{SERIF};font-weight:600;font-size:46px;line-height:56px;color:#FFFFFF">Sell-side global markets: functional architecture along the trade lifecycle</h1>'
 f'<p style="position:absolute;left:{M}px;top:100px;width:2200px;height:28px;margin:0;font-size:19px;line-height:28px;color:#DDE5F0">Ten lifecycle stages from onboarding to market data, left to right, over one cross-cutting platform. Standards are inputs, not the structure.</p>'
 f'<p style="position:absolute;left:{W-M-chip_w}px;top:48px;width:{chip_w}px;height:36px;box-sizing:border-box;margin:0;padding:0 18px;border-radius:18px;background:#FFF1CF;color:#4A2F00;border:2px solid {AMBER};font-size:14px;line-height:32px;font-weight:700;text-align:center;white-space:nowrap">{chip_txt}</p>')
# data
links=[{'from':name_of(l['from']),'to':name_of(l['to']),'label':l['label'],'std':l['std'],'thread':l['thread']} for l in d['links']]
DATA={'links':links,'standards':[{'name':s['name'],'used_for':s['used_for'],'verified':s['verified']} for s in std],
      'matrix':mrows,'coverage':covcells,'gaps':cov['gaps']}
data_js=json.dumps(DATA,ensure_ascii=False,separators=(',',':')); assert '</' not in data_js
script=("const DATA = "+data_js+";\n"
"class Component extends DCLogic {\n  renderVals() {\n    const D = DATA;\n"
"    const flows = D.links.map((l, i) => ({ n: i + 1, thread: l.thread, from: l.from, to: l.to, label: l.label, std: l.std, hasStd: !!l.std, noStd: !l.std }));\n"
"    const mk = (s) => ({ name: s.name, usedFor: s.used_for, verified: !!s.verified, unverified: !s.verified });\n"
"    const half = Math.ceil(D.standards.length / 2);\n"
"    return {\n"
"      fl0: flows.filter((f) => f.thread === 'Flow trade'),\n      fl1: flows.filter((f) => f.thread === 'Flow margin and collateral'),\n      fl2: flows.filter((f) => f.thread === 'Flow reporting'),\n"
"      stdA: D.standards.slice(0, half).map(mk),\n      stdB: D.standards.slice(half).map(mk),\n"
"      matrix: D.matrix,\n      coverage: D.coverage.map((v) => ({ n: v.n, note: v.note, isVerified: v.ver === true, isUnverified: v.ver === false })),\n"
"      gaps: D.gaps.map((t) => ({ text: t }))\n    };\n  }\n}")
page=f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<title>Sell-side markets functional architecture, detailed view</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
{FONTLINK}
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
{mat}
{std_html}
{legend_html}
{hon_html}
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
NC=len(ALLC)
json.dump({'w':W,'h':H_TOTAL,'n':NC},open(ROOT+'/main_size.json','w'))
print('Main',W,H_TOTAL,'comps',NC,'stage_bottom',stage_bottom,'PBOT',PBOT,'rowA',HA,'rowB',HB,'colw',COLW,'cardw platform',CARDW)
