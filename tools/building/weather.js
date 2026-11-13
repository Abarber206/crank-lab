/* ---------- weather: rain ----------
   Some matches it rains. Streaks fall around you (drawn on the GPU, wrapped in a box that follows the camera; none
   fall inside houses), the light goes grey and soft, the distance closes in, there's rain on the roof and the
   leaves and thunder now and then. It comes on and clears gradually. */
const WEATHER={k:0,want:0,mesh:null,u:null,snd:null,thT:12,fixed:null};
function weatherBuild(){ if(WEATHER.mesh) return; const N=isTouch?1400:3200, B=36, pos=new Float32Array(N*2*3), off=new Float32Array(N*2*4);
  for(let i=0;i<N;i++){ const x=Math.random()*B, y=Math.random()*B, z=Math.random()*B, sp=0.8+Math.random()*0.4; for(let e=0;e<2;e++){ off.set([x,y,z,sp],(i*2+e)*4); pos.set([0,e,0],(i*2+e)*3); } }
  const g=new THREE.BufferGeometry(); g.setAttribute('position',new THREE.BufferAttribute(pos,3)); g.setAttribute('off',new THREE.BufferAttribute(off,4)); g.boundingSphere=new THREE.Sphere(new THREE.Vector3(),1e6);
  WEATHER.u={time:{value:0},cam:{value:new THREE.Vector3()},k:{value:0},B:{value:B},indoorMap:INDOOR.u.map,indoorBox:INDOOR.u.box};
  const m=new THREE.ShaderMaterial({uniforms:WEATHER.u,transparent:true,depthWrite:false,fog:false,
    vertexShader:INDOOR_GLSL+`attribute vec4 off; uniform float time,k,B; uniform vec3 cam; varying float vA;
      void main(){ vec3 p=off.xyz+vec3(time*1.6,-time*17.0*off.w,time*0.7); p=mod(p-cam+B*0.5,B)+cam-B*0.5; // wrapped round the camera
        float cn; float ik=indoorK(p,cn); float vis=step(fract(off.x*7.31+off.z*3.17),k)*(1.0-step(0.5,ik)); // as many as it's raining hard, none indoors
        p+=vec3(0.06,-0.95,0.03)*position.y; vA=(0.16+0.22*position.y)*vis*(1.0-smoothstep(B*0.32,B*0.5,length(p-cam)));
        gl_Position=projectionMatrix*viewMatrix*vec4(p,1.0); if(vis<0.5) gl_Position=vec4(2.0,2.0,2.0,1.0); }`,
    fragmentShader:`varying float vA; void main(){ gl_FragColor=vec4(0.78,0.84,0.92,vA); }`});
  const L=new THREE.LineSegments(g,m); L.frustumCulled=false; L.renderOrder=4; scene.add(L); WEATHER.mesh=L; }
// a new match decides the weather (about one in three is wet)
function weatherRoll(){ WEATHER.want=WEATHER.fixed!=null?WEATHER.fixed:(Math.random()<0.35?0.6+Math.random()*0.4:0); }
function stepWeather(dt){ if(!INDOOR.tex) return; weatherBuild(); const live=playing||(typeof BR!=='undefined'&&BR.on); const want=live?WEATHER.want:0;
  WEATHER.k+=Math.sign(want-WEATHER.k)*Math.min(Math.abs(want-WEATHER.k),dt*0.08); const k=WEATHER.k, u=WEATHER.u; u.time.value=performance.now()/1000; u.cam.value.copy(camera.position); u.k.value=k; WEATHER.mesh.visible=k>0.01;
  // the sound: rain all round (duller and quieter indoors), thunder now and then
  if(AC){ if(!WEATHER.snd){ const m0=master; if(AUDIO.amb) master=AUDIO.amb; WEATHER.snd=loopSound(out=>{ const mk=(type,f,q,v,r)=>{ const s=AC.createBufferSource(); s.buffer=noiseBuf; s.loop=true; s.playbackRate.value=r; const fl=AC.createBiquadFilter(); fl.type=type; fl.frequency.value=f; fl.Q.value=q; const g=AC.createGain(); g.gain.value=v; s.connect(fl).connect(g).connect(out); s.start(0,Math.random()*0.4); return [s,fl]; };
        const a=mk('bandpass',2400,0.5,0.9,1.0), b=mk('lowpass',700,0.6,0.6,0.7), c=mk('highpass',6000,0.4,0.25,1.2); WEATHER.lp=b[1]; return [a[0],b[0],c[0]]; }); master=m0; }
    WEATHER.snd.set(k*(AUDIO.inside?0.22:0.42),camera.position.clone().setY(camera.position.y+6));
    if(k>0.4&&live){ WEATHER.thT-=dt; if(WEATHER.thT<=0){ WEATHER.thT=14+Math.random()*26; const f=$('stormFlash'); if(f){ f.style.background='rgba(230,235,255,.3)'; setTimeout(()=>{ f.style.background='rgba(230,235,255,0)'; },110); } setTimeout(()=>{ sfxGain=0.7*k; sfx('storm_close'); sfxGain=1; },600+Math.random()*1800); } } } }
// while drawing: grey, soft light and a closer horizon (put back afterwards, so the day's own lighting is untouched)
function weatherTint(){ const k=WEATHER.k; if(k<0.01||!scene.fog) return null; const fc=scene.fog.color.clone(), fn=scene.fog.near, si=sun.intensity, hi=hemi.intensity, bg=scene.background&&scene.background.isColor?scene.background.clone():null;
  scene.fog.color.lerp(_wCol,0.7*k); scene.fog.near=fn+(0.0075-fn)*k*0.85; sun.intensity=si*(1-0.62*k); hemi.intensity=hi*(1-0.18*k); if(bg) scene.background.lerp(_wCol,0.75*k); const rs=skyTint(_wZ,_wM,_wH,0.85*k,0.9);
  return ()=>{ rs(); scene.fog.color.copy(fc); scene.fog.near=fn; sun.intensity=si; hemi.intensity=hi; if(bg) scene.background.copy(bg); }; }
const _wCol=new THREE.Color(0x8a939e);
// the sky dome (and the water's idea of it) pulled toward a colour while drawing; returns how to put it back
function skyTint(zen,mid,hor,k,glowK){ if(typeof skyDome==='undefined'||!skyDome||!skyDome.material.uniforms.zen) return ()=>{}; const u=skyDome.material.uniforms, sv=[u.zen.value.clone(),u.mid.value.clone(),u.hor.value.clone(),u.glow.value.clone()];
  const wu=typeof WATER!=='undefined'&&WATER.mat?WATER.mat.uniforms:null, ws=wu?[wu.zen.value.clone(),wu.hor.value.clone()]:null;
  u.zen.value.lerp(zen,k); u.mid.value.lerp(mid,k); u.hor.value.lerp(hor,k); u.glow.value.multiplyScalar(1-glowK*k); if(wu){ wu.zen.value.lerp(zen,k); wu.hor.value.lerp(hor,k); }
  return ()=>{ u.zen.value.copy(sv[0]); u.mid.value.copy(sv[1]); u.hor.value.copy(sv[2]); u.glow.value.copy(sv[3]); if(wu){ wu.zen.value.copy(ws[0]); wu.hor.value.copy(ws[1]); } }; }
const _wZ=new THREE.Color(0x6f7883), _wM=new THREE.Color(0x8c95a0), _wH=new THREE.Color(0xa3abb4);
