# ---------- 54. buggies take damage: hard crashes, landings and zombies wear them down; they blacken and dent, smoke, then
#               burn out (riders thrown clear) and come back to their garage a minute later ----------
rep("    home:{x,y,z,yaw},solid:","    hp:KART_HP,dead:0,home:{x,y,z,yaw},solid:")
rep("const KMAX=17.5,","const KART_HP=420;\nconst KMAX=17.5,")
# damage from hard hits (walls, other buggies, landings) and from ramming zombies
rep("if(wasAir&&k.vy<-3.5){ sfxAt('kart_land',","if(wasAir&&k.vy<-3.5){ if(k.vy<-11) kartDamage(k,(-k.vy-11)*12); sfxAt('kart_land',")
rep("k.vx*=0.6; k.vz*=0.6; k.sqV-=1.2; burst(z.pos.clone().setY(z.pos.y+1),6,4,0.08,goreMat); }); } }","k.vx*=0.6; k.vz*=0.6; k.sqV-=1.2; kartDamage(k,6); burst(z.pos.clone().setY(z.pos.y+1),6,4,0.08,goreMat); }); } }")
rep("function kartNet(){","""function kartDamage(k,n){ if(k.dead||n<=0) return; k.hp=Math.max(0,k.hp-n); kartLook(k); if(k.hp<=0) kartWreck(k); }
// the look of the damage: paint scorches darker, the body sits askew, smoke from the engine (grey, then black with sparks)
function kartLook(k){ const f=1-k.hp/KART_HP; if(f<0.2&&!k.dmgMat) return;
  if(!k.dmgMat){ k.body.traverse(m=>{ if(m.isMesh&&m.material&&KART_PAINT.some(c=>m.material.color&&m.material.color.getHex()===c)){ k.dmgMat=m.material.clone(); k.paintCol=m.material.color.clone(); m.material=k.dmgMat; } }); }
  if(k.dmgMat) k.dmgMat.color.copy(k.paintCol).lerp(new THREE.Color(0x2a2522),Math.min(0.75,f*0.9));
  k.skew={x:(f>0.4?0.03:0)+(f>0.7?0.03:0),z:(f>0.5?-0.04:0)}; }
function kartWreck(k){ k.dead=60; const c=_kz.set(k.x,k.y+0.8,k.z).clone(); sfxAt('boom',c); burst(c,26,8,0.18,goreMat?matFor.metal.chip:undefined); burst(c,18,6,0.12);
  if(P.kart&&P.kart.k===k){ exitKart(true); P.vel.y=7; } k.vx=k.vz=0; k.g.visible=false; }
function kartNet(){""")
rep("+(k.thr||0).toFixed(1)]; }","+(k.thr||0).toFixed(1),Math.round(k.hp)]; }")
rep("k.tgt={x:kk[2],y:kk[3],z:kk[4],yaw:kk[5],pitch:kk[6],roll:kk[7],vx:kk[8],vz:kk[9],steer:kk[10],thr:kk[11]||0,t:performance.now()}; }","k.tgt={x:kk[2],y:kk[3],z:kk[4],yaw:kk[5],pitch:kk[6],roll:kk[7],vx:kk[8],vz:kk[9],steer:kk[10],thr:kk[11]||0,t:performance.now()}; if(kk[12]!=null&&kk[12]<k.hp){ k.hp=kk[12]; kartLook(k); if(k.hp<=0) kartWreck(k); } }")
# while wrecked: hidden, can't be used; after a minute it's back in its garage, good as new
rep("  for(const k of karts){ const dCam=Math.hypot(k.x-camera.position.x,k.z-camera.position.z);","""  for(const k of karts){ if(k.dead>0){ k.dead-=dt; if(k.dead<=0){ k.dead=0; Object.assign(k,{x:k.home.x,y:k.home.y,z:k.home.z,yaw:k.home.yaw,pitch:0,roll:0,vx:0,vz:0,vy:0,hp:KART_HP,seats:[null,null],driver:null,local:false,tgt:null,skew:null}); if(k.dmgMat) k.dmgMat.color.copy(k.paintCol); k.g.visible=true; kartPose(k); } continue; }
  }
  for(const k of karts){ if(k.dead) continue; const dCam=Math.hypot(k.x-camera.position.x,k.z-camera.position.z);""")
rep("  k.body.position.y=k.sq; k.body.rotation.x=k.lean; k.body.rotation.z=k.croll;","  k.body.position.y=k.sq; k.body.rotation.x=k.lean+(k.skew?k.skew.x:0); k.body.rotation.z=k.croll+(k.skew?k.skew.z:0);\n  if(k.hp<KART_HP*0.5&&dCam<80&&Math.random()<dt*(k.hp<KART_HP*0.25?14:6)){ const p=kartPoint(k,0,1.05,0.8,_ku); kartPuff(p,k.hp<KART_HP*0.25?0x2a2a2a:0x8f8f8f,new THREE.Vector3((Math.random()-.5)*0.4,1.2,(Math.random()-.5)*0.4),0.35,1.6); if(k.hp<KART_HP*0.25&&Math.random()<0.2) burst(p,2,2,0.03); }")
rep("function kartTargets(consider){ if(!karts) return; for(const k of karts){ if(Math.abs","function kartTargets(consider){ if(!karts) return; for(const k of karts){ if(k.dead) continue; if(Math.abs")
rep("function resetKarts(){ if(!karts) return; if(P.kart){ kartForget(); P.onGround=false; } kartPark=null;\n  for(const k of karts){ Object.assign(k,{","function resetKarts(){ if(!karts) return; if(P.kart){ kartForget(); P.onGround=false; } kartPark=null;\n  for(const k of karts){ if(k.dmgMat) k.dmgMat.color.copy(k.paintCol); k.g.visible=true; Object.assign(k,{dead:0,hp:KART_HP,skew:null,")
rep("for(const o of karts) if(o!==k&&Math.abs(o.x-x)<4&&Math.abs(o.z-z)<4) ps.add(o.solid);","for(const o of karts) if(o!==k&&!o.dead&&Math.abs(o.x-x)<4&&Math.abs(o.z-z)<4) ps.add(o.solid);")
rep("if(karts) for(const k of karts) if(Math.abs(k.x-E.pos.x)<5","if(karts) for(const k of karts) if(!k.dead&&Math.abs(k.x-E.pos.x)<5")
rep("  for(const o of karts){ if(o===k||Math.abs(o.x-k.x)>4","  for(const o of karts){ if(o===k||o.dead||Math.abs(o.x-k.x)>4")
rep("  const ox=k.x, oz=k.z, nx=ox+k.vx*dt, nz=oz+k.vz*dt;","  const sp0=Math.hypot(k.vx,k.vz), ox=k.x, oz=k.z, nx=ox+k.vx*dt, nz=oz+k.vz*dt;")
rep("  { const dx=k.x-SPAWN[0], dz=k.z-SPAWN[2], d=Math.hypot(dx,dz); if(d>WORLD_EDGE){ k.x=SPAWN[0]","  { const lost=sp0-Math.hypot(k.vx,k.vz); if(lost>6) kartDamage(k,(lost-6)*16); } // a hard knock (a wall, a tree, another buggy) costs health\n  { const dx=k.x-SPAWN[0], dz=k.z-SPAWN[2], d=Math.hypot(dx,dz); if(d>WORLD_EDGE){ k.x=SPAWN[0]")
