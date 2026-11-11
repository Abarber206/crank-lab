# patch144: boats that float. The hull rides on five points (bow, stern, both sides, middle), each held up by the water
# under it (with a swell on the sea, ripples on rivers) or by the ground under its keel, and the boat pitches and rolls
# on springs toward them: it bobs, dips its nose into waves, lifts it under power and leans into turns. Any water deep
# enough to float the keel carries it, so it runs up streams. Driven at a beach it slides up the sand, grinds to a stop
# and sits there tilted on the slope (the propeller needs water to push; it can back off while the stern is still wet),
# carving grooves in the sand; a stranded boat nobody is near goes back to its mooring after a minute. No water shows
# inside the hull. A boat passenger sits with a hand on the rail instead of holding an imaginary roll cage, and the
# speed readout no longer sits on the ammo count.
a=s.index("function simBoat(k,inp,dt){"); b=s.index("function boatModel(k,dt,dCam){")
s=s[:a]+r"""// the hull's five points: [x, z, keel height] in the boat's own frame (forward is -z)
const BPTS=[[0,-1.85,0.02],[0,1.95,-0.28],[-0.72,0.35,-0.14],[0.72,0.35,-0.14],[0,0,-0.24]], BFLOAT=0.07;
function boatSwell(x,z,t,sea){ return sea?0.075*Math.sin(x*0.31+t*1.15)+0.055*Math.sin(z*0.27-t*0.92+1.3)+0.03*Math.sin((x+z)*0.6+t*2.1):0.012*Math.sin(x*0.9+t*2.4)+0.01*Math.sin(z*1.1-t*1.9); }
// for each hull point: the height the boat's origin would need to be held up there, and whether it's water or ground
function boatSupport(k,x,z,yaw,t,out){ const fx=-Math.sin(yaw), fz=-Math.cos(yaw), rx=Math.cos(yaw), rz=-Math.sin(yaw), S=WGEN.sea&&WGEN.sea(); let wet=0;
  for(let i=0;i<5;i++){ const p=BPTS[i], px=x+rx*p[0]-fx*p[1], pz=z+rz*p[0]-fz*p[1], g=terrainH(px,pz), w=waterAt(px,pz);
    const sea=w>-999&&S&&Math.abs(w-S.Y)<0.05, fl=w>-999?w+boatSwell(px,pz,t,sea)-BFLOAT:-1e9, gr=g-p[2]+0.02;
    const o=out[i]||(out[i]={}); o.h=Math.max(fl,gr); o.ground=gr>=fl; o.depth=w>-999?w-g:-1; o.x=px; o.z=pz; if(!o.ground) wet++; }
  return wet; }
const _bs=[], _bs2=[];
const boatGnd=B=>B.reduce((a,p)=>a+(p.ground?(p.depth>0.12?0.15:1):0),0)/5; // how much of the hull sits on dry ground
function simBoat(k,inp,dt){ const fx=-Math.sin(k.yaw), fz=-Math.cos(k.yaw), rx=Math.cos(k.yaw), rz=-Math.sin(k.yaw);
  k.bobT+=dt; let vf=k.vx*fx+k.vz*fz, vl=k.vx*rx+k.vz*rz; boatSupport(k,k.x,k.z,k.yaw,k.bobT,_bs);
  const gnd=boatGnd(_bs), prop=_bs[1].depth>0.12, vf0=vf;
  // the motor pushes only with the propeller in the water
  if(prop){ if(inp.fw>0.1) vf+=BACC*inp.fw*dt*Math.max(0,Math.min(1,1.1-vf/BMAX))*(vf<-0.3?2.2:1);
    else if(inp.fw<-0.1){ if(vf>0.3) vf-=BACC*1.4*(-inp.fw)*dt; else vf=Math.max(-BREV,vf-BACC*0.6*(-inp.fw)*dt); } }
  vf-=vf*((inp.fw>0.1&&prop?0.05:0.3)+0.006*Math.abs(vf))*dt;                  // water drag
  if(gnd>0){ const c=(gnd*11+1)*dt; vf=Math.abs(vf)<=c?0:vf-Math.sign(vf)*c; vl*=Math.exp(-gnd*10*dt); } // the keel dragging on the ground
  vl*=Math.exp(-(inp.hb?0.8:2.6)*dt);
  const sMax=0.62; k.steer+=(inp.st*sMax-k.steer)*Math.min(1,dt*4);
  if(gnd<0.6) k.yaw-=k.steer*1.25*Math.max(0.35,Math.min(1,(Math.abs(vf)+1.2)/6))*(vf<-0.2?-1:1)*(1-gnd)*dt;
  k.slip=Math.abs(vl); k.vf=vf; k.thr=prop?inp.fw:0; k.brk=false; k.acc=(k.acc||0)+((vf-vf0)/Math.max(dt,1e-3)-(k.acc||0))*Math.min(1,dt*6);
  k.vx=fx*vf+rx*vl; k.vz=fz*vf+rz*vl;
  const sp0=Math.hypot(k.vx,k.vz), ox=k.x, oz=k.z, nx=ox+k.vx*dt, nz=oz+k.vz*dt;
  // a bank too steep to slide up (a cliff, a rock) stops it like a wall
  const steep=(x,z)=>{ boatSupport(k,x,z,k.yaw,k.bobT,_bs2); return _bs2[0].ground&&_bs2[0].h-k.y>0.55; };
  if(!steep(nx,nz)&&!kartHits(k,nx,nz,k.yaw,ox,oz)){ k.x=nx; k.z=nz; }
  else if(!steep(nx,oz)&&!kartHits(k,nx,oz,k.yaw,ox,oz)){ k.x=nx; k.vz*=0.3; }
  else if(!steep(ox,nz)&&!kartHits(k,ox,nz,k.yaw,ox,oz)){ k.z=nz; k.vx*=0.3; }
  else { if(sp0>3){ sfxAt('kart_bump',_kz.set(k.x,k.y+0.3,k.z)); if(P.kart&&P.kart.k===k) shake=Math.max(shake,Math.min(0.2,sp0*0.02)); } k.vx*=-0.15; k.vz*=-0.15; }
  { const lost=sp0-Math.hypot(k.vx,k.vz); if(lost>6) kartDamage(k,(lost-6)*12); }
  { const dx=k.x-SPAWN[0], dz=k.z-SPAWN[2], d=Math.hypot(dx,dz); if(d>WORLD_EDGE){ k.x=SPAWN[0]+dx/d*WORLD_EDGE; k.z=SPAWN[2]+dz/d*WORLD_EDGE; k.vx*=0.3; k.vz*=0.3; } }
  boatFloat(k,dt,vf,inp); boatTracks(k); kartRam(k,vf); }
// the hull settles on its points: height, pitch and roll each on a soft spring, so it bobs and rocks rather than snapping
function boatFloat(k,dt,vf,inp){ const t=k.bobT; boatSupport(k,k.x,k.z,k.yaw,t,_bs); const B=_bs;
  const plane=Math.max(0,Math.min(1,(vf-4)/(BMAX-4))), gnd=boatGnd(B);
  const hMid=(B[0].h+B[1].h)/2*0.35+(B[2].h+B[3].h)/2*0.35+B[4].h*0.3;
  const yT=Math.max(hMid+0.08*plane*(1-gnd),Math.max(...B.map(p=>p.ground?p.h:-1e9))-0.03);
  let pT=Math.atan2(B[0].h-B[1].h,3.8)+(1-gnd)*(0.085*plane+Math.max(-0.05,Math.min(0.07,(k.acc||0)*0.012))), rT=Math.atan2(B[3].h-B[2].h,1.44);
  if(gnd<0.6) rT-=(k.steer||0)*Math.min(1,Math.abs(vf)/BMAX)*0.26*(1-gnd);   // leans into the turn
  const stiff=gnd>0.2?60:24, damp=gnd>0.2?14:4.5;
  k.vy+=(stiff*(yT-k.y)-damp*k.vy)*dt; k.y+=k.vy*dt; if(k.y<yT-0.25){ k.y=yT-0.25; k.vy=Math.max(0,k.vy); }
  k.pv=(k.pv||0)+((stiff*0.55)*(pT-k.pitch)-damp*0.8*(k.pv||0))*dt; k.rv=(k.rv||0)+((stiff*0.5)*(rT-k.roll)-damp*0.75*(k.rv||0))*dt;
  k.pitch+=k.pv*dt; k.roll+=k.rv*dt; k.air=false; k.gnd=gnd;
  // a sudden drop on to a wave or the beach: a splash and a jolt
  if(k.vy<-1.2&&B.some(p=>!p.ground)&&k.y<yT-0.05&&dt>0){ if(!k.slapT||k.slapT<k.bobT-0.4){ k.slapT=k.bobT; const w=waterAt(k.x,k.z); if(w>-999){ const p=kartPoint(k,0,0,-1.5,_ku); p.y=w+0.1; burst(p,8,3,0.08,splashMat); sfxAt('step_water',p); } } } }
function settleBoat(k,dt){ k.vf=0; k.thr=0; k.slip=0; k.steer*=Math.exp(-dt*3); k.acc=0; k.bobT+=dt;
  if(Math.hypot(k.vx,k.vz)>0.05){ const c=Math.exp(-dt*(1.2+(k.gnd||0)*10)); k.vx*=c; k.vz*=c; const nx=k.x+k.vx*dt, nz=k.z+k.vz*dt; if(!kartHits(k,nx,nz,k.yaw,k.x,k.z)){ k.x=nx; k.z=nz; } else { k.vx=k.vz=0; } } else { k.vx=k.vz=0; }
  boatFloat(k,dt,0,null);
  // stranded on the beach with nobody near for a minute: back to its mooring
  if((k.gnd||0)>=0.6&&!k.seats[0]&&!k.seats[1]&&Math.hypot(P.pos.x-k.x,P.pos.z-k.z)>40){ k.beachT=(k.beachT||0)+dt; if(k.beachT>60){ k.beachT=0; Object.assign(k,{x:k.home.x,y:k.home.y,z:k.home.z,yaw:k.home.yaw,pitch:0,roll:0,vx:0,vz:0,vy:0,pv:0,rv:0}); kartPose(k); } } else k.beachT=0; }
// grooves the keel cuts in sand and mud: dark, damp marks, the newest few hundred kept
const BTRK={m:null,n:0,max:360,last:new Map()};
function boatTracks(k){ if(!(k.gnd>0)) return; const sp=Math.hypot(k.vx,k.vz); if(sp<0.4) return;
  if(!BTRK.m){ const g=new THREE.PlaneGeometry(0.34,0.62); g.rotateX(-Math.PI/2); const m=new THREE.MeshLambertMaterial({color:0x5b4a33,transparent:true,opacity:0.55,depthWrite:false,polygonOffset:true,polygonOffsetFactor:-2,polygonOffsetUnits:-6});
    BTRK.m=new THREE.InstancedMesh(g,m,BTRK.max); BTRK.m.count=0; BTRK.m.frustumCulled=false; BTRK.m.receiveShadow=true; BTRK.m.renderOrder=1; scene.add(BTRK.m); }
  const L=BTRK.last.get(k)||[]; BTRK.last.set(k,L);
  for(let i=0;i<5;i++){ const p=_bs[i]; if(!p||!p.ground) continue; const l=L[i]; if(l&&Math.hypot(l[0]-p.x,l[1]-p.z)<0.5) continue; L[i]=[p.x,p.z];
    const y=terrainH(p.x,p.z)+0.015, [sl,gx,gz]=slopeAt(p.x,p.z); _bm.makeRotationY(k.yaw); _bq.setFromUnitVectors(_ZUP,_bn.set(-gx,1,-gz).normalize()); _bm.premultiply(_bm2.makeRotationFromQuaternion(_bq)); _bm.setPosition(p.x,y,p.z);
    const s_=i===1?1.3:i===4?1.1:0.8; _bm.scale(_bv.set(s_,1,1)); BTRK.m.setMatrixAt(BTRK.n%BTRK.max,_bm); BTRK.n++; BTRK.m.count=Math.min(BTRK.max,BTRK.n); BTRK.m.instanceMatrix.needsUpdate=true; } }
const _bm=new THREE.Matrix4(), _bm2=new THREE.Matrix4(), _bq=new THREE.Quaternion(), _bn=new THREE.Vector3(), _bv=new THREE.Vector3();
"""+s[b:]
# the wake only on water, from the stern
rep("""  k.wakeT-=dt; const sp=Math.hypot(k.vx,k.vz); if(k.wakeT<=0&&dCam<80&&sp>1.2){""","""  k.wakeT-=dt; const sp=Math.hypot(k.vx,k.vz); if(k.wakeT<=0&&dCam<80&&sp>1.2&&(k.gnd||0)<0.8){""")
# no water inside the hull: a depth-only lid inside the gunwales, drawn after the boat and before the water
rep("""  const out={}; for(const k in bins) out[k]=mergeGeos(bins[k]); out.outer=h.outer; out.inner=h.inner; out.top=h.top;""",
"""  const out={}; for(const k in bins) out[k]=mergeGeos(bins[k]); out.outer=h.outer; out.inner=h.inner; out.top=h.top;
  { const pos=[], N=24, Y=0.42; let prev=null; for(let n=0;n<=N;n++){ const t=0.06+0.94*n/N, w=Math.max(0.02,h.half(t)*0.94-0.07), z=h.zOf(t), cur=[[-w,Y,z],[w,Y,z]]; if(prev) pos.push(prev[0],cur[0],prev[1], prev[1],cur[0],cur[1]); prev=cur; }
    const g=new THREE.BufferGeometry(); g.setAttribute('position',new THREE.Float32BufferAttribute(pos.flat(),3)); out.cap=g; }""")
rep("""  mesh(G.outer,M.hull); mesh(G.inner,M.inner); mesh(G.top,M.white);""","""  mesh(G.outer,M.hull); mesh(G.inner,M.inner); mesh(G.top,M.white);
  { const cap=new THREE.Mesh(G.cap,kMat('bcap',()=>new THREE.MeshBasicMaterial({colorWrite:false,depthWrite:true,transparent:true,side:THREE.DoubleSide}))); cap.renderOrder=1; cap.castShadow=false; body.add(cap); }""")
# the passenger in a boat: a hand on the rail, not up on a roll cage
rep("""  else { T.shL=0.4; T.shLz=-0.2; T.elL=1.0; T.shR=2.55; T.shRz=0.42; T.elR=0.75; T.chZ=0.04; } }""",
    """  else if(S.seat.k.boat){ T.shL=0.35; T.shLz=-0.32; T.elL=0.9; T.shR=0.3; T.shRz=0.62; T.elR=0.55; T.chZ=0.02; }
  else { T.shL=0.4; T.shLz=-0.2; T.elL=1.0; T.shR=2.55; T.shRz=0.42; T.elR=0.75; T.chZ=0.04; } }""")
# the speed readout: no ammo count under it while you drive; on a phone it sits at the top
rep("  const xa=$('xAmmo'), showA=mode==='gun'&&!edit&&playing;","  const xa=$('xAmmo'), showA=mode==='gun'&&!edit&&playing&&!(P.kart&&P.kart.seat===0);")
s=s.replace("</style>","body.touch #kartHud{bottom:auto;top:calc(env(safe-area-inset-top,0px) + 58px)}\n</style>",1)
