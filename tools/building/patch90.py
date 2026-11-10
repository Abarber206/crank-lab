# ---------- 90. Buddy never fires at something it can't see (it checks line of sight, and moves to get a clear shot),
# opens doors in its way, and gives up on a path that isn't working sooner ----------
rep("AB.thinkT=0.3; AB.tgt=allyPickTarget(); }","AB.thinkT=0.3; AB.tgt=allyPickTarget(); allyLook(); }",2)
rep("function allyPickTarget(){ let best=null, bs=1e9; const pd=P.down&&!isDead();","""function allySees(z){ const eye=new THREE.Vector3(AB.pos.x,AB.pos.y+1.5,AB.pos.z), t=new THREE.Vector3(z.pos.x,z.pos.y+1.1*z.sc,z.pos.z), dist=t.distanceTo(eye), r=castShot(eye,t.sub(eye).normalize(),dist,0.05,null); return !(r.kind==='piece'&&r.t<dist-0.6); }
function allyLook(){ const z=AB.tgt, now=performance.now(); if(z&&z.alive){ AB.los=allySees(z); if(AB.los) AB.noLosT=0; else { AB.noLosT=(AB.noLosT||0)+0.3; if(AB.noLosT>2.4){ z.hideUntil=now+4000; AB.noLosT=0; } } } else { AB.los=true; AB.noLosT=0; }
  // a closed door right in front of it: open it
  if(!AB.down&&!AB.sky) near(AB.pos.x,AB.pos.z,1).forEach(p=>{ if(!p.doors||Math.abs(p.l*LVL-AB.pos.y)>2.2) return; p.doors.forEach((dr,c)=>{ if(!dr||dr.open) return; const q=doorCenter(p,c); if(Math.hypot(q.x-AB.pos.x,q.z-AB.pos.z)<1.9&&Math.hypot(AB.vel.x,AB.vel.z)<2.5) toggleDoor(p,c,false); }); }); }
function allyPickTarget(){ let best=null, bs=1e9; const pd=P.down&&!isDead(), nowT=performance.now();""")
rep("let s=Math.min(dA,dP*(pd?0.4:0.8)); if(z.type==='hurler') s-=6;","let s=Math.min(dA,dP*(pd?0.4:0.8)); if(z.hideUntil>nowT) s+=25; if(z.type==='hurler') s-=6;")
rep("  const r=castShot(eye,d,dist,0.05,null), blocked=r.kind==='piece'&&r.t<dist-0.8;","  const r=castShot(eye,d,dist,0.05,null), blocked=r.kind==='piece'&&r.t<dist-0.8; if(blocked){ AB.los=false; AB.fireT=0.25; return; }")
rep("    if(AB.wpn&&dz<allyRange()) allyFire(AB.tgt);","    if(AB.wpn&&dz<allyRange()&&AB.los!==false) allyFire(AB.tgt);")
# armed but no clear shot: close in on the creature (round the corner) instead of standing and staring
rep("    if(AB.tgt&&AB.tgt.alive){ face=Math.atan2(-(AB.tgt.pos.x-AB.pos.x),-(AB.tgt.pos.z-AB.pos.z));","    if(AB.wpn&&AB.tgt&&AB.tgt.alive&&AB.los===false&&!goal&&dp<25){ goal={x:AB.tgt.pos.x,z:AB.tgt.pos.z,r:3}; kite=null; strafe=0; }\n    if(AB.tgt&&AB.tgt.alive){ face=Math.atan2(-(AB.tgt.pos.x-AB.pos.x),-(AB.tgt.pos.z-AB.pos.z));")
rep("    AB.lostT=(dp>14&&Math.hypot(AB.vel.x,AB.vel.z)<1)?(AB.lostT||0)+dt:0;\n    if((dp>75||AB.lostT>5)&&!P.sky){","    AB.lostT=(dp>10&&Math.hypot(AB.vel.x,AB.vel.z)<1)?(AB.lostT||0)+dt:0;\n    if((dp>75||AB.lostT>3.5)&&!P.sky){")
