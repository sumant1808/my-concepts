import re,json,subprocess,sys
sys.path.insert(0,'/home/claude/sell-arch-canvas')
from common import *
from html.parser import HTMLParser
VOID={'meta','link','br','img','input','hr'}
for f,minfs in (('Main',12),('Summary',18)):
    src=open(f'project/{f}.dc.html',encoding='utf-8').read()
    class P(HTMLParser):
        def __init__(s): super().__init__(); s.st=[]; s.err=[]
        def handle_starttag(s,t,a):
            if t not in VOID: s.st.append(t)
        def handle_endtag(s,t):
            if not s.st or s.st[-1]!=t: s.err.append((t,s.st[-3:],s.getpos()))
            else: s.st.pop()
    p=P(); p.feed(src)
    m=re.search(r'<script type="text/x-dc" data-dc-script[^>]*>(.*?)</script>',src,re.S)
    open('/tmp/comp.js','w').write(m.group(1))
    nc=subprocess.run(['node','--check','/tmp/comp.js'],capture_output=True,text=True)
    stub="global.DCLogic=class{constructor(){this.props={};this.state={}}};(0,eval)(require('fs').readFileSync('/tmp/comp.js','utf8')+';globalThis.__C=Component;');const v=new __C().renderVals();console.log(Object.keys(v).join(','))"
    rv=subprocess.run(['node','-e',stub],capture_output=True,text=True)
    fs=[float(x) for x in re.findall(r'font-size:(\d+(?:\.\d+)?)px',src)]
    bad=[l for l in re.findall(r'<[a-z][^<>]*>',re.sub(r'<script.*?</script>','',src,flags=re.S)) if l.count('"')%2]
    print(f,'unbalanced',p.err[:3],'open',p.st,'| node --check rc',nc.returncode,nc.stderr[:100],'| renderVals keys',rv.stdout.strip(),rv.stderr[:100])
    print('  dashes',len(re.findall('[–—]',src)),'emoji',len(re.findall('[\U0001F300-\U0001FAFF☀-➿]',src)),'min font',min(fs),'(need',minfs,')','svg',src.count('<svg'),'iframe',src.count('<iframe'),'odd-quote tags',len(bad),'support line','<script src="./support.js"></script>' in src,'data-k',src.count('data-k'))
    print('  fonts links',src.count('fonts.googleapis.com'),'http refs',len(re.findall(r'https?://',src)),'preview',re.search(r'\$preview":\{[^}]*\}',src).group(0))
src=open('project/Main.dc.html',encoding='utf-8').read()
miss=[c['name'] for c in ALLC.values() if esc(c['name']) not in src]
print('Main missing component names',miss,'| C78 line',('BIAN:</b> Market Risk; Economic Capital' in src))
print('vendor grep',re.findall(r'(?i)murex|calypso|bloomberg|refinitiv|broadridge|summit|fidessa|ion |temenos|tradeweb|markitwire|dtcc|euroclear|clearstream|lseg',src)[:5])
# contrast
for a,b in [('#FFFFFF','#1F4E8C'),(NAVY,'#F2B84B'),(NAVY,'#6FBDB4'),(NAVY,'#CBD3DF'),(NAVY,'#FFFFFF'),(INK,'#FFFFFF'),(MUTED,'#FFFFFF'),(MUTED,'#FCEFD4'),(MUTED,'#DCE8F7'),(MUTED,'#DAF0ED'),(MUTED,'#E8ECF2'),(INK,'#FCEFD4'),(INK,'#DCE8F7'),(INK,'#DAF0ED'),('#FFFFFF','#3A4556'),('#6B4200','#FFFFFF'),('#4A2F00','#FFF1CF'),(MUTED,'#F4F6F9'),(MUTED,'#FFF6E3'),(INK,'#FFF6E3'),('#DDE5F0',NAVY),('#D5E0EE',NAVY),(MUTED,'#E8ECF2')]:
    print(a,b,round(cr(a,b),2),end=' | ')
