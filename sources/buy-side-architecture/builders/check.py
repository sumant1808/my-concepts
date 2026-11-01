import re,sys,json
from html.parser import HTMLParser
src=open('project/Main.dc.html',encoding='utf-8').read()
VOID={'meta','link','br','img','input','hr'}
class P(HTMLParser):
    def __init__(s): super().__init__(); s.st=[]; s.err=[]
    def handle_starttag(s,t,a):
        if t not in VOID: s.st.append(t)
    def handle_startendtag(s,t,a): pass
    def handle_endtag(s,t):
        if not s.st or s.st[-1]!=t: s.err.append((t,s.st[-3:],s.getpos()))
        else: s.st.pop()
p=P(); p.feed(src); print('unbalanced:',p.err[:5],'left open:',p.st)
print('dashes:',len(re.findall('[–—]',src)))
print('emoji-ish:',len(re.findall('[\U0001F300-\U0001FAFF☀-➿]',src)))
fs=[int(x) for x in re.findall(r'font-size:(\d+)px',src)]; print('min font',min(fs))
print('svg count',src.count('<svg'),'iframe',src.count('<iframe'))
print('head support line', '<script src="./support.js"></script>' in src)
# extract script
m=re.search(r'<script type="text/x-dc" data-dc-script[^>]*>(.*?)</script>',src,re.S)
open('/tmp/comp.js','w').write(m.group(1))
holes=sorted(set(re.findall(r'\{\{\s*([^}]*?)\s*\}\}',src))); print(holes)
json.dump(holes,open('/tmp/holes.json','w'))
# quotes check: odd count of quotes within tags
bad=[l for l in re.findall(r'<[a-z][^<>]*>',re.sub(r'<script.*?</script>','',src,flags=re.S)) if l.count('"')%2]
print('odd-quote tags',len(bad),bad[:2])
def lum(h):
    h=h.lstrip('#'); c=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    c=[x/12.92 if x<=.03928 else ((x+.055)/1.055)**2.4 for x in c]; return .2126*c[0]+.7152*c[1]+.0722*c[2]
def cr(a,b):
    x,y=sorted([lum(a),lum(b)],reverse=True); return (x+.05)/(y+.05)
for fg,bg in [('#17202E','#FFFFFF'),('#17202E','#D9F0EC'),('#17202E','#DCE8F7'),('#17202E','#FAE8C6'),('#445066','#FFFFFF'),('#445066','#D9F0EC'),('#445066','#DCE8F7'),('#445066','#FAE8C6'),('#FFFFFF','#0B6E70'),('#FFFFFF','#1F4E8C'),('#FFFFFF','#8A5700'),('#FFFFFF','#3A4556'),('#0B1F3A','#BFE3DD'),('#0B1F3A','#C5D8F0'),('#0B1F3A','#F2D9A6'),('#0B1F3A','#E9EEF5'),('#DDE5F0','#0B1F3A'),('#7FD6D8','#0B1F3A'),('#FFFFFF','#0B1F3A'),('#4A2F00','#FFF1CF'),('#17202E','#FFF6E3'),('#445066','#FFF6E3'),('#6B4200','#FFFFFF'),('#17202E','#F4F6F9'),('#0B1F3A','#F4F6F9'),('#445066','#E9EEF5'),('#17202E','#E9EEF5')]:
    print(fg,bg,round(cr(fg,bg),2))
