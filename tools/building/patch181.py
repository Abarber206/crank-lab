# patch181: every decoration can be destroyed (see poiDecor/decoDamage in poi.js): bullets, the pickaxe (which farms it
# like a house) and explosions wear it down; it breaks for everyone in a party, and comes back with a new round.
# (poi.js is re-inserted by patch170 from the current files; decor.js by patch175.)
rep("""  { const dt=decoShot(o,d,Math.min(range,pt),nearT); if(dt!=null&&dt<pt-0.02){ pt=dt; pp=POI_SOLID; } }""",
    """  { const dh=decoShot(o,d,Math.min(range,pt),nearT); if(dh&&dh.t<pt-0.02){ pt=dh.t; pp=dh.s.dobj&&!dh.s.dobj.gone?dh.s.dobj.piece:POI_SOLID; } }""")
rep("""  if(!pieces.has(p.key)){ if(p.deco&&point) burst(point,3,3,0.07,hotSparkMat); return; }""","""  if(!pieces.has(p.key)){ if(p.dobj){ decoDamage(p.dobj,dmg,point); return; } if(p.deco&&point) burst(point,3,3,0.07,hotSparkMat); return; }""")
rep("""  const hit=aimHit(3.4);
  // the pickaxe chips builds""","""  const hit=aimHit(3.4);
  { const o=camera.position.clone(), d=aimDir(), dh=decoShot(o,d,camDist+3.4,Math.max(0,camDist*0.9)); // decoration in front of the pickaxe (and nearer than anything else)
    if(dh&&dh.s.dobj&&!dh.s.dobj.gone&&(!hit||dh.t<hit.distance)){ const pt=o.addScaledVector(d,dh.t); dmgNum(pt,PICK_DMG,'build'); sfx('pick_hit'); decoDamage(dh.s.dobj,PICK_DMG,pt,true); return; } }
  // the pickaxe chips builds""")
rep("""  propsNear(pos.x,pos.z,[]).forEach(pr=>{ const dd=Math.hypot(pr.x-pos.x,pr.z-pos.z); if(dd<X.r) propHit(pr,X.bld*0.5*(1-dd/X.r),new THREE.Vector3(pr.x,pr.base+1,pr.z),false); });""",
    """  propsNear(pos.x,pos.z,[]).forEach(pr=>{ const dd=Math.hypot(pr.x-pos.x,pr.z-pos.z); if(dd<X.r) propHit(pr,X.bld*0.5*(1-dd/X.r),new THREE.Vector3(pr.x,pr.base+1,pr.z),false); });
  { const ss=new Set(), seen=new Set(); staticsInto(ss,pos.x,pos.z,X.r+3); ss.forEach(s=>{ const o=s.dobj; if(!o||o.gone||seen.has(o)) return; seen.add(o); const dd=o.c.distanceTo(pos); if(dd<X.r+1.5) decoDamage(o,X.bld*(1-0.55*Math.min(1,dd/(X.r+1.5))),o.c.clone()); }); } // decoration in the blast""")
rep("""  else if(o.op==='break'){ const p=pieces.get(o.key); if(p) destroyPiece(p,o.pt?new THREE.Vector3(o.pt[0],o.pt[1],o.pt[2]):null); }""",
    """  else if(o.op==='break'){ const p=pieces.get(o.key); if(p) destroyPiece(p,o.pt?new THREE.Vector3(o.pt[0],o.pt[1],o.pt[2]):null); }
  else if(o.op==='dbreak'){ decoBreak(DECO.byId.get(o.id)); }""")
rep("""function clearBuilds(){ resetKarts();""","""function clearBuilds(){ resetKarts(); if(typeof decoReset==='function') decoReset();""")
