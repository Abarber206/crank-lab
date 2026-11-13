# patch195: bots arm up fast and edit like players
#  - each bot that jumps picks a landing spot right on a gun lying on the floor or a chest near where its team is
#    going (one bot per spot), so it lands on loot like a player does
#  - unarmed bots look for loot much further, open chests quicker
#  - behind one of their own walls with someone on the other side, skilled bots edit a window in it, shoot through,
#    and close it again
rep("""function brJumpOut(E){ if(!E.bus) return;""","""// where a bot lands: on a gun on the floor or a closed chest close to the spot its team chose, one bot per spot
function brPickLanding(b){ const [lx,lz]=b.land; let best=null, bd=1e9; const taken=BR.claimed||(BR.claimed=new Set());
  drops.forEach(d=>{ if(!brGunOk(d.item)||d.pending||taken.has(d)||brHouseAt(d.pos.x,d.pos.z)) return; const dd=Math.hypot(d.pos.x-lx,d.pos.z-lz); if(dd<70&&dd<bd){ bd=dd; best=d; } });
  if(!best) for(const c of chests){ if(c.open||taken.has(c)||brHouseAt(c.x,c.z)) continue; const dd=Math.hypot(c.x-lx,c.z-lz)+8; if(dd<70&&dd<bd){ bd=dd; best=c; } }
  if(best){ taken.add(best); const x=best.pos?best.pos.x:best.x, z=best.pos?best.pos.z:best.z; b.land=[x+(Math.random()-.5)*1.5,z+(Math.random()-.5)*1.5]; b.landOn=best; } }
function brJumpOut(E){ if(!E.bus) return; if(E!==P&&E.isBR) try{ brPickLanding(E); }catch(e){}""")
rep("""consider('chest',c,c.x,c.y,c.z,b.wpn?14:35)""","""consider('chest',c,c.x,c.y,c.z,b.wpn?14:60)""")
rep("""consider('drop',d,d.pos.x,d.pos.y,d.pos.z,b.wpn?18:45)""","""consider('drop',d,d.pos.x,d.pos.y,d.pos.z,b.wpn?18:70)""")
rep("""if(goal.act==='chest'&&b.prog>1.1&&b.loot&&!b.loot.c.open)""","""if(goal.act==='chest'&&b.prog>0.7&&b.loot&&!b.loot.c.open)""")
rep("""function brBuild(b,type,yaw,pitch){""","""function brEditWall(b,p,mask){ if(!p||!pieces.has(p.key)||p.owner!=='bot'||p.type!=='wall'||!wallMaskValid(mask)) return false; const nb0=[...(conn.get(p)||[])];
  p.mask=mask; buildPiece(p); startAnim(p,80); phaseCheck(p); popPlayerOut(); sfxAt('confirm',b.pos); reshaped(p,nb0); return true; }
function brBuild(b,type,yaw,pitch){""")
rep("""      // ramp rush: closing in on someone in the open, skilled bots ramp toward them""","""      // edit: their own wall between them and someone they just saw: open a window, shoot, close it
      if(b.edit&&(now-b.edit.t>1700||!b.alive)){ const ep=b.edit.p; if(pieces.has(ep.key)&&ep.mask!==511) brEditWall(b,ep,511); b.edit=null; }
      if(!b.edit&&!b.los&&b.skill>0.55&&b.lastSeen&&now-b.lastSeen.t<3000&&dT<30&&now-(b.editT||0)>2600&&!b.flee){ const eye=new THREE.Vector3(b.pos.x,b.pos.y+1.5,b.pos.z), dv=new THREE.Vector3(T.pos.x-b.pos.x,T.pos.y+1.2-eye.y,T.pos.z-b.pos.z).normalize(), r_=castShot(eye,dv,3.2,0.2,[T]);
        if(r_&&r_.kind==='piece'&&r_.piece&&r_.piece.owner==='bot'&&r_.piece.type==='wall'&&r_.piece.mask===511){ b.editT=now; if(brEditWall(b,r_.piece,511&~(1<<4))){ b.edit={p:r_.piece,t:now}; b.los=true; b.react=Math.min(b.react||0,0.15); } } }
      // ramp rush: closing in on someone in the open, skilled bots ramp toward them""")
rep("""  BR.on=true; BR.out=false;""","""  BR.on=true; BR.claimed=new Set(); BR.out=false;""")
# teams drop where they can glide to; an unarmed bot keeps looting unless someone armed is close (it used to run from
# every other unarmed bot it saw, all landing long)
rep("""if(Math.hypot(x-qx,z-qz)<380||k===29) return {x,z,s};""","""if(Math.hypot(x-qx,z-qz)<220||k===29) return {x,z,s};""")
rep("""const T=b.tgt&&(b.tgt.alive||b.tgt===P)&&!(b.tgt===P&&(BR.out||P.hp<=0))?b.tgt:null;""","""const T0_=b.tgt&&(b.tgt.alive||b.tgt===P)&&!(b.tgt===P&&(BR.out||P.hp<=0))?b.tgt:null, dT0_=T0_?T0_.pos.distanceTo(b.pos):0;
  const T=T0_&&!b.wpn&&dT0_>3&&(!(T0_===P?mode==='gun':!!T0_.wpn)||dT0_>30)?null:T0_; // (unarmed: loot on, unless an armed one is close)""")
# someone they've fought, they remember for a good while and go back to finish (players re-peek; bots used to forget in
# ten seconds and wander off)
rep("""if(fresh&&d<70) a=Math.max(a,0.55); if(!sees) a-=0.04;""","""if(fresh&&d<70) a=Math.max(a,0.55); if(!sees) a-=a>=1?0.012:0.04;""")
rep("""else if(b.sus&&b.wpn&&b.lastSeen&&now-b.lastSeen.t<12000)""","""else if(b.sus&&b.wpn&&b.lastSeen&&now-b.lastSeen.t<25000&&b.hp+b.sh>=50)""")
# close by, they hear you (footsteps through a wall): they know where you are and keep after you
rep("""if(fresh&&d<70) a=Math.max(a,0.55); if(!sees) a-=a>=1?0.012:0.04;""","""if(fresh&&d<70) a=Math.max(a,0.55); if(!sees) a-=a>=1?0.012:0.04;
        if(!sees&&d<12&&!T.crouch&&(a>0.3||Math.hypot(T.vel.x,T.vel.z)>2)){ a=Math.max(a,1.05); b.lastSeen={x:T.pos.x,z:T.pos.z,t:now}; } // heard""")
