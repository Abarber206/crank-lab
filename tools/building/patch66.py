# ---------- 66. a little more haze, and a bot teammate for solo Zombie horde ----------
rep("const HAZE_DENS=0.00095, HAZE_H=210;","const HAZE_DENS=0.00112, HAZE_H=215;")

# The teammate ("Buddy") drops in with you, follows you around and shoots zombies. It uses the same knocked / revive /
# reboot rules as a human teammate: it can be knocked (you hold Interact to revive it), bleed out into a reboot card
# (carry it to a van), and it comes for you: revives you when you're knocked, and if you bleed out it grabs your card and
# runs it to the nearest van. With nobody left standing the run ends as before.
rep('      <select id="modeSel" hidden>','''      <label class="allyopt" id="allyOpt" hidden><input type="checkbox" id="hordeBot"><span><b>Bot teammate</b><small>Plays horde with you · revives and reboots you, and you can do the same for it</small></span></label>
      <select id="modeSel" hidden>''')
rep(".modes{display:grid;",r""".allyopt{display:flex;align-items:center;gap:10px;padding:10px 14px;border-radius:10px;background:#15233a;border:1px solid rgba(255,255,255,.14);cursor:pointer}
.allyopt input{width:20px;height:20px;accent-color:#3f8fff;flex:none} .allyopt b{display:block;font:800 italic 17px/1.1 var(--font-hud);letter-spacing:.04em;text-transform:uppercase} .allyopt small{color:var(--muted);font-size:13px}
#menu.lobby .allyopt{background:rgba(4,18,64,.5);backdrop-filter:blur(8px)} #menu.lobby .allyopt small{color:rgba(225,236,255,.75)}
.modes{display:grid;""")
rep("function syncModeCards(){ const m=net.role==='client'?(party.mode||settings.mode):settings.mode;","function syncModeCards(){ const m=net.role==='client'?(party.mode||settings.mode):settings.mode; { const ao=$('allyOpt'); if(ao) ao.hidden=!(m==='horde'&&!net.role); }")
rep("initKarts(); initVans(); initForest();","initKarts(); initVans(); initForest(); { const hb=$('hordeBot'); hb.checked=!!settings.hordeBot; hb.addEventListener('change',()=>{ settings.hordeBot=hb.checked; saveSettings(); }); syncModeCards(); }")

# hook the teammate into the reboot rules
rep("function rbMatesUp(){ let n=0;","function rbMatesUp(){ let n=(AB&&AB.active&&!AB.down&&!AB.dead)?1:0;")
rep("function rbCanKnock(){ return !!net.role&&(horde.on||+settings.team>0)&&rbMatesUp()>0&&!P.sky&&!P.down; }",
    "function rbCanKnock(){ return (!!net.role&&(horde.on||+settings.team>0)||(!net.role&&horde.on&&!!AB&&AB.active))&&rbMatesUp()>0&&!P.sky&&!P.down; }")
rep("  if(net.role&&(horde.on||+settings.team>0)&&rbMatesUp()>0){",
    "  if((net.role&&(horde.on||+settings.team>0)||(!net.role&&horde.on&&AB&&AB.active))&&rbMatesUp()>0){")
rep("  setTimeout(rbRespawnNow,3000); }","  if(!net.role&&horde.on){ hordeOverSolo(); return; }\n  setTimeout(rbRespawnNow,3000); }")
rep("function rbRespawnNow(){ net.dead=false;","function rbRespawnNow(){ if(!net.role&&horde.on){ hordeOverSolo(); return; } net.dead=false;")
rep("  if(hurt(P,dmg)){ animEvent(localHero,'die'); horde.phase='over';","  if(hurt(P,dmg)){ if(rbCanKnock()){ rbKnock('zombie','zombie'); return; } animEvent(localHero,'die'); horde.phase='over';")
rep("function stepReboot(dt){ if(!net.role&&!RB.cards.size&&!P.down) return;","function stepReboot(dt){ if(!net.role&&!RB.cards.size&&!P.down&&!(AB&&AB.active)) return;")
rep("function rbTargets(consider){ if(!net.role) return;","function rbTargets(consider){ if(!net.role&&!(AB&&AB.active)) return;")
rep("  net.players.forEach(pl=>{ if(pl.id==='bot'||!pl.alive||!(pl.flags&256)||!sameTeam(pl)) return; const rv=RB.rev.get(pl.id)||0;",
    "  rbPeople().forEach(pl=>{ if(pl.id==='bot'||!pl.alive||!(pl.flags&256)||!sameTeam(pl)) return; const rv=RB.rev.get(pl.id)||0;")
rep("  net.players.forEach(pl=>{ const on=useHeld&&useTgt&&useTgt.kind==='revive'&&useTgt.pl===pl","  rbPeople().forEach(pl=>{ const on=useHeld&&useTgt&&useTgt.kind==='revive'&&useTgt.pl===pl")
rep("  else if(m.op==='grab'){ if(m.id===net.id&&RB.wait){","  else if(m.op==='grab'){ if(m.id==='ally'){ const c=RB.cards.get('ally'); if(AB&&AB.dead&&c&&!c.holder) rbSend({op:'held',id:'ally',by:m.by}); return; } if(m.id===net.id&&RB.wait){")
rep("  else if(m.op==='boot'){ if(m.id!==net.id||!RB.wait) return;","  else if(m.op==='boot'){ if(m.id==='ally'){ const v=VANS&&VANS[m.van]; if(AB&&AB.dead&&v){ allyReboot(v); rbSend({op:'done',id:'ally',van:m.van,by:m.by}); } return; } if(m.id!==net.id||!RB.wait) return;")
rep("  if(m.op==='rev'){ RB.rev.delete(m.id); if(m.id===net.id&&P.down){","  if(m.op==='rev'){ RB.rev.delete(m.id); if(m.id==='ally'&&AB&&AB.down){ allyRevived(); return; } if(m.id===net.id&&P.down){")
rep("const msg=hold?((hp&&hp.name)||'A teammate')+' has your card · heading to a van'","const msg=hold?((hp&&hp.name)||(hold==='ally'?'Buddy':'A teammate'))+' has your card · heading to a van'")
rep("  if(!pl||!pl.alive){ pl=null; net.players.forEach(q=>{ if(!pl&&q.id!=='bot'&&q.alive&&sameTeam(q)) pl=q; }); } if(!pl) return false;",
    "  if(mine&&mine.holder==='ally'&&AB&&AB.active) pl=AB;\n  if(!pl||!pl.alive){ pl=null; net.players.forEach(q=>{ if(!pl&&q.id!=='bot'&&q.alive&&sameTeam(q)) pl=q; }); if(!pl&&AB&&AB.active&&!AB.dead) pl=AB; } if(!pl) return false;")
# zombies chase and hit the teammate too (not while it's down)
rep("function hordeTargets(){ const a=[]; if(!(net.dead||P.hp<=0||P.down)) a.push(P);","function hordeTargets(){ const a=[]; if(!(net.dead||P.hp<=0||P.down)) a.push(P); if(AB&&AB.active&&!AB.down&&!AB.dead&&!AB.sky) a.push(AB);")
rep("  if(who===P) hordeHurtMe(dmg,from);\n","  if(who===P) hordeHurtMe(dmg,from);\n  else if(who===AB) allyHurt(dmg);\n")
# a fresh solo run: clear cards and waiting, and the teammate drops in again with you
rep("  if(!net.role){ clearBuilds(); respawn(); emptyLoadout();","  if(!net.role){ clearBuilds(); rbReset(); net.dead=false; if(AB) AB.active=false; respawn(); emptyLoadout();")
# on the map, and stepped every frame
rep("  if(B&&B.active&&B.h.group.visible) dot(B.pos.x,B.pos.z,'#ff4b3a');","  if(B&&B.active&&B.h.group.visible) dot(B.pos.x,B.pos.z,'#ff4b3a'); if(AB&&AB.active&&AB.h.group.visible) dot(AB.pos.x,AB.pos.z,'#3f8fff');",2)
rep("stepGrass(dt); stepChests(dt); stepReboot(dt);","stepGrass(dt); stepChests(dt); stepReboot(dt); stepAlly(dt);")

rep("\n/* ---------- controller (standard gamepad mapping) ----------",r"""
/* ---------- the horde teammate ---------- */
var AB=null;
function allyOn(){ return !!settings.hordeBot&&horde.on&&!net.role&&playing!==undefined; }
function rbPeople(){ const a=[...net.players.values()]; if(AB&&AB.active) a.push(AB); return a; }
function hordeOverSolo(){ if(horde.phase==='over') return; horde.phase='over'; horde.t=6; horde.best=Math.max(horde.best,horde.wave-1);
  banner('Overrun!','You survived '+(horde.wave-1)+(horde.wave-1===1?' wave':' waves')+' · '+horde.kills+' zombies',5); sfx('lose'); }
function makeAlly(){ const pool=OUTFITS.filter(o=>o.id!==settings.outfit), o=pool[Math.floor(Math.random()*pool.length)], h=heroFor(o,'steel'); h.outfit=o.id; h.pickaxe='steel'; h.group.visible=false; scene.add(h.group);
  AB={id:'ally',name:'Buddy',team:0,h,pos:new THREE.Vector3(),vel:new THREE.Vector3(),onGround:true,groundSlab:null,crouch:false,yaw:0,dyaw:0,pitch:0,rot:0,hp:100,sh:50,
      active:false,down:null,dead:false,alive:true,flags:0,fireT:0,ammo:30,reloadT:0,tgt:null,thinkT:0,stuckT:0,prog:0,job:null,wpn:'ar',swingT:0}; }
function allySpawnNear(x,z,fromSky){ const a=Math.random()*6.283; AB.hp=100; AB.sh=50; AB.down=null; AB.dead=false; AB.alive=true; AB.prog=0; AB.ammo=30; AB.reloadT=0; AB.vel.set(0,0,0);
  AB.h.group.visible=true; animEvent(AB.h,'revive'); const px=x+Math.cos(a)*4, pz=z+Math.sin(a)*4;
  if(fromSky&&skyDropAllowed()) skyDrop(px,pz,fromSky,AB); else { AB.sky=null; AB.pos.set(px,terrainH(px,pz)+0.05,pz); } }
function allyHurt(dmg){ if(!AB||AB.down||AB.dead) return; animEvent(AB.h,'hurt');
  if(hurt(AB,dmg)){ if(!P.down&&!isDead()){ AB.down={hp:RB_DOWN_HP}; AB.hp=RB_DOWN_HP; AB.sh=0; sfxAt('rb_down',AB.pos); feed('<b>Buddy</b> is down · hold Interact on them to revive'); }
    else { AB.down={hp:0}; allyBleedOut(); } } }
function allyRevived(){ AB.down=null; AB.hp=RB_UP_HP; AB.sh=0; animEvent(AB.h,'revive'); sfx('rb_up'); feed('You revived <b>Buddy</b>'); }
function allyBleedOut(){ AB.down=null; AB.dead=true; AB.alive=false; animEvent(AB.h,'die'); setTimeout(()=>{ if(AB&&AB.dead) AB.h.group.visible=false; },900);
  const [gy]=groundAt(AB.pos.x,AB.pos.z,AB.pos.y+0.5,near(AB.pos.x,AB.pos.z)); feed('<b>Buddy</b> was eliminated');
  rbSend({op:'card',id:'ally',n:'Buddy',t:0,o:outfitIdx(AB.h.outfit),p:[+AB.pos.x.toFixed(2),+Math.max(gy,AB.pos.y-40).toFixed(2),+AB.pos.z.toFixed(2)],ttl:RB_TTL}); }
function allyReboot(v){ const a=Math.random()*6.283; allySpawnNear(v.x+Math.cos(a)*2,v.z+Math.sin(a)*2,SKY_AUTO+25); }
const _abE=new THREE.Vector3(), _abD=new THREE.Vector3();
function allyFire(z){ const eye=_abE.set(AB.pos.x,AB.pos.y+1.5,AB.pos.z), tgt=new THREE.Vector3(z.pos.x,z.pos.y+1.1*z.sc,z.pos.z), dist=tgt.distanceTo(eye);
  const d=_abD.copy(tgt).sub(eye).normalize(); d.x+=(Math.random()-.5)*0.04; d.y+=(Math.random()-.5)*0.03; d.z+=(Math.random()-.5)*0.04; d.normalize();
  const r=castShot(eye,d,dist,0.05,null), blocked=r.kind==='piece'&&r.t<dist-0.8;
  AB.h.rig.muzzle&&AB.h.rig.muzzle.getWorldPosition(_abE); tracer(_abE.clone(),blocked?r.point:eye.copy(_abE).addScaledVector(d,dist),0x9fd4ff); muzzleFlash(AB.h); sfxAt('shot',AB.pos); animEvent(AB.h,'fire','ar');
  if(!blocked&&Math.random()<Math.max(0.35,0.9-dist/70)) zombieHurt(z,26,'ally');
  AB.ammo--; AB.fireT=0.16+Math.random()*0.08; if(AB.ammo<=0){ AB.reloadT=2.1; AB.ammo=30; } }
function stepAlly(dt){
  if(allyOn()&&!AB) makeAlly(); if(!AB) return;
  if(!allyOn()){ if(AB.active){ AB.active=false; AB.h.group.visible=false; AB.down=null; AB.dead=false; const c=RB.cards.get('ally'); if(c){ rbKill(c); RB.cards.delete('ally'); RB.carry.delete('ally'); } if(AB.mark){ AB.h.group.remove(AB.mark); AB.mark=null; } } return; }
  if(!AB.active){ if(!playing&&!P.sky) return; AB.active=true; teamMarker(AB); allySpawnNear(P.pos.x,P.pos.z,P.sky?Math.max(SKY_AUTO+20,P.pos.y-terrainH(P.pos.x,P.pos.z)):0); }
  AB.flags=AB.down?256:0; AB.alive=!AB.dead; AB.dyaw=AB.yaw;
  if(AB.dead){ if(!RB.cards.has('ally')) allySpawnNear(P.pos.x,P.pos.z,SKY_BACK); return; } // its card expired: back in from the sky
  const now=performance.now(), card=RB.cards.get(net.id);
  let goal=null, face=null, fw=0, st=0, jump=false;
  if(AB.down){ AB.down.hp-=dt*RB_DOWN_HP/RB_BLEED; AB.hp=Math.max(0,AB.down.hp); if(AB.down.hp<=0||(P.down||isDead())&&false){ allyBleedOut(); return; }
    if(Math.hypot(P.pos.x-AB.pos.x,P.pos.z-AB.pos.z)>1.6&&!isDead()) goal={x:P.pos.x,z:P.pos.z,r:1.6}; }
  else if(AB.sky){ goal={x:P.pos.x,z:P.pos.z,r:3}; }
  else if(P.down&&!isDead()) goal={x:P.pos.x,z:P.pos.z,r:1.2,act:'revive',T:RB_REV_T};
  else if(RB.wait&&card&&!card.holder) goal={x:card.x,z:card.z,r:1.1,act:'grab',T:RB_GRAB_T,card};
  else if(RB.wait&&card&&card.holder==='ally'){ let v=null, bd=1e9; (VANS||[]).forEach(q=>{ const d=Math.hypot(q.tx-AB.pos.x,q.tz-AB.pos.z); if(d<bd){ bd=d; v=q; } }); if(v) goal={x:v.tx,z:v.tz,r:1.3,act:'boot',T:RB_BOOT_T,v}; }
  else { // follow you and fight
    AB.thinkT-=dt; if(AB.thinkT<=0){ AB.thinkT=0.3; let best=null, bd=40; horde.zs.forEach(z=>{ if(!z.alive) return; const d=z.pos.distanceTo(AB.pos); if(d<bd){ bd=d; best=z; } }); AB.tgt=best; }
    const dp=Math.hypot(P.pos.x-AB.pos.x,P.pos.z-AB.pos.z); if(dp>8||(isDead()&&dp>4)) goal={x:P.pos.x,z:P.pos.z,r:5};
    if(AB.tgt&&AB.tgt.alive) face=Math.atan2(-(AB.tgt.pos.x-AB.pos.x),-(AB.tgt.pos.z-AB.pos.z)); }
  // walk toward the goal, facing a zombie it's shooting at if it has one
  let a=null; if(goal){ const dx=goal.x-AB.pos.x, dz=goal.z-AB.pos.z, d=Math.hypot(dx,dz); if(d>goal.r) a=Math.atan2(-dx,-dz); }
  const want=face!=null&&!goal?.act?face:a!=null?a:AB.yaw, dy=((want-AB.yaw+Math.PI*3)%(Math.PI*2))-Math.PI; AB.yaw+=Math.max(-dt*7,Math.min(dt*7,dy));
  if(a!=null){ const sp=AB.down?0.2:1; fw=Math.cos(a-AB.yaw)*sp; st=Math.sin(AB.yaw-a)*sp; }
  // stuck on something: hop
  if(a!=null&&!AB.sky&&Math.hypot(AB.vel.x,AB.vel.z)<0.5){ AB.stuckT+=dt; if(AB.stuckT>0.35&&AB.onGround&&!AB.down) jump=true; } else AB.stuckT=0;
  // at the goal: revive you, grab your card, or reboot you at the van
  if(goal&&goal.act&&a==null&&!AB.down){ if(goal.act==='boot'&&now<goal.v.cd){ AB.prog=0; } else { AB.prog+=dt/goal.T; }
    if(AB.prog>=1){ AB.prog=0;
      if(goal.act==='revive'&&P.down){ P.down=null; P.hp=RB_UP_HP; P.sh=0; animEvent(localHero,'revive'); sfx('rb_up'); banner('Revived','by Buddy',1.6); }
      else if(goal.act==='grab'&&goal.card&&!goal.card.holder){ goal.card.holder='ally'; goal.card.g.visible=false; sfx('rb_grab'); feed('<b>Buddy</b> picked up your card'); }
      else if(goal.act==='boot'){ rbSend({op:'boot',id:net.id,by:'ally',van:goal.v.id}); feed('<b>Buddy</b> rebooted you'); } } }
  else if(!goal||!goal.act) AB.prog=0;
  AB.h.rig&&(AB.reviving=goal&&goal.act&&a==null);
  moveBody(AB,fw,st,jump,dt); const n=Math.max(1,Math.ceil(dt/0.008)); for(let k=0;k<n;k++) physStep(dt/n,AB);
  if(AB.pos.y<-20){ AB.pos.copy(P.pos); AB.vel.set(0,0,0); }
  // shooting
  if(AB.reloadT>0) AB.reloadT-=dt; AB.fireT-=dt;
  if(!AB.down&&!AB.sky&&!(goal&&goal.act)&&AB.tgt&&AB.tgt.alive&&AB.reloadT<=0&&AB.fireT<=0&&Math.abs(dy)<0.35&&AB.tgt.pos.distanceTo(AB.pos)<40) allyFire(AB.tgt);
  AB.pitch=AB.tgt&&AB.tgt.alive?Math.max(-0.6,Math.min(0.6,Math.atan2(AB.tgt.pos.y+1-(AB.pos.y+1.5),Math.hypot(AB.tgt.pos.x-AB.pos.x,AB.tgt.pos.z-AB.pos.z)))):0;
  animateRig(AB.h,{slope:slopeFor(AB),pos:AB.pos,vel:AB.vel,yaw:AB.yaw,pitch:AB.pitch,onGround:AB.onGround,crouch:!!(goal&&goal.act&&a==null),building:false,editing:false,gun:AB.down||AB.sky?false:'ar',ads:0,swingT:0,emote:null,
    down:!!AB.down,sky:AB.sky?AB.sky.phase:null,reload:AB.reloadT>0?{w:'ar',p:1-AB.reloadT/2.1}:null},dt); }

/* ---------- controller (standard gamepad mapping) ----------""")
