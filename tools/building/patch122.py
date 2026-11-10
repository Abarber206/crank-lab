# ---------- 122. aiming and shooting. Bullets are real: they leave at the gun's muzzle speed, take time to arrive, drop
# under gravity, and stop at the ground, water, a wall or a body (shotgun pellets and bots stay instant). Guns are zeroed,
# so a level aim is true out to the zero and you hold over beyond it; scopes show holdover marks and the range to what
# they are on, and drift a little unless you crouch. Recoil climbs in a pattern and settles back when you stop. ----------

# --- ballistics table: muzzle speed (m/s) and zero (m)
rep("const GUN_MODELS=['smg','mg','gatling',","""const BALL={sniper:[300,100],hunting:[280,100],dmr:[300,100],infantry:[290,75],ar:[260,50],burst:[260,50],heavyar:[250,50],mg:[250,50],lmg:[250,50],gatling:[230,40],
  smg:[200,30],csmg:[190,30],ssmg:[180,30],pistol:[180,30],revolver:[210,40],hcannon:[230,40]}, BULLET_G=9.8;
// how far above (+) or below (-) the line of sight a bullet is after d metres
function bulletRise(mdl,d){ const b=BALL[mdl]; if(!b) return 0; const ph=0.5*Math.asin(Math.min(1,BULLET_G*b[1]/(b[0]*b[0]))); return d*Math.tan(ph)-0.5*BULLET_G*Math.pow(d/(b[0]*Math.cos(ph)),2); }
const GUN_MODELS=['smg','mg','gatling',""")

# --- one place that credits a hit on a body (used by instant shots and by bullets when they land)
rep("  r.bodies.forEach((e,who)=>{ const dmg=Math.round(e.dmg); stat('h',dmg); hitMarker(dmg,e.head);\n    if(who.isZombie){","  r.bodies.forEach((e,who)=>creditHit(who,e,shBefore,P.wpn));\n  if(P.ammo[P.wpn]<=0) startReload();\n}\nfunction creditHit(who,e,shBefore,wpn){ { const dmg=Math.round(e.dmg); stat('h',dmg); hitMarker(dmg,e.head);\n    if(who.isZombie){")
rep("    else if(who===B){ dmgNum(B.pos.clone().setY(B.pos.y+(e.head?2.05:1.6)),dmg,e.head?'head':shBefore>0?'shield':'hp'); botHurt(dmg,net.id,P.wpn); }\n    else { dmgNum(who.pos.clone().setY(who.pos.y+(e.head?2.05:1.6)),dmg,e.head?'head':who.sh>0?'shield':'hp'); netSend({type:'hit',id:net.id,to:who.id,dmg,head:e.head,w:P.wpn}); } });\n  if(P.ammo[P.wpn]<=0) startReload();\n}",
    "    else if(who===B){ dmgNum(B.pos.clone().setY(B.pos.y+(e.head?2.05:1.6)),dmg,e.head?'head':shBefore>0?'shield':'hp'); botHurt(dmg,net.id,wpn); }\n    else { dmgNum(who.pos.clone().setY(who.pos.y+(e.head?2.05:1.6)),dmg,e.head?'head':who.sh>0?'shield':'hp'); netSend({type:'hit',id:net.id,to:who.id,dmg,head:e.head,w:wpn}); } } }")

# --- firing: a rifle or pistol round becomes a bullet
rep("  const r=fireWeapon(P,localHero,camera.position.clone(),aimDir(),P.wpn,camDist+0.4,tgts,spread);\n  if(net.role) netSend({type:'shot',id:net.id,w:P.wpn,e:r.ends});",
    "  const live=W.pellets===1&&BALL[W.model], r=live?fireBullet(W,tgts,spread):fireWeapon(P,localHero,camera.position.clone(),aimDir(),P.wpn,camDist+0.4,tgts,spread);\n  if(net.role) netSend({type:'shot',id:net.id,w:P.wpn,e:r.ends});")
rep("function shotSpread(W){",r"""/* Bullets. Anything within a few metres is hit at once (and must be clear from your own eyes, as before); otherwise the round
   flies: each frame it moves along its velocity, gravity pulls it down, and the stretch it covered is tested against
   bodies, builds, the ground and water. Damage falls off with the distance actually flown. */
const bullets=[], BULLET_NEAR=12, _bD=new THREE.Vector3(), _bN=new THREE.Vector3(), splashMat=new THREE.MeshBasicMaterial({color:0xdff1fa});
function bulletTargets(){ const t=[]; if(B&&B.active&&B.alive) t.push(B); net.players.forEach(pl=>{ if(pl.alive&&!sameTeam(pl)) t.push(pl); }); horde.zs.forEach(z=>{ if(z.alive) t.push(z); }); return t; }
function bulletDamage(W,dist){ return W.dmg*(dist<=W.f0?1:dist>=W.f1?W.fmin:1-(1-W.fmin)*(dist-W.f0)/(W.f1-W.f0)); }
function fireBullet(W,tgts,spread){
  const o=camera.position.clone(), d=spreadDir(aimDir(),spread), nearT=camDist+0.4, out={hit:false,dmg:0,head:false,point:null,bodies:new Map(),ends:[]};
  localHero.rig.muzzle.getWorldPosition(muzzleV); muzzleFlash(localHero);
  let r=castShot(o,d,BULLET_NEAR,nearT,tgts);
  { const eye=new THREE.Vector3(P.pos.x,P.pos.y+(P.crouch?1.12:1.6),P.pos.z), d2=r.point.clone().sub(eye), len=d2.length(); // clear from your own eyes to the aim point
    if(len>0.05){ d2.multiplyScalar(1/len); const r2=castShot(eye,d2,len+0.05,0.05,tgts); if(r2.kind==='piece'&&r2.t<len-0.05) r={...r2,t:r.t-len+r2.t}; } }
  out.ends.push([+r.point.x.toFixed(2),+r.point.y.toFixed(2),+r.point.z.toFixed(2)]);
  if(r.kind!=='none'){ tracer(muzzleV,r.point); const dmg=bulletDamage(W,r.t); // point blank: it is there already
    if(r.kind==='body'){ const dd=dmg*(r.head?W.head:1); out.hit=true; out.head=r.head; out.dmg=Math.round(dd); out.point=r.point; out.bodies.set(r.who,{dmg:dd,head:r.head,pt:r.point}); }
    else damagePiece(r.piece,dmg*(W.build||1),r.point);
    return out; }
  // away it goes, tipped up by the zero so it crosses the line of sight again at the zero distance
  const b=BALL[W.model], ph=0.5*Math.asin(Math.min(1,BULLET_G*b[1]/(b[0]*b[0])));
  _bN.set(0,1,0).addScaledVector(d,-d.y); if(_bN.lengthSq()<1e-6) _bN.set(0,0,0); else _bN.normalize();
  const v=d.clone().addScaledVector(_bN,Math.tan(ph)).normalize().multiplyScalar(b[0]), p=o.clone().addScaledVector(d,nearT);
  const g=new THREE.BufferGeometry().setFromPoints([muzzleV.clone(),muzzleV.clone()]), l=new THREE.Line(g,new THREE.LineBasicMaterial({color:0xfff0b0,transparent:true,opacity:0.95})); l.frustumCulled=false; scene.add(l);
  bullets.push({p,v,W,wpn:P.wpn,dist:nearT,t:0,l,off:muzzleV.clone().sub(p),tail:p.clone().add(muzzleV.clone().sub(p))});
  return out; }
function endBullet(i){ const b=bullets[i]; scene.remove(b.l); b.l.geometry.dispose(); b.l.material.dispose(); bullets.splice(i,1); }
function stepBullets(dt){ if(!bullets.length) return; dt=Math.min(dt,0.05); const tgts=bulletTargets();
  for(let i=bullets.length-1;i>=0;i--){ const b=bullets[i], W=b.W; b.t+=dt;
    _bD.copy(b.v).multiplyScalar(dt); _bD.y-=0.5*BULLET_G*dt*dt; const len=_bD.length(); _bD.multiplyScalar(1/len);
    const r=castShot(b.p,_bD,len,0,tgts); let tHit=r.kind==='none'?Infinity:r.t, what=r.kind;
    // the ground, and water lying on it
    { const ex=b.p.x+_bD.x*len, ey=b.p.y+_bD.y*len, ez=b.p.z+_bD.z*len, gy=terrainH(ex,ez), wy=waterAt(ex,ez), top=Math.max(gy,wy>-999?wy:-1e9);
      if(ey<top){ let lo=0, hi=len; for(let q=0;q<6;q++){ const m=(lo+hi)/2, x=b.p.x+_bD.x*m, z=b.p.z+_bD.z*m, w2=waterAt(x,z); if(b.p.y+_bD.y*m<Math.max(terrainH(x,z),w2>-999?w2:-1e9)) hi=m; else lo=m; }
        if(hi<tHit){ tHit=hi; what=wy>gy?'water':'ground'; } } }
    const hit=tHit<Infinity, adv=hit?tHit:len, flown=b.dist+adv;
    b.p.addScaledVector(_bD,adv); b.v.y-=BULLET_G*dt; b.dist=flown;
    // the streak: it leaves from the muzzle and joins the true path within a few metres
    { const k=Math.max(0,1-b.dist/28), head=_c.copy(b.p).addScaledVector(b.off,k), pa=b.l.geometry.attributes.position, tl=Math.min(b.dist,9+b.W.dmg*0.04);
      b.tail.copy(head).addScaledVector(_bD,-tl); pa.setXYZ(0,b.tail.x,b.tail.y,b.tail.z); pa.setXYZ(1,head.x,head.y,head.z); pa.needsUpdate=true; b.l.material.opacity=0.95*Math.min(1,0.35+b.dist/40); }
    if(hit){ const pt=b.p.clone(), dmg=bulletDamage(W,flown);
      if(what==='body'){ const dd=dmg*(r.head?W.head:1); creditHit(r.who,{dmg:dd,head:r.head,pt},B?B.sh:0,b.wpn); }
      else if(what==='piece') damagePiece(r.piece,dmg*(W.build||1),pt);
      else if(what==='water'){ burst(pt,5,3.2,0.07,splashMat); if(pt.distanceTo(P.pos)<60) sfxAt('step_water',pt); }
      else burst(pt,4,2.4,0.06,dustMat);
      endBullet(i); continue; }
    if(b.dist>W.range*1.25||b.t>4||b.p.y<-80) endBullet(i); } }
function shotSpread(W){""")
rep("stepPlayers(dt); stepTracers(dt);","stepPlayers(dt); stepTracers(dt); stepBullets(dt);")

# --- recoil: a pattern that walks, and a climb that settles back when you stop (less whatever you pulled down yourself)
rep("P.kick=(W.kick||0.014)*(1-0.55*adsK); P.yaw+=(Math.random()-.5)*(W.pellets>1||W.kick>0.05?0.01:0.007)*(1-0.6*adsK);",
    "P.shotN=first||W.pellets>1?0:(P.shotN||0)+1; P.kick=(W.kick||0.014)*(1-0.55*adsK)*(1+0.35*Math.min(1,P.shotN/8)); P.yaw+=(Math.sin(P.shotN*1.9+0.6)*0.55+(Math.random()-.5)*0.7)*(W.pellets>1||W.kick>0.05?0.01:0.007)*(1-0.6*adsK);")
rep("  if(P.kick>0){ const k=Math.min(P.kick,dt*0.5); P.pitch=Math.min(1.45,P.pitch+k); P.kick-=k; }",
    """  { if(P.pitchRef!==undefined){ const dl=P.pitch-P.pitchRef; if(dl<0&&P.rcl>0) P.rcl=Math.max(0,P.rcl+dl); } // pulling down against the climb is yours to keep
    if(P.kick>0){ const k=Math.min(P.kick,dt*0.5); P.pitch=Math.min(1.45,P.pitch+k); P.kick-=k; P.rcl=Math.min(0.5,(P.rcl||0)+k); }
    else if(P.rcl>0&&sinceShot>0.16){ const k=Math.min(P.rcl,dt*(0.12+P.rcl*5)); P.pitch-=k*0.9; P.rcl-=k; }
    // a scope drifts with your breathing: less crouched, more on the move
    if(scopeOn&&playing){ const A=0.0011*(P.crouch?0.35:1)*(1+2*Math.min(1,Math.hypot(P.vel.x,P.vel.z)/RUN)), t1=performance.now()/1000, t0=t1-dt; P.yaw+=A*(Math.sin(t1*1.3)-Math.sin(t0*1.3)); P.pitch+=A*0.7*(Math.sin(t1*2.6+0.5)-Math.sin(t0*2.6+0.5)); }
    P.pitchRef=P.pitch; }
  scopeTick(dt);""")

# --- scopes: holdover marks for the rifle in hand, and the range to what the scope is on
rep('<div id="scope" hidden><i class="h"></i><i class="v"></i><i class="m"></i><i class="c"></i><b id="scopeZ"></b></div>','<div id="scope" hidden><i class="h"></i><i class="v"></i><i class="m"></i><i class="c"></i><div id="scopeMk"></div><b id="scopeZ"></b><b id="scopeR"></b></div>')
rep("#scope{--R:min(34vh,34vw)}","""#scope{--R:min(34vh,34vw)}
#scopeMk span{position:absolute;left:50%;width:22px;height:1px;margin-left:-11px;background:#0b0d11}
#scopeMk span::after{content:attr(data-d);position:absolute;left:calc(100% + 5px);top:-5px;font:700 10px/1 var(--font-hud);color:#0b0d11}
#scopeMk span.L::after{left:auto;right:calc(100% + 5px)}
#scopeR{position:absolute;left:50%;top:calc(50% + var(--R) - 56px);transform:translateX(-50%);font:800 13px/1 var(--font-hud);color:rgba(255,235,160,.92);text-shadow:0 1px 3px #000;letter-spacing:.06em}""")
rep("function scopeLabel(){ const el=$('scopeZ'); if(!el||!scopeOn) return; el.textContent=(settings.fov/camera.fov).toFixed(1).replace(/\\.0$/,'')+'×'; }",
    r"""function scopeLabel(){ const el=$('scopeZ'); if(!el||!scopeOn) return; el.textContent=(settings.fov/camera.fov).toFixed(1).replace(/\.0$/,'')+'×'; scopeMarks(); }
// where the bullet will be at each hundred metres past the zero, drawn as rungs below the centre of the scope
function scopeMarks(){ const box=$('scopeMk'); if(!box) return; const W=WEAPONS[P.wpn], b=W&&BALL[W.model]; box.textContent=''; if(!b||!scopeOn) return;
  const H=renderer.domElement.clientHeight||innerHeight, f=Math.tan(camera.fov*Math.PI/360);
  let last=-99; for(let d=200;d<=Math.min(400,W.range);d+=100){ if(d<=b[1]) continue; const y=-bulletRise(W.model,d)/d/f*(H/2); if(y<5||y>H*0.3) continue; const s=document.createElement('span'), w=30-d/25; s.dataset.d=d/100; if((d/100)%2) s.className='L'; last=y; s.style.top='calc(50% + '+y.toFixed(1)+'px)'; s.style.width=w+'px'; s.style.marginLeft=-w/2+'px'; box.appendChild(s); } }
let scopeRT=0;
function scopeTick(dt){ if(!scopeOn){ scopeRT=0; return; } scopeRT-=dt; if(scopeRT>0) return; scopeRT=0.2;
  const o=camera.position, d=aimDir(), W=WEAPONS[P.wpn], far=Math.max(500,W.range), r=castShot(o.clone(),d,far,camDist+0.4,bulletTargets()); let t=r.kind==='none'?Infinity:r.t;
  for(let s=camDist+2;s<Math.min(t,far);s+=s<120?2:5){ const x=o.x+d.x*s, z=o.z+d.z*s, w=waterAt(x,z); if(o.y+d.y*s<Math.max(terrainH(x,z),w>-999?w:-1e9)){ t=s; break; } }
  $('scopeR').textContent=t<Infinity?Math.round(t-camDist)+' m':'– – –'; }""")

# --- without a scope: while aiming, a small pip under the crosshair shows where the round will land at the range you are on
rep('<div class="hud" id="cross">','<i id="dropPip" hidden></i><div class="hud" id="cross">')
rep("#cross{left:50%;top:50%;width:0;height:0;--sp:6px;--rp:0}","#cross{left:50%;top:50%;width:0;height:0;--sp:6px;--rp:0}\n#dropPip{position:fixed;left:50%;top:50%;width:5px;height:5px;margin:-3px 0 0 -3px;border-radius:50%;background:rgba(255,96,64,.95);box-shadow:0 0 0 1px rgba(0,0,0,.55);pointer-events:none;z-index:5}")
rep("function scopeTick(dt){ if(!scopeOn){ scopeRT=0; return; } scopeRT-=dt; if(scopeRT>0) return; scopeRT=0.2;\n  const o=camera.position, d=aimDir(), W=WEAPONS[P.wpn], far=Math.max(500,W.range),",
    "function scopeTick(dt){ const pip=$('dropPip'), W=WEAPONS[P.wpn], aim=playing&&mode==='gun'&&!edit&&W&&W.pellets===1&&BALL[W.model]&&(scopeOn||adsK>0.6);\n  if(!aim){ scopeRT=0; if(pip&&!pip.hidden) pip.hidden=true; return; } scopeRT-=dt; if(scopeRT>0) return; scopeRT=scopeOn?0.2:0.12;\n  const o=camera.position, d=aimDir(), far=Math.max(500,W.range),")
rep("  $('scopeR').textContent=t<Infinity?Math.round(t-camDist)+' m':'– – –'; }",
    "  if(scopeOn){ $('scopeR').textContent=t<Infinity?Math.round(t-camDist)+' m':'– – –'; pip.hidden=true; return; }\n  const y=t<Infinity?-bulletRise(W.model,t)/t/Math.tan(camera.fov*Math.PI/360)*((renderer.domElement.clientHeight||innerHeight)/2):0; pip.hidden=!(y>=3); if(y>=3) pip.style.transform='translateY('+y.toFixed(1)+'px)'; }")
