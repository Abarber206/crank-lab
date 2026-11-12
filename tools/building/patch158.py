# patch158: Battle Royale. You and 19 bots drop in from the sky across the island. Everyone starts with a pickaxe:
# loot guns from the floors of houses and from chests, stay inside the storm circle as it closes in phases, and be the
# last one standing.
# The bots: each one has its own skill. They land, head for houses (walking to a door and opening it), loot guns and
# upgrade them, and keep inside the safe zone, running for it when the storm moves. They notice enemies gradually:
# faster when you're close, moving, out in the open or shooting (they hear gunfire), slower when you crouch and keep
# still. Once they suspect someone they creep closer crouched; once they've seen them they fight: keeping a range that
# suits their gun, strafing, taking cover behind what they can, reloading, healing when hurt and out of sight. They
# fight each other as well as you. Eliminations show in the feed; their guns drop where they fall.
# Storm: a glowing purple wall with the circle on the minimap and the big map, a timer, and damage outside it that grows
# each phase.
rep("""<option value="horde">Zombie horde</option></select>""","""<option value="horde">Zombie horde</option><option value="br">Battle royale</option></select>""")
rep("""        <button type="button" class="mode" data-mode="horde" role="radio"><b>Zombie horde</b><small>Build a fort, survive the waves and earn points for the Locker.</small></button>""",
"""        <button type="button" class="mode" data-mode="horde" role="radio"><b>Zombie horde</b><small>Build a fort, survive the waves and earn points for the Locker.</small></button>
        <button type="button" class="mode" data-mode="br" role="radio"><b>Battle royale</b><small>Drop in with 19 bots, loot up, stay ahead of the storm, be the last one standing.</small></button>""")
rep("""  const ms=$('modeSel'); ms.value=settings.mode==='horde'?'horde':'fight';""","""  const ms=$('modeSel'); ms.value=settings.mode==='horde'||settings.mode==='br'?settings.mode:'fight';""")
rep("""function botOn(){ return settings.bot!=='off'&&net.role!=='client'&&settings.mode!=='horde'&&!horde.on; }""","""function botOn(){ return settings.bot!=='off'&&net.role!=='client'&&settings.mode!=='horde'&&settings.mode!=='br'&&!horde.on&&!(typeof BR!=='undefined'&&BR.on); }""")
rep("""function isDead(){ return net.dead||""","""function isDead(){ return (typeof BR!=='undefined'&&BR.on&&BR.out)||net.dead||""")
rep("""$('vitals').hidden=!(on||net.role||horde.on);""","""$('vitals').hidden=!(on||net.role||horde.on||(typeof BR!=='undefined'&&BR.on));""")
# HUD pieces
rep("""<div class="hud" id="feed"></div>""","""<div class="hud" id="feed"></div>
<div class="hud" id="brHud" hidden><span class="al"><b id="brAlive">20</b> alive</span><span class="kl"><b id="brKills">0</b> eliminations</span><span class="st" id="brStorm">Storm forms in 1:00</span></div>
<div id="stormFx" hidden></div>""")
rep("""#compass{top:calc(env(safe-area-inset-top,0px) + 8px);left:50%;transform:translateX(-50%)}""","""#compass{top:calc(env(safe-area-inset-top,0px) + 8px);left:50%;transform:translateX(-50%)}
#brHud{top:calc(env(safe-area-inset-top,0px) + 50px);left:50%;transform:translateX(-50%);display:flex;gap:8px;align-items:center;font:800 italic 14px/1 var(--font-hud);letter-spacing:.04em;text-transform:uppercase;color:#fff;white-space:nowrap}
#brHud span{background:rgba(6,14,40,.72);border-radius:6px;padding:6px 10px} #brHud b{font-size:17px;color:#ffe08a} #brHud .st{color:#e7c8ff} #brHud .st.close{background:rgba(120,40,190,.85);color:#fff}
#stormFx{position:fixed;inset:0;pointer-events:none;z-index:3;background:radial-gradient(ellipse at center,rgba(120,40,200,.18),rgba(90,20,170,.55));mix-blend-mode:normal}
@media (orientation:portrait){#brHud{top:calc(env(safe-area-inset-top,0px) + 8px);font-size:12px}}""")
# your shots hit the bots; noise for them to hear
rep("""function bulletTargets(){ const t=[]; if(B&&B.active&&B.alive) t.push(B);""","""function bulletTargets(){ const t=[]; if(B&&B.active&&B.alive) t.push(B); if(BR.on) for(const b of BR.bots) if(b.alive&&b.h.group.visible) t.push(b);""")
rep("""  const tgts=[]; if(B&&B.active&&B.alive) tgts.push(B); net.players.forEach(pl=>{ if(pl.alive&&!sameTeam(pl)) tgts.push(pl); }); horde.zs.forEach(z=>{ if(z.alive) tgts.push(z); });""",
"""  const tgts=[]; if(B&&B.active&&B.alive) tgts.push(B); net.players.forEach(pl=>{ if(pl.alive&&!sameTeam(pl)) tgts.push(pl); }); horde.zs.forEach(z=>{ if(z.alive) tgts.push(z); }); if(BR.on){ P.shotAt=performance.now(); for(const b of BR.bots) if(b.alive&&b.h.group.visible) tgts.push(b); }""")
rep("""    else if(who===B){ dmgNum(B.pos.clone().setY(B.pos.y+(e.head?2.05:1.6)),dmg,e.head?'head':shBefore>0?'shield':'hp'); botHurt(dmg,net.id,wpn); }""",
"""    else if(who===B){ dmgNum(B.pos.clone().setY(B.pos.y+(e.head?2.05:1.6)),dmg,e.head?'head':shBefore>0?'shield':'hp'); botHurt(dmg,net.id,wpn); }
    else if(who.isBR){ dmgNum(who.pos.clone().setY(who.pos.y+(e.head?2.05:1.6)),dmg,e.head?'head':who.sh>0?'shield':'hp'); brHurtBot(who,dmg,null,wpn); }""")
# the module
rep("""var AB=null;
function allyOn(){""","""/* ---------- battle royale ---------- */
var BR={on:false,bots:[],out:false,over:false,overT:0,kills:0,storm:null,wall:null,tick:0,hudT:0,place:0,frame:0};
const BR_N=19, BR_SHRINK=[[60,0.62,45],[50,0.4,40],[45,0.24,35],[40,0.13,30],[35,0.06,25],[30,0,25]], BR_DPS=[1,2,4,6,8,10]; // [wait, radius after (of the island), shrink time]
const BR_NAMES=['Rook2','Pixel','Nova','Talon','Bramble','Vex','Juno','Moss','Static','Kestrel','Cinder','Wisp','Dune','Echo','Sable','Quill','Rift','Ember','Glint','Hollow','Fable','Brick'];
function brMine(){ return settings.mode==='br'&&!net.role; }
function brSpot(){ const T0=Math.random()<0.75&&TOWNS.length?TOWNS[Math.floor(Math.random()*TOWNS.length)]:null; // most drop near a town, some out in the wild
  for(let k=0;k<200;k++){ const a=Math.random()*Math.PI*2, r=T0&&k<120?Math.random()*(T0.R+35):Math.sqrt(Math.random())*MAP_R*0.82, x=(T0&&k<120?T0.x:SPAWN[0])+Math.cos(a)*r, z=(T0&&k<120?T0.z:SPAWN[2])+Math.sin(a)*r, c=worldCell(x,z);
    if(c<0||waterAt(x,z)>-999||WORLD.SNOW[c]>40||terrainH(x,z)>60) continue; return [x,z]; } return [SPAWN[0],SPAWN[2]]; }
function brMakeBot(i){ const o=OUTFITS[Math.floor(Math.random()*OUTFITS.length)], pk=PICKAXES[Math.floor(Math.random()*PICKAXES.length)].id, h=heroFor(o,pk); h.outfit=o.id; h.pickaxe=pk; h.group.visible=false; scene.add(h.group);
  return {isBR:true,id:'br'+i,name:BR_NAMES[i%BR_NAMES.length],h,pos:new THREE.Vector3(),vel:new THREE.Vector3(),onGround:true,groundSlab:null,crouch:false,yaw:0,pitch:0,rot:0,sc:1,
    hp:100,sh:0,alive:true,wpn:null,ammo:0,reloadT:0,fireT:0,swingT:0,thinkT:Math.random()*0.4,stuckT:0,sideT:0,sideDir:1,skill:0.25+Math.random()*0.6,aw:new Map(),tgt:null,los:false,react:0,
    route:null,goal:null,loot:null,dest:null,heals:0,healT:0,shotAt:0,strafe:1,strafeT:0,lastSeen:null,kills:0}; }
function brStormWall(){ if(BR.wall) return BR.wall; const g=new THREE.CylinderGeometry(1,1,1,120,1,true);
  const m=new THREE.ShaderMaterial({transparent:true,depthWrite:false,side:THREE.DoubleSide,uniforms:{time:{value:0}},
    vertexShader:`varying vec2 vU; varying float vY; void main(){ vU=uv; vec4 w=modelMatrix*vec4(position,1.0); vY=w.y; gl_Position=projectionMatrix*viewMatrix*w; }`,
    fragmentShader:`uniform float time; varying vec2 vU; varying float vY; void main(){ float s=0.5+0.5*sin(vU.x*900.0+time*1.6+sin(vY*0.05+time*0.7)*3.0), f=0.5+0.5*sin(vY*0.08-time*2.2+vU.x*300.0);
      vec3 c=mix(vec3(0.42,0.12,0.78),vec3(0.75,0.45,1.0),s*0.6+f*0.25); float a=0.28+0.12*s+0.08*f; a*=1.0-smoothstep(160.0,320.0,vY); gl_FragColor=vec4(c,a); }`});
  const w=new THREE.Mesh(g,m); w.frustumCulled=false; w.renderOrder=3; scene.add(w); return BR.wall=w; }
function brStart(){
  BR.on=true; BR.out=false; BR.over=false; BR.overT=0; BR.kills=0; BR.place=0; P.shotAt=0;
  clearBuilds(); respawn(); emptyLoadout(); P.sh=0;
  if(B&&B.active){ B.active=false; B.h.group.visible=false; }
  while(BR.bots.length<BR_N) BR.bots.push(brMakeBot(BR.bots.length));
  for(const b of BR.bots){ const [x,z]=brSpot(); Object.assign(b,{hp:100,sh:0,alive:true,wpn:null,ammo:0,reloadT:0,fireT:0,tgt:null,route:null,goal:null,loot:null,dest:null,heals:0,healT:0,kills:0,lastSeen:null,crouch:false}); b.aw.clear();
    b.h.group.visible=true; animEvent(b.h,'revive'); skyDrop(x,z,SKY_MATCH*(0.75+Math.random()*0.3),b); b.land=[x,z]; }
  const sp=randomDropSpot(); if(skyDropAllowed()) cloudDrop(sp[0],sp[1],SKY_MATCH); else P.pos.set(sp[0],terrainH(sp[0],sp[1]),sp[1]);
  BR.storm={cx:SPAWN[0],cz:SPAWN[2],r:MAP_R*1.08,ph:0,state:'wait',t:BR_SHRINK[0][0]}; brNextCircle(); brStormWall().visible=true;
  $('brHud').hidden=false; syncBot(); banner('Battle royale','20 drop in · one walks out',3);
}
function brStop(){ BR.on=false; for(const b of BR.bots){ b.h.group.visible=false; b.alive=false; } if(BR.wall) BR.wall.visible=false; $('brHud').hidden=true; $('stormFx').hidden=true; syncBot(); }
function brNextCircle(){ const S=BR.storm, ph=BR_SHRINK[Math.min(S.ph,BR_SHRINK.length-1)], nr=MAP_R*ph[1], room=Math.max(0,S.r-nr)*0.85; let x=S.cx, z=S.cz;
  for(let k=0;k<40;k++){ const a=Math.random()*Math.PI*2, d=Math.sqrt(Math.random())*room, tx=S.cx+Math.cos(a)*d, tz=S.cz+Math.sin(a)*d; if(Math.hypot(tx-SPAWN[0],tz-SPAWN[2])<MAP_R*0.9-nr){ x=tx; z=tz; break; } }
  S.fx=S.cx; S.fz=S.cz; S.fr=S.r; S.tx=x; S.tz=z; S.tr=nr; }
function brAliveCount(){ let n=BR.out?0:1; for(const b of BR.bots) if(b.alive) n++; return n; }
const brOut=(E,S)=>Math.hypot(E.pos.x-S.cx,E.pos.z-S.cz)>S.r;
function brUpdate(dt){
  if(brMine()&&playing&&!BR.on) brStart();
  if(!brMine()&&BR.on) brStop();
  if(!BR.on) return;
  const S=BR.storm, now=performance.now(); BR.frame++;
  // the storm: wait, then close in to the next circle
  S.t-=dt; const ph=BR_SHRINK[Math.min(S.ph,BR_SHRINK.length-1)];
  if(S.state==='wait'){ if(S.t<=0){ S.state='shrink'; S.t=ph[2]; S.T=ph[2]; if(S.ph<BR_SHRINK.length) toast('The storm is closing in'); } }
  else { const k=1-Math.max(0,S.t)/S.T, e=k*k*(3-2*k); S.cx=S.fx+(S.tx-S.fx)*e; S.cz=S.fz+(S.tz-S.fz)*e; S.r=S.fr+(S.tr-S.fr)*e;
    if(S.t<=0){ S.ph++; if(S.ph<BR_SHRINK.length){ S.state='wait'; S.t=BR_SHRINK[S.ph][0]; brNextCircle(); } else { S.state='done'; S.t=1e9; } } }
  const W=BR.wall; W.position.set(S.cx,-60,S.cz); W.scale.set(Math.max(1,S.r),700,Math.max(1,S.r)); W.material.uniforms.time.value=now/1000;
  // storm damage, once a second
  BR.tick-=dt; if(BR.tick<=0){ BR.tick=1; const d=BR_DPS[Math.min(S.ph,BR_DPS.length-1)];
    if(!BR.out&&!P.sky&&brOut(P,S)){ P.hp-=d; const f=$('hurtfx'); f.classList.add('on'); void f.offsetWidth; f.classList.remove('on'); if(P.hp<=0) brPlayerOut('the storm'); }
    for(const b of BR.bots) if(b.alive&&!b.sky&&brOut(b,S)){ b.hp-=d; if(b.hp<=0) brBotOut(b,null,'the storm'); } }
  $('stormFx').hidden=!(playing&&!BR.out&&brOut(P,S));
  // the bots
  for(const b of BR.bots) if(b.alive) brStepBot(b,dt,now);
  // end of the match
  if(!BR.over){ const n=brAliveCount();
    if(!BR.out&&n===1){ BR.over=true; BR.overT=8; banner('Victory Royale!','#1 · '+BR.kills+(BR.kills===1?' elimination':' eliminations'),7); sfx('win'); addPoints(150+40*BR.kills); }
    else if(BR.out&&BR.place&&BR.overT<=0){ BR.over=true; BR.overT=7; } }
  else { BR.overT-=dt; if(BR.overT<=0){ BR.on=false; brStart(); } }
  // the HUD
  BR.hudT-=dt; if(BR.hudT<=0){ BR.hudT=0.25; $('brAlive').textContent=brAliveCount(); $('brKills').textContent=BR.kills; const el=$('brStorm'), t=Math.max(0,Math.ceil(S.t)), mm=Math.floor(t/60)+':'+String(t%60).padStart(2,'0');
    el.textContent=S.state==='wait'?'Storm closes in '+mm:S.state==='shrink'?'Storm closing · '+mm:'Final circle'; el.classList.toggle('close',S.state==='shrink'||(S.state==='wait'&&S.t<10)); }
}
function brPlayerOut(by){ if(BR.out) return; BR.out=true; P.hp=0; P.sh=0; animEvent(localHero,'die'); BR.place=brAliveCount()+1;
  banner('#'+BR.place,'Eliminated by '+by+' · '+BR.kills+(BR.kills===1?' elimination':' eliminations'),6); sfx('lose'); feed('<b>You</b> were eliminated by <b>'+esc(by)+'</b>',true); addPoints(10*BR.kills+Math.max(0,(21-BR.place))*4); BR.overT=0; }
function brHurtMe(dmg,b){ if(BR.out||P.hp<=0) return; dmgDirFrom(b.pos); const f=$('hurtfx'); f.classList.add('on'); void f.offsetWidth; f.classList.remove('on'); sfx('hurt'); animEvent(localHero,'hurt');
  if(hurt(P,dmg)) brPlayerOut(b.name); }
function brHurtBot(b,dmg,from,w){ if(!b.alive) return; animEvent(b.h,'hurt'); b.hurtAt=performance.now();
  const src=from?from:P; b.aw.set(src,Math.max(1.2,b.aw.get(src)||0)); b.lastSeen={x:src.pos.x,z:src.pos.z,t:performance.now()}; // shot: it knows where from
  if(hurt(b,dmg)) brBotOut(b,from,from?from.name:'You'); }
function brBotOut(b,from,byName){ if(!b.alive) return; b.alive=false; b.hp=0; animEvent(b.h,'die');
  if(b.wpn){ const p=b.pos.clone(); p.y+=0.6; netDrop(b.wpn,WEAPONS[b.wpn].mag||10,p,new THREE.Vector3(0,3,0),true); const a=ammoFor(b.wpn); netDrop(a[0],a[1],p.clone().add(new THREE.Vector3(0.6,0,0.4)),new THREE.Vector3(0,3,0),true); }
  if(!from&&byName==='You'){ BR.kills++; feed('<b>You</b> eliminated <b>'+esc(b.name)+'</b>'); }
  else if(from){ from.kills++; feed('<b>'+esc(from.name)+'</b> eliminated <b>'+esc(b.name)+'</b>'); }
  else feed('<b>'+esc(b.name)+'</b> was lost to '+esc(byName));
  const h=b.h; setTimeout(()=>{ if(!b.alive) h.group.visible=false; },2600); }
// who a bot could fight: you and the other bots, alive and on the ground
function brFoes(b){ const a=[]; if(!BR.out&&P.hp>0&&!P.sky) a.push(P); for(const o of BR.bots) if(o!==b&&o.alive&&!o.sky) a.push(o); return a; }
const _brE=new THREE.Vector3(), _brT=new THREE.Vector3(), _brD=new THREE.Vector3();
function brSees(b,T){ const eye=_brE.set(b.pos.x,b.pos.y+(b.crouch?1.1:1.55),b.pos.z), t=_brT.set(T.pos.x,T.pos.y+(T.crouch?0.95:1.3),T.pos.z), d=t.distanceTo(eye); if(d<0.5) return true;
  const r=castShot(eye,_brD.copy(t).sub(eye).normalize(),d,0.05,null); if(r.kind==='piece'&&r.t<d-0.6) return false;
  // hills in between
  for(let k=1;k<6;k++){ const f=k/6, x=eye.x+(t.x-eye.x)*f, z=eye.z+(t.z-eye.z)*f, y=eye.y+(t.y-eye.y)*f; if(terrainH(x,z)>y+0.2) return false; } return true; }
function brRange(b){ const W=WEAPONS[b.wpn]; return !W?2.2:W.pellets>1?9:W.range>150?55:28; }
function brFire(b,T){ const W=WEAPONS[b.wpn]; if(!W) return; const eye=_brE.set(b.pos.x,b.pos.y+(b.crouch?1.1:1.5),b.pos.z), tgt=_brT.set(T.pos.x,T.pos.y+(T.crouch?0.95:1.25),T.pos.z), dist=tgt.distanceTo(eye);
  const moving=Math.min(1,Math.hypot(T.vel.x,T.vel.z)/6), err=(0.075-0.06*b.skill)*(1+0.8*moving)*(T===P&&P.crouch?1.1:1), base=_brD.copy(tgt).sub(eye).normalize(), pel=Math.min(W.pellets||1,8); let dmg=0, head=false, last=null;
  b.h.rig.muzzle&&b.h.rig.muzzle.getWorldPosition(muzzleV);
  for(let k=0;k<pel;k++){ const d=base.clone(); d.x+=(Math.random()-.5)*2*(err+(pel>1?0.06:0)); d.y+=(Math.random()-.5)*1.4*err; d.z+=(Math.random()-.5)*2*(err+(pel>1?0.06:0)); d.normalize();
    const r=castShot(eye,d,Math.min(W.range||200,dist+30),0.3,[T]); last=r;
    if(r.kind==='body'){ const fall=r.t<=W.f0?1:r.t>=W.f1?W.fmin:1-(1-W.fmin)*(r.t-W.f0)/(W.f1-W.f0); dmg+=W.dmg*fall*(r.head?W.head*0.8:1)*(T===P?0.8:1); head=head||r.head; }
    else if(r.kind==='piece'&&k===0) damagePiece(r.piece,W.dmg*(W.build||1),r.point);
    if(k<3) tracer(muzzleV.clone(),r.point,0xffb070,b.h); }
  muzzleFlash(b.h); sfxAt(W.snd||'shot',b.pos); animEvent(b.h,'fire',b.wpn); b.shotAt=performance.now();
  if(dmg>0){ dmg=Math.round(dmg); if(T===P) brHurtMe(dmg,b); else brHurtBot(T,dmg,b,b.wpn); }
  b.ammo--; b.fireT=Math.max(0.12,W.rate||0.2)*(1.25-0.3*b.skill)+Math.random()*0.12+(pel>1?0.35:0); if(b.ammo<=0){ b.reloadT=Math.min(2.6,W.reload||2.1); b.ammo=W.mag||30; } }
const brGunOk=w=>{ const W=WEAPONS[w]; return !!W&&!W.throw&&w!=='rpg'&&w!=='glauncher'&&w!=='nade'; };
const brRank=w=>w?RARITIES.indexOf((WEAPONS[w]||{}).rarity)+(WEAPONS[w].pellets>1?0.3:0):-1;
// the doors into a house, each with a spot just outside it and one just inside
function brHouseDoors(h){ if(h.brDoors) return h.brDoors; const out=[], cx=(h.i0+h.w/2)*CELL, cz=(h.j0+h.d/2)*CELL;
  near(cx,cz,Math.ceil(Math.max(h.w,h.d)/2)+1).forEach(p=>{ if(!p.doors||p.l!==h.L) return; p.doors.forEach((dr,c)=>{ if(!dr) return; const q=doorCenter(p,c), n=p.axis==='x'?new THREE.Vector3(1,0,0):new THREE.Vector3(0,0,1); if(n.x*(q.x-cx)+n.z*(q.z-cz)<0) n.negate();
    out.push({p,c,x:q.x,z:q.z,ox:q.x+n.x*1.6,oz:q.z+n.z*1.6,ix:q.x-n.x*1.4,iz:q.z-n.z*1.4}); }); });
  return h.brDoors=out; }
function brHouseAt(x,z){ for(const t of TOWNS){ if(Math.hypot(t.x-x,t.z-z)>t.R+30) continue; for(const h of t.houses) if(x>h.i0*CELL-0.2&&x<(h.i0+h.w)*CELL+0.2&&z>h.j0*CELL-0.2&&z<(h.j0+h.d)*CELL+0.2) return h; } return null; }
function brRouteInto(b,h,x,z){ const doors=brHouseDoors(h); let dr=null, dd=1e9; for(const q of doors){ const v=Math.hypot(q.ox-b.pos.x,q.oz-b.pos.z); if(v<dd){ dd=v; dr=q; } }
  b.dest={pts:dr?[[dr.ox,dr.oz,1.0],[dr.ix,dr.iz,0.9],[x,z,1.2]]:[[x,z,1.5]],i:0,linger:3+Math.random()*3,h}; h.brVisit=performance.now(); }
function brPickHouse(b){ const S=BR.storm; let best=null, bs=1e9;
  for(const t of TOWNS){ const dt=Math.hypot(t.x-b.pos.x,t.z-b.pos.z); if(dt>320) continue; for(const h of t.houses){ if(h.brVisit&&performance.now()-h.brVisit<90000) continue; const x=(h.i0+h.w/2)*CELL, z=(h.j0+h.d/2)*CELL;
      if(Math.hypot(x-S.tx,z-S.tz)>S.tr*0.92+4&&S.ph>0) continue; const d=Math.hypot(x-b.pos.x,z-b.pos.z)+Math.random()*25; if(d<bs){ bs=d; best=h; } } }
  return best; }
function brStepBot(b,dt,now){
  const S=BR.storm;
  if(b.sky){ const [lx,lz]=b.land, dx=lx-b.pos.x, dz=lz-b.pos.z, d=Math.hypot(dx,dz); if(d>3){ const a=Math.atan2(-dx,-dz); b.yaw=a; moveBody(b,1,0,false,dt); } else moveBody(b,0,0,false,dt);
    const n=Math.max(1,Math.ceil(dt/0.008)); for(let k=0;k<n;k++) physStep(dt/n,b); brAnim(b,dt,now); return; }
  // think
  b.thinkT-=dt;
  if(b.thinkT<=0){ b.thinkT=0.3+Math.random()*0.1;
    // noticing people: gradually, faster when they're near, moving, in the open or shooting
    const foes=brFoes(b); let best=null, bv=0;
    foes.sort((p,q)=>p.pos.distanceToSquared(b.pos)-q.pos.distanceToSquared(b.pos));
    for(let i=0;i<foes.length;i++){ const T=foes[i], d=T.pos.distanceTo(b.pos); let a=b.aw.get(T)||0;
      if(d<90&&i<3){ const sees=brSees(b,T), mv=Math.min(1,Math.hypot(T.vel.x,T.vel.z)/5), cr=T.crouch?0.35:1, fresh=now-(T.shotAt||0)<1500;
        if(sees){ a+=0.33*(0.35+0.65*Math.max(0,1-d/90))*(0.45+mv)*cr*(1+b.skill)*(d<10?3:1); b.lastSeen={x:T.pos.x,z:T.pos.z,t:now}; if(a>=1) b.lastSeen.T=T; }
        if(fresh&&d<70) a=Math.max(a,0.55); if(!sees) a-=0.04;
        if(T===b.tgt) b.los=sees; }
      else if(now-(T.shotAt||0)<1500&&d<70) a=Math.max(a,0.5); // heard the shot
      else a-=0.05;
      a=Math.max(0,Math.min(1.6,a)); b.aw.set(T,a); if(a>bv){ bv=a; best=T; } }
    for(const [T,a] of b.aw) if(!T.alive&&T!==P||T===P&&(BR.out||P.hp<=0)) b.aw.delete(T);
    b.tgt=bv>=1?best:null; b.sus=bv>=0.3?best:null;
    if(b.tgt&&!b.react) b.react=0.5-0.35*b.skill;
    // looting
    if(!b.tgt||!b.wpn){ let L=null, bd=1e9;
      const myH=brHouseAt(b.pos.x,b.pos.z), bad=b.bad||(b.bad=new Set()); let far=null, fd=1e9;
      const consider=(kind,o,x,y,z,range)=>{ if(bad.has(o)) return; const dd=Math.hypot(x-b.pos.x,z-b.pos.z); if(dd>range) return; const h=brHouseAt(x,z);
        if(h&&h!==myH){ if(dd<fd){ fd=dd; far={h,x,z}; } return; } if(Math.abs(y-b.pos.y)>1.7) return; if(dd<bd){ bd=dd; L={kind,[kind==='drop'?'d':'c']:o,x,z}; } };
      drops.forEach(d=>{ if(!brGunOk(d.item)||d.pending||!d.landed) return; if(b.wpn&&brRank(d.item)<=brRank(b.wpn)) return; consider('drop',d,d.pos.x,d.pos.y,d.pos.z,b.wpn?18:45); });
      if(!L&&(!b.wpn||b.heals<1)) for(const c of chests){ if(c.open||!c.g.visible) continue; consider('chest',c,c.x,c.y,c.z,b.wpn?14:35); }
      if(L&&b.loot&&b.loot.kind===L.kind&&(b.loot.d||b.loot.c)===(L.d||L.c)) L=b.loot; b.loot=L;
      if(!L&&far&&!b.wpn&&!(b.dest&&b.dest.h===far.h&&!b.dest.done)) brRouteInto(b,far.h,far.x,far.z); }
    // where to go when nothing's going on: a house to loot, inside the next circle; then a spot inside the circle
    if(!b.dest||b.dest.done){ const h=!b.wpn||Math.random()<0.4?brPickHouse(b):null;
      if(h) brRouteInto(b,h,(h.i0+h.w/2)*CELL,(h.j0+h.d/2)*CELL);
      else { const a=Math.random()*Math.PI*2, r=Math.sqrt(Math.random())*Math.max(8,S.tr*0.8); b.dest={pts:[[S.tx+Math.cos(a)*r,S.tz+Math.sin(a)*r,4]],i:0,linger:3}; } }
    // a closed door right in front: open it
    near(b.pos.x,b.pos.z,1).forEach(p=>{ if(!p.doors||Math.abs(p.l*LVL-b.pos.y)>2.2) return; p.doors.forEach((dr,c)=>{ if(!dr||dr.open) return; const q=doorCenter(p,c); if(Math.hypot(q.x-b.pos.x,q.z-b.pos.z)<1.9) toggleDoor(p,c,false); }); });
  }
  // decide where to go this frame
  let goal=null, face=null, crouch=false, strafe=0, run=false;
  const dS=Math.hypot(b.pos.x-S.cx,b.pos.z-S.cz), stormNext=Math.hypot(b.pos.x-S.tx,b.pos.z-S.tz)>S.tr-3&&(S.state==='shrink'||S.t<25), stormNow=dS>S.r-4;
  const T=b.tgt&&(b.tgt.alive||b.tgt===P)&&!(b.tgt===P&&(BR.out||P.hp<=0))?b.tgt:null;
  if(stormNow||(stormNext&&!T)){ const dx=S.tx-b.pos.x, dz=S.tz-b.pos.z, d=Math.hypot(dx,dz)||1; goal={x:S.tx-dx/d*Math.min(S.tr*0.5,d),z:S.tz-dz/d*Math.min(S.tr*0.5,d),r:3}; run=true; if(T) face=Math.atan2(-(T.pos.x-b.pos.x),-(T.pos.z-b.pos.z)); }
  else if(T&&b.wpn){ const d=T.pos.distanceTo(b.pos), want=brRange(b); face=Math.atan2(-(T.pos.x-b.pos.x),-(T.pos.z-b.pos.z));
    if(!b.los&&b.lastSeen) goal={x:b.lastSeen.x,z:b.lastSeen.z,r:2,sneak:true};       // lost sight: go round to where they were
    else if(d>want*1.3) goal={x:T.pos.x,z:T.pos.z,r:want};
    else if(d<want*0.5&&!(WEAPONS[b.wpn].pellets>1)) goal={x:b.pos.x*2-T.pos.x,z:b.pos.z*2-T.pos.z,r:0.5};
    b.strafeT-=dt; if(b.strafeT<=0){ b.strafe=-b.strafe; b.strafeT=0.5+Math.random()*1.2; } strafe=b.strafe*(0.5+0.5*b.skill);
    if(b.hp<45&&b.heals>0&&!b.los&&now-(b.hurtAt||0)>2500){ b.healT+=dt; goal=null; strafe=0; crouch=true; if(b.healT>3.2){ b.healT=0; b.heals--; b.hp=Math.min(100,b.hp+35); } } else b.healT=0; }
  else if(T&&!b.wpn){ const d=T.pos.distanceTo(b.pos); face=Math.atan2(-(T.pos.x-b.pos.x),-(T.pos.z-b.pos.z));
    if(d<4) goal={x:T.pos.x,z:T.pos.z,r:1.6};                                      // cornered: swing
    else goal={x:b.pos.x*2-T.pos.x,z:b.pos.z*2-T.pos.z,r:0.5};                    // no gun: get away
    if(b.loot&&Math.hypot(b.loot.x-b.pos.x,b.loot.z-b.pos.z)<12) goal={x:b.loot.x,z:b.loot.z,r:b.loot.kind==='chest'?1.5:0.9,act:b.loot.kind}; run=true; }
  else if(b.loot){ goal={x:b.loot.x,z:b.loot.z,r:b.loot.kind==='chest'?1.5:0.9,act:b.loot.kind}; }
  else if(b.sus&&b.wpn&&b.lastSeen&&now-b.lastSeen.t<12000){ goal={x:b.lastSeen.x,z:b.lastSeen.z,r:6,sneak:true}; }   // stalk: creep up crouched
  else if(b.dest){ const q=b.dest.pts[b.dest.i]; if(q){ goal={x:q[0],z:q[1],r:q[2]}; if(Math.hypot(q[0]-b.pos.x,q[1]-b.pos.z)<q[2]){ b.dest.i++; } }
    else { b.dest.linger-=dt; if(b.dest.linger<=0) b.dest.done=true; } }
  if(goal&&goal.sneak){ crouch=true; }
  if(b.sus&&!T&&b.wpn) crouch=true;
  // steer
  let a=null; if(goal){ const dx=goal.x-b.pos.x, dz=goal.z-b.pos.z, d=Math.hypot(dx,dz); if(d>goal.r) a=Math.atan2(-dx,-dz); }
  const want=face!=null?face:a!=null?a:b.yaw, dy=((want-b.yaw+Math.PI*3)%(Math.PI*2))-Math.PI; b.yaw+=Math.max(-dt*(4+5*b.skill),Math.min(dt*(4+5*b.skill),dy));
  let fw=0, st=0, jump=false; if(a!=null){ fw=Math.cos(a-b.yaw); st=Math.sin(b.yaw-a); } if(strafe&&b.los) st+=strafe;
  b.crouch=crouch&&!run&&!b.swim;
  if(b.sideT>0){ b.sideT-=dt; if(a!=null){ st=b.sideDir; fw*=0.35; } }
  if(a!=null&&Math.hypot(b.vel.x,b.vel.z)<0.5){ b.stuckT+=dt; if(b.stuckT>0.35&&b.onGround) jump=true; if(b.stuckT>0.9&&!(b.sideT>0)){ b.sideT=0.9; b.sideDir=Math.random()<0.5?-1:1; } if(b.stuckT>2.5&&b.loot&&goal&&goal.act){ (b.bad||(b.bad=new Set())).add(b.loot.d||b.loot.c); b.loot=null; b.stuckT=0; } if(b.stuckT>1.8&&b.dest&&!(goal&&goal.act)&&b.dest.pts[b.dest.i]){ b.dest.i++; b.stuckT=0; b.dest.skips=(b.dest.skips||0)+1; if(b.dest.skips>3) b.dest.done=true; } } else b.stuckT=0;
  // act at the goal: open a chest, take a gun
  if(goal&&goal.act&&a==null){ b.prog=(b.prog||0)+dt;
    if(goal.act==='chest'&&b.prog>1.1&&b.loot&&!b.loot.c.open){ openChest(b.loot.c,true); b.heals+=1; b.loot=null; b.prog=0; b.thinkT=0.6; }
    else if(goal.act==='drop'&&b.prog>0.3&&b.loot&&drops.has(b.loot.d.id)){ const d=b.loot.d; if(b.wpn){ const p=b.pos.clone(); p.y+=0.6; netDrop(b.wpn,WEAPONS[b.wpn].mag||10,p,new THREE.Vector3(0,2,0),true); }
      b.wpn=d.item; const W=WEAPONS[d.item]; b.ammo=W.mag||30; b.reloadT=0; b.fireT=0.5; removeDrop(d.id); sfxAt('pickup',b.pos); b.loot=null; b.prog=0; } }
  else b.prog=0;
  moveBody(b,fw,st,jump,dt); const n=Math.max(1,Math.ceil(dt/0.01)); for(let k=0;k<n;k++) physStep(dt/n,b);
  if(b.pos.y<-20){ const [x,z]=brSpot(); b.pos.set(x,terrainH(x,z)+0.1,z); b.vel.set(0,0,0); }
  // fight
  if(b.reloadT>0) b.reloadT-=dt; b.fireT-=dt; if(b.react>0) b.react-=dt; if(b.swingT>0) b.swingT-=dt;
  if(T&&b.los&&b.react<=0&&b.reloadT<=0&&b.fireT<=0&&Math.abs(dy)<0.35&&!b.swim){ const d=T.pos.distanceTo(b.pos);
    if(b.wpn&&d<(WEAPONS[b.wpn].range||150)*0.9) brFire(b,T);
    else if(!b.wpn&&d<2.6){ b.swingT=SWING_T; b.fireT=PICK_CD+0.1; setTimeout(()=>{ if(b.alive&&T.pos.distanceTo(b.pos)<3.1){ if(T===P) brHurtMe(20,b); else brHurtBot(T,20,b,null); sfxAt('hit',T.pos); } },PICK_IMPACT*1000); } }
  if(T) b.pitch=Math.max(-0.6,Math.min(0.6,Math.atan2(T.pos.y+1-(b.pos.y+1.5),Math.hypot(T.pos.x-b.pos.x,T.pos.z-b.pos.z)))); else b.pitch*=0.9;
  brAnim(b,dt,now);
}
function brAnim(b,dt,now){ const d=b.pos.distanceTo(camera.position); b.h.group.visible=d<320||b.sky;
  if(!b.h.group.visible) return; if(d>120&&(BR.frame+b.h.group.id)%3) { b.h.group.position.copy(b.pos); return; } // far off: a third as often
  animateRig(b.h,{slope:slopeFor(b),pos:b.pos,vel:b.vel,yaw:b.yaw,pitch:b.pitch,onGround:b.onGround,crouch:b.crouch,building:false,editing:false,gun:b.sky||!b.wpn?false:b.wpn,ads:0,swingT:Math.max(0,b.swingT),emote:null,
    down:false,sky:b.sky?b.sky.phase:null,reload:b.reloadT>0&&b.wpn?{w:b.wpn,p:Math.max(0,1-b.reloadT/2.1)}:null},d>120?dt*3:dt); b.h.rig.pick.visible=!b.wpn&&!b.sky; }
function brMiniMap(g,tx,tz,sc,dpr){ if(!BR.on) return; const S=BR.storm; g.save(); g.strokeStyle='rgba(190,120,255,.95)'; g.lineWidth=2.2*dpr; g.beginPath(); g.arc(tx(S.cx),tz(S.cz),S.r*sc,0,7); g.stroke();
  if(S.state!=='done'){ g.strokeStyle='rgba(255,255,255,.85)'; g.setLineDash([5*dpr,4*dpr]); g.lineWidth=1.6*dpr; g.beginPath(); g.arc(tx(S.tx),tz(S.tz),S.tr*sc,0,7); g.stroke(); } g.restore(); }
var AB=null;
function allyOn(){""")
rep("""  rbMiniMap(g,tx,tz,c,dpr);""","""  rbMiniMap(g,tx,tz,c,dpr); brMiniMap(g,tx,tz,sc,dpr);""")
rep("""  rbBigMap(g,X,Z,u);""","""  rbBigMap(g,X,Z,u); if(BR.on){ brMiniMap(g,X,Z,(X(SPAWN[0]+100)-X(SPAWN[0]))/100,u); for(const b of BR.bots) if(b.alive&&!b.sky&&false) dot(b.pos.x,b.pos.z,'#ff4b3a'); }""")
rep("""if(playing||net.role) hordeUpdate(dt);""","""if(playing||net.role) hordeUpdate(dt); if(playing||BR.on) brUpdate(dt);""")
