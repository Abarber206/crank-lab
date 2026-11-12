# patch161: the battle bus. A Battle royale match starts with everyone riding a blue bus under a striped hot-air
# balloon on a straight line across the island, high up (a different line each match, shown on the maps). Jump out
# when you like (Jump: Space, or the jump button); you skydive from there. The bots pick their moment: each team
# jumps where the line passes closest to where it wants to land; your teammates jump right after you. Anyone still
# aboard at the far end is dropped out. The storm's first countdown starts when the bus has crossed. Sounds: the horn
# as it sets off, the engine and the balloon's burner while you ride, a rush of air when you jump.
rep("""var BR={on:false,bots:[]""","""const BRBUS={g:null,on:false,t:0,T:1,ax:0,az:0,bx:0,bz:0,y:0,yaw:0,snd:null,burnT:0};
function brBusModel(){ if(BRBUS.g) return BRBUS.g; const g=new THREE.Group(), M=c=>new THREE.MeshLambertMaterial({color:c}), box=(w,h,d,c,x,y,z)=>{ const m=new THREE.Mesh(rbox(w,h,d,Math.min(w,h,d)*0.12),M(c)); m.position.set(x,y,z); m.castShadow=true; g.add(m); return m; };
  box(2.7,2.3,8.6,0x2f6fe0,0,0,0); box(2.74,0.5,8.64,0xf2f2f2,0,0.95,0); box(2.76,0.62,7.0,0x1a2a40,0,0.25,0.2); box(2.4,0.9,0.1,0x1a2a40,0,0.3,-4.33); // body, white roof band, windows, windscreen
  box(2.0,0.3,0.12,0xffd23a,0,-0.55,-4.34); [-0.85,0.85].forEach(x=>box(0.3,0.22,0.08,0xfff3b0,x,-0.6,-4.36)); // bumper, lights
  [[-1.2,-2.8],[1.2,-2.8],[-1.2,2.8],[1.2,2.8]].forEach(([x,z])=>{ const w=new THREE.Mesh(new THREE.CylinderGeometry(0.55,0.55,0.4,16),M(0x1b1c20)); w.rotation.z=Math.PI/2; w.position.set(x*1.06,-1.15,z); g.add(w); });
  // the balloon: gores in two colours, a burner under it, and ropes down to the roof
  const B=new THREE.Group(); B.position.y=10.5; g.add(B); for(let i=0;i<12;i++){ const s=new THREE.Mesh(new THREE.SphereGeometry(5.2,6,18,i*Math.PI/6,Math.PI/6),M(i%2?0xffffff:0x2f6fe0)); s.scale.y=1.15; B.add(s); }
  const neck=new THREE.Mesh(new THREE.CylinderGeometry(1.4,2.6,2.2,16,1,true),M(0x2f6fe0)); neck.material.side=THREE.DoubleSide; neck.position.y=-5.8; B.add(neck);
  const fl=new THREE.Mesh(new THREE.ConeGeometry(0.45,1.6,10),new THREE.MeshBasicMaterial({color:0xffa030,transparent:true,opacity:0.85})); fl.position.y=-6.6; B.add(fl); BRBUS.flame=fl;
  for(const [x,z] of [[-1.2,-3.6],[1.2,-3.6],[-1.2,3.6],[1.2,3.6]]){ const a=new THREE.Vector3(x,1.2,z), b=new THREE.Vector3(x*0.9,4.1,z*0.35), r=new THREE.Mesh(new THREE.CylinderGeometry(0.03,0.03,a.distanceTo(b),5),M(0x6b5a44)); r.position.copy(a).add(b).multiplyScalar(0.5); r.lookAt(b); r.rotateX(Math.PI/2); g.add(r); }
  g.visible=false; scene.add(g); return BRBUS.g=g; }
function brBusPos(t,out){ const k=Math.max(0,Math.min(1,t/BRBUS.T)); return out.set(BRBUS.ax+(BRBUS.bx-BRBUS.ax)*k,BRBUS.y,BRBUS.az+(BRBUS.bz-BRBUS.az)*k); }
function brBusStart(){ const a=Math.random()*Math.PI*2, off=(Math.random()-.5)*MAP_R*0.75, dx=Math.cos(a), dz=Math.sin(a), px=-dz, pz=dx, cx=SPAWN[0]+px*off, cz=SPAWN[2]+pz*off, L=MAP_R*1.12;
  BRBUS.ax=cx-dx*L; BRBUS.az=cz-dz*L; BRBUS.bx=cx+dx*L; BRBUS.bz=cz+dz*L; BRBUS.yaw=Math.atan2(-dx,-dz); BRBUS.dx=dx; BRBUS.dz=dz;
  let top=0; for(let s=0;s<=60;s++){ const x=BRBUS.ax+(BRBUS.bx-BRBUS.ax)*s/60, z=BRBUS.az+(BRBUS.bz-BRBUS.az)*s/60; top=Math.max(top,terrainH(x,z)); } BRBUS.y=Math.max(top+190,SPAWN[1]+330);
  BRBUS.T=2*L/34; BRBUS.t=0; BRBUS.on=true; brBusModel().visible=true; sfx('honk');
  if(AC&&!BRBUS.snd) BRBUS.snd=loopSound(out=>{ const o1=AC.createOscillator(), o2=AC.createOscillator(), f=AC.createBiquadFilter(), n=AC.createBufferSource(), nf=AC.createBiquadFilter(), ng=AC.createGain();
      o1.type='sawtooth'; o1.frequency.value=52; o2.type='sawtooth'; o2.frequency.value=78.5; f.type='lowpass'; f.frequency.value=360; f.Q.value=2; const og=AC.createGain(); og.gain.value=0.16; o1.connect(f); o2.connect(f); f.connect(og).connect(out);
      n.buffer=noiseBuf; n.loop=true; nf.type='bandpass'; nf.frequency.value=900; nf.Q.value=0.7; ng.gain.value=0.22; n.connect(nf).connect(ng).connect(out); o1.start(); o2.start(); n.start(); BRBUS.burnG=ng; return [o1,o2,n]; }); }
// a team's drop: somewhere it wants to land near the bus's line, and the point on the line closest to it
function brTeamDrop(){ for(let k=0;k<30;k++){ const [x,z]=brSpot(), vx=BRBUS.bx-BRBUS.ax, vz=BRBUS.bz-BRBUS.az, L2=vx*vx+vz*vz, s=Math.max(0.06,Math.min(0.94,((x-BRBUS.ax)*vx+(z-BRBUS.az)*vz)/L2)), qx=BRBUS.ax+vx*s, qz=BRBUS.az+vz*s;
    if(Math.hypot(x-qx,z-qz)<380||k===29) return {x,z,s}; } }
function brJumpOut(E){ if(!E.bus) return; E.bus=false; const p=brBusPos(BRBUS.t,new THREE.Vector3()), h=Math.max(60,BRBUS.y-terrainH(p.x,p.z)-4);
  skyDrop(p.x+(Math.random()-.5)*2,p.z+(Math.random()-.5)*2,h,E); E.vel.set(BRBUS.dx*16,-6,BRBUS.dz*16);
  if(E===P){ sfx('bus_jump'); $('busTip').hidden=true; for(const b of BR.bots) if(b.bus&&b.team===0) b.jumpAt=BRBUS.t+0.3+Math.random()*0.9; }
  else { E.h.group.visible=true; } }
var BR={on:false,bots:[]""")
# the start: everyone aboard; the first storm countdown waits for the bus
rep("""    b.h.group.visible=true; animEvent(b.h,'revive'); skyDrop(x,z,SKY_MATCH*(b.team===0?0.98:0.75+Math.random()*0.3),b); b.land=[x,z]; }
  mates.forEach(b=>teamMarker(b)); if(skyDropAllowed())""","""    b.h.group.visible=false; animEvent(b.h,'revive'); b.sky=null; b.land=[x,z]; }
  mates.forEach(b=>teamMarker(b));
  brBusStart(); const drop=new Map(); for(const b of BR.bots){ if(!drop.has(b.team)) drop.set(b.team,brTeamDrop()); const d=drop.get(b.team); b.bus=true; b.land=[d.x+(Math.random()-.5)*14,d.z+(Math.random()-.5)*14]; b.jumpAt=b.team===0?Infinity:d.s*BRBUS.T+Math.random()*1.2; }
  P.bus=true; P.sky=null; P.vel.set(0,0,0); $('busTip').hidden=false;
  if(false)""")
rep("""  BR.storm={cx:SPAWN[0],cz:SPAWN[2],r:MAP_R*1.08,ph:0,state:'wait',t:BR_SHRINK[0][0]};""","""  BR.storm={cx:SPAWN[0],cz:SPAWN[2],r:MAP_R*1.08,ph:0,state:'wait',t:BR_SHRINK[0][0]+BRBUS.T};""")
rep("""function brStop(){ BR.on=false;""","""function brStop(){ BR.on=false; BRBUS.on=false; if(BRBUS.g) BRBUS.g.visible=false; if(BRBUS.snd) BRBUS.snd.set(0); P.bus=false; $('busTip').hidden=true;""")
rep("""  const S=BR.storm, now=performance.now(); BR.frame++;""","""  const S=BR.storm, now=performance.now(); BR.frame++;
  // the bus: on across the island; riders go where it goes; jump when you like, the bots when they planned to
  if(BRBUS.on){ BRBUS.t+=dt; const p=brBusPos(BRBUS.t,_brBP), G=BRBUS.g; G.position.set(p.x,p.y+Math.sin(now/900)*0.4,p.z); G.rotation.set(Math.sin(now/1300)*0.02,BRBUS.yaw,Math.sin(now/1100)*0.03);
    BRBUS.burnT-=dt; if(BRBUS.burnT<=0) BRBUS.burnT=1.5+Math.random()*3; const burn=BRBUS.burnT<0.8; BRBUS.flame.visible=burn; BRBUS.flame.scale.setScalar(0.8+Math.random()*0.4);
    if(BRBUS.snd){ BRBUS.snd.set(P.bus?0.75:0.45,p); if(BRBUS.burnG) BRBUS.burnG.gain.setTargetAtTime(burn?0.5:0.12,AC.currentTime,0.1); }
    if(P.bus){ P.pos.set(p.x,p.y+1.2,p.z); P.vel.set(0,0,0); P.onGround=false; P.fallTop=null; if(BRBUS.t>1.5&&(isHeld('jump')||touchJump)) brJumpOut(P); }
    for(const b of BR.bots) if(b.bus){ b.pos.set(p.x,p.y,p.z); b.vel.set(0,0,0); if(BRBUS.t>=b.jumpAt) brJumpOut(b); }
    if(BRBUS.t>=BRBUS.T){ if(P.bus) brJumpOut(P); for(const b of BR.bots) if(b.bus) brJumpOut(b); }
    if(BRBUS.t>=BRBUS.T+8||Math.hypot(p.x-SPAWN[0],p.z-SPAWN[2])>MAP_R*1.6){ BRBUS.on=false; G.visible=false; if(BRBUS.snd) BRBUS.snd.set(0); } }""")
rep("""function brStepBot(b,dt,now){
  const S=BR.storm;""","""const _brBP=new THREE.Vector3();
function brStepBot(b,dt,now){
  const S=BR.storm; if(b.bus) return;""")
rep("""    if(!BR.out&&!P.sky&&brOut(P,S)){""","""    if(!BR.out&&!P.sky&&!P.bus&&brOut(P,S)){""")
rep("""function brFoes(b){ const a=[]; if(b.team!==0&&!BR.out&&P.hp>0&&!P.sky)""","""function brFoes(b){ const a=[]; if(b.team!==0&&!BR.out&&P.hp>0&&!P.sky&&!P.bus)""")
rep("""for(const o of BR.bots) if(o!==b&&o.alive&&!o.sky&&o.team!==b.team) a.push(o); return a; }""","""for(const o of BR.bots) if(o!==b&&o.alive&&!o.sky&&!o.bus&&o.team!==b.team) a.push(o); return a; }""")
# the camera pulls well back while you ride; you aren't drawn on the bus
rep("""  downCamK+=((P.down?1:0)-downCamK)*Math.min(1,lastDt*3);""","""  downCamK+=((P.down?1:0)-downCamK)*Math.min(1,lastDt*3); busCamK+=((P.bus?1:0)-busCamK)*Math.min(1,lastDt*3);""")
rep("""back=2.9-1.35*adsK+3.4*skyCamK+1.4*kartCamK+0.9*downCamK, up=0.18+0.08*adsK+1.0*skyCamK+0.45*kartCamK+0.7*downCamK;""","""back=2.9-1.35*adsK+3.4*skyCamK+1.4*kartCamK+0.9*downCamK+15*busCamK, up=0.18+0.08*adsK+1.0*skyCamK+0.45*kartCamK+0.7*downCamK+3.5*busCamK;""")
rep("""let camDist=2.9;""","""let camDist=2.9, busCamK=0;""")
rep("""  camDist=dist; hero.visible=dist>0.85&&!scopeOn;""","""  camDist=dist; hero.visible=dist>0.85&&!scopeOn&&!P.bus;""")
# the tip, and the bus's line on the maps
rep("""<div id="stormFx" hidden></div>""","""<div id="stormFx" hidden></div>
<div class="hud" id="busTip" hidden><b>Battle bus</b> · press <kbd>Jump</kbd> to drop out</div>""")
rep("""#stormFx{position:fixed;""","""#busTip{bottom:calc(env(safe-area-inset-bottom,0px) + 150px);left:50%;transform:translateX(-50%);background:rgba(6,14,40,.8);border:2px solid #3f8fff;border-radius:10px;padding:10px 16px;font:800 italic 17px/1 var(--font-hud);letter-spacing:.04em;text-transform:uppercase;color:#fff;white-space:nowrap}
#busTip b{color:#8fc2ff} #busTip kbd{font:inherit;background:#ffd21a;color:#1a1400;border-radius:5px;padding:2px 7px}
#stormFx{position:fixed;""")
rep("""  for(const b of BR.bots) if(b.alive&&b.team===0){ g.fillStyle='#3f8fff';""","""  if(BRBUS.on){ g.strokeStyle='rgba(255,255,255,.8)'; g.setLineDash([3*dpr,3*dpr]); g.lineWidth=2*dpr; g.beginPath(); g.moveTo(tx(BRBUS.ax),tz(BRBUS.az)); g.lineTo(tx(BRBUS.bx),tz(BRBUS.bz)); g.stroke(); g.setLineDash([]);
    const q=brBusPos(BRBUS.t,_brBP); g.fillStyle='#2f6fe0'; g.strokeStyle='#fff'; g.lineWidth=1.5*dpr; g.beginPath(); g.arc(tx(q.x),tz(q.z),5*dpr,0,7); g.fill(); g.stroke(); }
  for(const b of BR.bots) if(b.alive&&b.team===0){ g.fillStyle='#3f8fff';""")
