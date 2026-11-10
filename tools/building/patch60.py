# ---------- 60. zombie horde: you start with no guns, and the first countdown waits until everyone has landed ----------
rep("  if(!net.role){ clearBuilds(); respawn(); if(skyDropAllowed()){","  if(!net.role){ clearBuilds(); respawn(); emptyLoadout(); if(skyDropAllowed()){")
rep("  respawn(); sfx('win'); if(skyDropAllowed()) matchDrop();","  respawn(); if(m.mode==='horde') emptyLoadout(); sfx('win'); if(skyDropAllowed()) matchDrop();")
rep("  if(horde.phase==='break'){ horde.t-=dt; if(horde.t<=0) startWave(); }",
"""  if(horde.phase==='break'){ horde.land=horde.wave===0&&hordeAirborne(); if(horde.land){ horde.landT=(horde.landT||0)+dt; if(horde.landT>90) horde.land=false; } // stuck in the air a long time: go anyway
    if(!horde.land){ horde.t-=dt; if(horde.t<=0){ horde.landT=0; startWave(); } } }""")
rep("function hordeStart(){","""// anyone still skydiving or gliding in (you, or a living squadmate)
function hordeAirborne(){ if(P.sky&&!isDead()) return true; let a=false; net.players.forEach(pl=>{ if(pl.id!=='bot'&&pl.alive&&(pl.flags&192)) a=true; }); return a; }
function hordeStart(){""")
rep("clearZombies(); horde.on=true; horde.wave=0; horde.kills=0; horde.phase='break'; horde.t=20;","clearZombies(); horde.on=true; horde.wave=0; horde.kills=0; horde.phase='break'; horde.t=20; horde.landT=0;")
rep("  return {type:'hz',w:horde.wave,ph:horde.phase,t:+horde.t.toFixed(1),","  return {type:'hz',ld:horde.land?1:0,w:horde.wave,ph:horde.phase,t:+horde.t.toFixed(1),")
rep("  horde.wave=m.w; horde.phase=m.ph; horde.t=m.t;","  horde.wave=m.w; horde.phase=m.ph; horde.t=m.t; horde.land=!!m.ld;")
rep("    sub='Wave '+(horde.wave+1)+' in '+t+'s';","    sub=horde.land?'Wave 1 starts when everyone lands':'Wave '+(horde.wave+1)+' in '+t+'s';")
