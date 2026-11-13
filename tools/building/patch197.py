# patch197: performance. A shot (and every bot's line-of-sight check) used to test the ray against every piece on the
# island; now it walks the grid cells along the ray and only looks at the pieces in and beside them (and not at the
# pictures and curtains). Bots check whether to edit a window a few times a second, not every frame.
rep("""function piecesNearRay(o,d,range){
  const out=[];
  for(const p of order){ _c.subVectors(p.group.position,o); const t=_c.dot(d); if(t<-4||t>range+4) continue;
    if(_c.addScaledVector(d,-t).lengthSq()<36){ for(const m of p.group.children) out.push(m); if(p.doorMeshes) out.push(...p.doorMeshes); } }
  return out;
}""","""const _prSeen=new Set();
function piecesNearRay(o,d,range){
  const out=[], seen=_prSeen; seen.clear(); const n=Math.ceil(Math.min(range,1000)/(CELL*0.8))+1;
  for(let k=0;k<=n;k++){ const t=Math.min(range,k*CELL*0.8)-2*(k===0), ci=Math.floor((o.x+d.x*t)/CELL), cj=Math.floor((o.z+d.z*t)/CELL);
    for(let a=ci-1;a<=ci+1;a++) for(let b=cj-1;b<=cj+1;b++){ const s=cellIndex.get(a+','+b); if(!s) continue;
      for(const p of s){ if(seen.has(p)||!p.group) continue; seen.add(p); _c.subVectors(p.group.position,o); const tt=_c.dot(d); if(tt<-4||tt>range+4) continue;
        if(_c.addScaledVector(d,-tt).lengthSq()<36){ for(const m of p.group.children) if(!m.userData.decor) out.push(m); if(p.doorMeshes) out.push(...p.doorMeshes); } } } }
  return out;
}""")
rep("""      if(!b.edit&&!b.los&&b.skill>0.55&&b.lastSeen&&now-b.lastSeen.t<3000&&dT<30&&now-(b.editT||0)>2600&&!b.flee){""","""      if(!b.edit&&!b.los&&b.skill>0.55&&b.lastSeen&&now-b.lastSeen.t<3000&&dT<30&&now-(b.editT||0)>2600&&!b.flee&&now-(b.editChk||0)>350&&(b.editChk=now)){""")
