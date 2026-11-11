# patch132: knocked down, the whole body lies on the ground. The body is tilted to the slope under it (up, down or across a
# hill) and then lowered or raised until its lowest point rests on the ground, measured on the real body each frame
rep("""    G.rotation.x=lerp(G.rotation.x,-1.38*e,Math.min(1,dt*10)); G.rotation.z=0; G.position.y=S.pos.y+0.3*e;
    A.crawl=(A.crawl||0)+dt*(0.6+Math.min(1.5,sp)*5.2);""",
"""    A.dnX=lerp(A.dnX||0,-1.38*e,Math.min(1,dt*10)); G.position.y=S.pos.y+0.3*e;
    A.crawl=(A.crawl||0)+dt*(0.6+Math.min(1.5,sp)*5.2);""")
rep("""    G.position.y=S.pos.y+(0.24+0.025*Math.abs(Math.cos(A.crawl))*mvK)*e; G.rotation.z=0.09*c1*mvK*e;                       // low, rolling towards the reaching arm""",
    """    G.position.y=S.pos.y+(0.24+0.025*Math.abs(Math.cos(A.crawl))*mvK)*e; A.dnZ=0.09*c1*mvK*e;                               // low, rolling towards the reaching arm""")
rep("""    A.handL=A.handR='flat'; A.turnL=A.turnR=0;
    for(const k of GUN_MODELS) if(r[k]) r[k].visible=false; r.gun.visible=r.pump.visible=r.hammer.visible=r.plan.visible=false; r.pick.visible=false;
    if(H.glider) H.glider.visible=false; return; }
  A.downT=0;""",
"""    A.handL=A.handR='flat'; A.turnL=A.turnR=0;
    for(const k of GUN_MODELS) if(r[k]) r[k].visible=false; r.gun.visible=r.pump.visible=r.hammer.visible=r.plan.visible=false; r.pick.visible=false;
    if(H.glider) H.glider.visible=false; downFit(H,S,dt,e); return; }
  A.downT=0; A.dnX=0; A.dnZ=0; A.dnOff=null; if(A.dnN) A.dnN.set(0,1,0);""")
rep("""function animateRig0(H,S,dt){""",
"""/* lying down on the ground: the slope under the body (a plane fitted to the terrain along and across it; a level floor when
   lying on a build or indoors), the body tilted to it, and then moved so its lowest point just touches it */
const _dfC=new Float32Array(768), _dfQ=new THREE.Quaternion(), _dfQ2=new THREE.Quaternion(), _dfE=new THREE.Euler(0,0,0,'YXZ'), _dfN=new THREE.Vector3(), _dfUp=new THREE.Vector3(0,1,0), _dfV=new THREE.Vector3(), _dfI=new THREE.Quaternion();
function downPoints(H){ const r=H.rig, skip=new Set([r.gun,r.pump,r.hammer,r.plan,r.pick,r.heldMag,r.heldShell,H.glider,...GUN_MODELS.map(k=>r[k])].filter(Boolean)), out=[];
  const walk=(o,chain)=>{ if(skip.has(o)) return; if(o.isSprite||o.isLine||o.isPoints) return; const ch=o===H.group?chain:chain.concat(o);
    if(o.isMesh&&o.geometry&&o.geometry.attributes.position){ const pa=o.geometry.attributes.position, n=pa.count, pts=[];
      if(n<=18){ for(let i=0;i<n;i++) pts.push(new THREE.Vector3().fromBufferAttribute(pa,i)); }
      else { const D=[]; for(let a=-1;a<=1;a++) for(let b=-1;b<=1;b++) for(let c=-1;c<=1;c++) if(a||b||c) D.push([a,b,c]); // its extremes in 26 directions
        const best=D.map(()=>[-1e9,0]), v=new THREE.Vector3();
        for(let i=0;i<n;i++){ v.fromBufferAttribute(pa,i); for(let j=0;j<26;j++){ const d=D[j], s_=v.x*d[0]+v.y*d[1]+v.z*d[2]; if(s_>best[j][0]) best[j]=[s_,i]; } }
        const seen=new Set(); best.forEach(b=>{ if(!seen.has(b[1])){ seen.add(b[1]); pts.push(new THREE.Vector3().fromBufferAttribute(pa,b[1])); } }); }
      out.push({o,chain:ch,pts}); }
    for(const c of o.children) walk(c,ch); };
  walk(H.group,[]); return out; }
function downFit(H,S,dt,e){ const G=H.group, A=H.anim, fx=-Math.sin(S.yaw), fz=-Math.cos(S.yaw), rx=Math.cos(S.yaw), rz=-Math.sin(S.yaw);
  // the ground: the terrain's own slope, unless the body is lying on something else (a floor, a build, a road deck)
  const cx=S.pos.x+fx*0.75, cz=S.pos.z+fz*0.75, onT=Math.abs(S.pos.y-terrainH(S.pos.x,S.pos.z))<0.3;
  let h0=S.pos.y, sf=0, sr=0;
  if(onT){ const hf=terrainH(cx+fx*0.95,cz+fz*0.95), hb=terrainH(cx-fx*0.95,cz-fz*0.95), hr=terrainH(cx+rx*0.45,cz+rz*0.45), hl=terrainH(cx-rx*0.45,cz-rz*0.45);
    sf=Math.max(-1.2,Math.min(1.2,(hf-hb)/1.9)); sr=Math.max(-1.2,Math.min(1.2,(hr-hl)/0.9)); h0=(hf+hb+hr+hl)*0.25+(S.pos.y-terrainH(S.pos.x,S.pos.z)); }
  const gy=(x,z)=>h0+sf*((x-cx)*fx+(z-cz)*fz)+sr*((x-cx)*rx+(z-cz)*rz);
  _dfN.set(-(sf*fx+sr*rx),1,-(sf*fz+sr*rz)).normalize(); if(!A.dnN) A.dnN=new THREE.Vector3(0,1,0); A.dnN.lerp(_dfN,Math.min(1,dt*9)).normalize();
  _dfQ.setFromUnitVectors(_dfUp,A.dnN); _dfQ2.copy(_dfI).slerp(_dfQ,e);
  _dfE.set(A.dnX||0,S.yaw,A.dnZ||0); G.quaternion.setFromEuler(_dfE).premultiply(_dfQ2);
  G.updateMatrixWorld(true);
  const pts=A.dnPts||(A.dnPts=downPoints(H)), C=_dfC; let lo=1e9, nc=0;
  for(const m of pts){ let vis=true; for(const c of m.chain) if(!c.visible){ vis=false; break; } if(!vis) continue;
    const w=m.o.matrixWorld; for(const p of m.pts){ _dfV.copy(p).applyMatrix4(w); const d=_dfV.y-gy(_dfV.x,_dfV.z); if(d<lo) lo=d;
      if(onT&&d<lo+0.08&&nc<256){ C[nc*3]=_dfV.x; C[nc*3+1]=_dfV.y; C[nc*3+2]=_dfV.z; nc++; } } }
  if(lo>1e8) return;
  if(onT){ const off=S.pos.y-terrainH(S.pos.x,S.pos.z); let n=0; for(let i=0;i<nc&&n<40;i++){ const y=C[i*3+1]; if(y-gy(C[i*3],C[i*3+2])>lo+0.08) continue; n++; const d=y-terrainH(C[i*3],C[i*3+2])-off; if(d<lo) lo=d; } } // the real ground under the lowest points
  const want=-lo+0.01; // the lowest point just on the ground
  A.dnOff=A.dnOff==null||want>A.dnOff?want:lerp(A.dnOff,want,Math.min(1,dt*12));
  G.position.y+=A.dnOff; }
function animateRig0(H,S,dt){""")
# the pose itself: flatter (belly down rather than arched up on head and toes), the head held a little up when still, and the
# crawling knee drawn up along the ground (out to the side) instead of down into it
rep("A.dnX=lerp(A.dnX||0,-1.38*e,Math.min(1,dt*10));","A.dnX=lerp(A.dnX||0,-1.5*e,Math.min(1,dt*10));")
rep("set(r.spine,'x',-0.16-0.02*br);","set(r.spine,'x',0.05-0.02*br);")
rep("set(r.chest,'x',-0.22-0.035*br*(1-mvK));","set(r.chest,'x',0-0.035*br*(1-mvK));")
rep("set(r.neck,'x',-0.32-0.4*mvK);","set(r.neck,'x',0.1+0.3*mvK);")
rep("for(const [L,up,sx] of [[r.legL,P2,-1],[r.legR,P1,1]]){ set(L.hp,'x',-0.05+0.6*up*mvK); set(L.hp,'z',sx*(0.12+0.5*up*mvK)); set(L.hp,'y',sx*1.25*up*mvK); set(L.kn,'x',-0.2-1.05*up*mvK); set(L.an,'x',0.75); }",
    "for(const [L,up,sx] of [[r.legL,P2,-1],[r.legR,P1,1]]){ set(L.hp,'x',-0.05+0.15*up*mvK); set(L.hp,'z',sx*(0.12+0.8*up*mvK)); set(L.hp,'y',sx*1.4*up*mvK); set(L.kn,'x',-0.2-1.2*up*mvK); set(L.an,'x',0.75); }")
