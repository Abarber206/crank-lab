# ---------- 94. skydive and glider feel ----------
# (a) glide: looking straight ahead (or a little down, as you naturally do in third person) is a shallow, almost level glide
# (about 9 m forward per metre lost); you have to look clearly down to dive. Near the ground it flares for a soft landing.
rep("    const G0=-0.22, TRIM=13, VMAX=33, VMIN=6;","    const G0=-0.15, TRIM=13, VMAX=33, VMIN=6;")
rep("    let gt=G0+(E.pitch||0)*1.15-(fw>0.3?0.14:0)+(fw<-0.3?0.16:0); gt=Math.max(-1.15,Math.min(0.42,gt));",
    "    const lp=(E.pitch||0)+0.14, lq=Math.abs(lp)<0.16?0:lp-Math.sign(lp)*0.16; // a dead band around 'ahead'\n    let gt=G0+lq*1.2-(fw>0.3?0.08:0)+(fw<-0.3?0.1:0); gt=Math.max(-1.15,Math.min(0.42,gt));\n    if(above<6&&gt<-0.06){ gt=Math.max(gt,-0.06-0.3*(above/6)); } // the flare")
rep("want=gl?Math.max(-0.95,Math.min(0.5,-0.2+(gam+0.22)*0.9))","want=gl?Math.max(-0.95,Math.min(0.5,-0.2+(gam+0.15)*0.9))")
# (b) freefall: snappier steering; the body banks into the way it's sliding and tips forward when it's tracking
rep("    tx=wx*sp; tz=wz*sp; ty=-(38+22*S.dive); acc=9;","    tx=wx*sp; tz=wz*sp; ty=-(38+22*S.dive); acc=15;")
rep("  A.skyX=lerp(A.skyX||0,want,Math.min(1,dt*(gl?5:3))); A.skyZ=lerp(A.skyZ||0,Math.max(-0.55,Math.min(0.55,-(A.yawRate||0)*(gl?0.2:0.07)))+(gl?Math.sin(A.t*1.1)*0.03:0),Math.min(1,dt*3));",
    "  const sRx=Math.cos(S.yaw), sRz=-Math.sin(S.yaw), lat=S.vel.x*sRx+S.vel.z*sRz, fwdV=-(S.vel.x*Math.sin(S.yaw)+S.vel.z*Math.cos(S.yaw));\n  A.skyX=lerp(A.skyX||0,want-(gl?0:Math.max(-0.2,Math.min(0.3,fwdV/60))),Math.min(1,dt*(gl?5:3))); A.skyZ=lerp(A.skyZ||0,Math.max(-0.7,Math.min(0.7,-(A.yawRate||0)*(gl?0.2:0.07)-lat*(gl?0.07:0.035)))+(gl?Math.sin(A.t*1.1)*0.03:Math.sin(A.t*2.3)*0.025),Math.min(1,dt*(gl?3:4.5)));")
# (c) landing: a thump, a puff of dust and a dip of the camera
rep("function endSky(E){ E.sky=null; E.fallTop=null; if(E.vel.y<-7) E.vel.y=-7; }","function endSky(E){ const gl=E.sky&&E.sky.phase==='glide'; E.sky=null; E.fallTop=null; if(E.vel.y<-7) E.vel.y=-7;\n  if(E===P){ camDip=Math.min(camDip,-0.22); sfx('land'); skyFovK*=0.5; } if(E.pos.distanceTo(P.pos)<60) burst(E.pos.clone().setY(E.pos.y+0.1),gl?8:14,gl?2.4:4,0.08,typeof dustMat!=='undefined'?dustMat:undefined); }")
# (d) speed you can feel: the view widens as you fall faster, and streaks of air rush past
rep("  if(a>=1) camera.fov=settings.fov*zoom;","  const zoom0=zoom; { const k=1+0.16*(typeof skyFovK==='number'?skyFovK:0); if(a>=1){ camera.fov=Math.min(118,settings.fov*zoom*k); if(AW.scope) camera.fov*=1+(SCOPE_STEPS[scopeLvl]-1)*adsK; camera.updateProjectionMatrix(); return; } }\n  if(a>=1) camera.fov=settings.fov*zoom;")
rep("var downCamK=0;\nfunction updateCamera(){\n","""var downCamK=0, skyFovK=0, _skyFovApplied=0, windFx=null;
function stepWind(dt){ const sp=P.sky?P.vel.length():0, want=P.sky?Math.max(0,Math.min(1,(sp-14)/40)):0; skyFovK+=(want-skyFovK)*Math.min(1,dt*2.5);
  if(Math.abs(skyFovK-_skyFovApplied)>0.004){ _skyFovApplied=skyFovK; applyFov(); }
  if(!windFx){ const N=46, g=new THREE.BufferGeometry(); g.setAttribute('position',new THREE.BufferAttribute(new Float32Array(N*6),3));
    const l=new THREE.LineSegments(g,new THREE.LineBasicMaterial({color:0xffffff,transparent:true,opacity:0,fog:false,depthWrite:false})); l.frustumCulled=false; l.visible=false; scene.add(l); windFx={l,N,p:[...Array(N)].map(()=>({x:0,y:0,z:0,on:false}))}; }
  const W=windFx, on=skyFovK>0.08&&sp>16; W.l.material.opacity+=((on?0.16+0.3*skyFovK:0)-W.l.material.opacity)*Math.min(1,dt*4); W.l.visible=W.l.material.opacity>0.01; if(!W.l.visible) return;
  const vx=P.vel.x/sp||0, vy=P.vel.y/sp||-1, vz=P.vel.z/sp||0, len=Math.min(7,sp*0.11), c=camera.position, a=W.l.geometry.attributes.position;
  // streaks hang in the air; you fall past them. One that's dropped behind is put back ahead, somewhere around your path
  let ux=-vz, uy=0, uz=vx; const ul=Math.hypot(ux,uz); if(ul<1e-3){ ux=1; uz=0; } else { ux/=ul; uz/=ul; } const wx=vy*uz-vz*uy, wy=vz*ux-vx*uz, wz=vx*uy-vy*ux;
  W.p.forEach((q,i)=>{ const dx=q.x-c.x, dy=q.y-c.y, dz=q.z-c.z, along=dx*vx+dy*vy+dz*vz; if(!q.on||along<-8||along>90||dx*dx+dy*dy+dz*dz>9000){ const d=on?12+Math.random()*60:1e4, r=2.5+Math.random()*13, t=Math.random()*6.283, cu=Math.cos(t)*r, cw=Math.sin(t)*r; q.x=c.x+vx*d+ux*cu+wx*cw; q.y=c.y+vy*d+uy*cu+wy*cw; q.z=c.z+vz*d+uz*cu+wz*cw; q.on=true; }
    a.setXYZ(i*2,q.x,q.y,q.z); a.setXYZ(i*2+1,q.x-vx*len,q.y-vy*len,q.z-vz*len); }); a.needsUpdate=true; }
function updateCamera(){
  stepWind(lastDt);
""")
# (e) freefall: belly-down you float (about 20 m/s down) and can track a long way across the map (24 m/s); diving is fast
# (58 m/s down) and you still carry 18 m/s across the ground
rep("    const sp=12+12*S.dive; let wx=fx*fw+rx*st, wz=fz*fw+rz*st;","    const sp=24-6*S.dive; let wx=fx*fw+rx*st, wz=fz*fw+rz*st;")
rep("    tx=wx*sp; tz=wz*sp; ty=-(38+22*S.dive); acc=15;","    tx=wx*sp; tz=wz*sp; ty=-(20+38*S.dive); acc=15;")
rep("const dive=gl?0:Math.max(0,Math.min(1,(-S.vel.y-38)/20)),","const dive=gl?0:Math.max(0,Math.min(1,(-S.vel.y-22)/32)),")
