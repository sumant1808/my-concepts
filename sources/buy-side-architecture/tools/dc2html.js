// Convert a .dc.html artboard into a standalone static HTML page (expands sc-for/sc-if with renderVals output).
const fs=require('fs');
const [,, src, out, titleOverride]=process.argv;
const t=fs.readFileSync(src,'utf8');
const sm=t.match(/<script type="text\/x-dc"[^>]*>([\s\S]*?)<\/script>/); if(!sm) throw new Error('no script');
const pm=t.match(/\$preview":\{"width":(\d+),"height":(\d+)/); const W=+pm[1],H=+pm[2];
class DCLogic{constructor(){this.props={};this.state={};} setState(s){Object.assign(this.state,s)}}
const Component=new Function('DCLogic',sm[1]+'\nreturn Component;')(DCLogic);
const vals=new Component().renderVals();
const body=t.match(/<x-dc>([\s\S]*)<\/x-dc>/)[1];
const helm=(body.match(/<helmet>([\s\S]*?)<\/helmet>/)||[,''])[1];
let tpl=body.replace(/<helmet>[\s\S]*?<\/helmet>/,'');
const get=(p,scope)=>{const parts=p.trim().split('.');let v;if(parts[0]==='true')return true;if(parts[0]==='false')return false;
  v=(parts[0] in scope)?scope[parts[0]]:vals[parts[0]];for(let i=1;i<parts.length&&v!=null;i++)v=v[parts[i]];return v;};
const esc=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
function findClose(s,from){ // from = index after the opening tag; returns [contentEnd, closeEnd]
  let depth=1,re=/<(\/?)sc-(for|if)\b[^>]*>/g;re.lastIndex=from;let m;
  while((m=re.exec(s))){ if(m[1]) depth--; else depth++; if(depth===0) return [m.index,re.lastIndex]; }
  throw new Error('unclosed sc tag');}
function render(s,scope){
  let o='',i=0;const re=/<sc-(for|if)\b([^>]*)>/g;
  while(true){re.lastIndex=i;const m=re.exec(s);if(!m){o+=sub(s.slice(i),scope);break;}
    o+=sub(s.slice(i,m.index),scope);
    const [ce,end]=findClose(s,re.lastIndex);const inner=s.slice(re.lastIndex,ce);
    if(m[1]==='if'){const v=get(m[2].match(/value="\{\{([^}]*)\}\}"/)[1],scope);if(v)o+=render(inner,scope);}
    else{const lm=m[2].match(/list="\{\{([^}]*)\}\}"/)[1],as=m[2].match(/as="([^"]*)"/)[1];const arr=get(lm,scope)||[];
      arr.forEach((it,ix)=>{o+=render(inner,Object.assign({},scope,{[as]:it,$index:ix}));});}
    i=end;}
  return o;}
function sub(s,scope){return s.replace(/\{\{([^}]*)\}\}/g,(m,p)=>{const v=get(p,scope);return v==null?'':esc(v);});}
let html=render(tpl,{});
if(/\{\{|<sc-|<x-dc/.test(html)) throw new Error('unresolved template syntax');
const title=titleOverride||(t.match(/<title>([^<]*)<\/title>/)||[,'Architecture'])[1];
const page=`<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>${title}</title>
${helm}
<style>html,body{margin:0;background:#E9EDF3}#wrap{transform-origin:0 0;width:${W}px;height:${H}px}#sizer{overflow:hidden}</style>
</head>
<body>
<div id="sizer"><div id="wrap">
${html}
</div></div>
<script>
(function(){var W=${W},H=${H},w=document.getElementById('wrap'),s=document.getElementById('sizer');
function fit(){var k=Math.min(1,window.innerWidth/W);w.style.transform='scale('+k+')';s.style.width=(W*k)+'px';s.style.height=(H*k)+'px';}
window.addEventListener('resize',fit);fit();})();
</script>
</body>
</html>
`;
fs.writeFileSync(out,page);console.log(out,page.length,'bytes',W+'x'+H);
