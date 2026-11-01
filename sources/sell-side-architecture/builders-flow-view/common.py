import json, html, os
SPEC='/home/claude/sell-arch/spec.json'
ROOT='/home/claude/sell-arch-canvas'
spec=json.load(open(SPEC,encoding='utf-8'))
esc=lambda s: html.escape(s,quote=True)
NAVY='#0B1F3A'; TEAL='#0F8B8D'; AMBER='#8A5600'
INK='#17202E'; MUTED='#3F4B61'; LINE='#B7C1D0'
# office colours: (fill, text, tint, border)
OFFICE={
 'Front':        ('#1F4E8C','#FFFFFF','#DCE8F7','#1F4E8C'),
 'Middle':       ('#F2B84B',NAVY,'#FCEFD4','#9A6A00'),
 'Back':         ('#6FBDB4',NAVY,'#DAF0ED','#2E7D74'),
 'Cross-cutting':('#CBD3DF',NAVY,'#E8ECF2','#3A4556'),
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
for k,(f,t,ti,b) in OFFICE.items():
    assert cr(f,t)>=4.5,(k,cr(f,t)); assert cr(NAVY,ti)>=4.5
def acs(ac):
    return [a for a in ACORD if a in ac]
def office_of(stage): return stage['office']
def comps_of(stage_or_plat): return [c for g in stage_or_plat['groups'] for c in g['components']]
ALLC={c['id']:c for s in spec['stages'] for g in s['groups'] for c in g['components']}
for g in spec['platform']['groups']:
    for c in g['components']: ALLC[c['id']]=c
EXT={e['id']:e for e in spec['externals']}
def name_of(i): return ALLC[i]['name'] if i in ALLC else EXT[i]['name']
