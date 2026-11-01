import json,os,sys,re
sys.path.insert(0,'/home/claude/sell-func-canvas')
from common import *
OUT=ROOT+'/project/Summary.dc.html'
d=spec
# slide label map: id -> (title, example line 1, example line 2)
SL={
 'G03':('Sales, Coverage','CRM, call reports','Axes, indications'),
 'G01':('Client Lifecycle','Onboarding, KYC','Categorisation'),
 'G02':('Credit and Legal','Credit approval','Agreements, SSIs'),
 'G04':('Quoting, Pricing','RFQ, streaming prices','Client APIs'),
 'G05':('Structuring','Pricing models','Suitability, approval'),
 'G06':('Order Management','Order system','Pre-trade risk, DMA'),
 'G07':('Execution','Smart routing, algos','FX aggregation'),
 'G08':('Trading Desk','Workstation','Trader positions'),
 'G09':('Trade Booking','Capture, enrichment','Fees, billing'),
 'G10':('Allocation','Affirmation, matching',''),
 'G11':('OTC Confirmation','Matching, recs','Lifecycle events'),
 'G15':('CCP Clearing','Give-ups, novation','Client accounts'),
 'G16':('Margin, Netting','Calls, compression',''),
 'G17':('Settlement','Instructions, fails',''),
 'G18':('Infrastructure','CSDs, FX PvP','Agent banks'),
 'G20':('Safekeeping','Segregated custody',''),
 'G21':('Asset Servicing','Corporate actions',''),
 'G23':('Prime Services','Margin lending, TRS',''),
 'G22':('Securities Finance','Lending, repo',''),
 'G24':('Finance Controls','Locates, short sales',''),
 'P3':('Collateral, Cash','Collateral, liquidity','Funding, payments'),
 'G12':('Risk and P&L','Risk engine, P&L','Price verification'),
 'P2':('Risk and Limits','Exposure, limits','Capital, XVA'),
 'G13':('Trade Reporting','MiFIR, EMIR, SFTR','Transparency, hub'),
 'P6':('Surveillance','Trade and comms','Control room, STORs'),
 'G27':('Conduct','Best execution','Client money, assets'),
 'G25':('Market Data Feeds','Feed handlers','Colocation'),
 'G26':('Data Distribution','Entitlements, licences','Tick history'),
 'P1':('Reference Data','Instruments, parties','Curves, calendars'),
 'P4':('Data, Analytics','Position store','Finance feed, lineage'),
 'P5':('Integration','Message gateway','Translation, APIs'),
 'P7':('Controls','Identity, access','Resilience, records'),
 'G28':('Reconciliation','Front to back','Nostro, depot'),
}
assert set(SL)==set(GRP)
SPLIT={'L1':1,'L2':1,'L3':3,'L4':2,'L5':2,'L6':3,'L7':3,'L8':2}   # cluster divider after n groups
W,H=1920,1080; M=24
GAP=12; BARX=M; BARW=56; LBLX=BARX+BARW+8; LBLW=186; BX0=LBLX+LBLW+8; BX1=W-M
SLOTS=7; BW=(BX1-BX0-(SLOTS-1)*GAP)//SLOTS
RH=91; RP=3; BH=RH-2*RP; TAB=26
def chip(t): return f'<span style="display:inline-block;margin-right:5px;padding:0 6px;border-radius:4px;background:{CHIPBG};color:#FFFFFF;font-size:18px;line-height:24px;font-weight:700">{t}</span>'
els=[]
els.append(f'<div style="position:absolute;left:0;top:0;width:{W}px;height:92px;background:{NAVY}"></div><div style="position:absolute;left:0;top:92px;width:{W}px;height:4px;background:{TEAL}"></div>')
TITLE='Sell-side markets: one functional architecture from pre-trade to post-trade'
els.append(f'<h1 style="position:absolute;left:{M}px;top:6px;width:{W-2*M}px;height:54px;margin:0;font-family:{SERIF};font-size:42px;line-height:54px;font-weight:600;color:#FFFFFF;white-space:nowrap">{esc(TITLE)}</h1>')
els.append(f'<p style="position:absolute;left:{M}px;top:60px;width:1340px;height:28px;margin:0;font-size:22px;line-height:28px;color:#D5E0EE;white-space:nowrap">Global markets sales and trading, multi-asset. Layers by lifecycle, with cross-lifecycle and common services underneath.</p>')
els.append(f'<p style="position:absolute;left:1380px;top:60px;width:{W-M-1380}px;height:28px;margin:0;font-size:22px;line-height:28px;font-weight:700;color:#FFD98A;text-align:right;white-space:nowrap">Reads top to bottom: pre-trade to post-trade</p>')
LEG_Y=H-60-8-48-6-28
AREA_Y=104; AREA_BOT=LEG_Y-8
bands={}; rows=[]
y=AREA_Y; prev=None; dashed=[]; labelmap=[]
bg=[];boxes=[];labs=[]
def box(x,y,g,bd):
    t,e1,e2=SL[g['id']]; cs=group_chips(g); ext=mostly_ext(g)
    if ext: dashed.append(t)
    labelmap.append((g['id'],g['name'],t,e1,e2,' '.join(cs) or '(none: all four)',ext,[ ]))
    chipdiv=''
    exl=f'<span style="display:block;margin-top:2px;font-size:18px;line-height:22px;color:{INK};white-space:nowrap;overflow:hidden;height:22px">{esc(e1)}</span>'
    if cs:
        chipdiv=f'<div style="height:24px;margin-top:auto"><span style="position:absolute;width:1px;height:1px;overflow:hidden;white-space:nowrap;font-size:18px;line-height:22px">Asset classes: </span>{"".join(chip(a) for a in cs)}</div>'
    else:
        exl+=f'<span style="display:block;font-size:18px;line-height:22px;color:{INK};white-space:nowrap;overflow:hidden;height:22px">{esc(e2)}</span>'
        assert e2
    style='dashed' if ext else 'solid'
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{BW}px;height:{BH}px;box-sizing:border-box;padding:4px 8px;background:#FFFFFF;border:2px {style} {bd};border-radius:8px;display:flex;flex-direction:column;color:{NAVY}">'
            f'<b style="display:block;font-size:20px;line-height:24px;font-weight:700;white-space:nowrap;overflow:hidden;height:24px">{esc(t)}</b>{exl}{chipdiv}</div>')
STRIP_Y=None
for L in LAYERS:
    b=L['band']; fill,tc,tint,bd=BAND[b]
    if prev is not None:
        y+= 14 if b=='B5' else (10 if b!=prev else 5)
    bands.setdefault(b,[y,0])
    if b=='B5':
        STRIP_Y=y; SH=TAB+RH
        els.append(f'<div style="position:absolute;left:{M}px;top:{y}px;width:{W-2*M}px;height:{SH}px;box-sizing:border-box;background:{tint};border:3px solid {bd};border-radius:10px"></div>')
        els.append(f'<div style="position:absolute;left:{LBLX}px;top:{y+3}px;width:{W-M-3-LBLX}px;height:{TAB-3}px;box-sizing:border-box;padding:0 12px;background:{NAVY};color:#FFFFFF;font-size:18px;line-height:23px;font-weight:700;white-space:nowrap;overflow:hidden">Serves every layer above: market data, reference data, analytics, integration, controls and reconciliation</div>')
        ry=y+TAB; rh=RH
    else:
        ry=y; rh=RH
        bg.append(f'<div style="position:absolute;left:{LBLX}px;top:{y}px;width:{W-M-LBLX}px;height:{RH}px;box-sizing:border-box;background:{tint};border:1px solid {bd};border-radius:8px"></div>')
    labs.append(f'<h2 style="position:absolute;left:{LBLX}px;top:{ry}px;width:{LBLW}px;height:{rh}px;box-sizing:border-box;margin:0;padding:4px 8px 4px 12px;display:flex;align-items:center;font-size:20px;line-height:24px;font-weight:700;color:{NAVY};overflow:hidden">{esc(L["name"])}</h2>')
    for i,g in enumerate(L['groups']):
        boxes.append(box(BX0+i*(BW+GAP),ry+RP,g,bd))
    n=SPLIT[L['id']]; assert 0<n<len(L['groups'])
    dx=BX0+n*(BW+GAP)-GAP//2-1
    boxes.append(f'<div aria-hidden="true" style="position:absolute;left:{dx}px;top:{ry+2}px;width:3px;height:{rh-4}px;background:{bd};border-radius:2px"></div>')
    y=ry+rh if b!='B5' else y+SH
    bands[b][1]=y; prev=b
assert y<=AREA_BOT,(y,AREA_BOT)
els+=bg+boxes+labs
names={b['id']:b['name'] for b in BANDS}
for bid,(a,z) in bands.items():
    fill,tc,tint,bd=BAND[bid]
    els.append(f'<h2 aria-label="Band: {esc(names[bid])}" style="position:absolute;left:{BARX}px;top:{a}px;width:{BARW}px;height:{z-a}px;box-sizing:border-box;margin:0;padding:6px 2px;display:flex;align-items:center;justify-content:center;text-align:center;writing-mode:vertical-rl;transform:rotate(180deg);background:{fill};color:{tc};border-radius:8px;font-family:{SERIF};font-weight:600;font-size:21px;line-height:24px;overflow:hidden">{esc(names[bid])}</h2>')
ay0=bands['B1'][0]; ay1=bands['B3'][1]
els.append(f'<div aria-hidden="true" style="position:absolute;left:5px;top:{ay0}px;width:14px;height:{ay1-ay0}px;background:{TEAL};clip-path:polygon(0 0,100% 0,100% calc(100% - 16px),50% 100%,0 calc(100% - 16px))"></div>')
# legend
def sw(bgc,bd,st='solid'): return f'<span style="display:inline-block;vertical-align:middle;margin-right:8px;width:30px;height:20px;box-sizing:border-box;background:{bgc};border:3px {st} {bd};border-radius:4px"></span>'
items=[chip('EQ')+chip('FI')+chip('FX')+chip('DR')+'asset-class focus','No chip: all four asset classes',sw('#FFFFFF','#3A4556','dashed')+'Mostly third-party run','<span style="display:inline-block;vertical-align:middle;margin-right:8px;width:3px;height:22px;background:#3A4556"></span>Two functions in one row','Stage tags: see detailed view']
els.append(f'<div style="position:absolute;left:{M}px;top:{LEG_Y}px;width:{W-2*M}px;height:28px;display:flex;gap:32px;align-items:center;font-size:18px;line-height:28px;color:{NAVY};white-space:nowrap">'+''.join(f'<span style="display:inline-block;height:28px;white-space:nowrap">{i}</span>' for i in items)+'</div>')
SHX={'X01':'institutions','X15':'agent lenders','X02':'venues','X03':'multi-dealer platforms','X18':'interdealer brokers','X04':'CCPs','X05':'CSDs','X07':'FX PvP','X08':'messaging network','X09':'repositories','X10':'ARMs and APAs','X16':'payments','X19':'tape providers','X06':'agent banks','X12':'data vendors','X13':'matching utilities','X14':'triparty agents','X17':'clearing brokers','X20':'issuers','X11':'regulators','X21':'tax authorities'}
XG=[('Clients',['X01','X15']),('Markets',['X02','X03','X18']),('Infrastructure',['X04','X05','X07','X08','X09','X10','X16','X19']),('Providers and regulators',['X06','X12','X13','X14','X17','X20','X11','X21'])]
assert sorted(sum([i for _,i in XG],[]))==sorted(EXT)==sorted(SHX)
allnames=[SHX[k] for _,i in XG for k in i]
EXT_Y=H-60-8-48
els.append(f'<p style="position:absolute;left:{M}px;top:{EXT_Y}px;width:{W-2*M}px;height:48px;margin:0;font-size:18px;line-height:24px;color:{INK}"><b>External parties ({len(EXT)}):</b> '+esc(', '.join(allnames))+'.</p>')
FOOT='Illustrative archetype, components AI-reviewed, layering not yet reviewed. Inputs: BIAN service domains (closest-fit labels), FINOS CALM vocabulary, FIX, ISO 20022, FpML and ISDA CDM. Detailed cross-referenced view available.'
els.append(f'<p style="position:absolute;left:{M}px;top:{H-60}px;width:{W-2*M}px;height:48px;margin:0;font-size:18px;line-height:24px;color:{MUTED}">{esc(FOOT)}</p>')
print('layout: rows end',y,'area bot',AREA_BOT,'legend',LEG_Y,'ext',EXT_Y,'foot',H-60,'bw',BW,'rh',RH,'dashed',dashed)
doc=f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<title>Sell-side markets functional architecture, one page</title>
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
<div style="position:relative;width:{W}px;height:{H}px;background:#F4F6F9;font-family:{FONT};color:{INK};overflow:hidden">
{chr(10).join(els)}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{W},"height":{H}}}}}'>
class Component extends DCLogic {{
renderVals() {{
return {{}};
}}
}}
</script>
</body>
</html>
'''
open(OUT,'w',encoding='utf-8').write(doc)
json.dump([list(r) for r in labelmap],open(ROOT+'/label_map.json','w'),indent=0)
