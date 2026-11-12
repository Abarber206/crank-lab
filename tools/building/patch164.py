# patch164: frame rate. Measured first (tests/tcalls.js, tests/tbench.js): standing in a town one frame was ~1900
# draw calls, ~460 of them from the reboot vans alone (each van ~75 separate parts, drawn again into two shadow maps),
# ~340 from furniture (drawn into the shadow maps from anywhere), ~180 per character (each finger joint a draw,
# and all of them again for shadows); by the river the water mirror added ~1100 more. In Battle royale the 19 bots'
# animation was most of the script time.
#  - Graphics presets in Settings: Performance (aims for 165+ FPS: smaller sun shadow map, no far shadows, a lighter
#    water mirror, no ambient occlusion, low grass, simple clouds, resolution that drops when needed), Balanced,
#    Quality. Performance is the default. And an FPS counter (on by default; a Settings switch).
#  - Auto resolution aims at the preset's frame rate (165 FPS for Performance) instead of 40-60.
#  - Vans: their fixed parts merged into a few meshes per material (75 draws to about 15).
#  - Characters: fingers and face details are hidden past 20 m (where they're a pixel or two) and never cast
#    shadows; past 45 m a character casts no shadow.
#  - Furniture is drawn within 45 m only and casts no shadow; dropped loot casts no shadow and isn't drawn past 90 m;
#    chests, cars, boats and vans cast shadows only within 60 m.
#  - The water mirror leaves out furniture, loot, chests, vans and far-off characters, and in the lighter mode is
#    drawn smaller, every other frame, for one water level.
#  - Battle royale bots: animated every frame up close, every 2nd frame past 35 m, every 4th past 90 m, every 8th
#    past 180 m or when behind you; their physics takes one step a frame when they're far.
#  - Dropped loot checks the floor under it twice a second instead of every frame, and spins only when you're near.
rep("""          <label for="sens">Look sensitivity""","""          <label for="gfxSel">Graphics preset <select id="gfxSel"><option value="performance">Performance (165+ FPS)</option><option value="balanced">Balanced</option><option value="quality">Quality</option></select></label>
          <label for="fpsC">Show FPS counter <input type="checkbox" id="fpsC"></label>
          <label for="sens">Look sensitivity""")
rep("""<div class="hud" id="feed"></div>""","""<div class="hud" id="feed"></div>
<div class="hud" id="fpsHud" hidden>— FPS</div>""")
rep("""#loadScr{position:fixed;""","""#fpsHud{top:calc(env(safe-area-inset-top,0px) + 8px);left:calc(env(safe-area-inset-left,0px) + 10px);font:800 12px/1 var(--font-hud);letter-spacing:.06em;color:#bfffb8;background:rgba(0,0,0,.45);border-radius:5px;padding:4px 7px;pointer-events:none;z-index:6}
#fpsHud.slow{color:#ffd27a} #fpsHud.bad{color:#ff8a7a}
#loadScr{position:fixed;""")
rep("""  const ar=$('autoRes'); ar.checked=settings.autoRes!==false; ar.addEventListener('change',()=>{ settings.autoRes=ar.checked; saveSettings(); });""",
"""  const ar=$('autoRes'); ar.checked=settings.autoRes!==false; ar.addEventListener('change',()=>{ settings.autoRes=ar.checked; saveSettings(); });
  { const gs=$('gfxSel'); if(!settings.gfx){ settings.gfx='performance'; settings.showFps=true; saveSettings(); setTimeout(()=>applyGfx('performance'),0); } else setTimeout(()=>applyGfx(settings.gfx,true),0);
    gs.value=settings.gfx; gs.addEventListener('change',()=>{ settings.gfx=gs.value; applyGfx(gs.value); saveSettings(); toast('Graphics: '+gs.options[gs.selectedIndex].text); });
    const fc=$('fpsC'); fc.checked=settings.showFps!==false; fc.addEventListener('change',()=>{ settings.showFps=fc.checked; saveSettings(); }); }""")
# presets
rep("""const PERF={reflect:true,ao:true,far:true,slow:0};""","""const PERF={reflect:true,ao:true,far:true,slow:0,target:165,refl:'lite'};
const GFX={performance:{map:2048,far:false,refl:'lite',ao:false,grass:'low',clouds:'simple',resMin:0.7,resMax:1,target:165},
           balanced:{map:2048,far:true,refl:'lite',ao:true,grass:'medium',clouds:'volumetric',resMin:0.85,resMax:1.25,target:120},
           quality:{map:4096,far:true,refl:'full',ao:true,grass:'high',clouds:'volumetric',resMin:1,resMax:2,target:60}};
// a preset sets the switches below it in Settings (they can still be changed one by one afterwards); init: only what isn't a saved switch
function applyGfx(name,init){ const G=GFX[name]||GFX.performance; PERF.target=G.target; PERF.refl=G.refl;
  const dpr=devicePixelRatio||1; dynRes.max=Math.min(dpr*G.resMax,isTouch?1.5:2); dynRes.min=Math.min(dynRes.max,dpr*G.resMin*(isTouch?0.85:1)); dynRes.ceil=9; dynRes.cur=dynRes.max; renderer.setPixelRatio(dynRes.cur); if(typeof fitView==='function'){ lastW=-1; fitView(); }
  const m=isTouch?Math.min(G.map,2048):G.map; if(sun.shadow.mapSize.x!==m){ sun.shadow.mapSize.set(m,m); if(sun.shadow.map){ sun.shadow.map.dispose(); sun.shadow.map=null; } }
  sunFar.castShadow=G.far&&settings.shadows!==false&&!isTouch; PERF.far=G.far;
  if(init) return;
  const set=(id,v)=>{ const el=$(id); if(!el) return; if(el.type==='checkbox'){ if(el.disabled) return; el.checked=v; } else el.value=v; el.dispatchEvent(new Event('change')); };
  set('aoC',G.ao); set('grassSel',G.grass); set('cloudSel',G.clouds); set('reflectC',true); set('autoRes',true); }""")
rep("""  if(settings.autoRes&&avg>30&&dynRes.cur<=dynRes.min+1e-3){""","""  const TG=1000/(PERF.target||60), HI=Math.max(TG*1.2,TG+1.2), LO=TG*0.82; // the frame time the preset aims for, and the band either side
  if(settings.autoRes&&avg>Math.max(30,HI*1.6)&&dynRes.cur<=dynRes.min+1e-3){""")
rep("""  else if(avg>24&&dynRes.cur>dynRes.min){ if(now-dynRes.upAt<6000) dynRes.ceil=dynRes.cur-0.05; next=Math.max(dynRes.min,dynRes.cur-0.25); }
  else if(avg<17.5&&dynRes.cur<Math.min(dynRes.max,dynRes.ceil)){""","""  else if(avg>HI&&dynRes.cur>dynRes.min){ if(now-dynRes.upAt<6000) dynRes.ceil=dynRes.cur-0.05; next=Math.max(dynRes.min,dynRes.cur-0.15); }
  else if(avg<LO&&dynRes.cur<Math.min(dynRes.max,dynRes.ceil)){""")
# FPS counter
rep("""function stepDynRes(raw,now){""","""const FPS={acc:0,n:0,worst:0,t:0};
function fpsTick(raw,now){ if(raw>1500) return; FPS.acc+=raw; FPS.n++; if(raw>FPS.worst) FPS.worst=raw; if(now-FPS.t<500) return; FPS.t=now;
  const el=document.getElementById('fpsHud'); if(!el) return; const on=settings.showFps!==false&&typeof playing!=='undefined'&&(playing||(typeof LOBBY!=='undefined'&&LOBBY.on)); el.hidden=!on;
  if(on&&FPS.n){ const ms=FPS.acc/FPS.n, f=Math.round(1000/ms); el.textContent=f+' FPS · '+ms.toFixed(1)+' ms · worst '+FPS.worst.toFixed(0)+' ms'; el.classList.toggle('slow',f<(PERF.target||60)*0.8); el.classList.toggle('bad',f<50); }
  FPS.acc=0; FPS.n=0; FPS.worst=0; }
function stepDynRes(raw,now){ fpsTick(raw,now);""")
# vans: merge the fixed parts
rep("""  g.position.set(x,y,z); g.rotation.y=yaw; scene.add(g);
  const flare=""","""  mergeMeshes(g,new Set([beacon]));
  g.position.set(x,y,z); g.rotation.y=yaw; scene.add(g);
  const flare=""")
rep("""// the terminal: READY with a pulsing ring,""","""// fixed parts hanging straight off a group, merged per material (and shadow casting) into one mesh each
function mergeMeshes(g,skip){ const by=new Map();
  for(const m of [...g.children]){ if(!m.isMesh||m.children.length||skip.has(m)||!m.material||m.material.map||m.material.transparent||Array.isArray(m.material)) continue; const k=m.material.uuid+(m.castShadow?'s':'')+(m.receiveShadow?'r':''); (by.get(k)||by.set(k,[]).get(k)).push(m); }
  for(const list of by.values()){ if(list.length<2) continue; let n=0; const gs=list.map(m=>{ m.updateMatrix(); let q=m.geometry.index?m.geometry.toNonIndexed():m.geometry.clone(); if(!q.attributes.normal) q.computeVertexNormals(); q.applyMatrix4(m.matrix); n+=q.attributes.position.count; return q; });
    const P=new Float32Array(n*3), N=new Float32Array(n*3); let o=0; for(const q of gs){ P.set(q.attributes.position.array,o*3); N.set(q.attributes.normal.array,o*3); o+=q.attributes.position.count; }
    const geo=new THREE.BufferGeometry(); geo.setAttribute('position',new THREE.BufferAttribute(P,3)); geo.setAttribute('normal',new THREE.BufferAttribute(N,3)); geo.computeBoundingSphere();
    const mm=new THREE.Mesh(geo,list[0].material); mm.castShadow=list[0].castShadow; mm.receiveShadow=list[0].receiveShadow; list.forEach(m=>g.remove(m)); g.add(mm); } }
// the terminal: READY with a pulsing ring,""")
# characters: fine detail list, never casting shadows
rep("""function heroFor(o,pk){ return createHero(o.jacket,Object.assign({},o,{pickaxe:pk||'steel'})); }""","""function heroFor(o,pk){ const H=createHero(o.jacket,Object.assign({},o,{pickaxe:pk||'steel'})); heroLodPrep(H); return H; }
// the small stuff (finger joints, the face's eyes, lids, brows and mouth) and the rest, for distance detail
function heroLodPrep(H){ const r=H.rig, fine=new Set(), add=o=>{ if(o) o.traverse(m=>{ if(m.isMesh) fine.add(m); }); };
  for(const a of [r.armL,r.armR]) if(a&&a.fj){ a.fj.mcp.forEach(add); (a.th||[]).forEach(add); }
  (r.eyes||[]).forEach(add); (r.lids||[]).forEach(add); (r.brows||[]).forEach(add); add(r.mouth);
  const rest=[]; H.group.traverse(m=>{ if(m.isMesh&&!fine.has(m)&&!(r.pick&&isUnder(m,r.pick))) rest.push([m,m.castShadow]); });
  fine.forEach(m=>{ m.castShadow=false; }); H.lod={fine:[...fine],rest,near:true,shad:true}; }
function isUnder(m,g){ for(let x=m;x;x=x.parent) if(x===g) return true; return false; }
function heroLod(H,d){ const L=H&&H.lod; if(!L) return; const near=d<20, shad=d<45;
  if(near!==L.near){ L.near=near; for(const m of L.fine) m.visible=near; }
  if(shad!==L.shad){ L.shad=shad; for(const [m,c] of L.rest) m.castShadow=c&&shad; } }""")
# the distance-detail step: characters, furniture, loot, chests, cars, boats, vans; what the mirror leaves out
rep("""function stepProps(dt){
  propCullT-=dt; if(propCullT<=0){ propCullT=0.25; const cx=camera.position.x, cz=camera.position.z;
    for(const p of props){ if(p.lazy) continue; const far=(p.x-cx)*(p.x-cx)+(p.z-cz)*(p.z-cz)>400*400; p.g.visible=!far&&(p.alive||p.dying>0); }""",
"""const LODS={t:0,mirror:[]};
const _castSet=(o,on)=>{ if(o.userData.cs===on) return; o.userData.cs=on; o.traverse(m=>{ if(m.isMesh){ if(m.userData.cs0===undefined) m.userData.cs0=m.castShadow; m.castShadow=on&&m.userData.cs0; } }); };
function stepLods(dt){ LODS.t-=dt; if(LODS.t>0) return; LODS.t=0.2; const c=camera.position, D=(x,z)=>Math.hypot(x-c.x,z-c.z), mir=LODS.mirror; mir.length=0;
  heroLod(localHero,0); if(B&&B.h) heroLod(B.h,D(B.pos.x,B.pos.z)); if(AB&&AB.h) heroLod(AB.h,D(AB.pos.x,AB.pos.z));
  net.players.forEach(pl=>{ if(pl.h){ const d=D(pl.pos.x,pl.pos.z); heroLod(pl.h,d); if(d>40) mir.push(pl.h.group); } });
  if(BR.on) for(const b of BR.bots){ const d=D(b.pos.x,b.pos.z); heroLod(b.h,d); if(d>40) mir.push(b.h.group); }
  drops.forEach(d=>{ if(!d.ns){ d.ns=1; _castSet(d.g,false); } d.g.visible=D(d.pos.x,d.pos.z)<90; mir.push(d.g); });
  for(const ch of chests){ _castSet(ch.g,D(ch.x,ch.z)<60); mir.push(ch.g); }
  for(const k of karts) _castSet(k.g,D(k.x,k.z)<60);
  if(VANS) for(const v of VANS){ _castSet(v.g,D(v.x,v.z)<60); mir.push(v.g); } }
function stepProps(dt){
  stepLods(dt);
  propCullT-=dt; if(propCullT<=0){ propCullT=0.25; const cx=camera.position.x, cz=camera.position.z;
    for(const p of props){ if(p.lazy) continue; const d2=(p.x-cx)*(p.x-cx)+(p.z-cz)*(p.z-cz), far=p.kind==='furn'?d2>45*45:d2>400*400; p.g.visible=!far&&(p.alive||p.dying>0);
      if(p.kind==='furn'&&!p.ns){ p.ns=1; _castSet(p.g,false); } }""")
rep("""  const hid=REFL.hid; hid.length=0; for(const o of [...WATER.meshes,VCLOUD.sky,grassMesh,flowerMesh]) if(o&&o.visible){ o.visible=false; hid.push(o); }""",
"""  const hid=REFL.hid; hid.length=0; for(const o of [...WATER.meshes,VCLOUD.sky,grassMesh,flowerMesh,...LODS.mirror]) if(o&&o.visible){ o.visible=false; hid.push(o); }
  for(const p of props) if(p.kind==='furn'&&p.g.visible){ p.g.visible=false; hid.push(p.g); }""")
# the lighter mirror: smaller, every other frame, one water level
rep("""  renderer.getDrawingBufferSize(REFL.sz); const w=Math.max(64,Math.round(REFL.sz.x*0.5)), h=Math.max(64,Math.round(REFL.sz.y*0.5));""","""  renderer.getDrawingBufferSize(REFL.sz); const rs=PERF.refl==='full'?0.5:0.38, w=Math.max(64,Math.round(REFL.sz.x*rs)), h=Math.max(64,Math.round(REFL.sz.y*rs));""")
rep("""  C.sort((a,b)=>a.o-b.o); if(C.length>2) C.length=2;""","""  C.sort((a,b)=>a.o-b.o); if(C.length>(PERF.refl==='full'?2:1)) C.length=PERF.refl==='full'?2:1;""")
rep("""need=!sl.ok||Math.abs(sl.rl-sl.lvl)>0.25||sl.age>=(act.length>1?6:3)||(reflStale(sl)&&(n===0||REFL.flip));""","""need=!sl.ok||Math.abs(sl.rl-sl.lvl)>0.25||sl.age>=(act.length>1?6:3)||(reflStale(sl)&&(PERF.refl==='full'?(n===0||REFL.flip):REFL.flip));""")
# bots: animate less often when far or behind; one physics step when far
rep("""function brAnim(b,dt,now){ const d=b.pos.distanceTo(camera.position); b.h.group.visible=d<320||b.sky;
  if(!b.h.group.visible) return; if(d>120&&(BR.frame+b.h.group.id)%3) { b.h.group.position.copy(b.pos); return; } // far off: a third as often""",
"""const _baF=new THREE.Vector3();
function brAnim(b,dt,now){ const d=b.pos.distanceTo(camera.position); b.h.group.visible=d<320||b.sky;
  b.animAcc=(b.animAcc||0)+dt; if(!b.h.group.visible) return;
  camera.getWorldDirection(_baF); const behind=(b.pos.x-camera.position.x)*_baF.x+(b.pos.z-camera.position.z)*_baF.z<-4;
  let every=d<35?1:d<90?2:d<180?4:8; if(behind) every=Math.max(every,8);
  if(every>1&&(BR.frame+b.h.group.id)%every){ b.h.group.position.copy(b.pos); b.h.group.rotation.y=b.yaw; return; } // far off or behind you: less often
  dt=Math.min(0.12,b.animAcc); b.animAcc=0;""")
rep("""    down:false,sky:b.sky?b.sky.phase:null,reload:b.reloadT>0&&b.wpn?{w:b.wpn,p:Math.max(0,1-b.reloadT/2.1)}:null},d>120?dt*3:dt); b.h.rig.pick.visible=!b.wpn&&!b.sky; }""",
"""    down:false,sky:b.sky?b.sky.phase:null,reload:b.reloadT>0&&b.wpn?{w:b.wpn,p:Math.max(0,1-b.reloadT/2.1)}:null},dt); b.h.rig.pick.visible=!b.wpn&&!b.sky; }""")
rep("""  moveBody(b,fw,st,jump,dt); const n=Math.max(1,Math.ceil(dt/0.01)); for(let k=0;k<n;k++) physStep(dt/n,b);""","""  moveBody(b,fw,st,jump,dt); const n=b.pos.distanceTo(camera.position)>60?1:Math.max(1,Math.ceil(dt/0.01)); for(let k=0;k<n;k++) physStep(dt/n,b);""")
# loot: the floor check twice a second, spinning only near
rep("""    else { const [g]=groundAt(d.pos.x,d.pos.z,d.pos.y+0.3,staticsInto(near(d.pos.x,d.pos.z),d.pos.x,d.pos.z,1)); if(g<d.pos.y-0.01){ d.landed=false; } } // the floor under it broke: fall again
    d.g.position.copy(d.pos); d.spin+=dt*0.8; d.model.rotation.y=d.spin;""","""    else { d.gT=(d.gT==null?Math.random()*0.5:d.gT)-dt; if(d.gT<=0){ d.gT=0.5; const [g]=groundAt(d.pos.x,d.pos.z,d.pos.y+0.3,staticsInto(near(d.pos.x,d.pos.z),d.pos.x,d.pos.z,1)); if(g<d.pos.y-0.01){ d.landed=false; } } } // the floor under it broke: fall again
    if(!d.landed||!d.placed){ d.g.position.copy(d.pos); d.placed=d.landed; } if(d.g.visible&&Math.abs(d.pos.x-camera.position.x)+Math.abs(d.pos.z-camera.position.z)<70){ d.spin+=dt*0.8; d.model.rotation.y=d.spin; }""")
# doors: the frame's jambs and head merged into one mesh per door wall; door shadows within 40 m; drawn within 90 m
rep("""hd.castShadow=hd.receiveShadow=true; g.add(hd); }
  doorPieces.add(p); }""","""hd.castShadow=hd.receiveShadow=true; g.add(hd); }
  mergeMeshes(g,new Set()); doorPieces.add(p); }""")
rep("""const vis=p.doorG.position.distanceTo(camera.position)<120; p.doorG.visible=vis;""","""const dd=p.doorG.position.distanceTo(camera.position), vis=dd<90; p.doorG.visible=vis; if(vis) _castSet(p.doorG,dd<40);""")
# the HUD: the height readout and the compass are only redrawn when they change
rep("""  sH.textContent=P.pos.y.toFixed(1);""","""  { const t=P.pos.y.toFixed(1); if(t!==updateHUD.h){ updateHUD.h=t; sH.textContent=t; } }""")
rep("""function drawCompass(){
""","""function drawCompass(){ if(Math.abs(P.yaw-(drawCompass.y??1e9))<0.0015&&!(BR.on&&drawCompass.n++%10===0)) return; drawCompass.y=P.yaw; drawCompass.n=drawCompass.n||1;
""")
# bots: look for people less often when far from you; check sight to the nearest two past 40 m
rep("""  b.thinkT-=dt;
  if(b.thinkT<=0){ b.thinkT=0.3+Math.random()*0.1;""","""  b.thinkT-=dt;
  if(b.thinkT<=0){ b.thinkT=(b.pos.distanceTo(camera.position)>200?0.6:0.3)+Math.random()*0.1;""")
rep("""      if(d<90&&i<3){""","""      if(d<90&&i<(d<40?3:2)){""")
# Performance preset: the sun's shadow map is redrawn every other frame (at 165 fps a one-frame lag can't be seen)
rep("""function renderMain(){ if(!AO.ok""","""function renderMain(){ if(PERF.target>=144){ renderer.shadowMap.autoUpdate=false; PERF.sf=(PERF.sf||0)+1; renderer.shadowMap.needsUpdate=(PERF.sf&1)===0||PERF.sfForce>0; if(PERF.sfForce>0) PERF.sfForce--; } else renderer.shadowMap.autoUpdate=true;
  if(!AO.ok""")
