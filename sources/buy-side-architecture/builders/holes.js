const fs=require('fs');
global.DCLogic=class{constructor(){this.props={};this.state={}}};
const code=fs.readFileSync('/tmp/comp.js','utf8')+'\n;globalThis.__C=Component;';
(0,eval)(code);
const v=new __C().renderVals();
const holes=JSON.parse(fs.readFileSync('/tmp/holes.json'));
const scope={f:v.flowsT[0],s:v.stdA[0],a:v.assumptions[0]};
let bad=[];
for(const h of holes){const [h0,...rest]=h.split('.');
 let o; if(h0 in v)o=v[h0]; else if(h0 in scope)o=scope[h0]; else if(h==='true'||h==='false')continue; else{bad.push(h);continue}
 for(const k of rest){ if(o==null||!(k in o)){bad.push(h);break} o=o[k]; }}
console.log('keys',Object.keys(v),'T',v.flowsT.length,'F',v.flowsF.length,'C',v.flowsC.length,'stdA',v.stdA.length,'stdB',v.stdB.length,'asm',v.assumptions.length,'unresolved',bad);
console.log(JSON.stringify(v.flowsF[3]),JSON.stringify(v.flowsC[2]));
// all items in each loop
for(const f of [...v.flowsT,...v.flowsF,...v.flowsC])for(const k of ['n','from','to','label','std','hasStd','noStd'])if(!(k in f))console.log('miss',k);
