# patch131: tracers and bullet streaks always leave from the muzzle.
#  - an instant tracer keeps its start on the shooter's muzzle for the moment it is shown, so running doesn't leave it behind
#  - a flying round's streak is never drawn further back than the muzzle (its tail used to reach ~3.5 m behind the gun on the
#    first frames, because the tail length counted the distance from the camera, not from the gun)
rep("""function tracer(a,b,col){
  const g=new THREE.BufferGeometry().setFromPoints([a.clone(),b.clone()]);
  const m=new THREE.LineBasicMaterial({color:col||0xffe08a,transparent:true,opacity:.95});
  const l=new THREE.Line(g,m); scene.add(l); tracers.push({l,t:0.08});
}
function stepTracers(dt){
  for(let i=tracers.length-1;i>=0;i--){ const t=tracers[i]; t.t-=dt; t.l.material.opacity=Math.max(0,t.t/0.08);""",
"""function tracer(a,b,col,H){
  const g=new THREE.BufferGeometry().setFromPoints([a.clone(),b.clone()]);
  const m=new THREE.LineBasicMaterial({color:col||0xffe08a,transparent:true,opacity:.95});
  const l=new THREE.Line(g,m); l.frustumCulled=false; scene.add(l); tracers.push({l,t:0.08,H:H&&H.rig&&H.rig.muzzle?H:null});
}
const _trM=new THREE.Vector3();
function stepTracers(dt){
  for(let i=tracers.length-1;i>=0;i--){ const t=tracers[i]; t.t-=dt; t.l.material.opacity=Math.max(0,t.t/0.08);
    if(t.H&&t.t>0){ t.H.rig.muzzle.getWorldPosition(_trM); const pa=t.l.geometry.attributes.position; pa.setXYZ(0,_trM.x,_trM.y,_trM.z); pa.needsUpdate=true; } // it stays on the gun""")
rep("if(W.pellets===1||k<4){ tracer(muzzleV,r.point,tracerCol); ends.push(",
    "if(W.pellets===1||k<4){ tracer(muzzleV,r.point,tracerCol,H); ends.push(")
rep("if(r.kind!=='none'){ tracer(muzzleV,r.point); const dmg=bulletDamage(W,r.t);",
    "if(r.kind!=='none'){ tracer(muzzleV,r.point,undefined,localHero); const dmg=bulletDamage(W,r.t);")
rep("bullets.push({p,v,W,wpn:P.wpn,dist:nearT,t:0,l,off:muzzleV.clone().sub(p),tail:p.clone().add(muzzleV.clone().sub(p))});",
    "bullets.push({p,v,W,wpn:P.wpn,dist:nearT,t:0,l,off:muzzleV.clone().sub(p),tail:p.clone().add(muzzleV.clone().sub(p)),m0:muzzleV.clone(),H:localHero});")
rep("""function ghostBullet(m,from){""","""function ghostBullet(m,from,H){""")
rep("""bullets.push({p,v,W,wpn:m.w,dist:0,t:0,l,off:from.clone().sub(p),tail:from.clone(),ghost:true}); }""",
    """bullets.push({p,v,W,wpn:m.w,dist:0,t:0,l,off:from.clone().sub(p),tail:from.clone(),ghost:true,m0:from.clone(),H:H||null}); }""")
rep("""      b.tail.copy(head).addScaledVector(_bD,-tl); pa.setXYZ(0,b.tail.x,b.tail.y,b.tail.z);""",
"""      if(b.H&&b.H.rig&&b.H.rig.muzzle&&b.t<0.25) b.H.rig.muzzle.getWorldPosition(b.m0); // the gun it left, while it is still close
      if(b.m0&&head.distanceTo(b.m0)<=tl) b.tail.copy(b.m0); else b.tail.copy(head).addScaledVector(_bD,-tl); // never further back than the muzzle
      pa.setXYZ(0,b.tail.x,b.tail.y,b.tail.z);""")
rep("(m.e||[]).forEach(e=>tracer(muzzleV,new THREE.Vector3(e[0],e[1],e[2]),0xffb070)); if(m.b) ghostBullet(m,muzzleV);",
    "(m.e||[]).forEach(e=>tracer(muzzleV,new THREE.Vector3(e[0],e[1],e[2]),0xffb070,pl.h)); if(m.b) ghostBullet(m,muzzleV,pl.h);")
# the opponent bot shooting its way out of a box: from its gun, not its eyes
rep("damagePiece(r.piece,GUN.dmg*(WEAPONS.ar.build||1),r.point); B.fireT=GUN.rate*1.5; tracer(eye,r.point,0xff9f80);",
    "damagePiece(r.piece,GUN.dmg*(WEAPONS.ar.build||1),r.point); B.fireT=GUN.rate*1.5; if(B.h&&B.h.rig.muzzle){ B.h.rig.muzzle.getWorldPosition(muzzleV); tracer(muzzleV,r.point,0xff9f80,B.h); } else tracer(eye,r.point,0xff9f80);")
rep("tracer(_abE.clone(),blocked?r.point:eye.copy(_abE).addScaledVector(d,dist),0x9fd4ff);",
    "tracer(_abE.clone(),blocked?r.point:eye.copy(_abE).addScaledVector(d,dist),0x9fd4ff,AB.h);")
# a round that lands before its streak was ever drawn (or between frames) still shows its last stretch, muzzle side first
rep("""    if(hit){ const pt=b.p.clone(), dmg=bulletDamage(W,flown);""",
"""    if(hit){ const pt=b.p.clone(), dmg=bulletDamage(W,flown); if(b.tail.distanceToSquared(pt)>0.04) tracer(b.tail,pt,b.l.material.color.getHex(),b.m0&&b.tail.equals(b.m0)?b.H:null);""")
