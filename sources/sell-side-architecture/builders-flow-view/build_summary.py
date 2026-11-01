import json,os,sys
sys.path.insert(0,'/home/claude/sell-arch-canvas')
from common import *
OUT=ROOT+'/project/Summary.dc.html'
d=spec
SHORT={'S0':'Onboarding','S1':'Origination','S2':'Execution','S3':'Confirmation','S4':'Risk and reporting','S5':'Clearing','S6':'Settlement','S7':'Custody','S8':'Financing and prime','S9':'Market data'}
LABEL={'G01':'Client Lifecycle','G02':'Credit and Documentation','G03':'Sales and Coverage','G04':'Quoting and Pricing','G05':'Structuring, Suitability',
 'G06':'Order Management','G07':'Execution and Routing','G08':'Trading Desk','G09':'Trade Capture and Booking','G10':'Allocation, Affirmation',
 'G11':'OTC Confirmation','G12':'Daily Risk and P&L','G13':'Regulatory Trade Reporting',
 'G15':'CCP and Listed Clearing','G16':'Margin and Netting','G17':'Settlement Processing','G18':'Market Infrastructure',
 'G20':'Safekeeping, Segregation','G21':'Asset Servicing','G22':'Securities Finance','G23':'Prime Services','G24':'Financing Controls',
 'G25':'Feed Acquisition','G26':'Distribution, Licensing',
 'P1':'Reference Data','P2':'Risk and Limits','P3':'Collateral, Liquidity, Cash','P4':'Data and Analytics','P5':'Integration and Messaging','P6':'Conduct and Reporting Oversight','P7':'Controls and Resilience'}
EX={'G01':'KYC, onboarding, categorisation','G02':'Credit, agreements, SSIs','G03':'CRM, axes and indications','G04':'RFQ, streaming, online channels','G05':'Pricing, NPA, suitability',
 'G06':'Order system, pre-trade risk','G07':'Routing, algos, FX aggregation','G08':'Workstation, positions','G09':'Capture, booking, fees','G10':'Allocation, affirmation',
 'G11':'Matching, recs, lifecycle','G12':'Risk, P&L, price verification','G13':'MiFIR, EMIR, CFTC, public',
 'G15':'Give-ups, CCP, client accounts','G16':'Margin, calls, netting','G17':'Instructions, status, fails','G18':'CSDs, FX PvP, agent banks',
 'G20':'Positions, client assets','G21':'Events, income, tax reclaims','G22':'Lending, borrowing, repo','G23':'Margin lending, synthetics','G24':'Locates, SFTR, rehypothecation',
 'G25':'Feeds, colocation','G26':'Entitlements, tick store',
 'P1':'Instrument, party, curve and calendar data','P2':'Exposure, limits, capital, XVA','P3':'Collateral, funding, payments, nostros','P4':'Trade store, finance feed, lineage',
 'P5':'Message gateway, translation, APIs','P6':'Surveillance, control room, best ex, STORs','P7':'Recs, client money, resilience, records'}
HOOK={'S0':'Cost: time to first trade','S4':'Cost: fines, capital, remediation','S5':'Cost: margin funding, CCP fees','S6':'Cost: fails and penalties','S7':'Fees: asset servicing','S9':'Cost: licences and latency'}
allg=[g for s in d['stages'] for g in s['groups']]+d['platform']['groups']
assert set(LABEL)==set(EX)=={g['id'] for g in allg}
def chips_for(g):
    u=set()
    for c in g['components']:
        u|=set(ACORD) if 'ALL' in c['ac'] else set(c['ac'])
    return [] if u==set(ACORD) else [a for a in ACORD if a in u]
def mostly_ext(g): return sum(c['external'] for c in g['components'])*2>len(g['components'])
W,H=1920,1080; M=24; GAP=8
COLW=(W-2*M-9*GAP)//10
def chip(t): return f'<span style="display:inline-block;margin-right:5px;padding:0 6px;border-radius:4px;background:{CHIPBG};color:#FFFFFF;font-size:18px;line-height:24px;font-weight:700">{t}</span>'
els=[]
# header
els.append(f'<div style="position:absolute;left:0;top:0;width:{W}px;height:96px;background:{NAVY}"></div><div style="position:absolute;left:0;top:96px;width:{W}px;height:4px;background:{TEAL}"></div>')
TITLE='From onboarding to market data: the sell-side trade lifecycle on one architecture'
els.append(f'<h1 data-k="title" style="position:absolute;left:{M}px;top:6px;width:{W-2*M}px;height:54px;margin:0;font-family:{SERIF};font-size:42px;line-height:54px;font-weight:600;color:#FFFFFF;white-space:nowrap">{esc(TITLE)}</h1>')
els.append(f'<p style="position:absolute;left:{M}px;top:62px;width:{W-2*M}px;height:28px;margin:0;font-size:22px;line-height:28px;color:#D5E0EE;white-space:nowrap">Global markets sales and trading, multi-asset. One functional architecture along ten lifecycle stages.</p>')
CY=110; CHH=88
ZY=CY+CHH+8; ZH=3*171+2*GAP   # stage zone
dashed=[];labelmap=[]
def box(x,y,w,h,g,office,pill=True,title_h=72,ex_h=44):
    fill,tc,tint,bd=OFFICE[office]
    ext=mostly_ext(g); cs=chips_for(g)
    if ext: dashed.append(LABEL[g['id']])
    labelmap.append((g['id'],g['name'],LABEL[g['id']],EX[g['id']],' '.join(cs) or '(none: all)',ext))
    ch=''.join(chip(a) for a in cs)
    chipdiv=(f'<div style="height:24px;margin-top:auto"><span style="position:absolute;width:1px;height:1px;overflow:hidden;white-space:nowrap">Asset classes: </span>{ch}</div>') if cs else ''
    style='dashed' if ext else 'solid'
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;box-sizing:border-box;padding:6px 8px 6px;background:#FFFFFF;border:3px {style} {bd};border-radius:8px;display:flex;flex-direction:column;color:{NAVY}">'
            f'<b data-k="t:{g["id"]}" style="display:block;font-size:20px;line-height:24px;font-weight:700;max-height:{title_h}px;overflow:hidden">{esc(LABEL[g["id"]])}</b>'
            f'<span data-k="e:{g["id"]}" style="display:block;margin-top:4px;font-size:18px;line-height:22px;color:{INK};max-height:{ex_h}px;overflow:hidden">{esc(EX[g["id"]])}</span>'
            f'{chipdiv}</div>')
for i,s in enumerate(d['stages']):
    x=M+i*(COLW+GAP); fill,tc,tint,bd=OFFICE[s['office']]
    border=f'<div style="position:absolute;left:{x}px;top:{CY}px;width:{COLW}px;height:{CHH}px;background:{bd};clip-path:polygon(0 0,calc(100% - 18px) 0,100% 50%,calc(100% - 18px) 100%,0 100%,18px 50%)"></div>' if s['office']=='Cross-cutting' else ''
    els.append(border)
    ins=2 if s['office']=='Cross-cutting' else 0
    els.append(f'<h2 aria-label="Stage {s["no"]}: {SHORT[s["id"]]}, {OFFICE_LABEL[s["office"]]}{'. Feeds every stage' if s['id']=='S9' else ''}" style="position:absolute;left:{x+ins}px;top:{CY+ins}px;width:{COLW-2*ins}px;height:{CHH-2*ins}px;box-sizing:border-box;margin:0;padding:8px 20px 6px 24px;display:flex;flex-direction:column;justify-content:flex-start;background:{fill};color:{tc};clip-path:polygon(0 0,calc(100% - 18px) 0,100% 50%,calc(100% - 18px) 100%,0 100%,18px 50%)">'
      f'<span style="display:block;font-size:22px;line-height:26px;font-weight:700">{s["no"]}</span>'
      f'<span data-k="n:{s["id"]}" style="display:block;font-size:20px;line-height:24px;font-weight:700">{esc(SHORT[s["id"]])}</span></h2>')
    n=len(s['groups']); assert n in (2,3)
    bh=(ZH-2*GAP)//3
    for j,g in enumerate(s['groups']):
        els.append(box(x,ZY+j*(bh+GAP),COLW,bh,g,s['office']))
    if n==2:
        assert s['id'] in HOOK,s['id']
        lab,txt=HOOK[s['id']].split(': ',1)
        els.append(f'<div data-k="h:{s["id"]}" style="position:absolute;left:{x}px;top:{ZY+2*(bh+GAP)}px;width:{COLW}px;height:{bh}px;box-sizing:border-box;padding:8px 10px;background:{tint};border-radius:8px;color:{INK};font-size:18px;line-height:22px;overflow:hidden"><b style="display:block;font-size:18px;line-height:22px;color:{NAVY}">{esc(lab)}</b>{esc(txt[0].upper()+txt[1:])}</div>')
    else: assert s['id'] not in HOOK
# platform band
PY=ZY+ZH+12; PH=176
pf,ptc,ptint,pbd=OFFICE['Cross-cutting']
els.append(f'<div style="position:absolute;left:{M}px;top:{PY}px;width:{W-2*M}px;height:{PH}px;box-sizing:border-box;background:{ptint};border:2px solid {pbd};border-radius:8px"></div>')
els.append(f'<h2 style="position:absolute;left:{M+14}px;top:{PY+6}px;width:{W-2*M-28}px;height:34px;margin:0;font-family:{SERIF};font-size:22px;line-height:32px;font-weight:600;color:{NAVY}">{esc(d["platform"]["name"])}<span style="font-family:{FONT};font-size:18px;font-weight:400;margin-left:16px;color:{MUTED}">serves every stage</span></h2>')
pg=d['platform']['groups']; PGAP=8; PW=(W-2*M-28-6*PGAP)//7
for j,g in enumerate(pg):
    els.append(box(M+14+j*(PW+PGAP),PY+42,PW,PH-42-14,g,'Cross-cutting',title_h=48,ex_h=66))
# legend
LY=PY+PH+10
def sw(bg,bd,st='solid'): return f'<span style="display:inline-block;vertical-align:middle;margin-right:8px;width:30px;height:20px;box-sizing:border-box;background:{bg};border:3px {st} {bd};border-radius:4px"></span>'
items=[]
for o in OFFICE:
    f,t,ti,b=OFFICE[o]; items.append((f'<span style="display:inline-block;vertical-align:middle;margin-right:8px;width:30px;height:20px;box-sizing:border-box;background:{f};border:1px solid {b};border-radius:4px"></span>{OFFICE_LABEL[o]}'))
items.append(''.join(chip(a) for a in ACORD)[:0]+chip('EQ')+chip('FI')+chip('FX')+chip('DR')+'single or partial')
items.append('No chip: all asset classes')
items.append(sw('#FFFFFF','#3A4556','dashed')+'Mostly third-party run')
# distribute by measured widths (estimated) ; use flex with gap
els.append(f'<div data-k="legend" style="position:absolute;left:{M}px;top:{LY}px;width:{W-2*M}px;height:28px;display:flex;gap:28px;align-items:center;font-size:18px;line-height:28px;color:{NAVY};white-space:nowrap">'+''.join(f'<span>{i}</span>' for i in items)+'</div>')
SHX={'X01':'institutions','X15':'agent lenders','X02':'venues','X03':'multi-dealer','X18':'interdealer brokers','X04':'CCPs','X05':'CSDs','X07':'FX PvP','X08':'messaging','X09':'repositories','X10':'ARMs and APAs','X16':'payments','X19':'tapes','X06':'agent banks','X12':'data vendors','X13':'utilities','X14':'triparty','X17':'clearing brokers','X20':'issuers','X11':'regulators','X21':'tax authorities'}
XG=[('Clients',['X01','X15']),('Markets',['X02','X03','X18']),('Infrastructure',['X04','X05','X07','X08','X09','X10','X16','X19']),('Providers and regulators',['X06','X12','X13','X14','X17','X20','X11','X21'])]
assert sorted(sum([i for _,i in XG],[]))==sorted(e['id'] for e in d['externals'])==sorted(SHX)
runs=[f'<span style="white-space:nowrap"><b>{n} ({len(i)}):</b> {esc(", ".join(SHX[k] for k in i))}</span>' for n,i in XG]
EXTY=LY+34
els.append(f'<p data-k="ext" style="position:absolute;left:{M}px;top:{EXTY}px;width:{W-2*M}px;height:48px;margin:0;font-size:18px;line-height:24px;color:{INK}"><b>External parties ({len(d["externals"])}):</b> '+'  |  '.join(runs[:3])+'<br>'+runs[3]+'</p>')
els.append(f'<p data-k="foot" style="position:absolute;left:{M}px;top:{H-62}px;width:{W-2*M}px;height:48px;margin:0;font-size:18px;line-height:24px;color:{MUTED}">Illustrative archetype, AI-reviewed, not practitioner-validated. Stage 1 is secondary-market origination; primary issuance is out of scope. Stage 9 feeds every stage. Inputs: BIAN service domains (closest-fit labels), FINOS CALM vocabulary, FIX, ISO 20022, FpML and ISDA CDM. Detailed cross-referenced view available.</p>')
print('layout: zone',ZY,ZY+ZH,'platform',PY,PY+PH,'legend',LY,'ext',EXTY,EXTY+48,'foot',H-38,'colw',COLW,'pw',PW)
assert EXTY+48<=H-62
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
import re
if os.environ.get('KEYS','1')=='0': doc=re.sub(r' data-k="[^"]*"','',doc)
open(OUT,'w',encoding='utf-8').write(doc)
json.dump([list(r) for r in labelmap],open(ROOT+'/label_map.json','w'),indent=0)
print('dashed',dashed)
