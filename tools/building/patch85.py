# ---------- 85. smarter Buddy: picks the creature that threatens you most, backs off and strafes instead of standing still,
# steps round things it's stuck on and catches up if left far behind, heals when out of a fight, swaps to a better gun,
# leaves chests you're standing at, covers you while reviving, and rides shotgun in your buggy (shooting from the seat) ----------
rep("AB.thinkT=0.3; let best=null, bd=40; horde.zs.forEach(z=>{ if(!z.alive) return; const d=z.pos.distanceTo(AB.pos); if(d<bd){ bd=d; best=z; } }); AB.tgt=best; }",
    "AB.thinkT=0.3; AB.tgt=allyPickTarget(); }")
rep("function stepAlly(dt){",r"""const allyRank=w=>['common','uncommon','rare','epic','legendary'].indexOf((WEAPONS[w]||{}).rarity);
function allyPickTarget(){ let best=null, bs=1e9; const pd=P.down&&!isDead();
  horde.zs.forEach(z=>{ if(!z.alive||(z.rise||0)>0.5) return; const dA=z.pos.distanceTo(AB.pos), dP=z.pos.distanceTo(P.pos); if(dA>48) return;
    let s=Math.min(dA,dP*(pd?0.4:0.8)); if(z.type==='hurler') s-=6; if(z.type==='runner'&&dP<12) s-=3; if(z===AB.tgt) s-=2; if(s<bs){ bs=s; best=z; } }); return best; }
function allyAnim(dt,extra){ animateRig(AB.h,Object.assign({slope:slopeFor(AB),pos:AB.pos,vel:AB.vel,yaw:AB.yaw,pitch:AB.pitch,onGround:AB.onGround,crouch:false,building:false,editing:false,gun:AB.wpn||false,ads:0,swingT:0,emote:null,
    reload:AB.reloadT>0&&AB.wpn?{w:AB.wpn,p:Math.max(0,1-AB.reloadT/2.1)}:null},extra),dt); }
function stepAlly(dt){""")
# riding in your buggy
rep("  const now=performance.now(), card=RB.cards.get(net.id);\n  let goal=null, face=null, fw=0, st=0, jump=false;",
r"""  const now=performance.now(), card=RB.cards.get(net.id);
  if(!AB.down&&now-(AB.hurtAt||0)>6000&&AB.hp<100) AB.hp=Math.min(100,AB.hp+6*dt); // catches its breath out of a fight
  if(AB.kart){ const k=AB.kart.k;
    if(!P.kart||P.kart.k!==k||k.dead||AB.down||isDead()||!karts.includes(k)){ if(k.seats[1]==='ally') k.seats[1]=null; AB.kart=null; kartPoint(k,1.8,0.3,0.2,AB.pos); AB.vel.set(0,0,0); AB.onGround=false; }
    else { seatWorld(k,1,AB.pos); AB.vel.set(0,0,0); AB.onGround=true; AB.thinkT-=dt; if(AB.thinkT<=0){ AB.thinkT=0.3; AB.tgt=allyPickTarget(); }
      if(AB.reloadT>0) AB.reloadT-=dt; AB.fireT-=dt; let look=k.yaw; const tg=AB.tgt&&AB.tgt.alive?AB.tgt:null;
      if(tg){ look=Math.atan2(-(tg.pos.x-AB.pos.x),-(tg.pos.z-AB.pos.z)); AB.yaw=look; if(AB.wpn&&AB.reloadT<=0&&AB.fireT<=0&&tg.pos.distanceTo(AB.pos)<allyRange()) allyFire(tg); } else AB.yaw=k.yaw;
      AB.pitch=0; allyAnim(dt,{yaw:tg&&AB.wpn?look:k.yaw,gun:tg&&AB.wpn?AB.wpn:false,seat:{k,s:1,look}}); AB.h.rig.pick.visible=false; return; } }
  let goal=null, face=null, fw=0, st=0, jump=false, kite=null, strafe=0;""")
rep("    const dp=Math.hypot(P.pos.x-AB.pos.x,P.pos.z-AB.pos.z);\n    if(!AB.wpn){ AB.lootT-=dt;",
r"""    const dp=Math.hypot(P.pos.x-AB.pos.x,P.pos.z-AB.pos.z);
    // left far behind (or wedged somewhere for a while): catch up, arriving just behind you
    AB.lostT=(dp>14&&Math.hypot(AB.vel.x,AB.vel.z)<1)?(AB.lostT||0)+dt:0;
    if((dp>75||AB.lostT>5)&&!P.sky){ const bx=P.pos.x+Math.sin(P.yaw)*4, bz=P.pos.z+Math.cos(P.yaw)*4, [gy]=groundAt(bx,bz,P.pos.y+1.2,near(bx,bz)); AB.pos.set(bx,Math.max(gy,terrainH(bx,bz))+0.05,bz); AB.vel.set(0,0,0); AB.lostT=0; AB.stuckT=0; }
    // you're driving: get in the passenger seat
    if(P.kart&&P.kart.seat===0&&!P.kart.k.seats[1]&&!P.kart.k.dead){ const k=P.kart.k, dk=Math.hypot(k.x-AB.pos.x,k.z-AB.pos.z);
      if(dk<4.5){ AB.kart={k,seat:1}; k.seats[1]='ally'; sfxAt('kart_in',AB.pos); return; } goal={x:k.x,z:k.z,r:2.5}; }
    if(!goal){ AB.lootT-=dt;""")
rep("if(dP<45&&dA+0.3*dP<bd){ bd=dA+0.3*dP; best={kind:'drop',d,x:d.pos.x,z:d.pos.z}; } });","if(dP<45&&(!AB.wpn||(allyRank(d.item)>allyRank(AB.wpn)&&dA<14))&&dA+0.3*dP<bd){ bd=dA+0.3*dP; best={kind:'drop',d,x:d.pos.x,z:d.pos.z}; } });")
rep("        if(!best) for(const c of chests){ if(c.open||!c.g.visible) continue;","        if(!best&&!AB.wpn) for(const c of chests){ if(c.open||!c.g.visible||Math.hypot(c.x-P.pos.x,c.z-P.pos.z)<8) continue;")
rep("    if(AB.tgt&&AB.tgt.alive){ face=Math.atan2(-(AB.tgt.pos.x-AB.pos.x),-(AB.tgt.pos.z-AB.pos.z));","    if(AB.wpn&&AB.tgt&&AB.tgt.alive&&!(goal&&goal.act)){ const dzz=AB.tgt.pos.distanceTo(AB.pos); if(dzz<6.5&&dp<16) kite=Math.atan2(AB.tgt.pos.x-AB.pos.x,AB.tgt.pos.z-AB.pos.z); else if(dzz<allyRange()&&!goal) strafe=Math.sin(now/650+1)>0?0.5:-0.5; }\n    if(AB.tgt&&AB.tgt.alive){ face=Math.atan2(-(AB.tgt.pos.x-AB.pos.x),-(AB.tgt.pos.z-AB.pos.z));")
rep("  if(a!=null){ const sp=AB.down?0.2:1; fw=Math.cos(a-AB.yaw)*sp; st=Math.sin(AB.yaw-a)*sp; }",
r"""  if(a!=null){ const sp=AB.down?0.2:1; fw=Math.cos(a-AB.yaw)*sp; st=Math.sin(AB.yaw-a)*sp; }
  if(kite!=null&&!AB.down){ fw=Math.cos(kite-AB.yaw); st=Math.sin(AB.yaw-kite); } else if(strafe&&a==null&&!AB.down) st=strafe;
  // wedged against something: step sideways round it for a moment
  if(AB.stuckT>0.9&&!(AB.sideT>0)){ AB.sideT=0.8; AB.sideDir=Math.random()<0.5?-1:1; } if(AB.sideT>0){ AB.sideT-=dt; if(a!=null&&!AB.down){ st=AB.sideDir; fw*=0.35; } }""")
rep("  if(!AB.down&&!AB.sky&&!(goal&&goal.act)&&AB.tgt&&AB.tgt.alive&&AB.reloadT<=0&&AB.fireT<=0&&Math.abs(dy)<0.45){","  if(!AB.down&&!AB.sky&&(!(goal&&goal.act)||(goal.act==='revive'&&a==null))&&AB.tgt&&AB.tgt.alive&&AB.reloadT<=0&&AB.fireT<=0&&(Math.abs(dy)<0.45||(goal&&goal.act))){")
rep("function allyHurt(dmg){ if(!AB||AB.down||AB.dead) return; animEvent(AB.h,'hurt');","function allyHurt(dmg){ if(!AB||AB.down||AB.dead) return; AB.hurtAt=performance.now(); animEvent(AB.h,'hurt');")
rep("function allySpawnNear(x,z,fromSky){ const a=Math.random()*6.283;","function allySpawnNear(x,z,fromSky){ const a=Math.random()*6.283; if(AB.kart){ if(AB.kart.k.seats[1]==='ally') AB.kart.k.seats[1]=null; AB.kart=null; }")
