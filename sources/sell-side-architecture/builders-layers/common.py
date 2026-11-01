import json, html, os
SPEC='/home/claude/sell-arch/spec.json'
ROOT='/home/claude/sell-func-canvas'
spec=json.load(open(SPEC,encoding='utf-8'))
esc=lambda s: html.escape(s,quote=True)
NAVY='#0B1F3A'; TEAL='#0F8B8D'; AMBER='#8A5600'
INK='#17202E'; MUTED='#3F4B61'; LINE='#B7C1D0'
# band colours: (bar fill, bar text, tint, border)
BAND={
 'B1':('#1F4E8C','#FFFFFF','#DCE8F7','#1F4E8C'),   # dark blue
 'B2':('#F2B84B',NAVY,'#FCEFD4','#9A6A00'),        # light amber
 'B3':('#2E7D74','#FFFFFF','#DAF0ED','#2E7D74'),   # mid teal-green
 'B4':('#C9B8E8',NAVY,'#EFE9F9','#5B4A8A'),        # light violet
 'B5':('#3A4556','#FFFFFF','#E8ECF2','#3A4556'),   # dark slate
}
OFFICE_LABEL={'Front':'Front office','Middle':'Middle office','Back':'Back office','Cross-cutting':'Cross-cutting'}
CHIPBG='#3A4556'
ACORD=['EQ','FI','FX','DR']
FONT="'DM Sans',system-ui,sans-serif"
SERIF="Fraunces,Georgia,serif"
FONTLINK='<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,700;1,400&amp;family=Fraunces:wght@600&amp;display=swap">'
CW,CWB=0.57,0.62
def nlines(text,width,fs,bold=False):
    cw=(CWB if bold else CW)*fs; n=1; cur=0.0
    for w in text.split():
        wl=len(w)*cw; add=wl if cur==0 else wl+cw
        if cur>0 and cur+add>width: n+=1; cur=wl
        else: cur+=add
    return n
def ev(x): return int(x)+(int(x)%2)
def lum(h):
    h=h.lstrip('#'); c=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    c=[x/12.92 if x<=.03928 else ((x+.055)/1.055)**2.4 for x in c]; return .2126*c[0]+.7152*c[1]+.0722*c[2]
def cr(a,b):
    x,y=sorted([lum(a),lum(b)],reverse=True); return (x+.05)/(y+.05)
for k,(f,t,ti,b) in BAND.items():
    assert cr(f,t)>=4.5,(k,'bar',cr(f,t)); assert cr(INK,ti)>=4.5,(k,'tint'); assert cr(MUTED,ti)>=4.5,(k,'muted tint',cr(MUTED,ti))
def acs(ac): return [a for a in ACORD if a in ac]
LAYERS=spec['layers']; BANDS=spec['bands']
ALLC={c['id']:c for l in LAYERS for g in l['groups'] for c in g['components']}
GRP={g['id']:g for l in LAYERS for g in l['groups']}
EXT={e['id']:e for e in spec['externals']}
def name_of(i): return ALLC[i]['name'] if i in ALLC else EXT[i]['name']
def group_chips(g):
    u=set()
    for c in g['components']: u|=set(ACORD) if 'ALL' in c['ac'] else set(c['ac'])
    return [] if u==set(ACORD) else [a for a in ACORD if a in u]
def mostly_ext(g): return sum(c['external'] for c in g['components'])*2>len(g['components'])
