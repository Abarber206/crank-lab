// build a site once: its pieces (put up by buildWorld like the houses) and its decoration
function planPOI(t){ if(t.blds) return t.blds; const D=poiDecor(); t.blds=POI_BUILD[t.kind](t,D); t.decor=D.flush(); return t.blds; }
// shots stop on solid decoration (containers, machines, the rocket...): a stand-in piece takes the hit
const POI_SOLID={key:'_deco',mat:'metal',type:'wall',deco:1,group:{position:new THREE.Vector3()}};
function decoShot(o,d,range,nearT){ let best=null; const ps=new Set(), n=Math.min(90,Math.ceil(range/4)); for(let k=0;k<=n;k++){ const t=k*4; staticsInto(ps,o.x+d.x*t,o.z+d.z*t,2.5); }
  ps.forEach(s=>{ if(!s.deco) return; for(const b of s.boxes){ const tb=rayBox(o,d,b); if(tb>=nearT&&tb<=range&&(!best||tb<best)) best=tb; } }); return best; }
