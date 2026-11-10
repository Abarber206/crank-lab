# ---------- 61. reboot cards and reboot vans ----------
# Go down in a party with a teammate still standing and you don't come straight back: you drop a reboot card (a
# floating holographic card with your portrait, in your team colour, with a beam of light over it). A teammate grabs
# it, carries it to a Reboot Van, and holds Interact at the van's terminal; you're launched back in from the sky with
# no loot. Vans stand outside every town but only show on the map while someone on your team needs rebooting.
# The card's owner decides who got it and when the reboot happens, so every screen agrees. A card left too long
# (or a squad with nobody left standing) falls back to the normal respawn.

# ---- HUD ----
rep('<div class="hud" id="chestBar" hidden>','''<div class="hud" id="rbWait" hidden><span class="rbt">Eliminated</span><p id="rbMsg"></p><span class="rbbar"><i id="rbBar"></i></span><small id="rbSub"></small></div>
<div class="hud" id="rbCarry" hidden><span class="rbchip"></span><span id="rbCarryT"></span></div>
<div class="hud" id="chestBar" hidden>''')
rep('#chestBar{left:50%;',r'''#rbWait{left:50%;top:calc(env(safe-area-inset-top,0px) + 96px);transform:translateX(-50%);width:min(420px,calc(100vw - 32px));box-sizing:border-box;display:grid;justify-items:center;gap:8px;padding:14px 18px 12px;background:rgba(6,16,48,.78);border:1px solid rgba(140,200,255,.35);border-radius:10px;box-shadow:0 10px 30px rgba(0,0,0,.4);text-align:center}
#rbWait .rbt{font:900 italic 24px/1 var(--font-hud);letter-spacing:.08em;text-transform:uppercase;color:#ff8a6a}
#rbWait p{margin:0;font:800 italic 17px/1.2 var(--font-hud);letter-spacing:.03em;text-transform:uppercase;color:#fff}
#rbWait small{font:700 13px/1.2 var(--font-hud);letter-spacing:.1em;text-transform:uppercase;color:#9fc6ff}
.rbbar{display:block;width:100%;height:6px;border-radius:3px;background:rgba(255,255,255,.14);overflow:hidden} .rbbar i{display:block;height:100%;width:100%;background:linear-gradient(90deg,#4fa8ff,#9fe0ff);transform-origin:left;transition:transform .3s linear}
#rbCarry{left:50%;top:calc(env(safe-area-inset-top,0px) + 58px);transform:translateX(-50%);display:flex;align-items:center;gap:8px;padding:7px 14px 7px 8px;background:rgba(6,16,48,.75);border:1px solid rgba(140,200,255,.45);border-radius:999px;font:800 italic 15px/1 var(--font-hud);letter-spacing:.05em;text-transform:uppercase;color:#dff0ff;white-space:nowrap}
.rbchip{width:16px;height:22px;border-radius:3px;background:linear-gradient(160deg,#bfe6ff,#3f8fff 55%,#1a3c9a);box-shadow:0 0 10px #6fb8ff,inset 0 0 0 1.5px #ffe08a;animation:rbchip 1.6s ease-in-out infinite} @keyframes rbchip{50%{transform:rotateY(180deg)}}
#chestBar{left:50%;''')
# the interact prompt and its progress bar also serve card grabs and van reboots
rep("const lt=useTgt.kind==='chest'&&useTgt.c.prog>0?'Opening chest':useTgt.label;","const lt=useTgt.kind==='chest'&&useTgt.c.prog>0?'Opening chest':(useTgt.busy&&useTgt.busy())||useTgt.label;")
rep("const pr=useTgt.kind==='chest'; $('usePB').hidden=!pr; if(pr) $('chestB').style.width=Math.min(100,useTgt.c.prog*100).toFixed(0)+'%';",
    "const pr=useTgt.kind==='chest'||!!useTgt.prog; $('usePB').hidden=!pr; if(pr) $('chestB').style.width=Math.min(100,(useTgt.prog?useTgt.prog():useTgt.c.prog)*100).toFixed(0)+'%';")
rep("  kartTargets(consider);\n  return best; }","  kartTargets(consider); rbTargets(consider);\n  return best; }")
rep("stepGrass(dt); stepChests(dt);","stepGrass(dt); stepChests(dt); stepReboot(dt);")
# vans are solid for people and buggies
rep("if(props.length) propsNear(E.pos.x,E.pos.z,ps);","if(props.length) propsNear(E.pos.x,E.pos.z,ps); if(VANS) for(const v of VANS) if(Math.abs(v.x-E.pos.x)<7&&Math.abs(v.z-E.pos.z)<7) ps.add(v.solid);")
rep("function kartHits(k,x,z,yaw,ox,oz){ const fx=-Math.sin(yaw), fz=-Math.cos(yaw), lo=k.y+0.45, hi=k.y+1.4, ps=near(x,z,1); propsNear(x,z,ps);",
    "function kartHits(k,x,z,yaw,ox,oz){ const fx=-Math.sin(yaw), fz=-Math.cos(yaw), lo=k.y+0.45, hi=k.y+1.4, ps=near(x,z,1); propsNear(x,z,ps); if(VANS) for(const v of VANS) if(Math.abs(v.x-x)<8&&Math.abs(v.z-z)<8) ps.add(v.solid);")
# going down: wait for a reboot when a teammate is still up, otherwise the old respawn
rep("    setTimeout(()=>{ net.dead=false; const a=Math.random()*Math.PI*2, r=8+Math.random()*20; respawn(); P.pos.set(SPAWN[0]+Math.cos(a)*r,0,SPAWN[2]+Math.sin(a)*r); if(skyDropAllowed()) skyDrop(P.pos.x,P.pos.z,SKY_BACK); },3000); }",
    "    afterDeath(); }",2)
rep("$('respawn').addEventListener('click',()=>{ respawn();","$('respawn').addEventListener('click',()=>{ if(RB.wait) rbGiveUp(false); else if(net.dead&&net.role) net.dead=false; respawn();")
rep("net.peer=null; net.role=null; net.host=null; net.conns.clear(); net.code=null; net.id='me'; net.dead=false;","net.peer=null; net.role=null; net.host=null; net.conns.clear(); net.code=null; net.id='me'; net.dead=false; rbReset();")
rep("function dropPlayer(id){ kartLeft(id);","function dropPlayer(id){ kartLeft(id); rbLeft(id);")
rep("  respawn(); if(m.mode==='horde') emptyLoadout(); sfx('win');","  rbReset(); respawn(); if(m.mode==='horde') emptyLoadout(); sfx('win');")
# networking: every rb message is a broadcast; the host applies it and relays it
rep("  else if(m.type==='ready'){ party.ready.set(from,!!m.v); partySync(); }","  else if(m.type==='ready'){ party.ready.set(from,!!m.v); partySync(); }\n  else if(m.type==='rb'){ onRb(m); netSend(m,from); }")
rep("  else if(m.type==='shot'){ if(m.id!==net.id) onShot(m); }","  else if(m.type==='shot'){ if(m.id!==net.id) onShot(m); }\n  else if(m.type==='rb') onRb(m);")
# sounds
rep("    case 'pickup':","""    case 'rb_grab': tone('sine',660,990,0.22,0.11); tone('sine',990,1480,0.3,0.08,0.07); tone('triangle',1480,1975,0.35,0.05,0.15); noise(7000,0.3,0.05,1,0,'highpass'); break;
    case 'rb_drop': tone('sine',520,780,0.5,0.07); tone('sine',780,1170,0.6,0.05,0.12); noise(5000,0.5,0.04,1,0.05,'highpass'); break;
    case 'rb_boot': tone('sawtooth',110,880,1.1,0.05); tone('sine',220,1760,1.15,0.07,0.04); noise(2500,0.9,0.06,0.7,0.15,'bandpass',9000); tone('triangle',880,1320,0.45,0.11,1.1); tone('triangle',1320,1760,0.5,0.08,1.25); break;
    case 'rb_tick': tone('square',1200,1180,0.03,0.025); break;
    case 'pickup':""")
# spectate a teammate while you wait
rep("function updateCamera(){\n","function updateCamera(){\n  if(rbSpectate()) return;\n")
# the map: cards on the ground and (only while someone on your team needs it) every van
rep("  horde.zs.forEach(z=>{ if(!z.alive) return; const px=tx(z.pos.x), pz=tz(z.pos.z); if(px<0||pz<0||px>S||pz>S) return; g.fillStyle=z.type==='brute'",
    "  rbMiniMap(g,tx,tz,c,dpr);\n  horde.zs.forEach(z=>{ if(!z.alive) return; const px=tx(z.pos.x), pz=tz(z.pos.z); if(px<0||pz<0||px>S||pz>S) return; g.fillStyle=z.type==='brute'")
rep("  if(B&&B.active&&B.h.group.visible) dot(B.pos.x,B.pos.z,'#ff4b3a');\n  // you: an arrow pointing where you face, with a soft pulse",
    "  if(B&&B.active&&B.h.group.visible) dot(B.pos.x,B.pos.z,'#ff4b3a');\n  rbBigMap(g,X,Z,u);\n  // you: an arrow pointing where you face, with a soft pulse")
rep("initKarts(); initForest();","initKarts(); initVans(); initForest();")

rep("\n/* ---------- controller (standard gamepad mapping) ----------",r"""
/* ---------- reboot cards and reboot vans ---------- */
var VANS; var RB={cards:new Map(),carry:new Set(),wait:null,noMate:0,spec:{yaw:0,who:null}};
var RB_TTL=100, RB_GRAB_T=1.0, RB_BOOT_T=4, RB_VAN_CD=25;
function rbCol(c){ return horde.on?0x3f8fff:(TEAM_COL[c.t]||0x3f8fff); }
function rbMate(c){ return c.id===net.id||horde.on||(+settings.team>0&&c.t===+settings.team); }
function rbMatesUp(){ let n=0; net.players.forEach(pl=>{ if(pl.id!=='bot'&&pl.alive&&sameTeam(pl)) n++; }); return n; }
function rbNeeded(){ for(const c of RB.cards.values()) if(rbMate(c)) return true; return RB.carry.size>0; }
function rbSend(m){ m.type='rb'; onRb(m); netSend(m); }
function rbRespawnNow(){ net.dead=false; const a=Math.random()*Math.PI*2, r=8+Math.random()*20; respawn(); P.pos.set(SPAWN[0]+Math.cos(a)*r,0,SPAWN[2]+Math.sin(a)*r); if(skyDropAllowed()) skyDrop(P.pos.x,P.pos.z,SKY_BACK); }
// you just went down in a room
function afterDeath(){
  RB.carry.forEach(id=>rbSend({op:'drop',id,p:[+P.pos.x.toFixed(2),+P.pos.y.toFixed(2),+P.pos.z.toFixed(2)]})); // cards you were carrying fall where you fell
  if(net.role&&(horde.on||+settings.team>0)&&rbMatesUp()>0){
    const [gy]=groundAt(P.pos.x,P.pos.z,P.pos.y+0.5,near(P.pos.x,P.pos.z)); RB.wait={t0:performance.now(),ttl:RB_TTL}; RB.noMate=0; RB.spec.who=null; RB.spec.yaw=P.yaw;
    rbSend({op:'card',id:net.id,n:net.name||'Player',t:+settings.team||0,o:outfitIdx(settings.outfit),p:[+P.pos.x.toFixed(2),+Math.max(gy,P.pos.y-40).toFixed(2),+P.pos.z.toFixed(2)],ttl:RB_TTL});
    return; }
  setTimeout(rbRespawnNow,3000); }
function rbGiveUp(drop=true){ if(!RB.wait) return; RB.wait=null; rbSend({op:'gone',id:net.id}); if(drop) rbRespawnNow(); else net.dead=false; }
function rbReset(){ RB.cards.forEach(c=>rbKill(c)); RB.cards.clear(); RB.carry.clear(); if(RB.wait){ RB.wait=null; net.dead=false; } if(VANS) VANS.forEach(v=>{ v.cd=0; v.prog=0; v.req=0; }); }
function rbLeft(id){ const c=RB.cards.get(id); if(c){ rbKill(c); RB.cards.delete(id); RB.carry.delete(id); } RB.cards.forEach(c=>{ if(c.holder===id){ c.holder=null; c.g.visible=true; } }); }
function rbKill(c){ if(c.g){ scene.remove(c.g); c.g.traverse(o=>{ if(o.geometry) o.geometry.dispose(); }); } }
function onRb(m){ const now=performance.now();
  if(m.op==='card'){ const old=RB.cards.get(m.id); if(old) rbKill(old);
    const c={id:m.id,n:m.n,t:m.t|0,o:m.o|0,x:m.p[0],y:m.p[1],z:m.p[2],holder:null,exp:now+(m.ttl||RB_TTL)*1000,prog:0,req:0}; c.g=rbCardMesh(c); RB.cards.set(m.id,c);
    if(m.id!==net.id&&rbMate(c)){ feed(`<b>${esc(c.n)}</b> is down · grab their reboot card`); sfxAt('rb_drop',new THREE.Vector3(c.x,c.y,c.z)); } }
  else if(m.op==='grab'){ if(m.id===net.id&&RB.wait){ const c=RB.cards.get(net.id); if(c&&!c.holder) rbSend({op:'held',id:net.id,by:m.by}); } }
  else if(m.op==='held'){ const c=RB.cards.get(m.id); if(!c) return; c.holder=m.by; c.prog=0; c.req=0; c.g.visible=false;
    if(m.by===net.id){ RB.carry.add(m.id); sfx('rb_grab'); toast('Got '+c.n+"'s card · take it to a Reboot Van"); }
    else if(m.id===net.id){ const pl=net.players.get(m.by); feed(`<b>${esc((pl&&pl.name)||'A teammate')}</b> picked up your card`); sfx('rb_grab'); } }
  else if(m.op==='drop'){ const c=RB.cards.get(m.id); if(!c) return; c.holder=null; c.x=m.p[0]; c.z=m.p[2]; const [gy]=groundAt(c.x,c.z,m.p[1]+0.5,near(c.x,c.z)); c.y=Math.max(gy,m.p[1]-40); c.g.visible=true; RB.carry.delete(m.id); }
  else if(m.op==='boot'){ if(m.id!==net.id||!RB.wait) return; const v=VANS&&VANS[m.van]; if(!v) return; RB.wait=null; net.dead=false; respawn(); emptyLoadout();
    const a=Math.random()*6.283; P.pos.set(v.x+Math.cos(a)*4,0,v.z+Math.sin(a)*4); if(skyDropAllowed()) skyDrop(P.pos.x,P.pos.z,SKY_AUTO+25); else P.pos.y=terrainH(P.pos.x,P.pos.z)+0.1;
    rbSend({op:'done',id:net.id,van:m.van,by:m.by}); banner('Rebooted','Back in the fight',2); }
  else if(m.op==='done'){ const c=RB.cards.get(m.id); const nm=c?c.n:'A teammate'; if(c){ rbKill(c); RB.cards.delete(m.id); } RB.carry.delete(m.id);
    const v=VANS&&VANS[m.van]; if(v){ v.cd=now+RB_VAN_CD*1000; v.prog=0; v.req=0; v.flash=2.4; if(Math.hypot(v.x-P.pos.x,v.z-P.pos.z)<140) sfxAt('rb_boot',new THREE.Vector3(v.x,v.y+2,v.z)); }
    if(m.by===net.id) feed(`You rebooted <b>${esc(nm)}</b>`); else if(m.id!==net.id){ const pl=net.players.get(m.by); feed(`<b>${esc((pl&&pl.name)||'A teammate')}</b> rebooted <b>${esc(nm)}</b>`); } }
  else if(m.op==='gone'){ const c=RB.cards.get(m.id); if(c){ rbKill(c); RB.cards.delete(m.id); } RB.carry.delete(m.id); }
}
function esc(s){ return String(s).replace(/[&<>"]/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'})[ch]); }
// ---- the card: a holographic trading card with your portrait, a sheen sweeping across it, a beam you can see from afar ----
function rbCardFace(c){ const W=256, H=360, cv=document.createElement('canvas'); cv.width=W; cv.height=H; const g=cv.getContext('2d'), col='#'+rbCol(c).toString(16).padStart(6,'0');
  const draw=img=>{ g.clearRect(0,0,W,H); const rr=(x,y,w,h,r)=>{ g.beginPath(); g.moveTo(x+r,y); g.arcTo(x+w,y,x+w,y+h,r); g.arcTo(x+w,y+h,x,y+h,r); g.arcTo(x,y+h,x,y,r); g.arcTo(x,y,x+w,y,r); g.closePath(); };
    const bg=g.createLinearGradient(0,0,0,H); bg.addColorStop(0,'#eaf6ff'); bg.addColorStop(0.18,col); bg.addColorStop(1,'#0a1a4a'); rr(4,4,W-8,H-8,22); g.fillStyle=bg; g.fill();
    g.save(); rr(4,4,W-8,H-8,22); g.clip(); g.globalAlpha=0.12; g.fillStyle='#fff'; for(let i=-H;i<W+H;i+=26){ g.beginPath(); g.moveTo(i,0); g.lineTo(i+12,0); g.lineTo(i+12-H*0.6,H); g.lineTo(i-H*0.6,H); g.fill(); }
    g.globalAlpha=0.22; for(let r=30;r<300;r+=34){ g.beginPath(); g.arc(W/2,H*0.42,r,0,7); g.strokeStyle='#fff'; g.lineWidth=1.5; g.stroke(); } g.restore(); g.globalAlpha=1;
    g.lineWidth=6; g.strokeStyle='#ffe08a'; rr(10,10,W-20,H-20,18); g.stroke(); g.lineWidth=2; g.strokeStyle='rgba(255,255,255,.7)'; rr(18,18,W-36,H-36,14); g.stroke();
    // the reboot glyph: a circular arrow
    g.save(); g.translate(W/2,44); g.strokeStyle='#fff'; g.lineWidth=5; g.beginPath(); g.arc(0,0,15,0.5,5.6); g.stroke(); g.fillStyle='#fff'; g.beginPath(); g.moveTo(15*Math.cos(5.6)+8,15*Math.sin(5.6)-1); g.lineTo(15*Math.cos(5.6)-6,15*Math.sin(5.6)-9); g.lineTo(15*Math.cos(5.6)-4,15*Math.sin(5.6)+8); g.fill(); g.restore();
    g.font='900 italic 20px "Arial Black",Arial,sans-serif'; g.textAlign='center'; g.fillStyle='#fff'; g.fillText('REBOOT',W/2,86);
    // the portrait in a glowing window
    g.save(); rr(40,98,W-80,182,14); g.fillStyle='rgba(4,10,30,.55)'; g.fill(); g.clip(); const gl=g.createRadialGradient(W/2,200,10,W/2,200,120); gl.addColorStop(0,'rgba(170,220,255,.75)'); gl.addColorStop(1,'rgba(170,220,255,0)'); g.fillStyle=gl; g.fillRect(40,98,W-80,182);
    if(img) g.drawImage(img,W/2-84,92,168,224); else { g.fillStyle='rgba(255,255,255,.8)'; g.beginPath(); g.arc(W/2,160,26,0,7); g.fill(); g.fillRect(W/2-34,192,68,80); } g.restore();
    g.lineWidth=3; g.strokeStyle='#ffe08a'; rr(40,98,W-80,182,14); g.stroke();
    const nm=String(c.n||'Player').slice(0,14).toUpperCase(); let fs=30; g.font=`900 italic ${fs}px "Arial Black",Arial,sans-serif`; while(g.measureText(nm).width>W-56&&fs>14){ fs-=2; g.font=`900 italic ${fs}px "Arial Black",Arial,sans-serif`; }
    g.lineWidth=5; g.strokeStyle='rgba(0,10,40,.8)'; g.strokeText(nm,W/2,320); g.fillStyle='#fff'; g.fillText(nm,W/2,320); tex.needsUpdate=true; };
  const tex=new THREE.CanvasTexture(cv); tex.anisotropy=4; const o=OUTFITS[c.o]||OUTFITS[0], src=document.querySelector(`#outfits [data-id="${o.id}"] img`);
  draw(null); if(src){ const im=new Image(); im.onload=()=>draw(im); im.src=src.src; } return tex; }
var _rbSheen=null, _rbBeam=null;
function rbCardMesh(c){ const g=new THREE.Group(), col=rbCol(c), tex=rbCardFace(c), W=0.78, H=1.1;
  const face=new THREE.MeshBasicMaterial({map:tex,transparent:true,fog:false}); const f1=new THREE.Mesh(new THREE.PlaneGeometry(W,H),face), f2=f1.clone(); f2.rotation.y=Math.PI; f1.position.z=0.006; f2.position.z=-0.006;
  const frame=new THREE.Mesh(new THREE.BoxGeometry(W*0.97,H*0.97,0.01),new THREE.MeshBasicMaterial({color:col,fog:false}));
  if(!_rbSheen){ const cv=document.createElement('canvas'); cv.width=128; cv.height=8; const x=cv.getContext('2d'), gr=x.createLinearGradient(0,0,128,0); gr.addColorStop(0,'rgba(255,255,255,0)'); gr.addColorStop(0.45,'rgba(255,255,255,0)'); gr.addColorStop(0.5,'rgba(255,255,255,.85)'); gr.addColorStop(0.55,'rgba(255,255,255,0)'); gr.addColorStop(1,'rgba(255,255,255,0)'); x.fillStyle=gr; x.fillRect(0,0,128,8); _rbSheen=new THREE.CanvasTexture(cv); _rbSheen.wrapS=THREE.RepeatWrapping; }
  const shT=_rbSheen.clone(); shT.needsUpdate=true; shT.wrapS=THREE.RepeatWrapping; shT.repeat.set(0.6,1); shT.rotation=0.5; shT.center.set(0.5,0.5);
  const sheen=new THREE.Mesh(new THREE.PlaneGeometry(W*0.94,H*0.94),new THREE.MeshBasicMaterial({map:shT,transparent:true,blending:THREE.AdditiveBlending,depthWrite:false,fog:false,side:THREE.DoubleSide})); sheen.position.z=0.009;
  const card=new THREE.Group(); card.add(frame,f1,f2,sheen); card.position.y=1.35; g.add(card);
  if(!_rbBeam){ const cv=document.createElement('canvas'); cv.width=4; cv.height=128; const x=cv.getContext('2d'), gr=x.createLinearGradient(0,128,0,0); gr.addColorStop(0,'rgba(255,255,255,.85)'); gr.addColorStop(0.25,'rgba(255,255,255,.35)'); gr.addColorStop(1,'rgba(255,255,255,0)'); x.fillStyle=gr; x.fillRect(0,0,4,128); _rbBeam=new THREE.CanvasTexture(cv); }
  const beam=new THREE.Mesh(new THREE.CylinderGeometry(0.32,0.32,36,20,1,true).translate(0,18,0),new THREE.MeshBasicMaterial({map:_rbBeam,color:col,transparent:true,opacity:0.55,blending:THREE.AdditiveBlending,depthWrite:false,side:THREE.DoubleSide,fog:false}));
  const core=new THREE.Mesh(new THREE.CylinderGeometry(0.06,0.06,36,8,1,true).translate(0,18,0),new THREE.MeshBasicMaterial({map:_rbBeam,color:0xffffff,transparent:true,opacity:0.6,blending:THREE.AdditiveBlending,depthWrite:false,fog:false}));
  const ring=new THREE.Mesh(new THREE.RingGeometry(0.45,0.62,48).rotateX(-Math.PI/2),new THREE.MeshBasicMaterial({color:col,transparent:true,opacity:0.7,blending:THREE.AdditiveBlending,depthWrite:false,fog:false})); ring.position.y=0.04;
  const N=16, pos=new Float32Array(N*3); for(let i=0;i<N;i++){ const a=Math.random()*6.283, r=0.15+Math.random()*0.45; pos[i*3]=Math.cos(a)*r; pos[i*3+1]=Math.random()*2.2; pos[i*3+2]=Math.sin(a)*r; }
  const pg=new THREE.BufferGeometry(); pg.setAttribute('position',new THREE.BufferAttribute(pos,3)); const sparks=new THREE.Points(pg,new THREE.PointsMaterial({color:0xcfeaff,size:0.07,transparent:true,opacity:0.9,blending:THREE.AdditiveBlending,depthWrite:false,fog:false}));
  g.add(beam,core,ring,sparks); g.position.set(c.x,c.y,c.z); scene.add(g); c.card=card; c.sheen=shT; c.beam=beam; c.ring=ring; c.sparks=sparks; c.ph=Math.random()*6; return g; }
// ---- the vans: one parked outside every town, broadside on to the town so its terminal faces you ----
function initVans(){ VANS=[]; const vanCfg=[];
  TOWNS.forEach((t,k)=>{ const r=seeded(4400+k*31), a0=r()*6.283; let best=null;
    for(let ring=0;ring<3&&!best;ring++) for(let q=0;q<16;q++){ const a=a0+q*Math.PI/8, R=t.R+9+ring*6, x=t.x+Math.cos(a)*R, z=t.z+Math.sin(a)*R;
      if(townAt(x,z,3)||roadDistAt(x,z)<ROAD_HW+4.5||slopeAt(x,z)[0]>0.22) continue; if(chests.some(c=>Math.hypot(c.x-x,c.z-z)<10)) continue;
      if(karts&&karts.some(kk=>Math.hypot(kk.x-x,kk.z-z)<10)) continue; best={x,z,a}; break; }
    if(!best) return; const dx=t.x-best.x, dz=t.z-best.z; let yaw=0, bd=-9; for(const y of [0,Math.PI/2,Math.PI,Math.PI*1.5]){ const d=Math.cos(y)*dx-Math.sin(y)*dz; if(d>bd){ bd=d; yaw=y; } }
    vanCfg.push({x:best.x,z:best.z,yaw,town:t.name}); });
  vanCfg.forEach((o,i)=>{ const y=Math.min(...[[-1.2,-2.2],[1.2,-2.2],[-1.2,2.2],[1.2,2.2],[0,0]].map(([a,b])=>terrainH(o.x+a,o.z+b))); const v=makeVan(o.x,y-0.05,o.z,o.yaw); v.id=i; v.town=o.town; VANS.push(v);
    props.forEach(p=>{ if(!p.gone&&Math.hypot(p.x-o.x,p.z-o.z)<7.5){ p.gone=true; p.alive=false; p.g.visible=false; } }); }); }
var _vanMats;
function vanScreen(ready){ const cv=document.createElement('canvas'); cv.width=256; cv.height=128; const g=cv.getContext('2d'); const gr=g.createLinearGradient(0,0,0,128); gr.addColorStop(0,ready?'#1c5cff':'#3a3f4a'); gr.addColorStop(1,ready?'#0a1f6a':'#1a1d24'); g.fillStyle=gr; g.fillRect(0,0,256,128);
  g.strokeStyle=ready?'#9fe0ff':'#8a8f99'; g.lineWidth=4; g.strokeRect(6,6,244,116); g.save(); g.translate(58,64); g.lineWidth=7; g.strokeStyle='#fff'; g.beginPath(); g.arc(0,0,26,0.5,5.6); g.stroke(); g.fillStyle='#fff'; g.beginPath(); g.moveTo(26*Math.cos(5.6)+12,26*Math.sin(5.6)-2); g.lineTo(26*Math.cos(5.6)-9,26*Math.sin(5.6)-14); g.lineTo(26*Math.cos(5.6)-6,26*Math.sin(5.6)+12); g.fill(); g.restore();
  g.fillStyle='#fff'; g.font='900 italic 34px "Arial Black",Arial,sans-serif'; g.textAlign='left'; g.textBaseline='middle'; g.fillText(ready?'REBOOT':'CHARGING',100,64); const t=new THREE.CanvasTexture(cv); return new THREE.MeshBasicMaterial({map:t}); }
function makeVan(x,y,z,yaw){ if(!_vanMats) _vanMats={white:new THREE.MeshPhongMaterial({color:0xf1f3f6,shininess:60,specular:0x444444}),blue:new THREE.MeshPhongMaterial({color:0x1f5fd8,shininess:70,specular:0x555555}),orange:new THREE.MeshPhongMaterial({color:0xff7a1a,shininess:40}),
    dark:new THREE.MeshPhongMaterial({color:0x22262d,shininess:30}),glass:new THREE.MeshPhongMaterial({color:0x2a4466,shininess:120,specular:0xaaccff}),rub:new THREE.MeshLambertMaterial({color:0x18191c}),metal:new THREE.MeshPhongMaterial({color:0xb8bec6,shininess:90,specular:0x888888}),
    lamp:new THREE.MeshBasicMaterial({color:0x9fe0ff}),ready:vanScreen(true),wait:vanScreen(false)};
  const M=_vanMats, g=new THREE.Group(), add=(geo,mat,px,py,pz,rx=0,ry=0,rz=0)=>{ const m=new THREE.Mesh(geo,mat); m.position.set(px,py,pz); m.rotation.set(rx,ry,rz); m.castShadow=m.receiveShadow=true; g.add(m); return m; };
  const B=(w,h,d)=>new THREE.BoxGeometry(w,h,d);
  add(B(2.0,0.35,4.3),M.dark,0,0.62,0);                       // chassis
  add(B(2.12,2.05,2.9),M.white,0,1.82,0.55);                  // the box at the back
  add(B(2.14,0.26,2.92),M.blue,0,1.32,0.55); add(B(2.15,0.07,2.93),M.orange,0,1.5,0.55); // livery stripes
  add(B(2.0,1.45,1.35),M.white,0,1.52,-1.5);                  // cab
  add(B(2.02,0.5,1.37),M.blue,0,0.98,-1.5);
  add(B(1.84,0.62,0.06),M.glass,0,1.92,-2.17,-0.18); for(const s of [-1,1]) add(B(0.06,0.55,0.9),M.glass,s*1.005,1.95,-1.55);
  add(B(2.1,0.22,0.12),M.metal,0,0.8,-2.2); for(const s of [-1,1]){ add(new THREE.CylinderGeometry(0.11,0.11,0.05,14).rotateX(Math.PI/2),M.lamp,s*0.75,1.2,-2.19); add(B(0.16,0.1,0.04),new THREE.MeshBasicMaterial({color:0xd01818}),s*0.9,1.25,2.01); }
  for(const [wx,wz] of [[-1,-1.45],[1,-1.45],[-1,1.35],[1,1.35]]){ add(new THREE.CylinderGeometry(0.46,0.46,0.32,20).rotateZ(Math.PI/2),M.rub,wx*0.92,0.46,wz); add(new THREE.CylinderGeometry(0.26,0.26,0.34,12).rotateZ(Math.PI/2),M.metal,wx*0.92,0.46,wz); }
  // the roof: a dish on a mast and a light bar that blazes when someone's rebooted
  add(new THREE.CylinderGeometry(0.05,0.05,0.7,8),M.metal,0.4,3.2,0.9); const dish=add(new THREE.SphereGeometry(0.62,20,10,0,Math.PI*2,0,Math.PI*0.42),M.white,0.4,3.55,0.9,-0.9,0,0.3); dish.material=M.white;
  add(new THREE.CylinderGeometry(0.04,0.04,0.5,6),M.metal,0.4,3.55,0.55,-0.9);
  const beacon=add(B(0.9,0.14,0.22),M.lamp,-0.35,2.93,-0.1);
  // the terminal on the kerb side: a screen and two handles
  const term=new THREE.Group(); term.position.set(1.07,1.62,0.55); g.add(term);
  const panel=new THREE.Mesh(B(0.08,0.95,1.5),M.dark); term.add(panel); const scr=new THREE.Mesh(new THREE.PlaneGeometry(1.32,0.66),M.ready); scr.rotation.y=Math.PI/2; scr.position.x=0.045; scr.position.y=0.06; term.add(scr);
  g.position.set(x,y,z); g.rotation.y=yaw; scene.add(g);
  const flare=new THREE.Mesh(new THREE.CylinderGeometry(0.55,0.55,46,20,1,true).translate(0,23,0),new THREE.MeshBasicMaterial({color:0x7fc8ff,transparent:true,opacity:0,blending:THREE.AdditiveBlending,depthWrite:false,side:THREE.DoubleSide,fog:false})); flare.position.y=2.9; flare.visible=false; g.add(flare);
  const c=Math.round(Math.cos(yaw)), s=Math.round(Math.sin(yaw)), hx=Math.abs(c)*1.08+Math.abs(s)*2.2, hz=Math.abs(s)*1.08+Math.abs(c)*2.2;
  const tx=x+c*1.75, tz=z-s*1.75; // where you stand to use the terminal (local +x, rotated)
  return {x,y,z,yaw,g,scr,beacon,flare,cd:0,prog:0,req:0,flash:0,tx,tz,solid:{boxes:[[x-hx,y,z-hz,x+hx,y+2.85,z+hz]],key:'van'+Math.round(x)+'_'+Math.round(z),isVan:true}}; }
// ---- interact: grab a card (hold), reboot at a van (hold) ----
function rbTargets(consider){ if(!net.role) return; const now=performance.now();
  RB.cards.forEach(c=>{ if(c.holder||c.id===net.id||!rbMate(c)) return; consider(c.x,c.y,c.z,2.4,{kind:'rcard',pri:2,c,label:'Grab '+c.n+"'s reboot card",prog:()=>c.prog,busy:()=>c.prog>0?'Grabbing card':null}); });
  if(RB.carry.size&&VANS) VANS.forEach(v=>{ const ready=now>=v.cd, names=[...RB.carry].map(id=>(RB.cards.get(id)||{}).n||'teammate').join(' & ');
    consider(v.tx,v.y,v.tz,2.6,{kind:'rvan',pri:2,v,label:ready?'Reboot '+names:'Van charging · '+Math.ceil((v.cd-now)/1000)+'s',prog:ready?()=>v.prog:null,busy:()=>v.prog>0?'Rebooting '+names:null}); }); }
var _rbTick=0;
function stepReboot(dt){ if(!net.role&&!RB.cards.size) return; const now=performance.now(), T=now/1000;
  // hold to grab / hold to reboot
  for(const c of RB.cards.values()){ const on=useHeld&&useTgt&&useTgt.kind==='rcard'&&useTgt.c===c&&!isDead();
    if(on&&!c.req){ c.prog+=dt/RB_GRAB_T; if(c.prog>=1){ c.req=now; rbSend({op:'grab',id:c.id,by:net.id}); } } else if(!on&&!c.req) c.prog=Math.max(0,c.prog-dt*3);
    if(c.req&&now-c.req>2000&&!c.holder){ c.req=0; c.prog=0; } }
  if(VANS) for(const v of VANS){ const on=useHeld&&useTgt&&useTgt.kind==='rvan'&&useTgt.v===v&&!isDead()&&now>=v.cd&&RB.carry.size>0;
    if(on&&!v.req){ v.prog+=dt/RB_BOOT_T; _rbTick-=dt; if(_rbTick<=0){ _rbTick=0.25; sfx('rb_tick'); } if(v.prog>=1){ v.req=now; RB.carry.forEach(id=>rbSend({op:'boot',id,by:net.id,van:v.id})); } }
    else if(!on&&!v.req) v.prog=Math.max(0,v.prog-dt*2);
    if(v.req&&now-v.req>3000){ v.req=0; v.prog=0; }
    // looks: the screen says ready or charging; the light bar pulses while it charges you up, and a column of light goes up when it fires
    const ready=now>=v.cd; if(v.scr.material!==(ready?_vanMats.ready:_vanMats.wait)) v.scr.material=ready?_vanMats.ready:_vanMats.wait;
    const lit=v.prog>0?0.6+0.4*Math.sin(T*18):ready?0.55+0.25*Math.sin(T*2.2+v.id):0.15; v.beacon.scale.set(1,1,1); v.beacon.material.color.setHSL(0.56,1,0.35+0.4*lit);
    if(v.flash>0||v.prog>0){ v.flash=Math.max(0,v.flash-dt); v.flare.visible=true; v.flare.material.opacity=Math.max(v.prog*0.35,Math.min(1,v.flash)*0.7); } else if(v.flare.visible) v.flare.visible=false; }
  // cards bob, spin and shimmer
  for(const c of RB.cards.values()){ if(!c.g.visible) continue; const d=Math.hypot(c.x-camera.position.x,c.z-camera.position.z); if(d>600) continue;
    c.card.rotation.y+=dt*1.3; c.card.position.y=1.35+Math.sin(T*2+c.ph)*0.12; c.sheen.offset.x=(T*0.45+c.ph)%1;
    c.beam.material.opacity=0.38+0.17*Math.sin(T*3+c.ph); const s=1+0.18*Math.sin(T*4+c.ph); c.ring.scale.set(s,1,s);
    const pa=c.sparks.geometry.attributes.position; for(let i=0;i<pa.count;i++){ let y=pa.getY(i)+dt*(0.35+(i%5)*0.08); if(y>2.4) y=0.05; pa.setY(i,y); } pa.needsUpdate=true;
    // settle onto whatever is under it now (a build broken out from under it)
    if(d<80){ const [gy]=groundAt(c.x,c.z,c.y+0.3,near(c.x,c.z)); if(gy<c.y-0.02) c.y=Math.max(gy,c.y-dt*9); } c.g.position.set(c.x,c.y,c.z);
    if(now>c.exp+8000&&c.id!==net.id){ rbKill(c); RB.cards.delete(c.id); } } // its owner left without saying (they respawned or dropped)
  // you, waiting
  const el=$('rbWait');
  if(RB.wait){ const left=Math.max(0,RB.wait.ttl-(now-RB.wait.t0)/1000), mine=RB.cards.get(net.id), hold=mine&&mine.holder, hp=hold&&net.players.get(hold);
    if(rbMatesUp()===0){ RB.noMate+=dt; if(RB.noMate>3){ feed('No teammates left standing · respawning'); rbGiveUp(true); } } else RB.noMate=0;
    if(left<=0&&RB.wait){ feed('Your card expired · respawning'); rbGiveUp(true); }
    if(RB.wait){ if(el.hidden) el.hidden=false; const msg=hold?((hp&&hp.name)||'A teammate')+' has your card · heading to a van':'Your card is waiting where you fell';
      if($('rbMsg').textContent!==msg) $('rbMsg').textContent=msg; const who=RB.spec.who&&net.players.get(RB.spec.who), sub=(who?'Spectating '+(who.name||'teammate')+' · ':'')+'card expires in '+Math.floor(left/60)+':'+String(Math.floor(left%60)).padStart(2,'0');
      if($('rbSub').textContent!==sub) $('rbSub').textContent=sub; $('rbBar').style.transform='scaleX('+(left/RB.wait.ttl).toFixed(3)+')'; } }
  if(!RB.wait&&!el.hidden) el.hidden=true;
  // you, carrying
  const ce=$('rbCarry'); if(RB.carry.size&&!isDead()){ const names=[...RB.carry].map(id=>(RB.cards.get(id)||{}).n||'teammate').join(' & '), t='Carrying '+names+"'s card · find a Reboot Van";
    if(ce.hidden) ce.hidden=false; if($('rbCarryT').textContent!==t) $('rbCarryT').textContent=t; } else if(!ce.hidden) ce.hidden=true; }
// waiting for a reboot: watch a teammate (the one carrying your card first), orbiting slowly behind them
function rbSpectate(){ if(!RB.wait) return false; const mine=RB.cards.get(net.id); let pl=mine&&mine.holder&&net.players.get(mine.holder);
  if(!pl||!pl.alive){ pl=null; net.players.forEach(q=>{ if(!pl&&q.id!=='bot'&&q.alive&&sameTeam(q)) pl=q; }); } if(!pl) return false;
  if(RB.spec.who!==pl.id){ RB.spec.who=pl.id; RB.spec.yaw=pl.dyaw??pl.yaw; }
  RB.spec.yaw+=angDiff(pl.dyaw??pl.yaw,RB.spec.yaw)*Math.min(1,lastDt*2.5);
  const px=pl.pos.x, py=pl.pos.y+1.5, pz=pl.pos.z; camera.position.set(px+Math.sin(RB.spec.yaw)*4.8,py+1.3,pz+Math.cos(RB.spec.yaw)*4.8);
  const gy=terrainH(camera.position.x,camera.position.z)+0.4; if(camera.position.y<gy) camera.position.y=gy; camera.lookAt(px,py,pz);
  hero.visible=false; skyDome.position.copy(camera.position);
  { const st=(sc.right-sc.left)/sun.shadow.mapSize.x, a=Math.round(pl.pos.dot(_lX)/st)*st, b=Math.round(pl.pos.dot(_lY)/st)*st, cc=pl.pos.dot(SUN_DIR);
    sun.target.position.set(0,0,0).addScaledVector(_lX,a).addScaledVector(_lY,b).addScaledVector(SUN_DIR,cc); sun.position.copy(sun.target.position).addScaledVector(SUN_DIR,65); }
  return true; }
// ---- map icons ----
function rbVanIcon(g,x,y,s,ready){ g.save(); g.translate(x,y); g.fillStyle=ready?'#1f5fd8':'#59606b'; g.strokeStyle='#fff'; g.lineWidth=1.4*s/7; const w=s*1.5, h=s*1.1;
  g.beginPath(); if(g.roundRect) g.roundRect(-w/2,-h/2,w,h,s*0.25); else g.rect(-w/2,-h/2,w,h); g.fill(); g.stroke();
  g.strokeStyle='#fff'; g.lineWidth=s*0.18; g.beginPath(); g.arc(0,0,s*0.3,0.5,5.6); g.stroke(); g.restore(); }
function rbCardIcon(g,x,y,s,col){ g.save(); g.translate(x,y); g.shadowColor=col; g.shadowBlur=s*1.2; g.fillStyle=col; g.strokeStyle='#ffe08a'; g.lineWidth=s*0.2;
  g.beginPath(); g.moveTo(0,-s); g.lineTo(s*0.7,0); g.lineTo(0,s); g.lineTo(-s*0.7,0); g.closePath(); g.fill(); g.shadowBlur=0; g.stroke(); g.restore(); }
function rbMiniMap(g,tx,tz,c,dpr){ if(!rbNeeded()) return; const now=performance.now(), clampTo=(px,pz,r)=>{ const dx=px-c, dz=pz-c, m=Math.hypot(dx,dz), lim=c-r-2; return m>lim?[c+dx/m*lim,c+dz/m*lim]:[px,pz]; };
  if(VANS) VANS.forEach(v=>{ const [qx,qz]=clampTo(tx(v.x),tz(v.z),7*dpr); rbVanIcon(g,qx,qz,6*dpr,now>=v.cd); });
  RB.cards.forEach(cd=>{ if(cd.holder||!rbMate(cd)) return; const [qx,qz]=clampTo(tx(cd.x),tz(cd.z),6*dpr); rbCardIcon(g,qx,qz,5*dpr,'#'+rbCol(cd).toString(16).padStart(6,'0')); }); }
function rbBigMap(g,X,Z,u){ if(!rbNeeded()) return; const now=performance.now();
  if(VANS) VANS.forEach(v=>{ rbVanIcon(g,X(v.x),Z(v.z),8*u,now>=v.cd); g.font=`800 ${Math.round(10*u)}px "Chakra Petch",sans-serif`; g.textAlign='center'; g.textBaseline='top'; g.lineWidth=3*u; g.strokeStyle='rgba(0,0,0,.75)'; g.fillStyle='#bfe0ff'; g.strokeText('Reboot Van',X(v.x),Z(v.z)+8*u); g.fillText('Reboot Van',X(v.x),Z(v.z)+8*u); });
  RB.cards.forEach(cd=>{ if(cd.holder||!rbMate(cd)) return; rbCardIcon(g,X(cd.x),Z(cd.z),7*u,'#'+rbCol(cd).toString(16).padStart(6,'0')); }); }

/* ---------- controller (standard gamepad mapping) ----------""")
# a reboot card (or a van, or a downed teammate) wins over loot lying on the same spot, so the hold isn't interrupted
rep("const face=d>0.05?(dx*fx+dz*fz)/d:1, s=d-face*0.9;","const face=d>0.05?(dx*fx+dz*fz)/d:1, s=d-face*0.9-(o.pri||0);")
