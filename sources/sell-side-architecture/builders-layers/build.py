import json,os,sys
sys.path.insert(0,'/home/claude/sell-func-canvas')
from common import *
KEYS=os.environ.get('KEYS','1')=='1'
HF=ROOT+'/heights.json'
HT=json.load(open(HF)) if os.path.exists(HF) else {}
def hh(k,est): return int(HT[k]) if k in HT else est
def dk(k): return f' data-k="{k}"' if KEYS else ''
OUT=ROOT+'/project/Main.dc.html'
d=spec
W=3040; M=48
BARX=M; BARW=64; LBLX=BARX+BARW+8; LBLW=280; SX0=LBLX+LBLW+8; SX1=W-M
NS=8; SG=10; SLOT=(SX1-SX0-(NS-1)*SG)//NS
GPAD=8; ROWPAD=8; CG=6
bg=[];cards=[];labels=[]
def chip(t): return (f'<span style="display:inline-block;font-size:12px;line-height:16px;font-weight:700;padding:1px 6px;border-radius:3px;color:#FFFFFF;background:{CHIPBG};margin-right:4px">{t}</span>')
def schip(t): return (f'<span style="display:inline-block;font-size:12px;line-height:16px;font-weight:700;padding:0 5px;border-radius:3px;color:{NAVY};background:#FFFFFF;border:1px solid {NAVY};margin-right:4px">{t}</span>')
XREF=[('BIAN:','bian'),('FIX:','fix'),('FpML/CDM:','fpml_cdm'),('ISO 20022:','iso20022'),('MT:','swift_mt')]
def role_line(c): return f"{c['sor']} · CALM {c['calm']}"+(' · third party' if c['external'] else '')
def card_est(c,iw):
    h=16+nlines(c['name'],iw,13,True)*17+2+nlines(c['does'],iw,12)*16+4
    if [a for a in c['ac'] if a!='ALL']: h+=22
    h+=nlines(role_line(c),iw,12)*16+4
    for lab,k in XREF:
        if c[k]: h+=nlines(lab+' '+c[k],iw,12)*16
    return ev(h+4)
def card_html(c,x,y,w,h,tint):
    border='2px dashed #3A4556' if c['external'] else f'1px solid {LINE}'
    body=f'<b style="display:block;font-size:13px;line-height:17px;color:{INK}">{esc(c["name"])}</b>'
    body+=f'<span style="display:block;margin-top:2px;color:{INK}">{esc(c["does"])}</span>'
    if 'ALL' not in c['ac']:
        body+='<span style="display:block;margin-top:4px;line-height:20px"><span style="position:absolute;width:1px;height:1px;overflow:hidden;white-space:nowrap">Asset classes: </span>'+''.join(chip(a) for a in acs(c['ac']))+'</span>'
    body+=f'<span style="display:block;margin-top:4px;font-style:italic;color:{MUTED}">{esc(role_line(c))}</span>'
    for lab,k in XREF:
        if c[k]: body+=f'<span style="display:block;margin-top:1px;color:{MUTED}"><b style="color:{INK}">{lab}</b> {esc(c[k])}</span>'
    return f'<article{dk("c:"+c["id"])} style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;box-sizing:border-box;padding:8px 10px;background:#FFFFFF;border:{border};border-radius:6px;font-size:12px;line-height:16px;color:{INK}">{body}</article>'

# ---------------- header
HDR=168
chip_txt='Illustrative archetype · components AI-reviewed · layering not yet reviewed · Nov 2026'
chip_w=int(len(chip_txt)*8.2)+44
header=(f'<header style="position:absolute;left:0;top:0;width:{W}px;height:{HDR}px;background:{NAVY}"></header>'
 f'<div style="position:absolute;left:0;top:{HDR}px;width:{W}px;height:6px;background:{TEAL}"></div>'
 f'<h1 style="position:absolute;left:{M}px;top:32px;width:2100px;height:58px;margin:0;font-family:{SERIF};font-weight:600;font-size:46px;line-height:58px;color:#FFFFFF">Sell-side global markets: functional architecture from pre-trade to post-trade</h1>'
 f'<p style="position:absolute;left:{M}px;top:100px;width:2300px;height:52px;margin:0;font-size:19px;line-height:26px;color:#DDE5F0">Eight horizontal layers in five bands: lifecycle layers from pre-trade to post-trade, cross-lifecycle services that act on positions at several points, and common services that serve every layer above. Standards are inputs, not the structure.</p>'
 f'<p style="position:absolute;left:{W-M-chip_w}px;top:44px;width:{chip_w}px;height:36px;box-sizing:border-box;margin:0;padding:0 18px;border-radius:18px;background:#FFF1CF;color:#4A2F00;border:2px solid {AMBER};font-size:14px;line-height:32px;font-weight:700;text-align:center;white-space:nowrap">{chip_txt}</p>')
Y0=HDR+6+44
labels.append(f'<p style="position:absolute;left:{LBLX}px;top:{HDR+6+12}px;width:{W-LBLX-M}px;height:22px;margin:0;font-size:14px;line-height:22px;font-weight:700;color:{NAVY}">Reads top to bottom, pre-trade to post-trade. Layers L6 and L7 act across the lifecycle; common services (L8) serve every layer above. No connectors are drawn: see the key flows below.</p>')

# ---------------- layers
bandspan={}   # band -> (y0,y1)
y=Y0
def span_of(g): return 1 if len(g['components'])<=3 else 2
def gw_of(s): return s*SLOT+(s-1)*SG
prev_band=None
STRIP_TAB=30
for L in LAYERS:
    b=L['band']
    if prev_band is not None:
        y+= 44 if b=='B5' else (18 if b!=prev_band else 6)
    if b=='B5':
        labels.append(f'<div style="position:absolute;left:{M}px;top:{y}px;width:{W-2*M}px;height:{STRIP_TAB}px;box-sizing:border-box;padding:0 {BARW+16}px;background:{NAVY};color:#FFFFFF;font-size:14px;line-height:30px;font-weight:700">Common services: serves every layer above (L1 to L7). Market data and reference data are here, not at the end of the trade.</div>')
        bandspan.setdefault(b,[y,0]); ystrip=y; y+=STRIP_TAB
    bandspan.setdefault(b,[y,0])
    fill,tc,tint,bd=BAND[b]
    # measure groups
    gs=[]
    spans={g['id']:span_of(g) for g in L['groups']}
    while sum(spans.values())<NS:
        cand=[g for g in L['groups'] if spans[g["id"]]<min(4,len(g['components']))]
        if not cand: break
        gbest=max(cand,key=lambda g:(-(-len(g['components'])//spans[g['id']]),len(g['components'])))
        spans[gbest['id']]+=1
    for g in L['groups']:
        s=spans[g['id']]; gw=gw_of(s); nc=s
        iw=(gw-2*GPAD-(nc-1)*8)//nc
        gl=hh('g:'+g['id'],ev(nlines(g['name'],gw-2*GPAD,14,True)*18+22))
        comps=g['components']; per=-(-len(comps)//nc)
        cols=[]; hmax=0
        for k in range(nc):
            part=comps[k*per:(k+1)*per]
            hs=[(c,hh('c:'+c['id'],card_est(c,iw-22))) for c in part]
            cols.append(hs); hmax=max(hmax,sum(h for _,h in hs)+CG*(len(hs)-1))
        gs.append((g,s,gw,gl,cols,iw,GPAD+gl+6+hmax+GPAD))
    # label cell
    serves=L.get('serves')
    def sv(l):
        if l['id']=='L8': return 'Serves every layer above, L1 to L7'
        s=l['serves']; return 'Serves '+(', '.join(s[:-1])+' and '+s[-1] if len(s)>1 else s[0])+(', and the lifecycle layers they touch' if False else '')
    stg=' '.join(schip(s) for s in sorted(L['stages']))
    lab_est=ev(16+25*nlines(L['name'],LBLW-24,20,True)+18*nlines(L['purpose'],LBLW-24,13)+60)
    lh=hh('l:'+L['id'],lab_est)
    rowh=ROWPAD*2+max(max(x[6] for x in gs),lh)
    # row background
    bg.append(f'<div style="position:absolute;left:{LBLX}px;top:{y}px;width:{W-M-LBLX}px;height:{rowh}px;box-sizing:border-box;background:{tint};border:1px solid {bd};border-radius:8px"></div>')
    lblbody=(f'<span style="display:block;font-size:12px;line-height:16px;font-weight:700;color:{MUTED}">Layer {L["id"][1:]} · {OFFICE_LABEL[L["office"]]}</span>'
      f'<h2 style="margin:2px 0 4px;font-family:{SERIF};font-weight:600;font-size:20px;line-height:25px;color:{NAVY}">{esc(L["name"])}</h2>'
      f'<p style="margin:0 0 4px;font-size:13px;line-height:18px;color:{INK}">{esc(L["purpose"])}</p>'
      f'<p style="margin:0;font-size:12px;line-height:20px;color:{MUTED}"><span style="position:absolute;width:1px;height:1px;overflow:hidden;white-space:nowrap">Stage in the lifecycle presentation: </span>{stg}</p>')
    if L['id'] in ('L6','L7','L8'):
        lblbody+=f'<p style="margin:2px 0 0;font-size:12px;line-height:16px;font-weight:700;color:{NAVY}">{esc(sv(L))}</p>'
    labels.append(f'<div{dk("l:"+L["id"])} style="position:absolute;left:{LBLX}px;top:{y+ROWPAD}px;width:{LBLW}px;height:{lh}px;box-sizing:border-box;padding:4px 12px;color:{INK}">{lblbody}</div>')
    gh=rowh-2*ROWPAD
    gx=SX0
    for (g,s,gw,gl,cols,iw,_h) in gs:
        bg.append(f'<div style="position:absolute;left:{gx}px;top:{y+ROWPAD}px;width:{gw}px;height:{gh}px;box-sizing:border-box;background:#FFFFFF;border:2px solid {bd};border-radius:6px"></div>')
        gstg=' '.join(schip(t) for t in g['stages'])
        labels.append(f'<div{dk("g:"+g["id"])} style="position:absolute;left:{gx+GPAD}px;top:{y+ROWPAD+GPAD-2}px;width:{gw-2*GPAD}px;height:{gl}px;box-sizing:border-box;color:{NAVY}"><h3 style="margin:0;font-size:14px;line-height:18px;font-weight:700;color:{NAVY}">{esc(g["name"])}</h3>'
          f'<p style="margin:2px 0 0;font-size:12px;line-height:20px;color:{MUTED}"><span style="position:absolute;width:1px;height:1px;overflow:hidden;white-space:nowrap">Stage in the lifecycle presentation: </span>{gstg} {esc(OFFICE_LABEL[g["office"]])}</p></div>')
        for k,hs in enumerate(cols):
            cy=y+ROWPAD+GPAD+gl+6
            for c,h in hs:
                cards.append(card_html(c,gx+GPAD+k*(iw+8),cy,iw,h,tint)); cy+=h+CG
        gx+=gw+SG
    bandspan[b][1]=y+rowh
    y+=rowh; prev_band=b
STACK_BOT=y
# band bars
reads={b['id']:b for b in BANDS}
for bid,(a,z) in bandspan.items():
    fill,tc,tint,bd=BAND[bid]
    nm=reads[bid]['name']
    labels.append(f'<h2 aria-label="Band: {esc(nm)}. {esc(reads[bid]["reads"])}" style="position:absolute;left:{BARX}px;top:{a}px;width:{BARW}px;height:{z-a}px;box-sizing:border-box;margin:0;padding:10px 0;display:flex;align-items:center;justify-content:center;text-align:center;writing-mode:vertical-rl;transform:rotate(180deg);background:{fill};color:{tc};border-radius:8px;font-family:{SERIF};font-weight:600;font-size:22px;line-height:28px;letter-spacing:.2px">{esc(nm)}</h2>')
# reading arrow (placed shape) beside bands B1..B3
ay0=bandspan['B1'][0]; ay1=bandspan['B3'][1]
labels.append(f'<div aria-hidden="true" style="position:absolute;left:10px;top:{ay0}px;width:30px;height:{ay1-ay0}px;background:{NAVY};clip-path:polygon(0 0,100% 0,100% calc(100% - 26px),50% 100%,0 calc(100% - 26px))"></div>')
labels.append(f'<p style="position:absolute;left:10px;top:{ay0}px;width:30px;height:{ay1-ay0-26}px;margin:0;display:flex;align-items:center;justify-content:center;writing-mode:vertical-rl;color:#FFFFFF;font-size:13px;line-height:16px;font-weight:700;letter-spacing:.4px">pre-trade to post-trade</p>')

# ---------------- externals
EY=STACK_BOT+48
LINES=[('Clients and markets','Who the bank trades with and where',['X01','X15','X02','X03','X18']),
       ('Infrastructure','Clearing, settlement, messaging, reporting and payments networks',['X04','X05','X07','X08','X09','X10','X16','X19']),
       ('Providers and regulators','Agents, data, utilities, issuers and authorities',['X06','X12','X13','X14','X17','X20','X11','X21'])]
assert sorted(sum([i for _,_,i in LINES],[]))==sorted(EXT)
yy=EY+68
ext_cards=[];ext_lbl=[]
for nm,sub,ids in LINES:
    hs=[]
    for xid in ids:
        e=EXT[xid]; iw=SLOT-22
        hs.append(hh('x:'+xid,ev(16+nlines(e['name'],iw,13,True)*17+4+nlines(e['role'],iw,12)*16+4+20)))
    rh=max(hs)
    ext_lbl.append(f'<div style="position:absolute;left:{LBLX}px;top:{yy}px;width:{LBLW}px;height:{rh}px;box-sizing:border-box;padding:4px 12px"><h3 style="margin:0;font-size:15px;line-height:20px;font-weight:700;color:{NAVY}">{nm}</h3><p style="margin:2px 0 0;font-size:12px;line-height:16px;color:{MUTED}">{sub}</p></div>')
    for i,xid in enumerate(ids):
        e=EXT[xid]; x=SX0+i*(SLOT+SG)
        att=' '.join(e['layers'])
        ext_cards.append(f'<article{dk("x:"+xid)} style="position:absolute;left:{x}px;top:{yy}px;width:{SLOT}px;height:{hs[i]}px;box-sizing:border-box;padding:8px 10px;background:#FFFFFF;border:1px solid #6B7A92;border-radius:6px;font-size:12px;line-height:16px;color:{INK}"><b style="display:block;font-size:13px;line-height:17px;margin-bottom:4px">{esc(e["name"])}</b><span style="display:block;color:{MUTED}">{esc(e["role"])}</span><span style="display:block;margin-top:4px;color:{INK}"><b>Attaches to:</b> {att}</span></article>')
    yy+=rh+10
EBOT=yy+6
bg.insert(0,f'<div style="position:absolute;left:{M}px;top:{EY}px;width:{W-2*M}px;height:{EBOT-EY}px;box-sizing:border-box;background:#FFFFFF;border:1px solid {LINE};border-radius:8px"></div>')
labels.append(f'<h2 style="position:absolute;left:{M+16}px;top:{EY+12}px;width:{W-2*M-32}px;height:48px;margin:0;font-family:{SERIF};font-weight:600;font-size:24px;line-height:48px;color:{NAVY}">External parties <span style="font-family:{FONT};font-size:14px;line-height:20px;vertical-align:middle;font-weight:400;color:{MUTED};margin-left:12px">{len(EXT)} parties outside the bank, each attached to the layers listed on its card. Third-party run components inside the layers have dashed edges.</span></h2>')
labels+=ext_lbl; cards+=ext_cards

# ---------------- panels
PSTYLE=f'position:absolute;box-sizing:border-box;padding:20px;background:#FFFFFF;border:1px solid #B7C1D0;border-radius:8px;font-size:13px;line-height:18px;color:{INK};'
def h2s(t,i): return f'<h2 id="{i}" style="margin:0 0 6px;font-family:{SERIF};font-weight:600;font-size:22px;line-height:28px;color:{NAVY}">{esc(t)}</h2>'
def note(t): return f'<p style="margin:0 0 10px;font-size:13px;line-height:18px;color:{MUTED}">{esc(t)}</p>'
def h3s(t): return f'<h3 style="margin:14px 0 4px;font-size:14px;line-height:20px;font-weight:700;color:{NAVY}">{esc(t)}</h3>'
YA=EBOT+48
FW=1500; MW=W-2*M-FW-32
fc=(30,430,250,110,FW-42-30-430-250-110-48)
THREADS=[('Flow trade','Trade flow'),('Flow margin and collateral','Margin and collateral flow'),('Flow reporting','Reporting flow')]
assert set(l['thread'] for l in d['links'])==set(t for t,_ in THREADS)
def flowlist(name):
    g=' '.join(f'{c}px' for c in fc)
    return ('<ol style="list-style:none;margin:0;padding:0">'
     f'<sc-for list="{{{{{name}}}}}" as="f" hint-placeholder-count="3">'
     f'<li style="display:grid;grid-template-columns:{g};column-gap:12px;padding:6px 0;border-bottom:1px solid #E1E6EE;font-size:13px;line-height:18px;color:{INK}">'
     f'<span style="font-weight:700;color:{NAVY}">{{{{f.n}}}}</span>'
     '<span><b>{{f.from}}</b> to <b>{{f.to}}</b></span><span>{{f.label}}</span><span style="font-size:12px;line-height:16px;color:'+MUTED+'">{{f.layers}}</span>'
     f'<span style="font-size:12px;line-height:16px;color:{MUTED}">'
     '<sc-if value="{{f.hasStd}}" hint-placeholder-val="{{true}}">{{f.std}}</sc-if>'
     '<sc-if value="{{f.noStd}}" hint-placeholder-val="{{false}}"><i>no standard named</i></sc-if></span></li></sc-for></ol>')
fh=f'<div aria-hidden="true" style="display:grid;grid-template-columns:{" ".join(f"{c}px" for c in fc)};column-gap:12px;padding:4px 0;font-size:12px;line-height:18px;font-weight:700;color:{NAVY};border-bottom:2px solid {NAVY}"><span>No.</span><span>From and to</span><span>What moves</span><span>Layers</span><span>Standard</span></div>'
flows_html=(f'<section{dk("p:flows")} style="{PSTYLE}left:{M}px;top:{YA}px;width:{FW}px;height:{{H}}px" aria-labelledby="flows-h">'
 +h2s('Key flows','flows-h')+note('Illustrative only: a selection of representative flows between components and external parties, not the integration estate. The diagram has no connector arrows by design; read these rows instead. Three headings follow the three threads of the links. The Layers column shows where each flow starts and ends; EXT is an external party.')
 +fh+''.join(h3s(t)+flowlist('fl'+str(i)) for i,(_,t) in enumerate(THREADS))+'</section>')
# matrix by layer
FAM=[('BIAN','BIAN','BIAN'),('CALM','CALM','CALM'),('FIX','FIX','FIX'),('FpML_CDM','FpML / CDM','FpML_CDM'),('ISO20022','ISO 20022','ISO20022'),('SWIFT_MT','Swift MT','SWIFT_MT'),('other','Regulation and other','regs')]
LCOL=170
mc=[LCOL]+[(MW-42-LCOL-7*10)//7]*7
mg=' '.join(f'{c}px' for c in mc)
xm=d['xref_matrix']; cov=xm['coverage']
LAY={l['id']:l for l in LAYERS}
fieldmap={'BIAN':'bian','FIX':'fix','FpML_CDM':'fpml_cdm','ISO20022':'iso20022','SWIFT_MT':'swift_mt'}
for r in xm['layers']:
    comps=[c for g in LAY[r['layer']]['groups'] for c in g['components']]
    assert len(comps)==r['components']
    for fk,f in fieldmap.items():
        n=sum(1 for c in comps if c[f])
        if n!=r['counts'][fk]: print('NOTE count mismatch',r['layer'],fk,'matrix',r['counts'][fk],'fields',n)
    n=sum(1 for c in comps if c['regs'])
    if n!=r['counts']['regs']: print('NOTE regs mismatch',r['layer'],'matrix',r['counts']['regs'],'fields',n)
mrows=[]
for r in xm['layers']:
    row={'layer':f"{r['layer']} {r['name']}"}
    for key,lab,ck in FAM:
        cnt=r['components'] if key=='CALM' else r['counts'][ck]
        row[key+'N']=f"{cnt} of {r['components']}"; row[key+'T']=r['families'][key]
    mrows.append(row)
covcells=[]
for key,lab,ck in FAM:
    cv=cov[ck]; covcells.append({'lab':lab,'n':f"{cv['matched']} of {cov['total_components']}",'ver':cv.get('verified',None),'note':cv.get('note','')})
def cell(k): return f'<span style="overflow-wrap:anywhere"><b>{{{{r.{k}N}}}}</b><br>{{{{r.{k}T}}}}</span>'
mhead=''.join(f'<span>{lab}</span>' for _,lab,_ in FAM)
mat=(f'<section{dk("p:matrix")} style="{PSTYLE}left:{M+FW+32}px;top:{YA}px;width:{MW}px;height:{{H}}px" aria-labelledby="mat-h">'
 +h2s('Standards cross-reference matrix','mat-h')
 +note('Layers as rows, standards families as columns. Each cell gives the number of the layer\'s components carrying a reference in that family, then what the references are. References are left blank where no honest match exists.')
 +f'<div aria-hidden="true" style="display:grid;grid-template-columns:{mg};column-gap:10px;padding:4px 0;font-size:12px;line-height:18px;font-weight:700;color:{NAVY};border-bottom:2px solid {NAVY}"><span>Layer</span>{mhead}</div>'
 +'<ol style="list-style:none;margin:0;padding:0"><sc-for list="{{matrix}}" as="r" hint-placeholder-count="3">'
 +f'<li style="display:grid;grid-template-columns:{mg};column-gap:10px;padding:6px 0;border-bottom:1px solid #E1E6EE;font-size:12px;line-height:16px;color:{INK}"><b style="font-size:13px;line-height:18px;color:{NAVY}">{{{{r.layer}}}}</b>'
 +''.join(cell(k) for k,_,_ in FAM)+'</li></sc-for></ol>'
 +h3s('Coverage summary: components carrying a reference, of all components')
 +f'<ul style="list-style:none;margin:0;padding:0;display:grid;grid-template-columns:{mg};column-gap:10px;font-size:12px;line-height:16px"><li style="font-weight:700;color:{NAVY}">All layers</li>'
 +'<sc-for list="{{coverage}}" as="v" hint-placeholder-count="7"><li><b style="font-size:13px;line-height:18px;color:'+NAVY+'">{{v.n}}</b><br>'
 +'<sc-if value="{{v.isVerified}}" hint-placeholder-val="{{true}}"><span style="display:inline-block;margin:2px 0;padding:0 6px;border-radius:3px;background:'+NAVY+';color:#FFFFFF;font-weight:700">Verified</span><br></sc-if>'
 +'<sc-if value="{{v.isUnverified}}" hint-placeholder-val="{{false}}"><span style="display:inline-block;margin:2px 0;padding:0 5px;border-radius:3px;border:2px solid '+AMBER+';color:#6B4200;font-weight:700">Not verified</span><br></sc-if>'
 +'{{v.note}}</li></sc-for></ul>'
 +h3s('Gaps: where no standard fits')
 +'<ul style="margin:0;padding:0 0 0 20px;font-size:13px;line-height:18px;column-count:2;column-gap:32px"><sc-for list="{{gaps}}" as="g" hint-placeholder-count="4"><li style="margin:0 0 4px">{{g.text}}</li></sc-for></ul></section>')
# stage traceability
KIND={'lifecycle':'Lifecycle stage, placed by what happens','cross-lifecycle':'Cross-lifecycle, not a step','common':'Common, serves every layer','platform':'Split by purpose'}
tcols=(190,180,80,560,FW-42-190-180-80-560-4*12)
tg=' '.join(f'{c}px' for c in tcols)
trows=[{'stage':f"{t['stage']} {t['name']}" if t['stage']!='PLATFORM' else 'PLATFORM '+t['name'],'kind':KIND[t['kind']],'layers':' '.join(t['layers']),'groups':'; '.join(t['groups']),'note':t['note']} for t in xm['stage_traceability']]
assert {t['stage'] for t in xm['stage_traceability']}>={f'S{i}' for i in range(10)}
trace_html=(f'<section{dk("p:trace")} style="{PSTYLE}left:{M}px;top:{{Y}}px;width:{FW}px;height:{{H}}px" aria-labelledby="tr-h">'
 +h2s('Stage traceability: S0 to S9 and the platform strip','tr-h')
 +note('The stage tags on layers and groups come from the earlier lifecycle presentation (stages S0 to S9 and a cross-cutting platform strip). This table maps each stage to the layers and groups that now deliver it. S4 and S8 are cross-lifecycle, not steps, and S9 is a common service to every layer.')
 +f'<div aria-hidden="true" style="display:grid;grid-template-columns:{tg};column-gap:12px;padding:4px 0;font-size:12px;line-height:18px;font-weight:700;color:{NAVY};border-bottom:2px solid {NAVY}"><span>Stage</span><span>Reading</span><span>Layers</span><span>Groups (layer / group)</span><span>Note</span></div>'
 +'<ol style="list-style:none;margin:0;padding:0"><sc-for list="{{trace}}" as="t" hint-placeholder-count="3">'
 +f'<li style="display:grid;grid-template-columns:{tg};column-gap:12px;padding:7px 0;border-bottom:1px solid #E1E6EE;font-size:12px;line-height:16px;color:{INK}"><b style="font-size:13px;line-height:18px;color:{NAVY}">{{{{t.stage}}}}</b><span>{{{{t.kind}}}}</span><span>{{{{t.layers}}}}</span><span>{{{{t.groups}}}}</span><span>{{{{t.note}}}}</span></li></sc-for></ol></section>')
# standards
std=d['standards']
SWd=MW; sci=SWd-42; colw2=(sci-32)//2
def stdcol(name):
    return ('<ul style="list-style:none;margin:0;padding:0">'
     f'<sc-for list="{{{{{name}}}}}" as="s" hint-placeholder-count="3">'
     f'<li style="display:flex;gap:12px;align-items:flex-start;padding:7px 0;border-bottom:1px solid #E1E6EE;font-size:12px;line-height:16px;color:{INK}">'
     '<span style="flex:0 0 96px;width:96px">'
     f'<sc-if value="{{{{s.verified}}}}" hint-placeholder-val="{{{{true}}}}"><span style="display:block;box-sizing:border-box;width:96px;text-align:center;padding:2px 0;background:{NAVY};color:#FFFFFF;border:2px solid {NAVY};border-radius:4px;font-size:12px;line-height:16px;font-weight:700">Verified</span></sc-if>'
     f'<sc-if value="{{{{s.unverified}}}}" hint-placeholder-val="{{{{false}}}}"><span style="display:block;box-sizing:border-box;width:96px;text-align:center;padding:2px 0;background:#FFFFFF;color:#6B4200;border:2px solid {AMBER};border-radius:4px;font-size:12px;line-height:16px;font-weight:700">Not verified</span></sc-if></span>'
     '<span style="flex:1 1 auto"><b style="display:block;font-size:13px;line-height:18px">{{s.name}}</b>{{s.usedFor}}<br><span style="color:'+MUTED+'"><b>Layers:</b> {{s.layers}}</span></span></li></sc-for></ul>')
nunv=sum(1 for s in std if not s['verified'])
std_html=(f'<section{dk("p:std")} style="{PSTYLE}left:{M+FW+32}px;top:{{Y}}px;width:{SWd}px;height:{{H}}px" aria-labelledby="std-h">'
 +h2s('Standards used as inputs','std-h')
 +note(f'{len(std)} entries, {len(std)-nunv} verified and {nunv} not verified. Each informed a component name, an identifier, a message or a report; none defines the structure. Verified means a cited source was read; not verified means not checked against the source for this draft and to be validated before external use.')
 +f'<div style="display:grid;grid-template-columns:{colw2}px {colw2}px;column-gap:32px">'+stdcol('stdA')+stdcol('stdB')+'</div></section>')
# legend
LW=1180; HW=W-2*M-LW-32
def lrow(sample,sw,text):
    return f'<li style="display:flex;gap:12px;align-items:flex-start;padding:3px 0;font-size:13px;line-height:18px;color:{INK}"><span style="flex:0 0 {sw}px;width:{sw}px">{sample}</span><span>{esc(text)}</span></li>'
def sec(title,rows): return h3s(title)+'<ul style="list-style:none;margin:0;padding:0">'+''.join(rows)+'</ul>'
def bsw(b):
    f,t,ti,bd=BAND[b]
    return f'<span style="display:block;width:112px;height:26px;box-sizing:border-box;padding:3px 6px;background:{f};color:{t};border:1px solid {bd};border-radius:4px;font-size:12px;line-height:18px;font-weight:700;text-align:center;white-space:nowrap">{ {"B4":"Cross-lifecycle","B5":"Common"}.get(b,reads[b]["name"]) }</span>'
roles=[('system of record','holds the authoritative copy of its data'),('engagement','where clients, traders or staff interact with the bank'),('calculation','derives values, risk or analytics'),('data','supplies or stores reference and market data'),('integration','moves and translates data between systems'),('control','enforces limits, rules, checks and oversight')]
calm=[('actor','a person or role'),('ecosystem','a wider set of parties and systems'),('system','a deployable application or platform'),('service','a capability offered through an interface'),('database','a store of records'),('network','a network or messaging fabric'),('ldap','a directory used for identity'),('webclient','a browser or app front end'),('data-asset','a managed dataset')]
used_calm={c['calm'] for c in ALLC.values()}; assert used_calm<={a for a,_ in calm},used_calm
dash='<span style="display:block;width:96px;height:26px;box-sizing:border-box;padding:3px 6px;background:#FFFFFF;border:2px dashed #3A4556;border-radius:6px;font-size:12px;line-height:18px;text-align:center">third party</span>'
solid=f'<span style="display:block;width:96px;height:26px;box-sizing:border-box;padding:3px 6px;background:#FFFFFF;border:1px solid {LINE};border-radius:6px;font-size:12px;line-height:18px;text-align:center">solid</span>'
legend_html=(f'<section{dk("p:legend")} style="{PSTYLE}left:{M}px;top:{{Y}}px;width:{LW}px;height:{{H}}px" aria-labelledby="leg-h">'
 +h2s('Legend','leg-h')+note('How to read the layers, groups and cards. CALM terms are vocabulary only.')
 +sec('Bands (vertical bars at the left)',[lrow(bsw(b),112,reads[b]['reads']) for b in reads])
 +sec('Stage tags and office',[lrow(schip('S2')+schip('S3'),112,'Stage in the lifecycle presentation: S0 to S9 are the ten stages of the earlier lifecycle view and PLATFORM is its cross-cutting strip. A traceability tag only, not a sequence.'),
    lrow('<b>Office</b>',112,'Front, Middle, Back or Cross-cutting, as small text. Office is a convention and banks differ. A layer shows its dominant office; a group shows its own.')])
 +sec('Asset classes',[lrow(''.join(chip(a) for a in ['EQ','FI']),112,'EQ equities, FI fixed income (rates and credit), FX foreign exchange, DR derivatives (OTC and listed). A chip means the component is specific to those classes.'),
    lrow('<span style="display:block;width:112px;font-size:12px;line-height:18px;font-weight:700">No chip</span>',112,'No chip means the component applies to all four asset classes (ALL).')])
 +sec('Card edge',[lrow(solid,112,'Solid edge: the bank runs it'),lrow(dash,112,'Dashed edge and the words third party: usually run by a third party; the bank keeps oversight')])
 +sec('Cross-reference lines on cards',[lrow('<b>BIAN:</b>',112,'closest-fit service domain label'),lrow('<b>FIX:</b>',112,'FIX message types'),lrow('<b>FpML/CDM:</b>',112,'FpML or CDM model family'),lrow('<b>ISO 20022:</b>',112,'business area codes only'),lrow('<b>MT:</b>',112,'Swift MT numbers, unverified'),lrow('<i>role line</i>',112,'role, then the CALM node type, for example system of record · CALM database')])
 +sec('Role, as the first word of the role line',[lrow(f'<b>{esc(a)}</b>',112,b) for a,b in roles])
 +sec('CALM 1.1 node types (glosses are the analyst\'s)',[lrow(f'<b>{esc(a)}</b>',112,b) for a,b in calm])+'</section>')
# honesty
lims=[
 'Layering not yet reviewed. The component content was AI-reviewed. The grouping of components into eight layers and five bands is an analyst judgement on an archetype and has not been practitioner-validated.',
 'CALM is vocabulary only. Every component carries a CALM 1.1 node type as a label, but this is not a CALM document: no relationships, flows or controls are modelled.',
 'BIAN names are closest-fit labels, checked against the version 10 service landscape only. BIAN is oriented to banks and has no lifecycle view of capital markets, so the structure is the analyst\'s own. A card with no BIAN line had no matching domain. Later releases may rename domains.',
 'ISO 20022 is shown at business area level only (for example secl, sese, colr, auth). Message identifiers were not checked, and sell-side use of setr and fxtr was not checked.',
 'Swift MT numbers are analyst knowledge and are not verified. Verified: the coexistence of ISO 15022 and ISO 20022 for securities (MT to ISO 20022 is coexistence, not a forced cut-over), and the end of MT/MX coexistence for cross-border payments on 22 November 2025 (MT103/202 retired).',
 f'{nunv} of {len(std)} standards entries are marked not verified, including many regulatory regimes. They were not checked against the source for this draft and should be validated before external use: UK MiFIR, best execution, pre- and post-trade transparency, EMIR risk-mitigation and clearing duties, CFTC Part 43, SEC SBSR, UMR phase-in and CCP margin models, CASS and 15c3-3, Reg SHO, 15c3-5 and RTS 6, KYC and AML, MiFID categorisation and suitability, ISDA, GMRA and GMSLA, LEI, ISIN, CFI and FIGI, FRTB, SA-CCR and BCBS 239, ISDA DRR, US broker-dealer regimes, MiFID II recording of communications, UK MAR Articles 11 and 18, and the Swift MT numbers. Mapping to components is indicative, not legal or regulatory advice.',
 'FIX names were checked against a third-party FIX Latest dictionary. CDM was checked at model level, not function level. FpML and CDM references are family level.',
 'The key flows are illustrative; the real integration estate is far denser and most components also read from the common services.',
 'Not every trade passes every lifecycle layer: FX skips custody, uncleared OTC skips the CCP, listed derivatives skip CSD settlement.']
asm=d['assumptions']
lis=''.join(f'<li style="margin:0 0 8px;font-size:13px;line-height:18px;color:{INK}">{esc(t)}</li>' for t in lims)
alis=''.join(f'<li style="margin:0 0 6px;font-size:13px;line-height:18px;color:{INK}">{esc(t)}</li>' for t in asm)
hon_html=(f'<section{dk("p:hon")} style="{PSTYLE}left:{M+LW+32}px;top:{{Y}}px;width:{HW}px;height:{{H}}px;background:#FFF6E3;border-color:{AMBER}" aria-labelledby="hon-h">'
 +h2s('Limitations and assumptions','hon-h')+note('What this diagram does not establish, and the choices made to draw one archetype.')
 +f'<div style="column-count:2;column-gap:40px"><h3 style="margin:0 0 4px;font-size:14px;line-height:20px;font-weight:700;color:{NAVY}">Limitations</h3><ul style="margin:0 0 12px;padding:0 0 0 20px">{lis}</ul>'
 +f'<h3 style="margin:0 0 4px;font-size:14px;line-height:20px;font-weight:700;color:{NAVY}">Assumptions</h3><ol style="margin:0;padding:0 0 0 22px">{alis}</ol></div></section>')
HA=max(hh('p:flows',2300),hh('p:matrix',2300))
flows_html=flows_html.replace('{H}',str(HA)); mat=mat.replace('{H}',str(HA))
YB=YA+HA+32
HB=max(hh('p:trace',1200),hh('p:std',1200))
trace_html=trace_html.replace('{H}',str(HB)).replace('{Y}',str(YB)); std_html=std_html.replace('{H}',str(HB)).replace('{Y}',str(YB))
YC=YB+HB+32
HC=max(hh('p:legend',1200),hh('p:hon',1200))
legend_html=legend_html.replace('{H}',str(HC)).replace('{Y}',str(YC)); hon_html=hon_html.replace('{H}',str(HC)).replace('{Y}',str(YC))
H_TOTAL=YC+HC+64
footer=f'<p style="position:absolute;left:{M}px;top:{YC+HC+24}px;width:{W-2*M}px;height:20px;margin:0;font-size:14px;line-height:20px;color:{MUTED}">Detailed reference view; see the one-page view for presentation.</p>'
# data
links=[{'from':name_of(l['from']),'to':name_of(l['to']),'label':l['label'],'std':l['std'],'thread':l['thread'],'layers':(l['from_layer']+' to '+l['to_layer'])} for l in d['links']]
DATA={'links':links,'standards':[{'name':s['name'],'used_for':s['used_for'],'verified':s['verified'],'layers':' '.join(s['layers'])} for s in std],
      'matrix':mrows,'coverage':covcells,'gaps':cov['gaps'],'trace':trows}
data_js=json.dumps(DATA,ensure_ascii=False,separators=(',',':')); assert '</' not in data_js
script=("const DATA = "+data_js+";\n"
"class Component extends DCLogic {\n  renderVals() {\n    const D = DATA;\n"
"    const flows = D.links.map((l, i) => ({ n: i + 1, thread: l.thread, from: l.from, to: l.to, label: l.label, layers: l.layers, std: l.std, hasStd: !!l.std, noStd: !l.std }));\n"
"    const mk = (s) => ({ name: s.name, usedFor: s.used_for, layers: s.layers, verified: !!s.verified, unverified: !s.verified });\n"
"    const half = Math.ceil(D.standards.length / 2);\n"
"    return {\n"
"      fl0: flows.filter((f) => f.thread === 'Flow trade'),\n      fl1: flows.filter((f) => f.thread === 'Flow margin and collateral'),\n      fl2: flows.filter((f) => f.thread === 'Flow reporting'),\n"
"      stdA: D.standards.slice(0, half).map(mk),\n      stdB: D.standards.slice(half).map(mk),\n"
"      matrix: D.matrix,\n      trace: D.trace,\n      coverage: D.coverage.map((v) => ({ n: v.n, note: v.note, isVerified: v.ver === true, isUnverified: v.ver === false })),\n"
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
{chr(10).join(bg)}
{chr(10).join(cards)}
{chr(10).join(labels)}
{flows_html}
{mat}
{trace_html}
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
json.dump({'w':W,'h':H_TOTAL,'n':len(ALLC),'g':len(GRP),'l':len(LAYERS),'b':len(BANDS)},open(ROOT+'/main_size.json','w'))
print('Main',W,H_TOTAL,'comps',len(ALLC),'stack',STACK_BOT,'ext',EBOT,'rowA',HA,'rowB',HB,'rowC',HC,'slot',SLOT)
