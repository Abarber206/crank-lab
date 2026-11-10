# ---------- 29. skydiving and the glider ----------
# settings: on by default
rep("instantBuild:false,","instantBuild:false, skyDrop:true,")
rep('          <label for="instantBuild">','          <label for="skyDropC">Drop in from the sky (skydive, then glide) <input type="checkbox" id="skyDropC"></label>\n          <label for="instantBuild">')
rep("const ib=$('instantBuild'); ib.checked=settings.instantBuild;","const skc=$('skyDropC'); skc.checked=settings.skyDrop!==false; skc.addEventListener('change',()=>{ settings.skyDrop=skc.checked; saveSettings(); });\nconst ib=$('instantBuild'); ib.checked=settings.instantBuild;")

rep("/* ---------- targeting ---------- */",r"""/* ---------- skydiving and the glider ----------
   You start high above the island (on your first Play in free play, when a party match starts, and when you come
   back after being eliminated in a party). In freefall you steer with the movement keys; push forward while looking
   down to dive (you fall faster and cover more ground). The glider opens by itself about 85 m above whatever is
   below you, or earlier when you press Jump. Gliding, you sink slowly and fly where you look: forward to speed up,
   back to slow down, sideways to slip. You land on the ground, a roof or a build, and the glider folds away.
   No shooting, building or editing until you land. */
const SKY_AUTO=85, SKY_FIRST=620, SKY_MATCH=520, SKY_BACK=160;
function skyDropAllowed(){ return settings.skyDrop!==false&&settings.mode!=='horde'&&!horde.on&&!botOn(); }
function skyDrop(x,z,h,E=P){ E.pos.set(x,terrainH(x,z)+h,z); E.vel.set(0,-6,0); E.onGround=false; E.groundSlab=null; E.fallTop=null; E.crouch=false;
  E.sky={phase:'fall',t:0,dive:0,jumpWas:true}; if(E===P){ if(edit) exitEdit(false); fireHeld=false; adsHeld=false; if(mode==='build') selectPick(); sfx('sky_start'); } }
function skyGround(E){ const [g]=groundAt(E.pos.x,E.pos.z,E.pos.y+0.4,solidNear(E)); return g; }
function deployGlider(E){ if(!E.sky||E.sky.phase!=='fall') return; E.sky.phase='glide'; E.sky.gt=0; if(E===P){ sfx('glider_open'); shake=Math.max(shake,0.05); } }
function endSky(E){ E.sky=null; E.fallTop=null; if(E.vel.y<-7) E.vel.y=-7; }
function skyMove(E,fw,st,jump,dt){ const S=E.sky; S.t+=dt;
  const fx=-Math.sin(E.yaw), fz=-Math.cos(E.yaw), rx=Math.cos(E.yaw), rz=-Math.sin(E.yaw), above=E.pos.y-skyGround(E);
  let tx, tz, ty, acc;
  if(S.phase==='fall'){
    S.dive+=((fw>0.3&&E.pitch<-0.45?1:0)-S.dive)*Math.min(1,dt*2.5);
    const sp=12+12*S.dive; let wx=fx*fw+rx*st, wz=fz*fw+rz*st; const m=Math.hypot(wx,wz); if(m>1){ wx/=m; wz/=m; }
    tx=wx*sp; tz=wz*sp; ty=-(38+22*S.dive); acc=9;
    E.vel.y=Math.max(ty,E.vel.y-GRAV*dt); if(E.vel.y<ty) E.vel.y+=(ty-E.vel.y)*Math.min(1,dt*2);
    if((jump&&!S.jumpWas&&S.t>1.0)||above<SKY_AUTO) deployGlider(E);
  } else { S.gt=(S.gt||0)+dt;
    const fwd=9+Math.max(-4.5,Math.min(7,fw*7)); tx=fx*fwd+rx*st*5; tz=fz*fwd+rz*st*5; acc=5;
    ty=-6.5-(fw>0.3?1.6:0)+(fw<-0.3?1.2:0); E.vel.y+=(ty-E.vel.y)*Math.min(1,dt*(S.gt<0.6?4:2)); }
  const dx=tx-E.vel.x, dz=tz-E.vel.z, d=Math.hypot(dx,dz), a=acc*dt; if(d<=a){ E.vel.x=tx; E.vel.z=tz; } else { E.vel.x+=dx/d*a; E.vel.z+=dz/d*a; }
  S.jumpWas=jump; }
function skyPhys(dt,E){ if(E===P&&isDead()){ E.sky=null; return; } const ps=solidNear(E), h=eh(E), ox=E.pos.x, oz=E.pos.z, nx=ox+E.vel.x*dt, nz=oz+E.vel.z*dt;
  if(!blocked(nx,oz,ox,oz,E.pos.y,h,0.3,ps)) E.pos.x=nx; else E.vel.x=0;
  if(!blocked(E.pos.x,nz,E.pos.x,oz,E.pos.y,h,0.3,ps)) E.pos.z=nz; else E.vel.z=0;
  E.pos.y+=E.vel.y*dt; E.onGround=false; E.groundSlab=null;
  const g=skyGround(E);
  if(E.pos.y<=g+(E.sky.phase==='glide'?0.9:0)){ if(E.pos.y<g) E.pos.y=g; endSky(E); } }
/* the glider: a delta-wing hang glider, its striped sail in your outfit's colour (sunlight glows through the fabric), on a
   metal frame with a control bar. The group's origin is the middle of the control bar, which sits in the rider's hands. */
const gliderMats={};
function gliderSailMat(){ if(gliderMats.sail) return gliderMats.sail; const m=new THREE.MeshLambertMaterial({vertexColors:true,side:THREE.DoubleSide,emissive:0x5a5a5a});
  m.onBeforeCompile=sh=>{ sh.fragmentShader=sh.fragmentShader.replace('vec3 totalEmissiveRadiance = emissive;','vec3 totalEmissiveRadiance = emissive * vColor;'); }; return gliderMats.sail=m; }
function gliderFrameMat(){ return gliderMats.frame||(gliderMats.frame=new THREE.MeshPhongMaterial({color:0x3a3f47,shininess:60,specular:0x777777})); }
function makeGlider(col){ const g=new THREE.Group(), body=new THREE.Group(), span=3.7, root=1.9, N=14, pos=[], cols=[], cA=new THREE.Color(col), cW=new THREE.Color(0xf6f2e8), cD=cA.clone().multiplyScalar(0.62), cT=cA.clone().lerp(new THREE.Color(0x1d1f27),0.55);
  const P_=x=>{ const u=Math.abs(x)/(span/2); return {le:-root*0.55+u*root*0.66, te:root*0.45-u*root*0.08-Math.sin(u*Math.PI*3)*0.04*u, y:0.18*(1-u*u)}; };
  for(let i=0;i<N;i++){ const x0=-span/2+span*i/N, x1=-span/2+span*(i+1)/N, a=P_(x0), b=P_(x1), mid=i===N/2-1||i===N/2, tip=i===0||i===N-1;
    const c=tip?cT:mid?cD:(i%4===1||i%4===2)&&!(i===N/2-2||i===N/2+1)?cW:cA;
    const v=[[x0,a.y,a.le],[x1,b.y,b.le],[x1,b.y*0.55,b.te],[x0,a.y*0.55,a.te]]; for(const q of [0,1,2,0,2,3]){ pos.push(...v[q]); cols.push(c.r,c.g,c.b); } }
  const sg=new THREE.BufferGeometry(); sg.setAttribute('position',new THREE.Float32BufferAttribute(pos,3)); sg.setAttribute('color',new THREE.Float32BufferAttribute(cols,3)); sg.computeVertexNormals();
  const sail=new THREE.Mesh(sg,gliderSailMat()); sail.position.y=1.0; sail.castShadow=true; body.add(sail);
  const V=(x,y,z)=>new THREE.Vector3(x,y,z), tp=P_(span/2), nose=V(0,1.15,-root*0.55), kp=V(0,1.06,-0.08);
  const bars=[[nose,V(0,1.07,root*0.47)],[nose,V(-span/2,1.0+tp.y,tp.le)],[nose,V(span/2,1.0+tp.y,tp.le)],[V(-span*0.33,1.05,0.06),V(span*0.33,1.05,0.06)],
    [kp,V(-0.45,0,0)],[kp,V(0.45,0,0)],[V(-0.47,0,0),V(0.47,0,0)],[V(0,1.06,0.12),V(0,0.62,0.06)],[kp,V(0,1.42,-0.08)]];
  const fg=mergeGeos(bars.map(([a,b])=>beamGeo(a,b,0.032))); fg.computeVertexNormals(); body.add(new THREE.Mesh(fg,gliderFrameMat()));
  // grips on the control bar and the rigging wires from the kingpost and the bar to the tips and nose
  const gg=mergeGeos([beamGeo(V(-0.3,0,0),V(-0.12,0,0),0.05),beamGeo(V(0.12,0,0),V(0.3,0,0),0.05)]); body.add(new THREE.Mesh(gg,gliderMats.grip||(gliderMats.grip=new THREE.MeshLambertMaterial({color:0x1b1b1f}))));
  const tipL=V(-span/2,1.0+tp.y,tp.le), tipR=V(span/2,1.0+tp.y,tp.le), wp=[];
  for(const [a,b2] of [[V(0,1.42,-0.08),tipL],[V(0,1.42,-0.08),tipR],[V(0,1.42,-0.08),nose],[V(-0.45,0,0),tipL],[V(0.45,0,0),tipR],[V(-0.45,0,0),nose],[V(0.45,0,0),nose]]) wp.push(a.x,a.y,a.z,b2.x,b2.y,b2.z);
  const wg=new THREE.BufferGeometry(); wg.setAttribute('position',new THREE.Float32BufferAttribute(wp,3)); body.add(new THREE.LineSegments(wg,gliderMats.wire||(gliderMats.wire=new THREE.LineBasicMaterial({color:0x9aa3ad,transparent:true,opacity:0.7}))));
  g.add(body); g.visible=false; return g; }
const _skA=new THREE.Vector3(), _skB=new THREE.Vector3();
function animateSky(H,S,dt){ const G=H.group, r=H.rig, A=H.anim, gl=S.sky==='glide', t=A.t;
  if(G.rotation.order!=='YXZ') G.rotation.order='YXZ';
  const dive=gl?0:Math.max(0,Math.min(1,(-S.vel.y-38)/20)), want=gl?-0.2:-(1.18+0.32*dive);
  A.skyX=lerp(A.skyX||0,want,Math.min(1,dt*(gl?5:3))); A.skyZ=lerp(A.skyZ||0,Math.max(-0.45,Math.min(0.45,-(A.yawRate||0)*(gl?0.14:0.07))),Math.min(1,dt*4));
  const th=A.skyX, hu=0.94; G.rotation.x=th; G.rotation.z=A.skyZ;
  G.position.set(S.pos.x-hu*Math.sin(th)*Math.sin(S.yaw),S.pos.y+hu*(1-Math.cos(th)),S.pos.z-hu*Math.sin(th)*Math.cos(S.yaw));
  const sm=1-Math.exp(-dt*10), set=(o,ax,v)=>{ o.rotation[ax]=lerp(o.rotation[ax],v,sm); }, fl=Math.sin(t*9)*0.06*(1-dive), fl2=Math.sin(t*7.3+1)*0.05*(1-dive);
  if(!gl){ // freefall: belly down, arms out and bent, knees bent (swept back in a dive)
    set(r.armL.sh,'x',lerp(-0.2,1.1,dive)+fl); set(r.armR.sh,'x',lerp(-0.2,1.1,dive)-fl); set(r.armL.sh,'z',lerp(-1.25,-0.3,dive)); set(r.armR.sh,'z',lerp(1.25,0.3,dive));
    set(r.armL.el,'x',lerp(0.75,0.1,dive)); set(r.armR.el,'x',lerp(0.75,0.1,dive));
    set(r.legL.hp,'x',lerp(0.3,0.05,dive)+fl2); set(r.legR.hp,'x',lerp(0.3,0.05,dive)-fl2); set(r.legL.hp,'z',lerp(-0.22,-0.05,dive)); set(r.legR.hp,'z',lerp(0.22,0.05,dive));
    set(r.legL.kn,'x',lerp(-0.85,-0.1,dive)); set(r.legR.kn,'x',lerp(-0.85,-0.1,dive)); set(r.neck,'x',-th*0.55);
  } else { // gliding: hanging under the bar, legs swinging a little
    const sw=Math.sin(t*1.8)*0.12;
    set(r.armL.sh,'x',-2.75); set(r.armR.sh,'x',-2.75); set(r.armL.sh,'z',-0.28); set(r.armR.sh,'z',0.28); set(r.armL.el,'x',0.3); set(r.armR.el,'x',0.3);
    set(r.legL.hp,'x',0.18+sw); set(r.legR.hp,'x',0.12-sw); set(r.legL.hp,'z',-0.06); set(r.legR.hp,'z',0.06); set(r.legL.kn,'x',-0.3); set(r.legR.kn,'x',-0.22); set(r.neck,'x',0.12); }
  r.gun.visible=r.pump.visible=r.hammer.visible=r.plan.visible=false; r.pick.visible=false;
  // the glider unfolds (wingtips first) when it opens; its control bar stays in the rider's hands
  if(!H.glider||H.glider.parent!==G||H.gliderFor!==H.outfit){ if(H.glider&&H.glider.parent) H.glider.parent.remove(H.glider); const o=OUTFITS.find(q=>q.id===H.outfit); H.glider=makeGlider((o&&o.accent)||0xff6a3d); H.gliderFor=H.outfit; G.add(H.glider); }
  A.glK=Math.max(0,Math.min(1,(A.glK||0)+(gl?dt*2.6:-dt*4))); const e=1-Math.pow(1-A.glK,3), gd=H.glider;
  gd.visible=A.glK>0.01;
  if(gd.visible){ G.updateMatrixWorld(true); r.armL.hand.getWorldPosition(_skA); r.armR.hand.getWorldPosition(_skB); _skA.add(_skB).multiplyScalar(0.5); G.worldToLocal(_skA);
    gd.position.copy(_skA); gd.scale.set(Math.max(0.05,e),Math.max(0.25,e),Math.max(0.35,e)); gd.rotation.set(-th-0.02-(1-e)*0.5+Math.sin(t*1.3)*0.025*e,0,-A.skyZ*0.25); } }
function moveBody(E,fw,st,jump,dt){ if(E.sky){ skyMove(E,fw,st,jump,dt); return; } moveBody0(E,fw,st,jump,dt); }

/* ---------- targeting ---------- */""")
rep("function moveBody(E,fw,st,jump,dt){\n  const fx=-Math.sin(E.yaw)","function moveBody0(E,fw,st,jump,dt){\n  const fx=-Math.sin(E.yaw)")
# physics, the rig, the camera
rep("  updatePhase(E);\n  const ps=solidNear(E), h=eh(E);\n  const lift=liftTarget(E,ps);","  if(E.sky){ skyPhys(dt,E); return; }\n  updatePhase(E);\n  const ps=solidNear(E), h=eh(E);\n  const lift=liftTarget(E,ps);")
rep("  // ----- events decay -----","""  // ----- skydiving / gliding; afterwards the body levels out and the glider folds away -----
  if(S.sky){ animateSky(H,S,dt); return; }
  if(G.rotation.x||G.rotation.z){ G.rotation.x*=Math.exp(-dt*12); G.rotation.z*=Math.exp(-dt*12); if(Math.abs(G.rotation.x)<1e-3) G.rotation.x=0; if(Math.abs(G.rotation.z)<1e-3) G.rotation.z=0; A.skyX=G.rotation.x; A.skyZ=G.rotation.z; const th=G.rotation.x; G.position.x-=0.94*Math.sin(th)*Math.sin(S.yaw); G.position.y+=0.94*(1-Math.cos(th)); G.position.z-=0.94*Math.sin(th)*Math.cos(S.yaw); }
  if(H.glider&&H.glider.visible){ A.glK=Math.max(0,(A.glK||0)-dt*4); const e=A.glK; H.glider.scale.set(Math.max(0.05,e),Math.max(0.2,e),Math.max(0.3,e)); H.glider.visible=e>0.01; }
  // ----- events decay -----""")
rep("    gun:mode==='gun'&&!edit?P.wpn:false,ads:adsK,swingT,reload:(mode==='gun'&&P.reloadT>0)?{w:P.wpn,p:1-P.reloadT/P.reloadDur}:null,emote:P.emote},dt);",
    "    gun:mode==='gun'&&!edit?P.wpn:false,ads:adsK,swingT,reload:(mode==='gun'&&P.reloadT>0)?{w:P.wpn,p:1-P.reloadT/P.reloadDur}:null,emote:P.emote,sky:P.sky?P.sky.phase:null},dt);")
rep("      gun:pl.wpn==='pick'?false:pl.wpn,ads:(pl.flags&32)?1:0,swingT:pl.swingT,emote:pl.emote},dt);","      gun:pl.wpn==='pick'?false:pl.wpn,ads:(pl.flags&32)?1:0,swingT:pl.swingT,emote:pl.emote,sky:(pl.flags&128)?'glide':(pl.flags&64)?'fall':null},dt);")
rep("const f=(P.onGround?1:0)|(P.crouch?2:0)|(mode==='build'&&!edit?4:0)|(net.dead?8:0)|(edit?16:0)|(adsK>0.5?32:0);","const f=(P.onGround?1:0)|(P.crouch?2:0)|(mode==='build'&&!edit?4:0)|(net.dead?8:0)|(edit?16:0)|(adsK>0.5?32:0)|(P.sky?(P.sky.phase==='glide'?128:64):0);")
rep("  const side=0.6-0.05*adsK, back=2.9-1.35*adsK, up=0.18+0.08*adsK;","  skyCamK+=((P.sky?(P.sky.phase==='fall'?1:0.7):0)-skyCamK)*Math.min(1,lastDt*2.5);\n  const side=0.6-0.05*adsK-0.3*skyCamK, back=2.9-1.35*adsK+3.4*skyCamK, up=0.18+0.08*adsK+1.0*skyCamK;")
rep("let camY=0, camDip=0;","let camY=0, camDip=0, skyCamK=0;")
# no fall damage from a glide; no fighting in the air
rep("function stepFall(){\n","function stepFall(){\n  if(P.sky){ P.fallTop=null; return; }\n")
rep("function fireDown(src){\n  if(isDead()) return;","function fireDown(src){\n  if(isDead()||P.sky) return;")
rep("function tryPlace(type,E=P){\n  if(E===P&&isDead()) return false;","function tryPlace(type,E=P){\n  if(E===P&&isDead()||E.sky) return false;")
rep("function enterEdit(){","function enterEdit(){\n  if(P.sky) return;")
rep("  const I=ITEMS[P.item]; if(!I||P.useT>0||isDead()) return;","  const I=ITEMS[P.item]; if(!I||P.useT>0||isDead()||P.sky) return;")
rep("  if(!playing||isDead()||edit||invOpen) return null;","  if(!playing||isDead()||edit||invOpen||P.sky) return null;")
# when you drop in
rep("function respawn(){ animEvent(localHero,'revive'); P.pos.set(...SPAWN);","function respawn(){ animEvent(localHero,'revive'); P.sky=null; P.pos.set(...SPAWN);")
rep("  setTimeout(()=>{ if(!playing){ lockFailed=!locked; menu.hidden=true; playing=true; } },700);","  setTimeout(()=>{ if(!playing){ lockFailed=!locked; menu.hidden=true; playing=true; } },700);\n  if(!P.everPlayed){ P.everPlayed=true; if(!net.role&&skyDropAllowed()) skyDrop(SPAWN[0],SPAWN[2],SKY_FIRST); } // the first time in: from the sky")
s=s.replace("const a=Math.random()*Math.PI*2, r=8+Math.random()*20; respawn(); P.pos.set(SPAWN[0]+Math.cos(a)*r,0,SPAWN[2]+Math.sin(a)*r);","const a=Math.random()*Math.PI*2, r=8+Math.random()*20; respawn(); P.pos.set(SPAWN[0]+Math.cos(a)*r,0,SPAWN[2]+Math.sin(a)*r); if(skyDropAllowed()) skyDrop(P.pos.x,P.pos.z,SKY_BACK);")
rep("  respawn(); round.you=0; round.bot=0;","  respawn(); round.you=0; round.bot=0; if(skyDropAllowed()){ const a=Math.random()*6.283; skyDrop(SPAWN[0]+Math.cos(a)*30,SPAWN[2]+Math.sin(a)*30,SKY_MATCH); }")
rep("respawn(); sfx('win');","respawn(); sfx('win'); if(skyDropAllowed()){ const a=Math.random()*6.283; skyDrop(SPAWN[0]+Math.cos(a)*30,SPAWN[2]+Math.sin(a)*30,SKY_MATCH); }")
# sounds: the drop, the glider opening, and the wind (a roar in freefall, a softer rush with sail flutter while gliding)
rep("    case 'groan': zombieGroan(0.34); break;","""    case 'groan': zombieGroan(0.34); break;
    case 'sky_start': noise(300,1.2,0.25,0.6,0,'lowpass',1400); noise(3000,0.8,0.06,0.8,0.1,'highpass'); break;
    case 'glider_open': noise(320,0.4,0.6,0.7,0,'lowpass',140); noise(2400,0.22,0.18,1.2,0.03,'bandpass',900); knock(180,0.07,0.3,3,0.05); noise(1600,0.5,0.06,0.8,0.12,'bandpass',600); break;""")
rep("  amb.t+=dt; const on=playing&&!document.hidden,","""  if(!amb.sky){ const s2=AC.createBufferSource(); s2.buffer=noiseBuf; s2.loop=true; const f2=AC.createBiquadFilter(); f2.type='bandpass'; f2.Q.value=0.8; f2.frequency.value=700; const g2=AC.createGain(); g2.gain.value=0;
    const lfo=AC.createOscillator(), lg=AC.createGain(); lfo.frequency.value=7.5; lg.gain.value=0; lfo.connect(lg).connect(g2.gain); lfo.start(); s2.connect(f2).connect(g2).connect(master); s2.start(); amb.sky={g:g2,f:f2,lg}; }
  { const v=P.sky?P.vel.length():0, fall=P.sky&&P.sky.phase==='fall', glide=P.sky&&P.sky.phase==='glide', now=AC.currentTime;
    amb.sky.g.gain.setTargetAtTime(playing&&!document.hidden&&P.sky?(fall?0.05+0.07*Math.min(1,v/60):0.03):0,now,0.25); amb.sky.f.frequency.setTargetAtTime(fall?500+v*16:900,now,0.3); amb.sky.lg.gain.setTargetAtTime(glide?0.012:0,now,0.3); }
  amb.t+=dt; const on=playing&&!document.hidden,""")
rep("  const dm=new THREE.Mesh(doorGeo(true),doorMat({mat:'wood'})); g.add(dm);","  const dm=new THREE.Mesh(doorGeo(true),doorMat({mat:'wood'})); g.add(dm);\n  const gw=makeGlider(0xff6a3d); gw.visible=true; gw.scale.setScalar(0.003); g.add(gw);")
rep("if(!horde.on){ ambBirdT-=dt; if(ambBirdT<=0){","if(!horde.on&&!P.sky){ ambBirdT-=dt; if(ambBirdT<=0){")
