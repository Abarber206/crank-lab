# patch136: motorboats, built on the buggy. A small open boat (white hull with a painted stripe, a console with a
# windscreen and wheel, a driver's seat and a bench up front, an outboard motor that swings as you steer) moored at
# the sea's edge and on the rivers near each town. Same controls, seats, network sync, damage and Buddy-rides-along
# as the buggy; it floats, rides up onto the plane at speed, leans into turns, drifts, and leaves a wake. It won't go
# up onto land: it runs aground and stops. Get out in deep water and you swim.
rep("function seatWorld(k,s,out){ const sl=KART_SEATS[s];","function seatWorld(k,s,out){ const sl=(k.boat?BOAT_SEATS:KART_SEATS)[s];")
rep("""function kartPose(k){ k.g.position.set(k.x,k.y,k.z); k.g.rotation.set(k.pitch,k.yaw,k.roll); k.g.updateMatrixWorld(true);
  const fx=-Math.sin(k.yaw), fz=-Math.cos(k.yaw); k.solid.boxes=""",
"""function kartPose(k){ k.g.position.set(k.x,k.y,k.z); k.g.rotation.set(k.pitch,k.yaw,k.roll); k.g.updateMatrixWorld(true);
  const fx=-Math.sin(k.yaw), fz=-Math.cos(k.yaw); if(k.boat){ k.solid.boxes=[-1.6,-0.55,0.55,1.6].map((a,i)=>{ const cx=k.x-fx*a, cz=k.z-fz*a, r=i===0?0.55:0.85; return [cx-r,k.y-0.3,cz-r,cx+r,k.y+0.72,cz+r]; }); return; }
  k.solid.boxes=""")
rep("""function kartHits(k,x,z,yaw,ox,oz){ const fx=-Math.sin(yaw), fz=-Math.cos(yaw), lo=k.y+0.45, hi=k.y+1.4,""",
    """function kartHits(k,x,z,yaw,ox,oz){ const fx=-Math.sin(yaw), fz=-Math.cos(yaw), lo=k.y+(k.boat?-0.1:0.45), hi=k.y+1.4,""")
rep("""  for(const a of [-0.85,0,0.85]){ const b=hit(x-fx*a,z-fz*a); if(b&&b!==hit(ox-fx*a,oz-fz*a)) return true; } return false; }""",
    """  for(const a of (k.boat?[-1.6,-0.55,0.55,1.6]:[-0.85,0,0.85])){ const b=hit(x-fx*a,z-fz*a); if(b&&b!==hit(ox-fx*a,oz-fz*a)) return true; } return false; }""")
# the zombie ramming, shared with the boat
rep("""  // ram the zombies
  if(horde.on&&Math.abs(vf)>4){""","""  kartRam(k,vf); }
function kartRam(k,vf){
  if(horde.on&&Math.abs(vf)>4){""")
rep("""function kartShove(k,E){ if(!E||E.kart) return; const fx=-Math.sin(k.yaw), fz=-Math.cos(k.yaw);
  if(Math.abs(E.pos.x-k.x)>3||Math.abs(E.pos.z-k.z)>3||E.pos.y>k.y+1.35||E.pos.y+1.7<k.y+0.3) return;
  for(const a of [-0.8,0,0.8]){ const cx=k.x-fx*a, cz=k.z-fz*a, dx=E.pos.x-cx, dz=E.pos.z-cz, d=Math.hypot(dx,dz), m=0.72+R;""",
"""function kartShove(k,E){ if(!E||E.kart) return; const fx=-Math.sin(k.yaw), fz=-Math.cos(k.yaw);
  if(Math.abs(E.pos.x-k.x)>4||Math.abs(E.pos.z-k.z)>4||E.pos.y>k.y+1.35||E.pos.y+1.7<k.y+(k.boat?-0.3:0.3)) return;
  for(const a of (k.boat?[-1.6,-0.55,0.55,1.6]:[-0.8,0,0.8])){ const cx=k.x-fx*a, cz=k.z-fz*a, dx=E.pos.x-cx, dz=E.pos.z-cz, d=Math.hypot(dx,dz), m=(k.boat?(a<-1?0.55:0.88):0.72)+R;""")
rep("""for(let s=0;s<2;s++){ if(k.seats[s]) continue; const p=kartPoint(k,s?0.95:-0.95,0,0.1,_ku); consider(p.x,k.y,p.z,2.3,{kind:'kart',k,s,label:s?'Ride as passenger':'Drive'}); } } }""",
    """for(let s=0;s<2;s++){ if(k.seats[s]) continue; const p=kartPoint(k,k.boat?(s?1.3:-1.3):(s?0.95:-0.95),0,k.boat?(s?-0.55:0.85):0.1,_ku); consider(p.x,k.boat?Math.max(k.y-0.9,Math.min(k.y,P.pos.y)):k.y,p.z,k.boat?2.6:2.3,{kind:'kart',k,s,label:s?'Ride as passenger':'Drive'}); } } }""")
rep("""    if(k.local&&k.seats[0]===me){ const inp=playing&&k.inp?k.inp:{fw:0,st:0,hb:false}; k.inp=null; let t=dt; while(t>1e-5){ const h=Math.min(t,1/60); simKart(k,inp,h); t-=h; } }
    else if(k.driver&&k.tgt) interpKart(k,dt);
    else if(dCam<160) settleKart(k,dt);
    kartModel(k,dt,dCam);""",
"""    if(k.local&&k.seats[0]===me){ const inp=playing&&k.inp?k.inp:{fw:0,st:0,hb:false}; k.inp=null; let t=dt; while(t>1e-5){ const h=Math.min(t,1/60); (k.boat?simBoat:simKart)(k,inp,h); t-=h; } }
    else if(k.driver&&k.tgt) interpKart(k,dt);
    else if(dCam<160) (k.boat?settleBoat:settleKart)(k,dt);
    (k.boat?boatModel:kartModel)(k,dt,dCam);""")
rep("""function initKarts(){ karts=[];""","""function initKarts(){ karts=[]; initKarts0(); initBoats(); }
function initKarts0(){""")
rep("""// where a point on the buggy is in the world""",r"""/* ---------- the motorboat ---------- */
const BOAT_SEATS=[[0,0.6,0.92],[0,0.6,-0.5]], BMAX=12.5, BREV=4, BACC=6.5, BDRAFT=0.16, BOAT_MIN=0.32;
let boatGeo=null;
// the hull: sections from the bow (t=0) to the stern (t=1), each a rounded V; the bow is raised and comes to a point
function boatHull(){ const N=26, half=t=>t<0.55?0.95*Math.pow(Math.sin(Math.min(1,t/0.55)*Math.PI/2),0.75):0.95-0.06*(t-0.55)/0.45, sheer=t=>0.72+0.32*Math.pow(1-t,2.2), keel=t=>-0.28+0.5*Math.pow(1-t,3),
    zOf=t=>-2.3+4.6*t, prof=[[1,1],[0.99,0.7],[0.96,0.42],[0.9,0.18],[0.74,0.02],[0.45,-0.08],[0,-0.12]]; // [width, height] down one side: 1 is the gunwale, -0.12 the keel (scaled per section)
  const sec=(t,inset)=>{ const B=Math.max(0.001,half(t)-inset), H=sheer(t), K=keel(t)+inset*0.8, pts=[]; for(let s=-1;s<=1;s+=2){ const list=s<0?prof:prof.slice().reverse(); for(const [w,h] of list){ if(s>0&&w===0) continue; const y=h>=0?K+(H-K)*(0.2+0.8*h):K+(0.2*(H-K))*(1+h/0.12)*0+K*0+((H-K)*0.2)*(1+h/0.12); pts.push([s*w*B,Math.max(K,Math.min(H,y)),zOf(t)]); } } return pts; };
  const strip=(A,Bs,flip,out)=>{ for(let i=0;i<A.length-1;i++){ const a=A[i], b=A[i+1], c=Bs[i], d=Bs[i+1]; if(flip) out.push(a,c,b, b,c,d); else out.push(a,b,c, b,d,c); } };
  const outer=[], inner=[], top=[], tr=[]; let prevO=null, prevI=null;
  for(let n=0;n<=N;n++){ const t=n/N, O=sec(t,0), I=sec(Math.max(t,0.07),0.055); if(prevO){ strip(prevO,O,false,outer); strip(prevI,I,true,inner); top.push(prevO[0],O[0],prevI[0], O[0],I[0],prevI[0], prevO[prevO.length-1],prevI[prevI.length-1],O[O.length-1], O[O.length-1],prevI[prevI.length-1],I[I.length-1]); } prevO=O; prevI=I; }
  const S=sec(1,0); for(let i=1;i<S.length-1;i++) tr.push(S[0],S[i+1],S[i]); // the transom
  const mk=list=>{ const g=new THREE.BufferGeometry(); g.setAttribute('position',new THREE.Float32BufferAttribute(list.flat(),3)); g.computeVertexNormals(); return g; };
  return {outer:mk(outer.concat(tr)),inner:mk(inner),top:mk(top),half,sheer,keel,zOf}; }
function buildBoatGeo(){ const h=boatHull(), V=(x,y,z)=>new THREE.Vector3(x,y,z), bins={}; const put=(slot,geo,x=0,y=0,z=0,rx=0,ry=0,rz=0)=>{ const q=geo.clone(); q.applyMatrix4(new THREE.Matrix4().compose(V(x,y,z),new THREE.Quaternion().setFromEuler(new THREE.Euler(rx,ry,rz)),V(1,1,1))); (bins[slot]||(bins[slot]=[])).push(q); };
  // a painted stripe and a dark boot-top line along both sides, just proud of the hull
  for(const [slot,y0,y1] of [['paint',0.36,0.47],['dark',0.02,0.1]]){ const pos=[]; const N=40;
    for(let s=-1;s<=1;s+=2) for(let n=0;n<N;n++){ const t0=0.04+0.96*n/N, t1=0.04+0.96*(n+1)/N, p=(t,y)=>{ const B=h.half(t), K=h.keel(t), H=h.sheer(t), f=Math.max(0,Math.min(1,(y-K)/(H-K))); const w=f>0.2?0.96+0.04*(f-0.2)/0.8:0.74+0.22*f/0.2; return [s*(B*w+0.012),y,h.zOf(t)]; };
      const a=p(t0,y0), b=p(t1,y0), c=p(t0,y1), d=p(t1,y1); if(s>0) pos.push(a,c,b, b,c,d); else pos.push(a,b,c, b,d,c); }
    const g=new THREE.BufferGeometry(); g.setAttribute('position',new THREE.Float32BufferAttribute(pos.flat(),3)); g.setAttribute('uv',new THREE.Float32BufferAttribute(new Array(pos.length*2).fill(0),2)); g.computeVertexNormals(); (bins[slot]||(bins[slot]=[])).push(g); }
  // the deck: a flat floor inside, and the transom cap
  put('deck',new THREE.BoxGeometry(1.5,0.05,3.7),0,0.06,0.45);
  // the console: a box with a dash, a windscreen, the wheel on its back
  put('white',rbox(0.72,0.86,0.56,0.06),0,0.49,0.28); put('dark',new THREE.BoxGeometry(0.62,0.06,0.3),0,0.9,0.36,-0.5);
  put('glass',new THREE.BoxGeometry(0.76,0.36,0.03),0,1.08,0.08,-0.42); put('chrome',new THREE.BoxGeometry(0.8,0.03,0.05),0,1.25,0.0,-0.42);
  // the driver's seat (a box seat on a pedestal) and a bench across the bow
  put('seat',rbox(0.56,0.16,0.48,0.05),0,0.5,0.95); put('seat',rbox(0.56,0.42,0.1,0.04),0,0.76,1.17,0.12); put('metal',new THREE.CylinderGeometry(0.06,0.09,0.38,10),0,0.25,0.95);
  put('seat',rbox(1.3,0.16,0.5,0.05),0,0.5,-0.55); put('white',rbox(1.34,0.36,0.46,0.03),0,0.26,-0.55);
  // a rail round the bow, cleats, the motor well
  { const rp=[]; for(let n=0;n<=10;n++){ const t=0.02+0.3*n/10; rp.push([h.half(t)*0.92,h.sheer(t)+0.2,h.zOf(t)]); } for(const s of [-1,1]) for(let n=0;n<10;n++){ const a=rp[n], b=rp[n+1]; put('chrome',tubeGeo(V(s*a[0],a[1],a[2]),V(s*b[0],b[1],b[2]),0.018)); if(n%3===0) put('chrome',tubeGeo(V(s*a[0],a[1],a[2]),V(s*a[0],a[1]-0.2,a[2]),0.016)); }
    put('chrome',tubeGeo(V(-rp[0][0],rp[0][1],rp[0][2]),V(rp[0][0],rp[0][1],rp[0][2]),0.018)); }
  for(const s of [-1,1]) for(const z of [-1.2,1.9]) put('chrome',new THREE.BoxGeometry(0.05,0.04,0.2),s*(h.half((z+2.3)/4.6)-0.06),h.sheer((z+2.3)/4.6)+0.02,z);
  put('white',new THREE.BoxGeometry(1.5,0.4,0.08),0,0.28,1.98);
  const out={}; for(const k in bins) out[k]=mergeGeos(bins[k]); out.outer=h.outer; out.inner=h.inner; out.top=h.top;
  // the outboard: cowling, a leg down into the water, the propeller
  const mo=[]; const pm=(geo,x,y,z,rx=0)=>{ const q=geo.clone(); q.applyMatrix4(new THREE.Matrix4().compose(V(x,y,z),new THREE.Quaternion().setFromEuler(new THREE.Euler(rx,0,0)),V(1,1,1))); mo.push(q); };
  pm(rbox(0.42,0.5,0.52,0.1),0,0.62,0.18); pm(new THREE.BoxGeometry(0.44,0.08,0.54),0,0.38,0.18); pm(new THREE.BoxGeometry(0.12,0.75,0.2),0,0.0,0.16); pm(new THREE.CylinderGeometry(0.07,0.09,0.32,10),0,-0.38,0.12,Math.PI/2);
  out.motor=mergeGeos(mo); out.prop=(()=>{ const bl=[]; for(let i=0;i<3;i++){ const q=new THREE.BoxGeometry(0.05,0.28,0.02); q.translate(0,0.14,0); q.rotateZ(i*Math.PI*2/3); bl.push(q); } return mergeGeos(bl); })();
  out.sw=(kartGeo||(kartGeo=buildKartGeo())).sw; return out; }
function makeBoatModel(pi){ if(!boatGeo) boatGeo=buildBoatGeo(); const G=boatGeo, paint=KART_PAINT[pi%KART_PAINT.length];
  const M={paint:kMat('p'+pi,()=>new THREE.MeshPhongMaterial({color:paint,shininess:90,specular:0x5a5a5a})),hull:kMat('hull',()=>new THREE.MeshPhongMaterial({color:0xf3f1ec,shininess:80,specular:0x6a6a6a})),
    inner:kMat('hullIn',()=>new THREE.MeshLambertMaterial({color:0xe2ded4,side:THREE.DoubleSide})),deck:kMat('deck',()=>new THREE.MeshLambertMaterial({color:0xb9a27e})),white:kMat('white',()=>new THREE.MeshPhongMaterial({color:0xf1efe9,shininess:60})),
    dark:kMat('dark',()=>new THREE.MeshPhongMaterial({color:0x1e2025,shininess:40,specular:0x333333})),chrome:kMat('chrome',()=>new THREE.MeshPhongMaterial({color:0xd8dde2,shininess:120,specular:0xffffff})),
    metal:kMat('metal',()=>new THREE.MeshPhongMaterial({color:0x8d939b,shininess:60,specular:0x777777})),seat:kMat('bseat',()=>new THREE.MeshLambertMaterial({color:0xece6da})),
    glass:kMat('glass',()=>new THREE.MeshPhongMaterial({color:0x9fc4d6,transparent:true,opacity:0.38,shininess:120,specular:0xffffff,depthWrite:false})),motor:kMat('motor',()=>new THREE.MeshPhongMaterial({color:0x202226,shininess:70,specular:0x444444}))};
  const g=new THREE.Group(), body=new THREE.Group(); g.rotation.order='YXZ'; g.add(body);
  const mesh=(geo,mat,par)=>{ const m=new THREE.Mesh(geo,mat); m.castShadow=mat!==M.glass; m.receiveShadow=true; (par||body).add(m); return m; };
  mesh(G.outer,M.hull); mesh(G.inner,M.inner); mesh(G.top,M.white); for(const k of ['paint','dark','deck','white','chrome','metal','seat','glass']) if(G[k]) mesh(G[k],M[k]);
  const sw=new THREE.Group(); sw.position.set(0,0.88,0.58); sw.rotation.x=-0.75; body.add(sw); const swm=mesh(G.sw,M.dark,sw);
  const motor=new THREE.Group(); motor.position.set(0,0,2.06); body.add(motor); mesh(G.motor,M.motor,motor); const prop=new THREE.Group(); prop.position.set(0,-0.38,0.3); motor.add(prop); mesh(G.prop,M.metal,prop);
  return {g,body,sw:swm,motor,prop}; }
function newBoat(id,pi,x,z,yaw){ const m=makeBoatModel(pi), y=waterAt(x,z)-BDRAFT; scene.add(m.g);
  const k=Object.assign(m,{id,boat:true,x,y,z,yaw,pitch:0,roll:0,vx:0,vz:0,vy:0,steer:0,spinA:0,air:false,sq:0,sqV:0,lean:0,croll:0,wh:[0,0,0,0],seats:[null,null],driver:null,local:false,inp:null,tgt:null,
    hp:KART_HP,dead:0,home:{x,y,z,yaw},solid:{boxes:[],isKart:true,key:'boat'+id},settleT:0,puffT:0,flagT:0,wakeT:0,bobT:Math.random()*9});
  kartPose(k); return k; }
// how deep the water is under the hull (the shallowest of five points along and across it)
function boatDepth(x,z,yaw){ const fx=-Math.sin(yaw), fz=-Math.cos(yaw), rx=Math.cos(yaw), rz=-Math.sin(yaw); let m=1e9;
  for(const [a,b] of [[0,0],[1.9,0],[-1.9,0.7],[-1.9,-0.7],[0.6,0.8],[0.6,-0.8]]){ const x2=x+fx*a+rx*b, z2=z+fz*a+rz*b, w=waterAt(x2,z2); m=Math.min(m,w>-999?w-terrainH(x2,z2):-1); } return m; }
// moorings: by each town that has the sea or a river near it, and a few more along the coast; side-on to the shore
function initBoats(){ const spots=[], free=(x,z)=>spots.every(s=>Math.hypot(s[0]-x,s[1]-z)>60)&&karts.every(k=>Math.hypot(k.x-x,k.z-z)>12);
  const tryNear=(cx,cz,R0,R1)=>{ for(let R=R0;R<=R1;R+=6) for(let q=0,n=Math.max(8,Math.round(R/3));q<n;q++){ const a=q/n*Math.PI*2+R*0.37, x=cx+Math.cos(a)*R, z=cz+Math.sin(a)*R; if(waterDepth(x,z)<0.6||!free(x,z)) continue;
      // the nearest shore, within a few metres
      let sh=null; for(let r=2;r<=9&&!sh;r+=1) for(let k=0;k<12;k++){ const b=k/12*Math.PI*2, sx=x+Math.cos(b)*r, sz=z+Math.sin(b)*r; if(waterAt(sx,sz)<-999||waterDepth(sx,sz)<0.05){ sh=[sx,sz,r]; break; } }
      if(!sh||sh[2]<2.5) continue; const yaw=Math.atan2(-(sh[1]-z),(sh[0]-x)); // side-on: forward runs along the shore
      for(const yw of [yaw,yaw+Math.PI]) if(boatDepth(x,z,yw)>=BOAT_MIN+0.08){ return [x,z,yw]; } }
    return null; };
  for(const t of TOWNS){ const s=tryNear(t.x,t.z,t.R+10,t.R+220); if(s){ spots.push(s); } }
  const S=WGEN.sea&&WGEN.sea(); if(S) for(let n=0;n<4;n++){ const lat=(n-1.5)*220, x=SPAWN[0]+S.nx*S.C0+(-S.nz)*lat, z=SPAWN[2]+S.nz*S.C0+S.nx*lat; const s=tryNear(x,z,0,90); if(s) spots.push(s); }
  spots.forEach((s,i)=>karts.push(newBoat(karts.length,(i*3+2)%KART_PAINT.length,s[0],s[1],s[2]))); }
function simBoat(k,inp,dt){ const fx=-Math.sin(k.yaw), fz=-Math.cos(k.yaw), rx=Math.cos(k.yaw), rz=-Math.sin(k.yaw);
  let vf=k.vx*fx+k.vz*fz, vl=k.vx*rx+k.vz*rz; const dep=boatDepth(k.x,k.z,k.yaw), afloat=dep>=BOAT_MIN-0.05;
  if(afloat){
    if(inp.fw>0.1) vf+=BACC*inp.fw*dt*Math.max(0,Math.min(1,1.1-vf/BMAX))*(vf<-0.3?2.2:1);
    else if(inp.fw<-0.1){ if(vf>0.3) vf-=BACC*1.4*(-inp.fw)*dt; else vf=Math.max(-BREV,vf-BACC*0.6*(-inp.fw)*dt); }
    vf-=vf*((inp.fw>0.1?0.05:0.3)+0.006*Math.abs(vf))*dt;      // water drag: off the throttle it slows, but coasts a good way
    vl*=Math.exp(-(inp.hb?0.8:2.6)*dt);                                       // and slips sideways in a turn
    const sMax=0.62; k.steer+=(inp.st*sMax-k.steer)*Math.min(1,dt*4);
    k.yaw-=k.steer*1.25*Math.max(0.35,Math.min(1,(Math.abs(vf)+1.2)/6))*(vf<-0.2?-1:1)*dt; }
  else { vf*=Math.exp(-5*dt); vl*=Math.exp(-5*dt); k.steer*=Math.exp(-dt*3); } // aground: it grinds to a stop
  k.slip=Math.abs(vl); k.vf=vf; k.thr=inp.fw; k.brk=false;
  k.vx=fx*vf+rx*vl; k.vz=fz*vf+rz*vl;
  const sp0=Math.hypot(k.vx,k.vz), ox=k.x, oz=k.z, nx=ox+k.vx*dt, nz=oz+k.vz*dt;
  // it stays in water deep enough to float in (backing off a bank is always allowed)
  const okD=(x,z)=>{ const d=boatDepth(x,z,k.yaw); return d>=BOAT_MIN||d>dep+1e-4; };
  if(okD(nx,nz)&&!kartHits(k,nx,nz,k.yaw,ox,oz)){ k.x=nx; k.z=nz; }
  else if(okD(nx,oz)&&!kartHits(k,nx,oz,k.yaw,ox,oz)){ k.x=nx; k.vz*=0.3; }
  else if(okD(ox,nz)&&!kartHits(k,ox,nz,k.yaw,ox,oz)){ k.z=nz; k.vx*=0.3; }
  else { if(sp0>3){ sfxAt('kart_bump',_kz.set(k.x,k.y+0.3,k.z)); if(P.kart&&P.kart.k===k) shake=Math.max(shake,Math.min(0.2,sp0*0.02)); } k.vx*=-0.15; k.vz*=-0.15; }
  { const lost=sp0-Math.hypot(k.vx,k.vz); if(lost>6) kartDamage(k,(lost-6)*12); }
  { const dx=k.x-SPAWN[0], dz=k.z-SPAWN[2], d=Math.hypot(dx,dz); if(d>WORLD_EDGE){ k.x=SPAWN[0]+dx/d*WORLD_EDGE; k.z=SPAWN[2]+dz/d*WORLD_EDGE; k.vx*=0.3; k.vz*=0.3; } }
  boatFloat(k,dt,vf); kartRam(k,vf); }
// riding the water: a spring toward the surface (higher when planing), a gentle bob, the nose up at speed, a lean into turns
function boatFloat(k,dt,vf){ k.bobT+=dt; const w=waterAt(k.x,k.z), plane=Math.max(0,Math.min(1,(vf-4)/(BMAX-4)));
  const tgt=w>-999?w-BDRAFT+0.09*plane+0.035*Math.sin(k.bobT*1.6+k.x*0.21):terrainH(k.x,k.z)+0.28;
  k.vy+=(55*(tgt-k.y)-7*k.vy)*dt; k.y+=k.vy*dt; k.air=false;
  const pt=0.075*plane+0.02*Math.sin(k.bobT*1.15+k.z*0.17)-(k.thr>0.1&&vf<4?-0.035:0), rt=k.steer*Math.min(1,Math.abs(vf)/BMAX)*0.22+0.025*Math.sin(k.bobT*0.9);
  k.pitch+=(pt-k.pitch)*Math.min(1,dt*3); k.roll+=(rt-k.roll)*Math.min(1,dt*3); }
function settleBoat(k,dt){ k.vf=0; k.thr=0; k.slip=0; k.steer*=Math.exp(-dt*3);
  if(Math.hypot(k.vx,k.vz)>0.05){ const c=Math.exp(-dt*1.2); k.vx*=c; k.vz*=c; const nx=k.x+k.vx*dt, nz=k.z+k.vz*dt; if(boatDepth(nx,nz,k.yaw)>=BOAT_MIN&&!kartHits(k,nx,nz,k.yaw,k.x,k.z)){ k.x=nx; k.z=nz; } else { k.vx=k.vz=0; } } else { k.vx=k.vz=0; }
  boatFloat(k,dt,0); }
function boatModel(k,dt,dCam){ kartPose(k); k.g.visible=dCam<300; if(dCam>110) return;
  if(k.hp<KART_HP*0.5&&Math.random()<dt*(k.hp<KART_HP*0.25?14:6)){ const p=kartPoint(k,0,0.9,2.1,_ku); kartPuff(p,k.hp<KART_HP*0.25?0x2a2a2a:0x8f8f8f,new THREE.Vector3((Math.random()-.5)*0.4,1.2,(Math.random()-.5)*0.4),0.35,1.6); }
  const vf=k.vf||0; k.motor.rotation.y=k.steer*0.9; k.sw.rotation.z=k.steer*2.4; k.spinA+=(k.driver?(6+Math.abs(vf)*3)*(k.thr<-0.1?-1:1):0)*dt; k.prop.rotation.z=k.spinA;
  // the wake: foam thrown from the stern and spray at the bow when it's moving
  k.wakeT-=dt; const sp=Math.hypot(k.vx,k.vz); if(k.wakeT<=0&&dCam<80&&sp>1.2){ k.wakeT=sp>6?0.04:0.09; const w=waterAt(k.x,k.z); if(w>-999){
    for(const sx of [-0.7,0.7]){ const p=kartPoint(k,sx,0,2.2,_ku); p.y=w+0.05; kartPuff(p,0xf4f8fb,new THREE.Vector3(sx*0.9+(Math.random()-.5)*0.6,0.3+Math.random()*0.4,0).applyAxisAngle(_ZUP,k.yaw),0.32+sp*0.03,0.6+sp*0.05); }
    if(sp>5){ const p=kartPoint(k,(Math.random()<0.5?-1:1)*0.5,0,-1.9,_ku); p.y=w+0.1; kartPuff(p,0xffffff,new THREE.Vector3((Math.random()-.5)*2,0.8+Math.random(),0).applyAxisAngle(_ZUP,k.yaw),0.22,0.5); } } } }
const _ZUP=new THREE.Vector3(0,1,0);
// where a point on the buggy is in the world""")
