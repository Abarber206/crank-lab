# ---------- 21. scarier creatures: inner glow, hunched bodies, veins, kinds that look and move apart, screech; the Hurler ----------
# baked joints can carry glowing parts (unlit, lit from within) and per-vertex skin shading
rep("function bakedMat(flat){ return bakedMats[flat]||(bakedMats[flat]=new THREE.MeshPhongMaterial({vertexColors:true,shininess:16,specular:0x1c1c1c})); }",
"""function bakedMat(flat,glow){ const k=flat+(glow?'g':''); if(bakedMats[k]) return bakedMats[k];
  const m=new THREE.MeshPhongMaterial({vertexColors:true,shininess:glow?6:16,specular:glow?0x101010:0x1c1c1c});
  if(glow) m.onBeforeCompile=sh=>{ // parts marked glow burn with their own colour whatever the light (creature holes, flames)
    sh.vertexShader=sh.vertexShader.replace('#include <common>','#include <common>\\nattribute float glow; varying float vGlow;').replace('#include <begin_vertex>','#include <begin_vertex>\\nvGlow=glow;');
    sh.fragmentShader=sh.fragmentShader.replace('#include <common>','#include <common>\\nvarying float vGlow;').replace('#include <tonemapping_fragment>','gl_FragColor.rgb=mix(gl_FragColor.rgb,vColor*1.6,vGlow);\\n#include <tonemapping_fragment>'); };
  return bakedMats[k]=m; }""")
rep("function bakeGeo(list,withColor){",
    "function bakeGeo(list,withColor,withGlow){")
rep("const P=new Float32Array(n*3), N=new Float32Array(n*3), C=withColor?new Float32Array(n*3):null, v=new THREE.Vector3(), nm=new THREE.Matrix3(); let o=0;\n  for(const [g,e] of parts){ const pa=g.attributes.position, na=g.attributes.normal, cnt=pa.count, flip=e.M.determinant()<0; nm.getNormalMatrix(e.M);",
    "const P=new Float32Array(n*3), N=new Float32Array(n*3), C=withColor?new Float32Array(n*3):null, GL=withGlow?new Float32Array(n):null, v=new THREE.Vector3(), nm=new THREE.Matrix3(); let o=0;\n  for(const [g,e] of parts){ const pa=g.attributes.position, na=g.attributes.normal, vc=g.attributes.color, cnt=pa.count, flip=e.M.determinant()<0; nm.getNormalMatrix(e.M);")
rep("      if(C){ C[(o+i)*3]=e.col.r; C[(o+i)*3+1]=e.col.g; C[(o+i)*3+2]=e.col.b; } }",
    "      if(C){ const t=vc?vc.getX(src):1; C[(o+i)*3]=e.col.r*t; C[(o+i)*3+1]=e.col.g*t; C[(o+i)*3+2]=e.col.b*t; } if(GL) GL[o+i]=e.glow||0; }")
rep("out.setAttribute('normal',new THREE.BufferAttribute(N,3)); if(C) out.setAttribute('color',new THREE.BufferAttribute(C,3));\n  out.computeBoundingSphere(); return out; }",
    "out.setAttribute('normal',new THREE.BufferAttribute(N,3)); if(C) out.setAttribute('color',new THREE.BufferAttribute(C,3)); if(GL) out.setAttribute('glow',new THREE.BufferAttribute(GL,1));\n  out.computeBoundingSphere(); return out; }")
rep("body.push({geo:m.geometry,M:m.matrix,col:m.material.color});","body.push({geo:m.geometry,M:m.matrix,col:m.material.color,glow:m.material.userData.glow||0});")
rep("e={body:bakeGeo(body,true),ink:ink.length&&OUTLINES?bakeGeo(ink,false):null,cast,recv}; }",
    "const hasGlow=body.some(b=>b.glow>0); e={body:bakeGeo(body,true,hasGlow),ink:ink.length&&OUTLINES?bakeGeo(ink,false):null,cast,recv,glow:hasGlow}; }")
rep("const bm=new THREE.Mesh(e.body,bakedMat(flat));","const bm=new THREE.Mesh(e.body,bakedMat(flat,e.glow));")

# the kinds: colours (holes and flames glow), claws and veins; the Hurler joins
a=s.index("const ZT={ // the purple creatures"); b=s.index("const ZCODE=['husk','runner','brute'];")
s=s[:a]+"""const ZT={ // the purple creatures: lurching Walkers, skinny crawling Runners, huge Brutes and Hurlers that throw pieces of themselves
  husk:  {name:'Walker',hp:110,spd:0.56,dmg:12,bld:16,sc:1,   body:0x6c4a8f,light:0x9a77c4,dark:0x1c0b26,vein:0x341444,wound:0xd0287e,core:0xff6ad2,claw:0xe9ddf4,pts:1},
  runner:{name:'Runner',hp:70, spd:0.98,dmg:8, bld:10,sc:0.95,body:0x8a68b5,light:0xb998e0,dark:0x221030,vein:0x3d1a52,wound:0xc23aa8,core:0xffa6f4,claw:0xf2e8fa,pts:1},
  brute: {name:'Brute', hp:520,spd:0.42,dmg:30,bld:55,sc:1.45,body:0x4b2a70,light:0x6f4a9c,dark:0x13071c,vein:0x26103a,wound:0xd2401e,core:0xff9a3c,claw:0xd8c8e8,pts:3},
  hurler:{name:'Hurler',hp:95, spd:0.5, dmg:10,bld:14,sc:1.05,body:0x5f4a86,light:0x8f78b8,dark:0x170b22,vein:0x2c1a40,wound:0x6fd62a,core:0xc8ff5a,claw:0xe4f2d0,pts:2,throwDmg:20,throwBld:60}
};
"""+s[b:]
rep("const ZCODE=['husk','runner','brute'];","const ZCODE=['husk','runner','brute','hurler'];")

# hitboxes measured from each kind's model
rep("""  if(Zt){ // the creature's skull, then the base of its flame crown: both count as the head
    for(const [up,fw,r] of [[2.06,Zt.hf,0.16],[2.34,Zt.hf+0.07,0.11]]){ const ht=raySphere(o,d,_d.set(E.pos.x+fx*fw*k,f+up*k,E.pos.z+fz*fw*k),r*k); if(ht>0&&(!best||ht<best.t)) best={t:ht,head:true}; } }""",
"""  if(Zt&&Zt.hit){ const H=Zt.hit, rx=Math.cos(E.yaw), rz=-Math.sin(E.yaw); let hT=0, bT=0; // spheres measured from the model: the head and flames, then legs, spine and arms
    const test=(L)=>{ let m=0; for(const [up,fw,r,sx] of L){ const t=raySphere(o,d,_d.set(E.pos.x+(fx*fw+rx*sx)*k,f+up*k,E.pos.z+(fz*fw+rz*sx)*k),r*k); if(t>0&&(!m||t<m)) m=t; } return m; };
    hT=test(H.head); bT=test(H.body);
    if(hT&&(!bT||hT<=bT+0.12*k)) return {t:hT,head:true}; // a ray that clips the shoulder on its way into the head still counts as a headshot
    return bT?{t:bT,head:false}:null; }""")
rep("dmgNum(who.pos.clone().setY(who.pos.y+(e.head?2.3:1.7)*who.sc)","dmgNum(who.pos.clone().setY(who.pos.y+(e.head?(ZT[who.type]&&ZT[who.type].hit?ZT[who.type].hit.top+0.15:2.3):1.4)*who.sc)")

# attacks: a longer wind-up, then the lunge
rep("function zombieAttack(z,who){ z.atk=0.45; z.swipe={who,t:0.28}; zsfx('claw',z.pos); }",
    """function zombieAttack(z,who){ z.atk=ZATK; z.swipe={who,t:0.44}; zsfx('claw',z.pos); }
function zombieDamage(who,dmg,from){ // the host hands out creature damage
  if(who===P) hordeHurtMe(dmg,from);
  else if(net.role==='host'){ const c=net.conns.get(who.id); if(c&&c.open) try{ c.send({type:'hit',id:'zombie',to:who.id,dmg,w:'zombie'}); }catch(e){} } }""")
rep("""  if(who===P) hordeHurtMe(T.dmg,z.pos);
  else if(net.role==='host'){ const c=net.conns.get(who.id); if(c&&c.open) try{ c.send({type:'hit',id:'zombie',to:who.id,dmg:T.dmg,w:'zombie'}); }catch(e){} }""",
    "  zombieDamage(who,T.dmg,z.pos);")

rep("if(z.chew&&pieces.has(z.chew.p.key)){ fw=0; if(z.atkT<=0){ z.atkT=0.95; z.atk=0.45;","if(z.chew&&pieces.has(z.chew.p.key)){ fw=0; if(z.atkT<=0){ z.atkT=0.95; z.atk=ZATK;")
rep("if(z.atkT<=0&&zombieCanHit(z,t)){ z.atkT=1.05; zombieAttack(z,t); } }","if(z.atkT<=0&&zombieCanHit(z,t)){ z.atkT=1.2; zombieAttack(z,t); } }")
# Hurlers keep their distance and throw; Walkers and Brutes lurch (surge, stall, surge)
rep("""    if(z.swipe){ z.swipe.t-=dt; if(z.swipe.t<=0) zombieSwipeLands(z); }""",
"""    if(z.swipe){ z.swipe.t-=dt; if(z.swipe.t<=0) zombieSwipeLands(z); }
    z.hold=false;
    if(z.type==='hurler'&&!z.goal&&hd>6.5){ z.thrCd=(z.thrCd??1.2+Math.random())-dt;
      if(hd<26&&z.thrCd<=0&&!(z.thr>0)){ z.thrCd=2.4+Math.random()*0.9; hurlerThrow(z,t); }
      if(hd<20||z.thr>0) z.hold=true; }""")
rep("  moveBody(z,fw,st,false,dt);\n}","""  if(z.hold||z.thr>0){ fw=0; st=0; }
  else if(fw&&(z.type==='husk'||z.type==='brute')) fw*=0.79+0.67*Math.max(0,Math.sin(z.walk)); // lurching
  moveBody(z,fw,st,false,dt);
}
/* Hurler chunks: torn off the glowing growths and lobbed in an arc. The host works out the throw and the damage;
   everyone sees the same throw (wind-up, chunk in hand, arc, splat). A direct hit hurts, a splat near you hurts a
   bit less, and a chunk that hits a build damages it. */
const gooL=[], GOO_G=16, gooMat=new THREE.MeshBasicMaterial({color:0xc8ff5a}), gooGlow=new THREE.MeshBasicMaterial({color:0x9cff3a,transparent:true,opacity:.55});
function hurlerThrow(z,t){
  const o=z.pos.clone(); o.y+=2.1*z.sc; const tg=t.pos.clone(); tg.y+=0.9; const d=Math.hypot(tg.x-o.x,tg.z-o.z), T=0.55+d*0.032;
  if(t.vel) tg.addScaledVector(t.vel,T*0.5); // lead a running target a little
  const v=[(tg.x-o.x)/T,(tg.y-o.y+0.5*GOO_G*T*T)/T,(tg.z-o.z)/T].map(n=>+n.toFixed(2));
  z.thr=0.75; z.throwQ={v,real:true}; zsfx('zthrow',z.pos);
  if(net.role==='host') netSend({type:'hz',goo:1,id:z.id,v}); }
function spawnGoo(p,v,real){ const m=new THREE.Mesh(makeZombie.ls||new THREE.SphereGeometry(.5,10,7),gooMat); m.scale.setScalar(.26); m.position.copy(p); scene.add(m);
  gooL.push({m,pos:p.clone(),vel:new THREE.Vector3(...v),t:0,real,trailT:0}); }
function gooSplat(g,pt){ scene.remove(g.m); burst(pt,12,5,0.08,gooMat); for(let q=0;q<3;q++) puff(pt.clone().add(new THREE.Vector3((Math.random()-.5)*.6,Math.random()*.4,(Math.random()-.5)*.6)),0.35,0.45,gooGlow); zsfx('splat',pt);
  if(!g.real) return; const T=ZT.hurler;
  hordeTargets().forEach(w=>{ if(w===g.hitWho) return; const dx=w.pos.x-pt.x, dz=w.pos.z-pt.z, dy=w.pos.y+0.9-pt.y; if(Math.hypot(dx,dz)<1.5&&Math.abs(dy)<1.6) zombieDamage(w,Math.round(T.throwDmg*0.6),pt); }); }
function stepGoo(dt){
  for(let i=gooL.length-1;i>=0;i--){ const g=gooL[i]; g.t+=dt; g.vel.y-=GOO_G*dt;
    const step=g.vel.length()*dt; _pd.copy(g.vel).normalize();
    const r=castShot(g.pos,_pd,step+0.05,0,hordeTargets());
    if(r.kind!=='none'&&g.t>0.04){ if(g.real){ if(r.kind==='body'){ g.hitWho=r.who; zombieDamage(r.who,ZT.hurler.throwDmg,g.pos); } else if(r.kind==='piece') damagePiece(r.piece,ZT.hurler.throwBld,r.point); }
      gooSplat(g,r.point); gooL.splice(i,1); continue; }
    g.pos.addScaledVector(g.vel,dt); const gy=terrainH(g.pos.x,g.pos.z);
    if(g.pos.y<=gy||g.t>4){ g.pos.y=Math.max(g.pos.y,gy); gooSplat(g,g.pos); gooL.splice(i,1); continue; }
    g.m.position.copy(g.pos); g.m.rotation.x+=dt*9; g.m.scale.set(.26+.04*Math.sin(g.t*30),.26-.04*Math.sin(g.t*30),.26);
    g.trailT-=dt; if(g.trailT<=0){ g.trailT=0.035; puff(g.pos,0.12,0.3,gooGlow,new THREE.Vector3(0,0.2,0)); } } }
function clearGoo(){ gooL.forEach(g=>scene.remove(g.m)); gooL.length=0; }""")
rep("function clearZombies(){ [...horde.zs.values()].forEach(dropZombie); }","function clearZombies(){ [...horde.zs.values()].forEach(dropZombie); clearGoo(); }")
rep("  horde.zs.forEach(z=>animateZombie(z,dt));\n  if(net.role==='host'){","  horde.zs.forEach(z=>animateZombie(z,dt)); stepGoo(dt);\n  if(net.role==='host'){")
rep("    animateZombie(z,dt); });\n}","    animateZombie(z,dt); }); stepGoo(dt);\n}")
rep("  if(m.over){ banner('Overrun!',","  if(m.goo){ const z=horde.zs.get(m.id); if(z&&z.alive){ z.thr=0.75; z.throwQ={v:m.v,real:false}; zsfx('zthrow',z.pos); } return; }\n  if(m.over){ banner('Overrun!',")
rep("if(s[7]&&z.atk<=0.05) z.atk=0.45;","if(s[7]&&z.atk<=0.05) z.atk=ZATK;")
# which kinds come when: Runners from wave 2, Hurlers from wave 3, Brutes from wave 4
rep("const w=horde.wave, r=Math.random(), type=w>=4&&r<Math.min(0.14,0.03*w)?'brute':w>=2&&r<0.3?'runner':'husk';",
    "const w=horde.wave, r=Math.random(), b=w>=4?Math.min(0.14,0.03*w):0, hu=w>=3?Math.min(0.16,0.04*w):0, type=r<b?'brute':r<b+hu?'hurler':w>=2&&r<b+hu+0.26?'runner':'husk';")
rep("g.fillStyle=z.type==='brute'?'#c6ff5a':'#7fdc4a';","g.fillStyle=z.type==='brute'?'#ff9a3c':z.type==='hurler'?'#c8ff5a':'#e070ff';")

# animation: per-kind gaits, the wind-up and lunge, the throw, the screech when one spots you
a=s.index("function animateZombie(z,dt){"); b=s.index("// dusk sky while the horde is on")
s=s[:a]+"""function animateZombie(z,dt){
  const g=z.m.g, R=z.m.R; g.position.copy(z.pos); g.rotation.y=z.yaw;
  if(!z.alive){ if(R.lump) R.lump.visible=false; const k=Math.min(1,z.deadT/0.6); g.rotation.x=-k*1.45; g.position.y=z.pos.y-0.1*k; if(z.deadT>1.1) g.scale.setScalar(z.sc*Math.max(0.01,1-(z.deadT-1.1)*2)); return; }
  const ty=z.type, sp=Math.hypot(z.vel.x,z.vel.z), mv=Math.min(1,sp/1.5), run=ty==='runner';
  z.walk+=dt*(run?2.6+sp*2.4:ty==='brute'?1.2+sp*1.4:1.4+sp*1.6);
  const s=Math.sin(z.walk), c=Math.cos(z.walk), now=performance.now();
  // the first time one gets close to you it stops, rears up and screeches
  if(!z.spotted&&!isDead()&&z.pos.distanceTo(P.pos)<26){ z.spotted=true; z.scr=0.9; if(now-zScreechAt>380){ zScreechAt=now; zsfx('screech',z.pos); } }
  z.scr=Math.max(0,(z.scr||0)-dt); const scr=z.scr>0?Math.min(1,(0.9-z.scr)/0.2)*Math.min(1,z.scr/0.3):0;
  // attack: rear back with the arms up, then lunge forward and rake down
  const A=z.atk, wind=A>ZSTRIKE?(ZATK-A)/(ZATK-ZSTRIKE):0, raise=A>ZSTRIKE?wind:A>0?A/ZSTRIKE:0, strike=A>0&&A<=ZSTRIKE?Math.sin((ZSTRIKE-A)/ZSTRIKE*Math.PI):0;
  // Hurler throw: the right arm draws back over the head holding a chunk, then whips forward and lets go
  let thW=0, thF=0; if(z.thr>0){ z.thr-=dt; if(z.thr>0.3) thW=Math.min(1,(0.75-z.thr)/0.3); else thF=Math.sin(Math.max(0,z.thr)/0.3*Math.PI);
    if(z.throwQ&&z.thr<=0.3){ const hp=new THREE.Vector3(); R.lump.getWorldPosition(hp); spawnGoo(hp,z.throwQ.v,z.throwQ.real); z.throwQ=null; } }
  if(R.lump) R.lump.visible=z.thr>0.3;
  // legs: Walkers drag the right leg, Runners gallop, Brutes stomp
  if(ty==='husk'){ R.legL.rotation.x=s*0.55*mv; R.legR.rotation.x=-0.22*mv-s*0.16*mv; R.hips.position.y=R.hipY-0.07*Math.max(0,-s)*mv; R.hips.rotation.z=s*0.15*mv; }
  else if(run){ R.legL.rotation.x=s*0.8*mv; R.legR.rotation.x=-s*0.8*mv; R.hips.position.y=R.hipY+Math.abs(c)*0.07*mv; R.hips.rotation.z=s*0.05*mv; }
  else { const a=ty==='brute'?0.42:0.5; R.legL.rotation.x=s*a*mv; R.legR.rotation.x=-s*a*mv; R.hips.position.y=R.hipY+Math.abs(c)*(ty==='brute'?0.06:0.04)*mv; R.hips.rotation.z=s*0.1*mv; }
  // spine: the hunch, a lurch on each step, rearing back to strike, snapping forward, rearing up to screech
  const lurch=ty==='husk'?0.14*Math.max(0,s)*mv:ty==='brute'?0.08*Math.abs(s)*mv:run?0.06*c*mv:0.05*Math.max(0,s)*mv;
  R.spine.rotation.x=R.tilt-lurch+raise*0.32-strike*0.42+scr*(run?0.7:0.4)+thW*0.25-thF*0.35;
  R.spine.rotation.y=(ty==='brute'?s*0.12*mv:0)-thW*0.45+thF*0.35; R.spine.rotation.z=Math.sin(z.walk*0.5)*0.08;
  // arms: hang and sway (Runners paw the ground like front legs), go up on the wind-up, rake down on the strike, fling out to screech
  const aB=R.armL0, sw=run?0.9*mv:0.14+0.12*mv;
  R.armL.rotation.x=aB+(run?-s*sw:Math.sin(z.walk*0.9)*sw)+raise*2.3-strike*0.3;
  R.armR.rotation.x=aB+(run?s*sw:-Math.sin(z.walk*0.9+0.6)*sw)+raise*2.0-strike*0.3-thW*2.7+thF*1.4;
  R.armL.rotation.z=-0.12-raise*0.25-scr*0.9; R.armR.rotation.z=0.12+raise*0.25+scr*0.9+thW*0.3;
  // lunge: the whole body thrusts toward you on the strike
  const lg=strike*(run?0.6:0.35)*z.sc; g.position.x-=Math.sin(z.yaw)*lg; g.position.z-=Math.cos(z.yaw)*lg;
  // head: jutting forward, twitching; thrown back to screech
  z.twT=(z.twT||0)-dt; if(z.twT<=0){ z.twT=0.25+Math.random()*1.4; z.twY=(Math.random()-.5)*1.0; z.twZ=(Math.random()-.5)*0.8; }
  const hk=Math.min(1,dt*(Math.random()<0.15?40:16)); R.head.rotation.y+=((z.twY||0)*(1-scr)-R.head.rotation.y)*hk; R.head.rotation.z+=((z.twZ||0)*(1-scr)-R.head.rotation.z)*hk;
  R.head.rotation.x=R.headTilt+scr*0.6+raise*0.15-strike*0.1;
  if(z.hitFlash>0){ z.hitFlash-=dt; g.position.x+=(Math.random()-.5)*0.06; }
  if(R.crown){ const t=now*0.001+z.id*1.7, f=1+scr*0.45+strike*0.15; // the flame crown flickers, and flares when it screeches or strikes
    R.crown.scale.set(f*(1+0.05*Math.sin(t*8.3)),f*(1+0.1*Math.sin(t*6.1)+0.05*Math.sin(t*13.7)),f*(1+0.05*Math.cos(t*7.7))); R.crown.rotation.z=0.06*Math.sin(t*3.1);
    if(R.crownGlow) R.crownGlow.material.opacity=0.14+0.08*(0.5+0.5*Math.sin(t*11))+scr*0.25; }
}
"""+s[b:]
# sounds: a shriek when one spots you, a wet tearing grunt for a throw, a splat
rep("    case 'groan': zombieGroan(0.34); break;",
"""    case 'groan': zombieGroan(0.34); break;
    case 'screech': voice({f0:560*r(),f1:300,dur:0.8,vol:0.4,vowel:VOW.HAH,vowel2:VOW.AH,breath:0.9,fry:0.85,jitter:0.12,attack:0.02}); voice({f0:880*r(),f1:470,dur:0.6,vol:0.18,vowel:VOW.HAH,vowel2:VOW.ER,breath:0.8,fry:0.6,jitter:0.15,attack:0.02,delay:0.03}); noise(2600,0.55,0.16,1.2,0,'bandpass',3800); break;
    case 'zthrow': noise(700,0.22,0.3,1,0,'lowpass',260); voice({f0:140*r(),f1:95,dur:0.35,vol:0.3,vowel:VOW.HUH,vowel2:VOW.UH,breath:0.7,fry:0.8,jitter:0.07,attack:0.02,delay:0.3}); break;
    case 'splat': noise(420,0.22,0.5,0.9,0,'lowpass',120); knock(150*r(),0.08,0.3,3); for(let q=0;q<3;q++) noise(1800+Math.random()*1500,0.04,0.08,2,0.04+q*0.04); break;""")
# a version tag on the menu, so it's easy to tell which copy of the game is loaded
rep("""      <p class="sub">A build-fight practice range.""","""      <p class="sub" id="verTag" style="opacity:.55;font-size:12px;margin:0 0 4px">Update: Nov 8 · dune buggies &amp; garages, smoother roads, skydive &amp; glider, scope zoom</p>
      <p class="sub">A build-fight practice range.""")
