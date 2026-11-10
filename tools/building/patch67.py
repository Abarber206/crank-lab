# ---------- 67. Buddy starts empty-handed like you: it swings its pickaxe at zombies, opens chests near you and picks up
# the first gun it finds (from chests or the floor), and goes back to the pickaxe if it's eliminated ----------
rep("active:false,down:null,dead:false,alive:true,flags:0,fireT:0,ammo:30,reloadT:0,tgt:null,thinkT:0,stuckT:0,prog:0,job:null,wpn:'ar',swingT:0}; }",
    "active:false,down:null,dead:false,alive:true,flags:0,fireT:0,ammo:30,reloadT:0,tgt:null,thinkT:0,stuckT:0,prog:0,job:null,wpn:null,swingT:0,loot:null,lootT:0}; }")
# a fresh spawn or a reboot: no gun (a revive keeps it)
rep("function allySpawnNear(x,z,fromSky){ const a=Math.random()*6.283; AB.hp=100; AB.sh=50;","function allySpawnNear(x,z,fromSky){ const a=Math.random()*6.283; AB.wpn=null; AB.loot=null; AB.hp=100; AB.sh=50;")
# shooting with whatever gun it has (shotguns hit hard up close, short range)
rep("  if(!blocked&&Math.random()<Math.max(0.35,0.9-dist/70)) zombieHurt(z,26,'ally');\n  AB.ammo--; AB.fireT=0.16+Math.random()*0.08; if(AB.ammo<=0){ AB.reloadT=2.1; AB.ammo=30; } }",
    "  const W=WEAPONS[AB.wpn]||WEAPONS.ar; if(!blocked&&Math.random()<Math.max(0.35,0.9-dist/70)) zombieHurt(z,Math.round(W.dmg*(W.pellets>1?Math.min(W.pellets,8)*0.7:1)*0.85),'ally');\n  AB.ammo--; AB.fireT=Math.max(0.14,W.rate)+Math.random()*0.08; if(AB.ammo<=0){ AB.reloadT=Math.min(2.6,W.reload||2.1); AB.ammo=W.mag||30; } }\nfunction allyRange(){ const W=WEAPONS[AB.wpn]; return !W?2.3:W.pellets>1?16:W.range>150?45:35; }\nconst allyGunOk=w=>{ const W=WEAPONS[w]; return !!W&&!W.throw&&w!=='rpg'&&w!=='glauncher'&&w!=='nade'; };")
rep("sfxAt('shot',AB.pos); animEvent(AB.h,'fire','ar');","sfxAt((WEAPONS[AB.wpn]&&WEAPONS[AB.wpn].snd)||'shot',AB.pos); animEvent(AB.h,'fire',AB.wpn||'ar');")
# no gun yet: go for a gun on the ground or a closed chest near you (never far from you), then fight
rep("    const dp=Math.hypot(P.pos.x-AB.pos.x,P.pos.z-AB.pos.z); if(dp>8||(isDead()&&dp>4)) goal={x:P.pos.x,z:P.pos.z,r:5};",
r"""    const dp=Math.hypot(P.pos.x-AB.pos.x,P.pos.z-AB.pos.z);
    if(!AB.wpn){ AB.lootT-=dt; if(AB.lootT<=0){ AB.lootT=0.5; let best=null, bd=1e9;
        drops.forEach(d=>{ if(!allyGunOk(d.item)||d.pending||!d.landed) return; const dP=Math.hypot(d.pos.x-P.pos.x,d.pos.z-P.pos.z), dA=Math.hypot(d.pos.x-AB.pos.x,d.pos.z-AB.pos.z); if(dP<45&&dA+0.3*dP<bd){ bd=dA+0.3*dP; best={kind:'drop',d,x:d.pos.x,z:d.pos.z}; } });
        if(!best) for(const c of chests){ if(c.open||!c.g.visible) continue; const dP=Math.hypot(c.x-P.pos.x,c.z-P.pos.z), dA=Math.hypot(c.x-AB.pos.x,c.z-AB.pos.z); if(dP<45&&dA+0.3*dP<bd){ bd=dA+0.3*dP; best={kind:'chest',c,x:c.x,z:c.z}; } }
        AB.loot=best; }
      const L=AB.loot, zNear=AB.tgt&&AB.tgt.alive&&AB.tgt.pos.distanceTo(AB.pos)<4;
      if(L&&!zNear){ if(L.kind==='drop'&&!drops.has(L.d.id)) AB.loot=null; else if(L.kind==='chest'&&L.c.open) AB.loot=null;
        else { goal={x:L.x,z:L.z,r:L.kind==='chest'?1.6:1.0,act:L.kind==='chest'?'chest':'take',T:L.kind==='chest'?1.2:0.25,L}; } } }
    if(!goal&&(dp>8||(isDead()&&dp>4))) goal={x:P.pos.x,z:P.pos.z,r:5};""")
rep("      else if(goal.act==='boot'){ rbSend({op:'boot',id:net.id,by:'ally',van:goal.v.id}); feed('<b>Buddy</b> rebooted you'); } } }",
r"""      else if(goal.act==='boot'){ rbSend({op:'boot',id:net.id,by:'ally',van:goal.v.id}); feed('<b>Buddy</b> rebooted you'); }
      else if(goal.act==='chest'&&!goal.L.c.open){ openChest(goal.L.c,true); AB.lootT=0.9; AB.loot=null; }
      else if(goal.act==='take'&&drops.has(goal.L.d.id)){ const d=goal.L.d; AB.wpn=d.item; const W=WEAPONS[d.item]; AB.ammo=W.mag||30; AB.reloadT=0; AB.fireT=0.4; removeDrop(d.id); sfxAt('pickup',AB.pos); feed('<b>Buddy</b> picked up '+(itemInfo(d.item).name||'a gun')); AB.loot=null; } } }""")
# with only the pickaxe: walk up to the zombie and swing
rep("  if(!AB.down&&!AB.sky&&!(goal&&goal.act)&&AB.tgt&&AB.tgt.alive&&AB.reloadT<=0&&AB.fireT<=0&&Math.abs(dy)<0.35&&AB.tgt.pos.distanceTo(AB.pos)<40) allyFire(AB.tgt);",
r"""  if(AB.swingT>0) AB.swingT-=dt;
  if(!AB.down&&!AB.sky&&!(goal&&goal.act)&&AB.tgt&&AB.tgt.alive&&AB.reloadT<=0&&AB.fireT<=0&&Math.abs(dy)<0.45){ const dz=AB.tgt.pos.distanceTo(AB.pos);
    if(AB.wpn&&dz<allyRange()) allyFire(AB.tgt);
    else if(!AB.wpn&&dz<zReach(AB.tgt)+0.9){ AB.swingT=SWING_T; AB.fireT=PICK_CD+0.05; setTimeout(()=>{ if(AB&&AB.tgt&&AB.tgt.alive&&AB.tgt.pos.distanceTo(AB.pos)<zReach(AB.tgt)+1.2){ zombieHurt(AB.tgt,30,'ally'); sfxAt('hit',AB.tgt.pos); } },PICK_IMPACT*1000); } }""")
# unarmed and a zombie is close: close in on it instead of hanging back
rep("    if(AB.tgt&&AB.tgt.alive) face=Math.atan2(-(AB.tgt.pos.x-AB.pos.x),-(AB.tgt.pos.z-AB.pos.z)); }",
    "    if(AB.tgt&&AB.tgt.alive){ face=Math.atan2(-(AB.tgt.pos.x-AB.pos.x),-(AB.tgt.pos.z-AB.pos.z)); if(!AB.wpn&&!goal&&AB.tgt.pos.distanceTo(AB.pos)<14&&AB.tgt.pos.distanceTo(AB.pos)>zReach(AB.tgt)+0.5) goal={x:AB.tgt.pos.x,z:AB.tgt.pos.z,r:zReach(AB.tgt)+0.5}; } }")
rep("crouch:!!(goal&&goal.act&&a==null),building:false,editing:false,gun:AB.down||AB.sky?false:'ar',ads:0,swingT:0,","crouch:!!(goal&&goal.act&&a==null),building:false,editing:false,gun:AB.down||AB.sky||!AB.wpn?false:AB.wpn,ads:0,swingT:Math.max(0,AB.swingT),")
rep("reload:AB.reloadT>0?{w:'ar',p:1-AB.reloadT/2.1}:null},dt); }","reload:AB.reloadT>0&&AB.wpn?{w:AB.wpn,p:Math.max(0,1-AB.reloadT/2.1)}:null},dt); AB.h.rig.pick.visible=!AB.wpn&&!AB.down&&!AB.sky; }")
