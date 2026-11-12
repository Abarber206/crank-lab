# patch159: Battle royale in teams: Solo, Duos, Trios or Squads (a choice under the mode). Your teammates are bots who
# drop with you, stay close, loot and fight alongside you (blue markers over them, blue on the map); bots in other
# teams play together the same way. Teammates never target each other and your shots pass by them. The match goes on
# until one team is left. The big map and minimap also shade the storm outside the circle.
rep("""      <label class="allyopt" id="allyOpt" hidden>""","""      <label class="allyopt" id="brTeamOpt" hidden><span><b>Team size</b><small>Bot teammates drop in with you</small></span><select id="brTeamSel"><option value="1">Solo</option><option value="2">Duos</option><option value="3">Trios</option><option value="4">Squads</option></select></label>
      <label class="allyopt" id="allyOpt" hidden>""")
rep("""function syncModeCards(){ const m=net.role==='client'?(party.mode||settings.mode):settings.mode; { const ao=$('allyOpt'); if(ao) ao.hidden=!(m==='horde'&&!net.role); }""",
"""function syncModeCards(){ const m=net.role==='client'?(party.mode||settings.mode):settings.mode; { const ao=$('allyOpt'); if(ao) ao.hidden=!(m==='horde'&&!net.role); const bo=$('brTeamOpt'); if(bo) bo.hidden=!(m==='br'&&!net.role); }""")
rep("""pop.appendChild($('allyOpt'));""","""pop.appendChild($('allyOpt')); pop.appendChild($('brTeamOpt'));""")
rep(""".allyopt input{width:20px;height:20px;accent-color:#3f8fff;flex:none}""",""".allyopt input{width:20px;height:20px;accent-color:#3f8fff;flex:none} #brTeamOpt span{flex:1} #brTeamOpt select{font:800 15px var(--font-hud);padding:6px 8px;border-radius:8px;background:#0d1a33;color:#fff;border:1px solid rgba(255,255,255,.25)}""")
rep("""function sameTeam(pl){ if(!pl||pl.id==='bot') return false;""","""function sameTeam(pl){ if(!pl||pl.id==='bot') return false; if(pl.isBR) return BR.on&&pl.team===0;""")
# the team setting
rep("""var BR={on:false,bots:[]""","""{ const s=$('brTeamSel'); s.value=String(settings.brTeam||1); s.addEventListener('change',()=>{ settings.brTeam=+s.value; saveSettings(); if(BR.on) BR.restart=true; }); s.addEventListener('click',e=>e.stopPropagation()); }
var BR={on:false,bots:[]""")
# teams at the start of a match: you and your teammates are team 0
rep("""  for(const b of BR.bots){ const [x,z]=brSpot(); Object.assign(b,{hp:100,""","""  const TS=Math.max(1,Math.min(4,settings.brTeam||1)); BR.ts=TS; let k=0; const mates=[];
  for(const b of BR.bots){ b.team=Math.floor((k+1)/TS); k++; if(b.team===0) mates.push(b); if(b.mark){ b.h.group.remove(b.mark); b.mark=null; } }
  const sp=randomDropSpot(), spots=new Map(); // each team drops together
  for(const b of BR.bots){ if(!spots.has(b.team)) spots.set(b.team,b.team===0?[sp[0],sp[1]]:brSpot()); }
  for(const b of BR.bots){ const s0=spots.get(b.team), a=Math.random()*6.283, rr=6+Math.random()*10, x=s0[0]+Math.cos(a)*rr, z=s0[1]+Math.sin(a)*rr; Object.assign(b,{hp:100,""")
rep("""    b.h.group.visible=true; animEvent(b.h,'revive'); skyDrop(x,z,SKY_MATCH*(0.75+Math.random()*0.3),b); b.land=[x,z]; }
  const sp=randomDropSpot(); if(skyDropAllowed())""","""    b.h.group.visible=true; animEvent(b.h,'revive'); skyDrop(x,z,SKY_MATCH*(b.team===0?0.98:0.75+Math.random()*0.3),b); b.land=[x,z]; }
  mates.forEach(b=>teamMarker(b)); if(skyDropAllowed())""")
rep("""  $('brHud').hidden=false; syncBot(); banner('Battle royale','20 drop in · one walks out',3);""","""  $('brHud').hidden=false; syncBot(); banner('Battle royale',TS===1?'20 drop in · one walks out':['','','Duos','Trios','Squads'][TS]+' · '+Math.ceil(20/TS)+' teams · one walks out',3);""")
rep("""function brAliveCount(){ let n=BR.out?0:1; for(const b of BR.bots) if(b.alive) n++; return n; }""","""function brAliveCount(){ let n=BR.out?0:1; for(const b of BR.bots) if(b.alive) n++; return n; }
function brTeamsLeft(){ const t=new Set(); if(!BR.out) t.add(0); for(const b of BR.bots) if(b.alive) t.add(b.team); return t; }""")
rep("""  if(!BR.over){ const n=brAliveCount();
    if(!BR.out&&n===1){""","""  if(BR.restart){ BR.restart=false; BR.on=false; brStart(); return; }
  if(!BR.over){ const n=brAliveCount(), TL=brTeamsLeft();
    if(TL.size===1&&TL.has(0)&&(!BR.out||[...BR.bots].some(b=>b.alive&&b.team===0))&&n>0&&(BR.ts>1||!BR.out)){ if(BR.out){ BR.over=true; BR.overT=8; banner('Your team won!','#1 · '+BR.kills+(BR.kills===1?' elimination':' eliminations'),7); sfx('win'); addPoints(80+40*BR.kills); } else {""")
rep("""banner('Victory Royale!','#1 · '+BR.kills+(BR.kills===1?' elimination':' eliminations'),7); sfx('win'); addPoints(150+40*BR.kills); }
    else if(BR.out&&BR.place&&BR.overT<=0){ BR.over=true; BR.overT=7; } }""","""banner('Victory Royale!','#1 · '+BR.kills+(BR.kills===1?' elimination':' eliminations'),7); sfx('win'); addPoints(150+40*BR.kills); BR.over=true; BR.overT=8; } }
    else if(BR.out&&!TL.has(0)&&BR.overT<=0){ BR.over=true; BR.overT=7; } }""")
# placement counts teams; your shots pass your teammates
rep("""BR.place=brAliveCount()+1;""","""const TL=brTeamsLeft(); BR.place=BR.ts>1?TL.size+(TL.has(0)?0:1):brAliveCount()+1; if(BR.ts>1&&TL.has(0)) feed('Your teammates fight on');""")
rep("""function bulletTargets(){ const t=[]; if(B&&B.active&&B.alive) t.push(B); if(BR.on) for(const b of BR.bots) if(b.alive&&b.h.group.visible) t.push(b);""","""function bulletTargets(){ const t=[]; if(B&&B.active&&B.alive) t.push(B); if(BR.on) for(const b of BR.bots) if(b.alive&&b.h.group.visible&&b.team!==0) t.push(b);""")
rep("""for(const b of BR.bots) if(b.alive&&b.h.group.visible) tgts.push(b); }""","""for(const b of BR.bots) if(b.alive&&b.h.group.visible&&b.team!==0) tgts.push(b); }""")
# foes: not your own team
rep("""function brFoes(b){ const a=[]; if(!BR.out&&P.hp>0&&!P.sky) a.push(P); for(const o of BR.bots) if(o!==b&&o.alive&&!o.sky) a.push(o); return a; }""",
"""function brFoes(b){ const a=[]; if(b.team!==0&&!BR.out&&P.hp>0&&!P.sky) a.push(P); for(const o of BR.bots) if(o!==b&&o.alive&&!o.sky&&o.team!==b.team) a.push(o); return a; }""")
# teammates: when a fight isn't on, stay with the team (yours stay with you)
rep("""  else if(b.loot){ goal={x:b.loot.x,z:b.loot.z,r:b.loot.kind==='chest'?1.5:0.9,act:b.loot.kind}; }""","""  else if(b.loot&&!(b.team===0&&!BR.out&&Math.hypot(P.pos.x-b.pos.x,P.pos.z-b.pos.z)>40)){ goal={x:b.loot.x,z:b.loot.z,r:b.loot.kind==='chest'?1.5:0.9,act:b.loot.kind}; }
  else if(b.team===0&&!BR.out&&!P.sky&&Math.hypot(P.pos.x-b.pos.x,P.pos.z-b.pos.z)>14){ goal={x:P.pos.x+Math.sin(b.h.group.id)*4,z:P.pos.z+Math.cos(b.h.group.id)*4,r:5}; run=Math.hypot(P.pos.x-b.pos.x,P.pos.z-b.pos.z)>30; }
  else if(BR.ts>1&&b.team!==0&&b.lead&&b.lead.alive&&b.lead!==b&&Math.hypot(b.lead.pos.x-b.pos.x,b.lead.pos.z-b.pos.z)>18){ goal={x:b.lead.pos.x,z:b.lead.pos.z,r:8}; }""")
rep("""  // decide where to go this frame""","""  if(!b.lead||!b.lead.alive||b.lead.team!==b.team){ b.lead=BR.bots.find(o=>o.alive&&o.team===b.team)||b; }
  // decide where to go this frame""")
# teammates help: they take on whoever is shooting you
rep("""function brHurtMe(dmg,b){ if(BR.out||P.hp<=0) return;""","""function brHurtMe(dmg,b){ if(BR.out||P.hp<=0) return; for(const m of BR.bots) if(m.alive&&m.team===0&&m.pos.distanceTo(b.pos)<80){ m.aw.set(b,Math.max(1.05,m.aw.get(b)||0)); m.lastSeen={x:b.pos.x,z:b.pos.z,t:performance.now()}; }""")
# teammates on the maps; storm shading
rep("""function brMiniMap(g,tx,tz,sc,dpr){ if(!BR.on) return; const S=BR.storm; g.save();""","""function brMiniMap(g,tx,tz,sc,dpr){ if(!BR.on) return; const S=BR.storm; g.save();
  g.fillStyle='rgba(120,40,210,.28)'; g.beginPath(); g.rect(-4000,-4000,9000,9000); g.arc(tx(S.cx),tz(S.cz),Math.max(0,S.r*sc),0,Math.PI*2,true); g.fill('evenodd');
  for(const b of BR.bots) if(b.alive&&b.team===0){ g.fillStyle='#3f8fff'; g.strokeStyle='#fff'; g.lineWidth=1.4*dpr; g.beginPath(); g.arc(tx(b.pos.x),tz(b.pos.z),4*dpr,0,7); g.fill(); g.stroke(); }""")
