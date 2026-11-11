# patch149: water.
#  - Rivers fade into the sea where they reach it: the river surface thins out over the last few metres instead of
#    ending in a lighter band laid on top of the sea (the current also slows as it goes out).
#  - Reflections on every body of water: two mirror images at once, one for each of the two water levels nearest to
#    where you are looking (the sea and a river, or a river and the lake it runs into). Each one comes in and goes out
#    smoothly instead of switching on and off as you walk along the shore, and water a little below a mirror's level
#    shares its picture. With only one water level in view, the cost is the same as before.
i=s.index("const REFL={lvl:-1e4"); j=s.index("const _rfD=new THREE.Vector3();")
s=s[:i]+r"""const REFL={cam:new THREE.PerspectiveCamera(),plane:new THREE.Plane(),clip:new THREE.Vector4(),q:new THREE.Vector4(),sz:new THREE.Vector2(),t:new THREE.Vector3(),hid:[],
  s:[0,1].map(()=>({rt:null,m:new THREE.Matrix4(),lvl:-1e4,rl:-1e4,K:0,k:0,ok:false,want:false,age:9})),t0:0,c:[],flip:0};
function reflDraw(sl,lvl){ const u=WATER.mat.uniforms, cp=camera.position;
  renderer.getDrawingBufferSize(REFL.sz); const w=Math.max(64,Math.round(REFL.sz.x*0.5)), h=Math.max(64,Math.round(REFL.sz.y*0.5));
  if(!sl.rt) sl.rt=new THREE.WebGLRenderTarget(w,h,{minFilter:THREE.LinearFilter,magFilter:THREE.LinearFilter,format:THREE.RGBAFormat}); else if(sl.rt.width!==w||sl.rt.height!==h) sl.rt.setSize(w,h);
  // the camera's mirror image below the surface
  const vc=REFL.cam; camera.updateMatrixWorld(); vc.position.set(cp.x,2*lvl-cp.y,cp.z);
  REFL.t.set(0,0,-1).applyQuaternion(camera.quaternion).add(cp); REFL.t.y=2*lvl-REFL.t.y;
  vc.up.set(0,1,0).applyQuaternion(camera.quaternion); vc.up.y=-vc.up.y; vc.lookAt(REFL.t); vc.updateMatrixWorld(); vc.projectionMatrix.copy(camera.projectionMatrix);
  sl.m.set(0.5,0,0,0.5, 0,0.5,0,0.5, 0,0,0.5,0.5, 0,0,0,1).multiply(vc.projectionMatrix).multiply(vc.matrixWorldInverse);
  // its near plane is tilted onto the water surface, so nothing below the surface is drawn (Lengyel's oblique clipping)
  REFL.plane.normal.set(0,1,0); REFL.plane.constant=-lvl; REFL.plane.applyMatrix4(vc.matrixWorldInverse);
  const cl=REFL.clip.set(REFL.plane.normal.x,REFL.plane.normal.y,REFL.plane.normal.z,REFL.plane.constant), pe=vc.projectionMatrix.elements, q=REFL.q;
  q.set((Math.sign(cl.x)+pe[8])/pe[0],(Math.sign(cl.y)+pe[9])/pe[5],-1,(1+pe[10])/pe[14]); cl.multiplyScalar(2/cl.dot(q));
  pe[2]=cl.x; pe[6]=cl.y; pe[10]=cl.z+1-0.003; pe[14]=cl.w;
  const hid=REFL.hid; hid.length=0; for(const o of [...WATER.meshes,VCLOUD.sky,grassMesh,flowerMesh]) if(o&&o.visible){ o.visible=false; hid.push(o); }
  if(FOREST.far) for(const kind in FOREST.far) for(const o of FOREST.far[kind]) if(o.visible){ o.visible=false; hid.push(o); } // the far trees: too far off to matter in a rippled mirror
  const prev=renderer.getRenderTarget(), au=renderer.shadowMap.autoUpdate; renderer.shadowMap.autoUpdate=false; // the shadow maps from the last frame serve
  renderer.setRenderTarget(sl.rt); renderer.clear(); renderer.render(scene,vc); renderer.setRenderTarget(prev); renderer.shadowMap.autoUpdate=au;
  for(const o of hid) o.visible=true;
  sl.rl=lvl; sl.ok=true; sl.age=0; }
function renderReflection(){ if(!WATER.mat) return; const u=WATER.mat.uniforms, now=performance.now(), dt=Math.min(0.1,Math.max(0,(now-(REFL.t0||now))/1000)); REFL.t0=now;
  const off_=()=>{ u.reflK.value=0; u.reflK2.value=0; for(const sl of REFL.s){ sl.k=0; sl.ok=false; sl.lvl=-1e4; } };
  if(settings.reflect===false||!PERF.reflect||!WATER.lv||!scene.visible){ off_(); return; }
  const cp=camera.position, LN=WATER.LN, i=Math.max(0,Math.min(LN-1,Math.floor((cp.x-SPAWN[0]+WHALF)/WATER.LC))), j=Math.max(0,Math.min(LN-1,Math.floor((cp.z-SPAWN[2]+WHALF)/WATER.LC)));
  // the water levels in view: under you, and the first water met straight ahead and a little to each side
  const C=REFL.c; C.length=0; const add=(l,o)=>{ if(l<-999||l>cp.y-0.12) return; for(const c of C) if(Math.abs(c.l-l)<0.5){ if(o<c.o){ c.o=o; c.l=l; } return; } C.push({l,o}); };
  add(WATER.lv[j*LN+i],WATER.ld[j*LN+i]);
  camera.getWorldDirection(_rfD); const hl=Math.hypot(_rfD.x,_rfD.z);
  if(hl>0.05){ const fx=_rfD.x/hl, fz=_rfD.z/hl;
    for(const a of [0,-0.5,0.5]){ const ca=Math.cos(a), sa=Math.sin(a), dx=fx*ca-fz*sa, dz=fx*sa+fz*ca;
      for(let s=1;s<=140;s+=s<20?1.5:4){ const x=cp.x+dx*s, z=cp.z+dz*s, w=waterAt(x,z); if(w>-999&&w<cp.y-0.1){ add(w,s*0.5*(a?1.6:1)); break; } } } }
  C.sort((a,b)=>a.o-b.o); if(C.length>2) C.length=2;
  for(const c of C){ const hgt=cp.y-c.l; c.K=(c.o>300||hgt<0.12||hgt>180)?0:(1-sstep(180,300,c.o))*(1-sstep(120,180,hgt)); }
  // each wanted level keeps the mirror it already has; a new one takes over a mirror that is no longer wanted
  const S2=REFL.s; for(const sl of S2) sl.want=false; const free=[];
  for(const c of C){ if(c.K<0.01) continue; let best=null; for(const sl of S2) if(!sl.want&&Math.abs(sl.lvl-c.l)<0.6&&(!best||Math.abs(sl.lvl-c.l)<Math.abs(best.lvl-c.l))) best=sl;
    if(best){ best.want=true; best.lvl=c.l; best.K=c.K; } else free.push(c); }
  for(const c of free){ const sl=S2.filter(t=>!t.want).sort((a,b)=>a.k-b.k)[0]; if(!sl) break; sl.want=true; sl.lvl=c.l; sl.K=c.K; sl.k=0; sl.ok=false; }
  for(const sl of S2){ sl.k=sl.want?Math.min(sl.K,sl.k+dt*3):Math.max(0,sl.k-dt*3); sl.age++; if(sl.k<=0&&!sl.want){ sl.ok=false; } }
  // draw one mirror a frame: a new one at once, otherwise whichever is oldest; with just one in use, every other frame (as before)
  const act=S2.filter(sl=>sl.want), fresh=act.find(sl=>!sl.ok||Math.abs(sl.rl-sl.lvl)>0.25);
  let pick=fresh||null; if(!pick&&act.length){ const old=act.reduce((a,b)=>a.age>=b.age?a:b); if(act.length>1||old.age>=2) pick=old; }
  if(pick) reflDraw(pick,pick.lvl);
  const [A,B]=S2;
  u.reflK.value=A.ok?A.k:0; if(A.ok){ u.reflT.value=A.rt.texture; u.reflM.value.copy(A.m); u.reflY.value=A.rl; }
  u.reflK2.value=B.ok?B.k:0; if(B.ok){ u.reflT2.value=B.rt.texture; u.reflM2.value.copy(B.m); u.reflY2.value=B.rl; }
}
"""+s[j:]
rep("""reflM:{value:new THREE.Matrix4()}, reflK:{value:0}, reflY:{value:0},""","""reflM:{value:new THREE.Matrix4()}, reflK:{value:0}, reflY:{value:0}, reflT2:{value:null}, reflM2:{value:new THREE.Matrix4()}, reflK2:{value:0}, reflY2:{value:0},""")
rep("""uniform sampler2D nT, reflT, hT; uniform mat4 reflM; uniform float time, lum, reflK, reflY;""","""uniform sampler2D nT, reflT, reflT2, hT; uniform mat4 reflM, reflM2; uniform float time, lum, reflK, reflY, reflK2, reflY2;""")
rep("""        if(reflK>0.0){ vec4 rc=reflM*vec4(vW,1.0); vec2 ruv=rc.xy/rc.w+a*vec2(0.022,0.05)/(1.0+dist*0.03);   // the mirror image, wobbled by the ripples
          mir=mix(mir,texture2D(reflT,clamp(ruv,0.003,0.997)).rgb,reflK*(1.0-smoothstep(0.6,2.2,abs(vW.y-reflY)))); } // (only water at the mirror's own level shows it)""",
"""        vec2 wob=a*vec2(0.022,0.05)/(1.0+dist*0.03); float d1=vW.y-reflY, d2=vW.y-reflY2;                  // the mirror images, wobbled by the ripples
        float w1=reflK*(d1>0.0?1.0-smoothstep(0.6,2.2,d1):1.0-smoothstep(1.5,5.0,-d1)), w2=reflK2*(d2>0.0?1.0-smoothstep(0.6,2.2,d2):1.0-smoothstep(1.5,5.0,-d2)); // (water at a mirror's level, or a little below it)
        if(w1>0.004&&w1>=w2){ vec4 rc=reflM*vec4(vW,1.0); mir=mix(mir,texture2D(reflT,clamp(rc.xy/rc.w+wob,0.003,0.997)).rgb,w1); }
        else if(w2>0.004){ vec4 rc=reflM2*vec4(vW,1.0); mir=mix(mir,texture2D(reflT2,clamp(rc.xy/rc.w+wob,0.003,0.997)).rgb,w2); }""")
# a river's mouth: it thins out over the sea instead of ending in a band
rep("""    else for(let q=0;q<n;q++) if(p[q][2]<=S.Y+0.02){ endQ=Math.min(n-1,q+6); break; }""","""    else for(let q=0;q<n;q++) if(p[q][2]<=S.Y+0.02){ endQ=Math.min(n-1,q+8); break; }""")
rep("""fade=Math.min(1,q/3,rv.into>=0?1:(endQ-q)/3), sp=rv.main?0.8:1.1;""","""fade=Math.min(1,q/3), sp=(rv.main?0.8:1.1)*(rv.into>=0||endQ===n-1&&p[n-1][2]>S.Y+0.02?1:Math.max(0.02,Math.min(1,(endQ-q)/9)));""")
rep("""float al=smoothstep(0.0,0.18,D)*mix(0.62,0.96,smoothstep(0.0,2.5,D)); al=max(al,F*smoothstep(0.0,0.1,D)); al=max(al,foam*0.8);""",
"""float al=smoothstep(0.0,0.18,D)*mix(0.62,0.96,smoothstep(0.0,2.5,D)); al=max(al,F*smoothstep(0.0,0.1,D)); al=max(al,foam*0.8); al*=mix(1.0,smoothstep(0.016,0.5,length(vFlow)),riv); // (a river thins out where it meets the sea)""")
