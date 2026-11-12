# patch152: water polish from play-testing.
#  - Swimming: the breaststroke stays under the water (the arms reach forward a little below the surface instead of
#    up out of it, and the body rides a touch lower; the head is still out).
#  - Reflections: the mirror camera no longer cuts off distant hills and cliffs (its tilted far plane used to slice
#    whole wedges out of the reflection, so turning left or right showed the wrong thing beside you); while you move
#    the mirror is redrawn every frame instead of every other one (no more jagged, juddering reflections); each sample
#    is softened over a few pixels, and only water within a couple of metres of a mirror's level uses it.
rep("""hipW=lerp(W-0.44,W-0.2,mvK)""","""hipW=lerp(W-0.44,W-0.33,mvK)""")
rep("""set(a.sh,'x',lerp(0.78+0.06*sc,1.75+1.15*reach,mvK)); set(a.sh,'z',sx*lerp(0.42+0.16*sc,0.22+0.95*out,mvK));""","""set(a.sh,'x',lerp(0.78+0.06*sc,1.4+0.75*reach-0.85*out,mvK)); set(a.sh,'z',sx*lerp(0.42+0.16*sc,0.22+0.9*out,mvK));""")
rep("""vc.lookAt(REFL.t); vc.updateMatrixWorld(); vc.projectionMatrix.copy(camera.projectionMatrix);""",
"""vc.lookAt(REFL.t); vc.updateMatrixWorld();
  vc.fov=camera.fov; vc.aspect=camera.aspect; vc.zoom=camera.zoom; vc.near=camera.near; vc.far=camera.far*40; vc.updateProjectionMatrix(); // (a far plane well out: the oblique cut below tilts it in)""")
rep("""  sl.rl=lvl; sl.ok=true; sl.age=0; }""","""  sl.rl=lvl; sl.ok=true; sl.age=0; sl.pose.copy(camera.matrixWorld); }""")
rep("""s:[0,1].map(()=>({rt:null,m:new THREE.Matrix4(),lvl:-1e4,rl:-1e4,K:0,k:0,ok:false,want:false,age:9})),t0:0,c:[],flip:0};""",
"""s:[0,1].map(()=>({rt:null,m:new THREE.Matrix4(),pose:new THREE.Matrix4(),lvl:-1e4,rl:-1e4,K:0,k:0,ok:false,want:false,age:9,o:0})),t0:0,c:[],flip:0};
const reflStale=sl=>{ const a=sl.pose.elements, b=camera.matrixWorld.elements; for(let i=0;i<15;i++) if(Math.abs(a[i]-b[i])>(i>=12?0.01:0.0008)) return true; return false; };""")
rep("""    if(best){ best.want=true; best.lvl=c.l; best.K=c.K; } else free.push(c); }
  for(const c of free){ const sl=S2.filter(t=>!t.want).sort((a,b)=>a.k-b.k)[0]; if(!sl) break; sl.want=true; sl.lvl=c.l; sl.K=c.K; sl.k=0; sl.ok=false; }""",
"""    if(best){ best.want=true; best.lvl=c.l; best.K=c.K; best.o=c.o; } else free.push(c); }
  for(const c of free){ const sl=S2.filter(t=>!t.want).sort((a,b)=>a.k-b.k)[0]; if(!sl) break; sl.want=true; sl.lvl=c.l; sl.K=c.K; sl.o=c.o; sl.k=0; sl.ok=false; }""")
rep("""  const act=S2.filter(sl=>sl.want), fresh=act.find(sl=>!sl.ok||Math.abs(sl.rl-sl.lvl)>0.25);
  let pick=fresh||null; if(!pick&&act.length){ const old=act.reduce((a,b)=>a.age>=b.age?a:b); if(act.length>1||old.age>=2) pick=old; }
  if(pick) reflDraw(pick,pick.lvl);""",
"""  // the nearer water's mirror is redrawn every frame while the view moves; the other one every other frame; standing
  // still, each now and then (for things moving in it)
  const act=S2.filter(sl=>sl.want).sort((a,b)=>a.o-b.o); REFL.flip^=1;
  for(let n=0;n<act.length;n++){ const sl=act[n], need=!sl.ok||Math.abs(sl.rl-sl.lvl)>0.25||sl.age>=(act.length>1?6:3)||(reflStale(sl)&&(n===0||REFL.flip));
    if(need) reflDraw(sl,sl.lvl); }""")
rep("""float w1=reflK*(d1>0.0?1.0-smoothstep(0.6,2.2,d1):1.0-smoothstep(1.5,5.0,-d1)), w2=reflK2*(d2>0.0?1.0-smoothstep(0.6,2.2,d2):1.0-smoothstep(1.5,5.0,-d2));""",
"""float w1=reflK*(d1>0.0?1.0-smoothstep(0.6,2.2,d1):1.0-smoothstep(1.0,2.6,-d1)), w2=reflK2*(d2>0.0?1.0-smoothstep(0.6,2.2,d2):1.0-smoothstep(1.0,2.6,-d2));""")
rep("""        if(w1>0.004&&w1>=w2){ vec4 rc=reflM*vec4(vW,1.0); mir=mix(mir,texture2D(reflT,clamp(rc.xy/rc.w+wob,0.003,0.997)).rgb,w1); }
        else if(w2>0.004){ vec4 rc=reflM2*vec4(vW,1.0); mir=mix(mir,texture2D(reflT2,clamp(rc.xy/rc.w+wob,0.003,0.997)).rgb,w2); }""",
"""        const vec2 ro=vec2(0.0011,0.0017);                                                                    // four taps a pixel apart: soft edges, no stair-steps
        if(w1>0.004&&w1>=w2){ vec4 rc=reflM*vec4(vW,1.0); vec2 u=clamp(rc.xy/rc.w+wob,0.004,0.996);
          mir=mix(mir,(texture2D(reflT,u+ro).rgb+texture2D(reflT,u-ro).rgb+texture2D(reflT,u+vec2(ro.x,-ro.y)).rgb+texture2D(reflT,u+vec2(-ro.x,ro.y)).rgb)*0.25,w1); }
        else if(w2>0.004){ vec4 rc=reflM2*vec4(vW,1.0); vec2 u=clamp(rc.xy/rc.w+wob,0.004,0.996);
          mir=mix(mir,(texture2D(reflT2,u+ro).rgb+texture2D(reflT2,u-ro).rgb+texture2D(reflT2,u+vec2(ro.x,-ro.y)).rgb+texture2D(reflT2,u+vec2(-ro.x,ro.y)).rgb)*0.25,w2); }""")
rep("""set(r.neck,'x',lerp(0.05,0.55,mvK));""","""set(r.neck,'x',lerp(0.05,0.7,mvK));""")
