# patch205: frame rate and skydivers.
#  - the scene graph has ~52,000 objects, ~50,000 of them inside hidden groups (house pieces drawn by their town's
#    batch, people out of view, trees not drawn...). three.js recomputed every one of their matrices every frame (and
#    again for the reflection): about two thirds of the game's whole CPU time. A hidden object is now left alone once
#    its matrix is right, until it moves, gets something added, or shows again.
#  - the game asks the browser for the fast graphics card (laptops with two GPUs), names the GPU in the FPS meter, and
#    says how to fix it once if a desktop is running slowly on built-in graphics.
#  - far-off skydivers (drawn as one baked figure) are baked in the skydive pose, and under an open glider, instead of
#    standing in an A-pose tilted over.
rep('''(function(){
"use strict";
const isTouch''','''(function(){
"use strict";
// hidden things keep their matrices: skip a hidden object's subtree once it has been brought up to date, until it moves
// (its position, rotation or scale change), something is added to or taken from it, or it shows again
(()=>{ const O=THREE.Object3D.prototype, add0=O.add, rem0=O.remove, dirty=o=>{ for(;o;o=o.parent) o._mwOk=false; };
  O.add=function(){ dirty(this); return add0.apply(this,arguments); };
  O.remove=function(){ dirty(this); return rem0.apply(this,arguments); };
  const T16=new Float64Array(16);
  O.updateMatrixWorld=function(force){
    if(this.matrixAutoUpdate) this.updateMatrix();
    if(this.matrixWorldNeedsUpdate||force){ const e=this.matrixWorld.elements; for(let i=0;i<16;i++) T16[i]=e[i];
      if(this.parent===null) this.matrixWorld.copy(this.matrix); else this.matrixWorld.multiplyMatrices(this.parent.matrixWorld,this.matrix); this.matrixWorldNeedsUpdate=false; force=true;
      for(let i=0;i<16;i++) if(T16[i]!==e[i]){ this._mwV=(this._mwV||0)+1; break; } }   // (counts real changes, so a hidden child knows when its parent moved)
    const ch=this.children, V=this._mwV||0;
    for(let i=0,l=ch.length;i<l;i++){ const c=ch[i];
      if(c.visible){ c.updateMatrixWorld(force); c._mwOk=false; continue; }
      const p=c.position, q=c.quaternion, s=c.scale; let k=c._mwK;
      if(c._mwOk&&c._mwP===V&&k[0]===p.x&&k[1]===p.y&&k[2]===p.z&&k[3]===q.x&&k[4]===q.y&&k[5]===q.z&&k[6]===q.w&&k[7]===s.x&&k[8]===s.y&&k[9]===s.z&&!c.matrixWorldNeedsUpdate) continue;
      c.updateMatrixWorld(true); if(!k) k=c._mwK=new Float64Array(10);
      k[0]=p.x; k[1]=p.y; k[2]=p.z; k[3]=q.x; k[4]=q.y; k[5]=q.z; k[6]=q.w; k[7]=s.x; k[8]=s.y; k[9]=s.z; c._mwP=V; c._mwOk=true; } }; })();
const isTouch''')
rep('''const renderer=new THREE.WebGLRenderer({canvas, antialias:!isTouch || devicePixelRatio<2});''',
'''const renderer=new THREE.WebGLRenderer({canvas, antialias:!isTouch || devicePixelRatio<2, powerPreference:isTouch?'default':'high-performance'});
// which graphics chip the browser is drawing with (a laptop with a gaming card can still be on its built-in one)
const GPU=(()=>{ let n=''; try{ const gl=renderer.getContext(), e=gl.getExtension('WEBGL_debug_renderer_info'); n=String(e?gl.getParameter(e.UNMASKED_RENDERER_WEBGL):gl.getParameter(gl.RENDERER)); }catch(e){}
  const m=n.match(/(GeForce |NVIDIA )?(RTX|GTX|Quadro|Radeon|Intel|Iris|UHD|Arc|Apple|Mali|Adreno|SwiftShader|llvmpipe|Microsoft Basic)[^,()]*/i), short=(m?m[0]:n).replace(/\\s*Direct3D.*$/i,'').replace(/\\s+/g,' ').trim().slice(0,28);
  const weak=/SwiftShader|llvmpipe|Basic Render|Microsoft Basic/i.test(n)||(/Intel|Radeon\\(TM\\) Graphics|Radeon Graphics|Vega \\d|Radeon \\d{3}M/i.test(n)&&!/RTX|GTX|Radeon RX|Arc A|Radeon Pro/i.test(n));
  return {name:n,short,weak,told:false,slowN:0}; })();''')
rep('''el.textContent=f+' FPS · '+ms.toFixed(1)+' ms · worst '+FPS.worst.toFixed(0)+' ms';''',
'''el.textContent=f+' FPS · '+ms.toFixed(1)+' ms · worst '+FPS.worst.toFixed(0)+' ms'+(GPU.short?' · '+GPU.short:''); el.title=GPU.name;''')
rep('''function fpsTick(raw,now){ if(raw>1500) return; FPS.acc+=raw; FPS.n++; if(raw>FPS.worst) FPS.worst=raw; if(now-FPS.t<500) return; FPS.t=now;''',
'''function fpsTick(raw,now){ if(raw>1500) return; FPS.acc+=raw; FPS.n++; if(raw>FPS.worst) FPS.worst=raw; if(now-FPS.t<500) return; FPS.t=now;
  if(GPU.weak&&!GPU.told&&!isTouch&&typeof playing!=='undefined'&&playing&&FPS.n){ GPU.slowN=FPS.acc/FPS.n>22?GPU.slowN+1:0; if(GPU.slowN>=8){ GPU.told=true; try{ banner('Running on built-in graphics','Your browser is drawing with '+(GPU.short||'the built-in chip')+', not your graphics card. Windows: Settings › Display › Graphics › your browser › High performance, then restart the browser.',12); }catch(e){} } }''')

# far-off skydivers: baked in the freefall pose, and hanging under an open glider
rep('''function brFar(b,on){ if(!on){ if(b.far) b.far.visible=false; return; } if(!b.far){ b.far=new THREE.Mesh(botFarGeo(b.h.outfit),bakedMat(false)); b.far.userData.noCull=true; b.far.castShadow=false; b.far.receiveShadow=false; scene.add(b.far); }
  const f=b.far; f.visible=true; f.position.copy(b.pos); f.rotation.set(b.sky&&b.sky.phase==='fall'?-1.2:0,b.yaw,0,'YXZ'); }''',
'''const BOT_SKY=new Map(), BOT_SKYQ=[];
// a figure in the air, baked once per outfit: run the skydive animation until it settles, keep its tilt, bake it (the
// glider's sail is doubled so it shows from below as well as above)
function botSkyGeo(id,kind){ const key=id+':'+kind; let g=BOT_SKY.get(key); if(g) return g;
  const o=OUTFITS.find(x=>x.id===id)||OUTFITS[0], h=heroFor(o), S={sky:kind,vel:new THREE.Vector3(0,kind==='glide'?-5:-23,kind==='glide'?-14:-4),yaw:0,pos:new THREE.Vector3()};
  for(let k=0;k<45;k++){ h.anim.t=(h.anim.t||0)+1/30; animateSky(h,S,1/30); }
  const th=h.group.rotation.x; h.group.position.set(0,0,0); h.group.rotation.set(0,0,0,'YXZ'); if(h.rig.pick) h.rig.pick.visible=false; if(h.lod) heroLod(h,500);
  g=flattenModel(h.group);
  if(kind==='glide'){ const P=g.attributes.position.array, N=g.attributes.normal.array, C=g.attributes.color.array, n=P.length/3, P2=new Float32Array(n*6), N2=new Float32Array(n*6), C2=new Float32Array(n*6);
    P2.set(P); N2.set(N); C2.set(C); for(let t=0;t<n;t+=3) for(let v=0;v<3;v++){ const s=t+[0,2,1][v], d=n+t+v; for(let a=0;a<3;a++){ P2[d*3+a]=P[s*3+a]; N2[d*3+a]=-N[s*3+a]; C2[d*3+a]=C[s*3+a]; } }
    const g2=new THREE.BufferGeometry(); g2.setAttribute('position',new THREE.BufferAttribute(P2,3)); g2.setAttribute('normal',new THREE.BufferAttribute(N2,3)); g2.setAttribute('color',new THREE.BufferAttribute(C2,3)); g2.computeBoundingSphere(); g.dispose(); g=g2; }
  g.userData.th=th; BOT_SKY.set(key,g); return g; }
// bake them ahead (one a frame, from the moment the match starts) so nobody waits on it mid-drop
function botSkyWarm(){ for(const b of BR.bots) if(b.h) for(const k of ['fall','glide']){ const key=b.h.outfit+':'+k; if(!BOT_SKY.has(key)&&!BOT_SKYQ.includes(key)) BOT_SKYQ.push(key); } }
function botSkyStep(){ const key=BOT_SKYQ.shift(); if(!key) return; const i=key.lastIndexOf(':'); try{ botSkyGeo(key.slice(0,i),key.slice(i+1)); }catch(e){ console.warn('sky figure',e); } }
function brFar(b,on){ if(!on){ if(b.far) b.far.visible=false; return; }
  if(!b.far){ b.far=new THREE.Mesh(botFarGeo(b.h.outfit),bakedMat(false)); b.far.userData.noCull=true; b.far.castShadow=false; b.far.receiveShadow=false; scene.add(b.far); b.farK='stand'; }
  let kind=b.sky&&b.sky.phase==='glide'?'glide':b.sky&&b.sky.phase==='fall'?'fall':'stand'; if(kind!=='stand'){ const key=b.h.outfit+':'+kind; if(!BOT_SKY.has(key)){ if(!BOT_SKYQ.includes(key)) BOT_SKYQ.push(key); kind='stand'; } }
  const f=b.far; if(b.farK!==kind){ b.farK=kind; f.geometry=kind==='stand'?botFarGeo(b.h.outfit):botSkyGeo(b.h.outfit,kind); }
  f.visible=true; const th=kind==='stand'?(b.sky&&b.sky.phase==='fall'?-1.2:0):(f.geometry.userData.th||0), hu=kind==='stand'?0:0.94;
  f.position.set(b.pos.x-hu*Math.sin(th)*Math.sin(b.yaw),b.pos.y+hu*(1-Math.cos(th)),b.pos.z-hu*Math.sin(th)*Math.cos(b.yaw)); f.rotation.set(th,b.yaw,0,'YXZ'); }''')
rep('''function brUpdate(dt){''','''function brUpdate(dt){ if(!BR.skyWarm&&BR.bots&&BR.bots.length){ BR.skyWarm=true; try{ botSkyWarm(); }catch(e){} } if(BOT_SKYQ.length) botSkyStep();''')
rep('''  BR.on=true; try{ weatherRoll(); }catch(e){}''','''  BR.on=true; try{ weatherRoll(); }catch(e){} BR.skyWarm=false;''')
