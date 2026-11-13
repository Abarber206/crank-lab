# patch192: battle-royale bots that play more like players
#  - two weapons: a long gun and a shotgun, and they swap to the shotgun up close and back to the long gun at range
#  - they gather materials as they go (and from chests) and build like players: a wall when they're shot, a ramp to take
#    height if they're any good, ramp rushes when they push someone, a wall behind them when they run, and a box around
#    themselves to heal in
#  - their aim settles while they hold on a target and stay still, and spreads when they move or spray
rep("""const brRank=w=>w?RARITIES.indexOf((WEAPONS[w]||{}).rarity)+(WEAPONS[w].pellets>1?0.3:0):-1;""","""const brRank=w=>w?RARITIES.indexOf((WEAPONS[w]||{}).rarity)+(WEAPONS[w].pellets>1?0.3:0):-1;
const brCls=w=>w&&WEAPONS[w]?(WEAPONS[w].pellets>1?'sg':'lg'):null, brSlotOf=(b,w)=>{ const c=brCls(w); return brCls(b.wpn)===c?'wpn':brCls(b.wpn2)===c?'wpn2':null; };
// a bot builds the way you do: face the piece, place it, pay for it
function brBuild(b,type,yaw,pitch){ if((b.mats||0)<BUILD_COST||b.sky||b.bus||b.swim) return false; const oy=b.yaw, op=b.pitch; b.yaw=yaw; b.pitch=pitch||0; let ok=false; try{ ok=tryPlace(type,b); }catch(e){} b.yaw=oy; b.pitch=op; if(ok){ b.mats-=BUILD_COST; b.buildT=performance.now(); } return ok; }
const brYawTo=(b,x,z)=>Math.atan2(-(x-b.pos.x),-(z-b.pos.z));""")
# loot: a better gun of either kind
rep("""drops.forEach(d=>{ if(!brGunOk(d.item)||d.pending||!d.landed) return; if(b.wpn&&brRank(d.item)<=brRank(b.wpn)) return;""","""drops.forEach(d=>{ if(!brGunOk(d.item)||d.pending||!d.landed) return; { const sl=brSlotOf(b,d.item); if(sl&&brRank(d.item)<=brRank(b[sl])) return; }""")
rep("""else if(goal.act==='drop'&&b.prog>0.3&&b.loot&&drops.has(b.loot.d.id)){ const d=b.loot.d; if(b.wpn){ const p=b.pos.clone(); p.y+=0.6; netDrop(b.wpn,WEAPONS[b.wpn].mag||10,p,new THREE.Vector3(0,2,0),true); }""",
"""else if(goal.act==='drop'&&b.prog>0.3&&b.loot&&drops.has(b.loot.d.id)&&b.wpn&&!brSlotOf(b,b.loot.d.item)&&!b.wpn2){ const d=b.loot.d; b.wpn2=b.wpn; b.ammo2=b.ammo; b.wpn=null; // a second kind of gun: keep both
      b.wpn=d.item; const W=WEAPONS[d.item]; b.ammo=W.mag||30; b.reloadT=0; b.fireT=0.5; removeDrop(d.id); sfxAt('pickup',b.pos); b.loot=null; b.prog=0; }
    else if(goal.act==='drop'&&b.prog>0.3&&b.loot&&drops.has(b.loot.d.id)){ const d=b.loot.d; if(brSlotOf(b,d.item)==='wpn2'){ const t=b.wpn; b.wpn=b.wpn2; b.wpn2=t; const ta=b.ammo; b.ammo=b.ammo2||0; b.ammo2=ta; } // (the one it replaces in hand)
      if(b.wpn){ const p=b.pos.clone(); p.y+=0.6; netDrop(b.wpn,WEAPONS[b.wpn].mag||10,p,new THREE.Vector3(0,2,0),true); }""")
rep("""openChest(b.loot.c,true); b.heals+=1;""","""openChest(b.loot.c,true); b.heals+=1; b.mats=Math.min(500,(b.mats||0)+30);""")
rep("""Object.assign(b,{hp:100,sh:0,alive:true,wpn:null,ammo:0,""","""Object.assign(b,{wpn2:null,ammo2:0,mats:0,aimK:0,spray:0,buildT:0,boxT:0,rushT:0,flee:false,hp:100,sh:0,alive:true,wpn:null,ammo:0,""")
# gathering materials while they roam (stands for farming)
rep("""    b.tgt=bv>=1?best:null; b.sus=bv>=0.3?best:null;""","""    b.tgt=bv>=1?best:null; b.sus=bv>=0.3?best:null;
    if(!b.tgt&&!b.sky) b.mats=Math.min(400,(b.mats||0)+(b.loot?0:3)); // (gathering as they go)""")
# shot at: wall up, ramp for height
rep("""function brHurtBot(b,dmg,from,w){ if(!b.alive) return; animEvent(b.h,'hurt'); b.hurtAt=performance.now();""","""function brHurtBot(b,dmg,from,w){ if(!b.alive) return; animEvent(b.h,'hurt'); const ph=b.hurtAt||0; b.hurtAt=performance.now();
  { const src=from||P, now=b.hurtAt; if(!b.flee&&now-(b.buildT||0)>900&&now-ph>250&&Math.random()<0.25+0.7*b.skill&&src&&src.pos){ const y=snapYaw(brYawTo(b,src.pos.x,src.pos.z)); if(brBuild(b,'wall',y,0)&&b.skill>0.45&&Math.random()<b.skill) setTimeout(()=>{ if(b.alive) brBuild(b,'ramp',y,0); },180+Math.random()*200); } }""")
# the fight: weapon choice, rushes, a wall when running, a box to heal in
rep("""    { const eh=b.hp+b.sh, th=(T.hp||0)+(T.sh||0), hurtAgo=now-(b.hurtAt||0);""","""    { const dT=T.pos.distanceTo(b.pos), want=dT<13?'sg':'lg'; // the right gun for the range
      if(b.wpn2&&brCls(b.wpn)!==want&&brCls(b.wpn2)===want&&b.reloadT<=0&&now-(b.swapAt||0)>900){ const t=b.wpn; b.wpn=b.wpn2; b.wpn2=t; const ta=b.ammo; b.ammo=b.ammo2||0; b.ammo2=ta; if(b.ammo<=0){ b.ammo=WEAPONS[b.wpn].mag||10; } b.fireT=Math.max(b.fireT,0.35); b.swapAt=now; sfxAt('equip',b.pos); }
      // ramp rush: closing in on someone in the open, skilled bots ramp toward them
      if(!b.flee&&b.skill>0.5&&b.los&&dT>9&&dT<45&&goal&&now-(b.rushT||0)>650&&b.onGround&&(b.mats||0)>=BUILD_COST*3&&Math.random()<b.skill*0.6){ b.rushT=now; brBuild(b,'ramp',snapYaw(brYawTo(b,T.pos.x,T.pos.z)),0); } }
    { const eh=b.hp+b.sh, th=(T.hp||0)+(T.sh||0), hurtAgo=now-(b.hurtAt||0);""")
rep("""      if(!b.flee&&!b.brave&&eh<40&&hurtAgo<1200&&th>eh+15) b.flee=true;                            // nearly finished, by someone healthier: run""","""      if(!b.flee&&!b.brave&&eh<40&&hurtAgo<1200&&th>eh+15){ b.flee=true; brBuild(b,'wall',snapYaw(brYawTo(b,T.pos.x,T.pos.z)),0); } // nearly finished, by someone healthier: wall off and run""")
rep("""    if(b.hp<45&&b.heals>0&&!b.los&&now-(b.hurtAt||0)>2500){ b.healT+=dt; goal=null; strafe=0; crouch=true;""","""    if(b.hp<45&&b.heals>0&&!b.los&&now-(b.hurtAt||0)>2500){ if(!b.healT&&now-(b.boxT||0)>8000&&b.onGround){ b.boxT=now; for(let q=0;q<4;q++) brBuild(b,'wall',q*Math.PI/2,0); } // box up, then heal
      b.healT+=dt; goal=null; strafe=0; crouch=true;""")
# aim: settles on a held target, spreads when moving or spraying
rep("""  const moving=Math.min(1,Math.hypot(T.vel.x,T.vel.z)/6), err=(0.075-0.06*b.skill)*(1+0.8*moving)*(T===P&&P.crouch?1.1:1),""","""  if(b.aimT!==T){ b.aimT=T; b.aimK=0; } const selfMv=Math.min(1,Math.hypot(b.vel.x,b.vel.z)/5), nowA=performance.now(); b.spray=Math.max(0,(b.spray||0)-(nowA-(b.lastShotA||nowA))/400)+1; b.lastShotA=nowA;
  const moving=Math.min(1,Math.hypot(T.vel.x,T.vel.z)/6), err=(0.075-0.06*b.skill)*(1+0.8*moving)*(T===P&&P.crouch?1.1:1)*(1.35-0.55*(b.aimK||0))*(1+0.35*selfMv)*(1+0.04*Math.min(10,b.spray)),""")
rep("""  muzzleFlash(b.h); sfxAt(gunSndKey(W),b.pos);""","""  b.aimK=Math.min(1,(b.aimK||0)+0.12+0.15*b.skill); muzzleFlash(b.h); sfxAt(gunSndKey(W),b.pos);""")
# behind a wall: shoot through it (break it) if they saw you there a moment ago, as players do; the gun swap has some
# hysteresis so it doesn't flip at one distance
rep("""  if(T&&b.los&&b.react<=0&&b.reloadT<=0&&b.fireT<=0&&Math.abs(dy)<0.35&&!b.swim){""","""  if(T&&(b.los||b.wpn&&b.lastSeen&&now-b.lastSeen.t<4000&&!b.flee&&T.pos.distanceTo(b.pos)<35)&&b.react<=0&&b.reloadT<=0&&b.fireT<=0&&Math.abs(dy)<0.35&&!b.swim){""")
rep("""const dT=T.pos.distanceTo(b.pos), want=dT<13?'sg':'lg';""","""const dT=T.pos.distanceTo(b.pos), want=dT<11?'sg':dT>16?'lg':brCls(b.wpn);""")
