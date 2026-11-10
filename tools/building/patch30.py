# ---------- 30. garages and the dune buggy ----------
# --- garages: some houses get a one-car garage beside them, on the street side, with a driveway ---
rep("""      out.push({i0,j0,w,d,L,side,mat,roof,floors,id:t.houses.length+out.length,skin:{style,paint:Math.floor(rs()*HOUSE_PAINT[style].length),roof:Math.floor(rs()*4)}});
      s+=along+1; } }""","""      out.push({i0,j0,w,d,L,side,mat,roof,floors,id:t.houses.length+out.length,skin:{style,paint:Math.floor(rs()*HOUSE_PAINT[style].length),roof:Math.floor(rs()*4)}});
      { // a garage on the far side of some houses, its door facing the same street; now and then a dune buggy inside
        const H=out[out.length-1], gr=seeded(t.seed+7919*(k+3));
        if(gr()<0.42){ const X_=side==='n'||side==='s', gi=X_?i0+w:(side==='w'?i0:i0+w-1), gj=X_?(side==='n'?j0:j0+d-1):j0+d;
          let ok=inTown(gi,gj,1,1); for(let a=-1;a<=1&&ok;a++) for(let b=-1;b<=1&&ok;b++){ const ii=gi+a, jj=gj+b; if(ii>=i0&&ii<i0+w&&jj>=j0&&jj<j0+d) continue; if(used.has(key(ii,jj))) ok=false; }
          if(ok){ used.add(key(gi,gj)); H.garage={i:gi,j:gj,kart:gr()<0.45,paint:Math.floor(gr()*8)}; s+=1; } } }
      s+=along+1; } }""")
rep("function housePieces(h){","function housePieces0(h){")
rep("// where loot goes inside a house (floor height + a little)",r"""function housePieces(h){ const out=housePieces0(h); if(h.garage) out.push(...garagePieces(h)); return out; }
/* A garage: a concrete floor, two walls and a wide open door (the overhead door is rolled up under the roof), a flat
   roof with a little parapet, a workbench with a pegboard of tools on the back wall and a shelving unit on the side.
   Its pieces are ordinary map pieces like the house's: they farm, break and collapse. Local frame: u runs along the
   door from the house side, w runs back from the door. */
function garageFrame(h){ const G=h.garage, C=CELL, X=h.side==='n'||h.side==='s';
  if(X){ const fN=h.side==='n'; return {X,p:(u,w)=>[G.i*C+u,fN?G.j*C+w:(G.j+1)*C-w],yaw:fN?0:Math.PI}; }
  const fW=h.side==='w'; return {X,p:(u,w)=>[fW?G.i*C+w:(G.i+1)*C-w,G.j*C+u],yaw:fW?Math.PI/2:-Math.PI/2}; }
function garageParts(h,l,build){ const f=garageFrame(h), G=h.garage, y0=l*LVL, o=new THREE.Vector3((G.i+.5)*CELL,y0-FT/2,(G.j+.5)*CELL), parts={tread:[],beam:[],inner:[]}, boxes=[];
  const bx=(u0,u1,w0,w1,ya,yb)=>{ const a=f.p(u0,w0), b=f.p(u1,w1); return [Math.min(a[0],b[0]),y0+ya,Math.min(a[1],b[1]),Math.max(a[0],b[0]),y0+yb,Math.max(a[1],b[1])]; };
  const add=(k,b,solid)=>{ const g=new THREE.BoxGeometry(b[3]-b[0],b[4]-b[1],b[5]-b[2]); g.translate((b[0]+b[3])/2-o.x,(b[1]+b[4])/2-o.y,(b[2]+b[5])/2-o.z); parts[k].push(g); if(solid) boxes.push(b); };
  build(bx,add,boxes);
  const out=[]; for(const k in parts){ if(!parts[k].length) continue; const g=mergeGeos(parts[k]); g.computeBoundingSphere(); if(k==='inner') g.setAttribute('inside',new THREE.BufferAttribute(new Float32Array(g.attributes.position.count).fill(1),1)); out.push([g,k]); }
  return {boxes,parts:out}; }
function garageFix(h){ return garageParts(h,h.L,(bx,add,boxes)=>{
  // workbench along the back wall: hardwood top, a lower shelf, steel legs, a vise
  const W0=4.2, W1=4.84;
  add('tread',bx(0.7,3.0,W0,W1,0.86,0.93)); add('tread',bx(0.76,2.94,W0+0.05,W1-0.05,0.17,0.21));
  for(const u of [0.74,2.91]) for(const w of [W0+0.03,W1-0.09]) add('beam',bx(u,u+0.05,w,w+0.05,0,0.86));
  add('beam',bx(2.55,2.75,W0+0.06,W0+0.26,0.93,1.05)); add('beam',bx(2.6,2.7,W0-0.06,W0+0.06,0.97,1.0));
  boxes.push(bx(0.7,3.0,W0,W1,0,0.93));
  // pegboard with tools hanging on it
  add('tread',bx(0.8,2.9,4.83,4.87,1.08,1.9));
  for(const [u,h1,h2] of [[1.05,1.25,1.62],[1.3,1.3,1.58],[1.52,1.2,1.66],[1.78,1.35,1.6],[2.05,1.28,1.64],[2.35,1.22,1.55],[2.62,1.3,1.7]]) add('beam',bx(u,u+0.05,4.79,4.83,h1,h2));
  add('beam',bx(1.2,1.42,4.79,4.83,1.64,1.7)); add('beam',bx(2.2,2.5,4.79,4.83,1.58,1.63));
  // shelving unit on the side wall, with crates and cans on it
  for(const u of [4.42,4.82]) for(const w of [1.8,3.85]) add('beam',bx(u,u+0.04,w,w+0.04,0,1.95));
  for(const y of [0.25,0.75,1.25,1.75]) add('tread',bx(4.42,4.86,1.8,3.89,y,y+0.04));
  for(const [w0,w1,y,hh] of [[1.9,2.35,0.29,0.32],[2.45,2.8,0.29,0.26],[3.1,3.7,0.29,0.36],[1.95,2.2,0.79,0.22],[2.3,2.55,0.79,0.22],[2.9,3.6,0.79,0.3],[2.0,2.6,1.29,0.28],[3.2,3.5,1.29,0.2],[2.2,2.4,1.79,0.18],[2.7,3.3,1.79,0.24]]) add('inner',bx(4.46,4.82,w0,w1,y,y+hh));
  boxes.push(bx(4.4,4.87,1.78,3.9,0,1.95));
  // the overhead door, rolled up: five panels on two tracks just under the roof, hung from it
  for(let n=0;n<5;n++) add('beam',bx(0.28,4.72,0.24+n*0.5,0.71+n*0.5,2.76,2.8));
  for(const u of [0.16,4.8]){ add('beam',bx(u,u+0.04,0.14,2.95,2.72,2.84)); add('beam',bx(u,u+0.04,0.14,0.2,0,2.84)); add('beam',bx(u,u+0.03,2.9,2.93,2.84,3.86)); }
  add('beam',bx(2.3,2.7,2.3,2.7,3.82,3.88)); // a ceiling light
}); }
function garageRoofFix(h){ return garageParts(h,h.L+1,(bx,add)=>{ // a parapet round the three open edges of the flat roof
  add('beam',bx(0.13,4.87,0.0,0.14,0,0.3)); add('beam',bx(0.13,4.87,4.86,5.0,0,0.3)); add('beam',bx(4.86,5.0,0,5.0,0,0.3)); }); }
function garagePieces(h){ const G=h.garage, L=h.L, X=h.side==='n'||h.side==='s', out=[];
  out.push({type:'floor',i:G.i,j:G.j,l:L,mat:'wood',skin:Object.assign({},h.skin,{garage:1}),fix:garageFix(h)});
  out.push({type:'floor',i:G.i,j:G.j,l:L+1,mat:'wood',skin:Object.assign({},h.skin,{garage:2}),fix:garageRoofFix(h)});
  if(X){ const fN=h.side==='n';
    out.push({type:'wall',axis:'z',i:G.i,j:fN?G.j:G.j+1,l:L,mask:448,mat:h.mat,out:fN?-1:1});
    out.push({type:'wall',axis:'z',i:G.i,j:fN?G.j+1:G.j,l:L,mask:511,mat:h.mat,out:fN?1:-1});
    out.push({type:'wall',axis:'x',i:G.i+1,j:G.j,l:L,mask:511,mat:h.mat,out:1}); }
  else { const fW=h.side==='w';
    out.push({type:'wall',axis:'x',i:fW?G.i:G.i+1,j:G.j,l:L,mask:448,mat:h.mat,out:fW?-1:1});
    out.push({type:'wall',axis:'x',i:fW?G.i+1:G.i,j:G.j,l:L,mask:511,mat:h.mat,out:fW?1:-1});
    out.push({type:'wall',axis:'z',i:G.i,j:G.j+1,l:L,mask:511,mat:h.mat,out:1}); }
  return out.map(q=>Object.assign(q,{skin:q.skin||h.skin,key:q.type==='wall'?`w${q.axis}${q.i}_${q.j}_${q.l}`:`f${q.i}_${q.j}_${q.l}`,dir:0,axis:q.axis||'x'})); }
// where loot goes inside a house (floor height + a little)""")
# concrete garage floor, a dark roofing membrane on the garage roof
rep("    floor:houseMat('floor',","    floor:s.garage?garageFloorMat(s.garage):houseMat('floor',")
rep("const wallKind=mask=>","const wallKind=mask=>mask===448?'garage':")
rep("const houseMatCache=new Map();",r"""const houseMatCache=new Map();
function garageFloorMat(kind){ return houseMat('gfloor'+kind,()=>{ const N=256, c=document.createElement('canvas'); c.width=c.height=N; const g=c.getContext('2d');
    g.fillStyle=kind===1?'#a9a59c':'#55575b'; g.fillRect(0,0,N,N);
    for(let i=0;i<5000;i++){ const v=Math.random(); g.fillStyle=v<.5?'rgba(40,38,34,.18)':'rgba(255,255,250,.14)'; g.fillRect(Math.random()*N,Math.random()*N,1+Math.random()*1.6,1+Math.random()*1.6); }
    if(kind===1){ const gr=g.createRadialGradient(N*0.55,N*0.5,4,N*0.55,N*0.5,N*0.24); gr.addColorStop(0,'rgba(30,26,22,.42)'); gr.addColorStop(0.6,'rgba(30,26,22,.16)'); gr.addColorStop(1,'rgba(0,0,0,0)'); g.fillStyle=gr; g.fillRect(0,0,N,N); // an oil stain
      g.fillStyle='rgba(60,56,50,.5)'; g.fillRect(N/2-1,0,2,N); g.fillRect(0,N/2-1,N,2); } // control joints
    const t=new THREE.CanvasTexture(c); t.wrapS=t.wrapT=THREE.RepeatWrapping; t.anisotropy=Math.min(8,renderer.capabilities.getMaxAnisotropy());
    return new THREE.MeshPhongMaterial({map:t,shininess:kind===1?14:4,specular:0x1a1a1a,polygonOffset:true,polygonOffsetFactor:1,polygonOffsetUnits:1}); },'HOUSE_CEIL'); }""")
rep("""    if(kind==='door'){ const c=style==='panel'?12:20;""","""    if(kind==='garage'){ const c=style==='panel'?12:22; // a header over the wide garage door, with a lamp each side
      trimRect(g,hg,mg,0,a-c,S,c,white,trimH); if(style!=='panel') trimRect(g,hg,mg,0,a-c-12,S,12,white,225);
      for(const lx of [S*0.07,S*0.93-16]){ const ly=a-c-62; trimRect(g,hg,mg,lx,ly,16,26,'#2b2b2b',215); g.fillStyle='#ffe7a3'; g.fillRect(lx+4,ly+5,8,14); mg.fillStyle='#000'; mg.fillRect(lx+4,ly+5,8,14); } }
    if(kind==='door'){ const c=style==='panel'?12:20;""")
# a concrete driveway from each garage door out to the street
rep("  const quad=(a,b,y,v0)=>{ const dx=b[0]-a[0], dz=b[1]-a[1], L=Math.hypot(dx,dz); if(L<0.05) return v0; const sx=-dz/L*WALK_W/2, sz=dx/L*WALK_W/2,",
    "  const quad=(a,b,y,v0,ww=WALK_W)=>{ const dx=b[0]-a[0], dz=b[1]-a[1], L=Math.hypot(dx,dz); if(L<0.05) return v0; const sx=-dz/L*ww/2, sz=dx/L*ww/2,")
rep("for(let s=0;s<=L;s+=1) for(const off of [-0.8,0,0.8]){","for(let s=0;s<=L;s+=1) for(const off of ww>2?[-1.6,-0.8,0,0.8,1.6]:[-0.8,0,0.8]){")
rep("      const b=X?[a[0],t.z+edge]:[t.x+edge,a[1]]; quad(a,b,y+0.002,0); SIDEWALKS.push([a,b]); } }",
    """      const b=X?[a[0],t.z+edge]:[t.x+edge,a[1]]; quad(a,b,y+0.002,0); SIDEWALKS.push([a,b]); }
    for(const h of t.houses){ if(!h.garage) continue; const f=garageFrame(h), m=f.p(2.5,0.02), X=f.X, across=X?m[1]-t.z:m[0]-t.x, edge=Math.sign(across)*(ROAD_HW+0.05);
      const a=[m[0],m[1]], b=X?[m[0],t.z+edge]:[t.x+edge,m[1]]; quad(a,b,y+0.004,0,3.4); SIDEWALKS.push([a,b]); } }""")

# --- the dune buggy ---
rep("/* ---------- targeting ---------- */",r"""/* ---------- the dune buggy ----------
   A small two-seat buggy, found in some garages. Walk up to it and press Interact to drive (left seat) or ride
   (right seat); Interact again gets you out. W/S drive and brake (and reverse), A/D steer, Jump is the handbrake (it
   lets the back slide out). It does about 63 km/h on asphalt and a bit less on grass, and it pulls up hills well. It climbs kerbs
   and ramps, flies off jumps, and stops dead on walls and trees. The driver can't fight; the passenger can shoot.
   The driver's game runs the buggy and sends where it is with their state; everyone else follows it smoothly. */
var karts=null;
const KART_PAINT=[0xe8521e,0x2f9e44,0xd62828,0x1f6fd1,0xf2c014,0xc9a66b,0x1fa2a0,0x8b3fd1], KWR=0.34, KWB=1.78, KTRACK=1.46;
const KART_SEATS=[[-0.32,0.68,0.12],[0.32,0.68,0.12]], KART_WHEELS=[[-0.73,-0.92,1],[0.73,-0.92,1],[-0.75,0.86,0],[0.75,0.86,0]];
const KMAX=17.5, KMAX_OFF=15.5, KREV=6, KACC=10, KBRK=17;
const ME=()=>net.role?net.id:'me';
let kartGeo=null; const kartMats={};
function kMat(k,make){ return kartMats[k]||(kartMats[k]=make()); }
function tubeGeo(a,b,r){ const v=new THREE.Vector3().subVectors(b,a), len=v.length(), g=new THREE.CylinderGeometry(r,r,len,8,1);
  g.applyMatrix4(new THREE.Matrix4().makeRotationFromQuaternion(new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0,1,0),v.normalize()))); g.translate((a.x+b.x)/2,(a.y+b.y)/2,(a.z+b.z)/2); return g; }
// the shapes are built once and shared by every buggy; only the paint (and its number) differ
function buildKartGeo(){ const bins={}, V=(x,y,z)=>new THREE.Vector3(x,y,z);
  const put=(slot,geo,x=0,y=0,z=0,rx=0,ry=0,rz=0)=>{ const q=geo.clone(); q.applyMatrix4(new THREE.Matrix4().compose(V(x,y,z),new THREE.Quaternion().setFromEuler(new THREE.Euler(rx,ry,rz)),V(1,1,1))); (bins[slot]||(bins[slot]=[])).push(q); };
  const tube=(slot,a,b,r=0.032)=>(bins[slot]||(bins[slot]=[])).push(tubeGeo(a,b,r));
  const cyl=(r,h,n=14)=>new THREE.CylinderGeometry(r,r,h,n);
  // chassis: floor pan, skid plate, side pods, nose and dash
  put('dark',rbox(1.26,0.07,2.1,0.03),0,0.33,0.05); put('metal',rbox(1.0,0.05,0.52,0.02),0,0.37,-1.12,0.34);
  for(const sx of [-1,1]){ put('paint',rbox(0.2,0.25,1.26,0.08),sx*0.6,0.47,-0.1); put('white',rbox(0.205,0.05,1.0,0.02),sx*0.6,0.56,-0.12); }
  put('paint',rbox(1.02,0.13,0.82,0.06),0,0.66,-0.93,-0.24); put('white',rbox(0.22,0.135,0.83,0.05),0,0.665,-0.93,-0.24);
  put('paint',rbox(1.02,0.27,0.11,0.05),0,0.5,-1.3); put('dark',rbox(0.6,0.12,0.04,0.02),0,0.47,-1.36);
  put('dark',rbox(1.06,0.17,0.15,0.05),0,0.77,-0.56);
  // seats: buckets with coloured bolsters and harness straps
  for(const sx of [-0.32,0.32]){ put('seat',rbox(0.46,0.1,0.48,0.05),sx,0.52,0.1); put('seat',rbox(0.46,0.64,0.1,0.05),sx,0.86,0.38,0.2);
    for(const bx of [-0.21,0.21]){ put('seatA',rbox(0.07,0.5,0.1,0.03),sx+bx,0.88,0.33,0.2); put('seatA',rbox(0.07,0.09,0.42,0.03),sx+bx,0.6,0.1); }
    put('seat',rbox(0.24,0.16,0.1,0.04),sx,1.24,0.45,0.2); for(const hx of [-0.09,0.09]) put('seatA',rbox(0.05,0.5,0.015,0.006),sx+hx,0.88,0.32,0.2); }
  tube('dark',V(-0.32,0.62,-0.62),V(-0.32,0.86,-0.37),0.025);
  // roll cage
  const C='cage';
  for(const sx of [-1,1]){ tube(C,V(sx*0.63,0.44,0.42),V(sx*0.55,1.46,0.42)); tube(C,V(sx*0.55,1.46,0.42),V(sx*0.52,1.41,-0.3)); tube(C,V(sx*0.52,1.41,-0.3),V(sx*0.6,0.73,-0.72));
    tube(C,V(sx*0.66,0.42,-0.78),V(sx*0.66,0.42,0.8)); tube(C,V(sx*0.63,0.73,-0.72),V(sx*0.62,0.73,0.42)); tube(C,V(sx*0.55,1.46,0.42),V(sx*0.45,0.56,1.06)); tube(C,V(sx*0.6,0.73,-0.72),V(sx*0.66,0.42,-0.78)); }
  tube(C,V(-0.55,1.46,0.42),V(0.55,1.46,0.42)); tube(C,V(-0.52,1.41,-0.3),V(0.52,1.41,-0.3)); tube(C,V(-0.6,0.73,-0.72),V(0.6,0.73,-0.72));
  tube(C,V(-0.45,0.56,1.06),V(0.45,0.56,1.06)); tube(C,V(-0.6,0.6,0.42),V(0.55,1.43,0.42)); tube(C,V(0,1.46,0.42),V(0,1.41,-0.3),0.028);
  tube('cage',V(-0.56,0.44,-1.4),V(0.56,0.44,-1.4),0.04); for(const sx of [-1,1]){ tube(C,V(sx*0.56,0.44,-1.4),V(sx*0.5,0.5,-1.26),0.035); tube(C,V(sx*0.3,0.44,-1.4),V(sx*0.26,0.7,-1.3),0.03); }
  tube(C,V(-0.26,0.7,-1.3),V(0.26,0.7,-1.3),0.03); tube(C,V(-0.5,0.42,1.2),V(0.5,0.42,1.2),0.035); for(const sx of [-1,1]) tube(C,V(sx*0.5,0.42,1.2),V(sx*0.45,0.56,1.06),0.03);
  // lights: a bar on the roof, two round headlamps, two tail lamps
  put('dark',rbox(0.9,0.09,0.1,0.03),0,1.52,-0.3); for(const x of [-0.33,-0.11,0.11,0.33]) put('lamp',cyl(0.036,0.03,10),x,1.52,-0.36,Math.PI/2);
  for(const sx of [-1,1]){ put('dark',cyl(0.075,0.07,14),sx*0.36,0.6,-1.34,Math.PI/2); put('lamp',cyl(0.056,0.02,14),sx*0.36,0.6,-1.38,Math.PI/2); put('tail',rbox(0.1,0.06,0.03,0.01),sx*0.42,0.6,1.08); }
  // engine at the back: block with fins, air filter, exhaust; a spare wheel on the rack above it
  put('dark',rbox(0.56,0.32,0.42,0.05),0,0.58,0.82); for(let n=0;n<5;n++) put('metal',rbox(0.5,0.02,0.3,0.005),0,0.76+n*0.035,0.82);
  put('chrome',cyl(0.1,0.15,14),0.22,0.9,0.8); put('chrome',cyl(0.04,0.1,10),0.22,0.98,0.8);
  tube('chrome',V(-0.2,0.55,0.95),V(-0.3,0.6,1.14),0.034); tube('chrome',V(-0.3,0.6,1.14),V(-0.33,0.8,1.26),0.034); put('dark',cyl(0.042,0.06,10),-0.335,0.84,1.28,-0.35);
  put('rub',cyl(0.3,0.17,20),0,1.0,0.76); put('metal',cyl(0.18,0.18,16),0,1.0,0.76); put('dark',rbox(0.66,0.03,0.05,0.01),0,1.09,0.76);
  for(const sx of [-1,1]) tube('cage',V(sx*0.42,0.88,0.6),V(sx*0.42,0.88,1.0),0.025);
  // suspension: arms out to every wheel and yellow coil-overs
  for(const [wx,wz,front] of KART_WHEELS){ const sx=Math.sign(wx);
    tube('metal',V(sx*0.32,0.38,wz-0.12),V(sx*0.62,0.34,wz),0.022); tube('metal',V(sx*0.32,0.38,wz+0.12),V(sx*0.62,0.34,wz),0.022); tube('metal',V(sx*0.34,0.54,wz),V(sx*0.6,0.46,wz),0.02);
    tube('spring',V(sx*0.6,0.4,wz),V(sx*0.46,0.78,wz+(front?0.08:-0.08)),0.045); tube('chrome',V(sx*0.6,0.4,wz),V(sx*0.46,0.82,wz+(front?0.08:-0.08)),0.018); }
  const geo={}; for(const k in bins){ geo[k]=mergeGeos(bins[k]); geo[k].computeBoundingSphere(); }
  // a chunky knobbly tyre (open tread band, sidewalls, lugs) round a dished five-spoke rim
  const side=(g,sx)=>g.rotateY(sx*Math.PI/2).translate(sx*0.14,0,0);
  const tyre=[new THREE.CylinderGeometry(KWR,KWR,0.28,24,1,true).rotateZ(Math.PI/2),side(new THREE.RingGeometry(0.19,KWR,24),1),side(new THREE.RingGeometry(0.19,KWR,24),-1)];
  for(let n=0;n<20;n++){ const lug=new THREE.BoxGeometry(0.12,0.05,0.09); lug.translate(n%2?0.06:-0.06,KWR+0.012,0); lug.rotateX(n/20*Math.PI*2); tyre.push(lug); }
  geo.tyre=mergeGeos(tyre);
  const rim=[side(new THREE.CircleGeometry(0.19,16),1).translate(-0.02,0,0),side(new THREE.CircleGeometry(0.19,16),-1).translate(0.02,0,0)];
  for(const sx of [-1,1]) for(let n=0;n<5;n++){ const sp=new THREE.BoxGeometry(0.03,0.15,0.045); sp.translate(sx*0.125,0.1,0); sp.rotateX(n/5*Math.PI*2+sx*0.3); rim.push(sp); }
  geo.rim=mergeGeos(rim); geo.hub=mergeGeos([cyl(0.06,0.3,10).rotateZ(Math.PI/2),...[0,1,2,3,4].map(n=>cyl(0.014,0.31,6).rotateZ(Math.PI/2).translate(0,Math.cos(n*1.2566)*0.085,Math.sin(n*1.2566)*0.085))]);
  // steering wheel, flag pole and its pennant
  geo.sw=mergeGeos([new THREE.TorusGeometry(0.15,0.022,8,20),new THREE.BoxGeometry(0.3,0.03,0.02),new THREE.BoxGeometry(0.03,0.15,0.02).translate(0,-0.075,0),new THREE.CylinderGeometry(0.04,0.04,0.05,10).rotateX(Math.PI/2)]);
  geo.pole=tubeGeo(V(0,0,0),V(0,1.55,0.05),0.01);
  const fl=new THREE.BufferGeometry(); fl.setAttribute('position',new THREE.Float32BufferAttribute([0,0,0, 0,-0.24,0, 0,-0.11,0.36],3)); fl.setAttribute('normal',new THREE.Float32BufferAttribute([1,0,0,1,0,0,1,0,0],3)); fl.setAttribute('uv',new THREE.Float32BufferAttribute([0,0,0,1,1,.5],2)); geo.flag=fl;
  return geo; }
function kartNumberMat(n){ return kMat('num'+n,()=>{ const c=document.createElement('canvas'); c.width=128; c.height=80; const g=c.getContext('2d');
  g.fillStyle='#f4f1ea'; g.beginPath(); g.ellipse(64,40,58,36,0,0,Math.PI*2); g.fill(); g.lineWidth=5; g.strokeStyle='#1d1f24'; g.stroke();
  g.fillStyle='#1d1f24'; g.font='900 italic 50px Arial, sans-serif'; g.textAlign='center'; g.textBaseline='middle'; g.fillText(String(n),64,43);
  const t=new THREE.CanvasTexture(c); return new THREE.MeshLambertMaterial({map:t,transparent:true}); }); }
function makeKartModel(pi,num){ if(!kartGeo) kartGeo=buildKartGeo(); const G=kartGeo, paint=KART_PAINT[pi%KART_PAINT.length];
  const M={paint:kMat('p'+pi,()=>new THREE.MeshPhongMaterial({color:paint,shininess:90,specular:0x5a5a5a})),seatA:kMat('sa'+pi,()=>new THREE.MeshLambertMaterial({color:new THREE.Color(paint).multiplyScalar(0.85)})),
    white:kMat('white',()=>new THREE.MeshPhongMaterial({color:0xf1efe9,shininess:60})),dark:kMat('dark',()=>new THREE.MeshPhongMaterial({color:0x1e2025,shininess:40,specular:0x333333})),
    cage:kMat('cage',()=>new THREE.MeshPhongMaterial({color:0x26282d,shininess:80,specular:0x5c5c5c})),metal:kMat('metal',()=>new THREE.MeshPhongMaterial({color:0x8d939b,shininess:60,specular:0x777777})),
    chrome:kMat('chrome',()=>new THREE.MeshPhongMaterial({color:0xd8dde2,shininess:120,specular:0xffffff})),seat:kMat('seat',()=>new THREE.MeshLambertMaterial({color:0x27282d})),
    rub:kMat('rub',()=>new THREE.MeshLambertMaterial({color:0x1c1c1e})),lamp:kMat('lamp',()=>new THREE.MeshPhongMaterial({color:0xfff6d8,emissive:0xfff0c0,emissiveIntensity:0.85})),
    tail:kMat('tail',()=>new THREE.MeshPhongMaterial({color:0xd01818,emissive:0x8a0000})),spring:kMat('spring',()=>new THREE.MeshPhongMaterial({color:0xf2c014,shininess:70,specular:0x777777}))};
  const g=new THREE.Group(), body=new THREE.Group(); g.rotation.order='YXZ'; g.add(body);
  const mesh=(geo,mat,par)=>{ const m=new THREE.Mesh(geo,mat); m.castShadow=true; m.receiveShadow=true; (par||body).add(m); return m; };
  for(const k of ['paint','white','dark','cage','metal','chrome','seat','seatA','rub','lamp','tail','spring']) if(G[k]) mesh(G[k],M[k]);
  for(const sx of [-1,1]){ const d=mesh(new THREE.PlaneGeometry(0.4,0.25),kartNumberMat(num)); d.position.set(sx*0.712,0.46,-0.12); d.rotation.y=sx*Math.PI/2; d.castShadow=false; }
  const sw=new THREE.Group(); sw.position.set(-0.32,0.88,-0.35); sw.rotation.x=-0.8; body.add(sw); const swm=mesh(G.sw,M.dark,sw);
  const wheels=KART_WHEELS.map(([x,z,front])=>{ const p=new THREE.Group(); p.position.set(x,KWR,z); g.add(p); const spin=new THREE.Group(); p.add(spin);
    mesh(G.tyre,M.rub,spin); mesh(G.rim,M.metal,spin); mesh(G.hub,M.chrome,spin); return {p,spin,front,x,z}; });
  const flagG=new THREE.Group(); flagG.position.set(0.47,0.6,1.08); body.add(flagG); mesh(G.pole,M.dark,flagG);
  const flag=new THREE.Mesh(G.flag,kMat('flag',()=>new THREE.MeshLambertMaterial({color:0xff6a1a,side:THREE.DoubleSide}))); flag.position.set(0,1.55,0.05); flagG.add(flag);
  return {g,body,wheels,sw:swm,flag}; }
function newKart(id,pi,x,y,z,yaw){ const m=makeKartModel(pi,[7,11,23,3,42,8,15,99,5,61,17,33][id%12]); scene.add(m.g);
  const k=Object.assign(m,{id,x,y,z,yaw,pitch:0,roll:0,vx:0,vz:0,vy:0,gvy:0,steer:0,spinA:0,air:false,sq:0,sqV:0,lean:0,croll:0,wh:[0,0,0,0],seats:[null,null],driver:null,local:false,inp:null,tgt:null,
    home:{x,y,z,yaw},solid:{boxes:[],isKart:true,key:'kart'+id},settleT:Math.random()*0.3,puffT:0,flagT:Math.random()*9});
  kartPose(k); return k; }
function initKarts(){ karts=[]; for(const t of TOWNS){ let n=0; for(const h of t.houses){ const G=h.garage; if(!G||!G.kart||n>=2) continue; n++; const f=garageFrame(h), c=f.p(2.5,2.25); karts.push(newKart(karts.length,G.paint,c[0],h.L*LVL,c[1],f.yaw)); } } }
// where a point on the buggy is in the world
const _kv=new THREE.Vector3(), _ku=new THREE.Vector3(), _kz=new THREE.Vector3();
function kartPoint(k,x,y,z,out){ return (out||_kv).set(x,y,z).applyEuler(k.g.rotation).add(k.g.position); }
function kartPose(k){ k.g.position.set(k.x,k.y,k.z); k.g.rotation.set(k.pitch,k.yaw,k.roll); k.g.updateMatrixWorld(true);
  const fx=-Math.sin(k.yaw), fz=-Math.cos(k.yaw); k.solid.boxes=[-0.8,0,0.8].map(a=>{ const cx=k.x-fx*a, cz=k.z-fz*a; return [cx-0.6,k.y+0.3,cz-0.6,cx+0.6,k.y+1.45,cz+0.6]; }); }
// does the buggy's body (three circles along it) run into anything new at (x,z)?
function kartHits(k,x,z,yaw,ox,oz){ const fx=-Math.sin(yaw), fz=-Math.cos(yaw), lo=k.y+0.45, hi=k.y+1.4, ps=near(x,z,1); propsNear(x,z,ps);
  for(const o of karts) if(o!==k&&Math.abs(o.x-x)<4&&Math.abs(o.z-z)<4) ps.add(o.solid);
  const hit=(cx,cz)=>{ for(const p of ps){ for(const b of p.boxes) if(b[4]>lo&&b[1]<hi&&circBox(b,cx,cz,0.7)) return b; if(p.slab) for(const s of [[0,0],[0.5,0],[-0.5,0],[0,0.5],[0,-0.5]]){ const t=slabTop(p,cx+s[0],cz+s[1]); if(t!==null&&t>lo&&t-ST<hi) return p; } } return null; };
  for(const a of [-0.85,0,0.85]){ const b=hit(x-fx*a,z-fz*a); if(b&&b!==hit(ox-fx*a,oz-fz*a)) return true; } return false; }
function kartGround(k,ps){ const out=k.wh; let i=0; for(const [wx,wz] of KART_WHEELS){ const p=kartPoint(k,wx,0,wz); out[i++]=groundAt(p.x,p.z,k.y+0.55,ps)[0]; } return out; }
function simKart(k,inp,dt){ const fx=-Math.sin(k.yaw), fz=-Math.cos(k.yaw), rx=Math.cos(k.yaw), rz=-Math.sin(k.yaw);
  let vf=k.vx*fx+k.vz*fz, vl=k.vx*rx+k.vz*rz; const ground=!k.air, paved=roadDistAt(k.x,k.z)<ROAD_HW+0.6||!!townAt(k.x,k.z,0), vmax=paved?KMAX:KMAX_OFF;
  if(ground){
    if(inp.fw>0.1){ if(vf<-0.3) vf+=KBRK*inp.fw*dt; else vf+=KACC*inp.fw*dt*Math.max(0.12,1-vf/vmax); }
    else if(inp.fw<-0.1){ if(vf>0.3) vf-=KBRK*(-inp.fw)*dt; else vf=Math.max(-KREV,vf-KACC*0.7*(-inp.fw)*dt); }
    else { const c=(1.3+0.06*Math.abs(vf))*dt; vf=Math.abs(vf)<=c?0:vf-Math.sign(vf)*c; }
    if(vf>vmax) vf-=Math.min(vf-vmax,5*dt);
    vf-=GRAV*Math.sin(k.pitch)*dt*(Math.sin(k.pitch)>0&&inp.fw>0.1?0.28:0.6); // big tyres and low gearing: it pulls up hills well, and rolls back down them
    if(inp.hb){ const c=KBRK*0.5*dt; vf=Math.abs(vf)<=c?0:vf-Math.sign(vf)*c; }
    vl*=Math.exp(-(inp.hb?1.4:9)*dt); }
  k.slip=Math.abs(vl); k.vf=vf; k.thr=inp.fw; k.brk=(inp.fw<-0.1&&vf>0.5)||inp.hb;
  k.vx=fx*vf+rx*vl; k.vz=fz*vf+rz*vl; // velocity stays in the old heading: turning hard (or the handbrake) lets it slide
  const sMax=0.56-0.26*Math.min(1,Math.abs(vf)/KMAX); k.steer+=(inp.st*sMax-k.steer)*Math.min(1,dt*7);
  if(ground) k.yaw-=vf*Math.tan(k.steer)/KWB*(inp.hb?1.35:1)*dt;
  // move, sliding along walls; a hard hit stops it with a bump
  const ox=k.x, oz=k.z, nx=ox+k.vx*dt, nz=oz+k.vz*dt;
  if(!kartHits(k,nx,nz,k.yaw,ox,oz)){ k.x=nx; k.z=nz; }
  else if(!kartHits(k,nx,oz,k.yaw,ox,oz)){ k.x=nx; k.vz*=0.3; }
  else if(!kartHits(k,ox,nz,k.yaw,ox,oz)){ k.z=nz; k.vx*=0.3; }
  else { const sp=Math.hypot(k.vx,k.vz); if(sp>4){ sfxAt('kart_bump',_kz.set(k.x,k.y+0.5,k.z)); if(P.kart&&P.kart.k===k) shake=Math.max(shake,Math.min(0.25,sp*0.02)); k.sqV-=sp*0.15; } k.vx*=-0.2; k.vz*=-0.2; }
  { const dx=k.x-SPAWN[0], dz=k.z-SPAWN[2], d=Math.hypot(dx,dz); if(d>MAP_R-2){ k.x=SPAWN[0]+dx/d*(MAP_R-2); k.z=SPAWN[2]+dz/d*(MAP_R-2); k.vx*=0.3; k.vz*=0.3; } }
  // ground under each wheel: height, nose and side tilt; off a ramp it flies
  k.g.position.set(k.x,k.y,k.z); k.g.rotation.set(k.pitch,k.yaw,k.roll);
  const ps=near(k.x,k.z,1), w=kartGround(k,ps), gC=(w[0]+w[1]+w[2]+w[3])/4;
  if(k.air){ k.vy-=GRAV*dt; k.y+=k.vy*dt; k.pitch+=(Math.max(-0.4,Math.min(0.35,k.vy*0.025))-k.pitch)*Math.min(1,dt*1.5); k.roll*=Math.exp(-dt*2);
    if(k.y<=gC){ if(k.vy<-4){ sfxAt('kart_land',_kz.set(k.x,k.y,k.z)); k.sqV+=k.vy*0.25; if(P.kart&&P.kart.k===k){ shake=Math.max(shake,Math.min(0.3,-k.vy*0.025)); camDip=Math.min(camDip,-0.12); } } k.y=gC; k.vy=0; k.air=false; } }
  else if(gC<k.y-0.35){ k.air=true; k.vy=Math.max(-12,Math.min(12,k.gvy)); }
  else { k.gvy=(gC-k.y)/dt; k.y=gC;
    const pt=Math.atan2((w[0]+w[1]-w[2]-w[3])/2,KWB), rt=Math.atan2((w[1]+w[3]-w[0]-w[2])/2,KTRACK);
    k.pitch+=(pt-k.pitch)*Math.min(1,dt*12); k.roll+=(rt-k.roll)*Math.min(1,dt*12); }
  // body sway: squat under power, dive under braking, lean out in corners, bob on the springs
  k.lean+=((-(inp.fw>0.1?0.035:0)+(k.brk?0.05:0))-k.lean)*Math.min(1,dt*6); k.croll+=((vf*k.steer*0.012)-k.croll)*Math.min(1,dt*6);
  // ram the zombies
  if(horde.on&&Math.abs(vf)>4){ const now=performance.now(); horde.zs.forEach(z=>{ if(!z.alive||(z.kartT||0)>now) return; const dx=z.pos.x-k.x, dz=z.pos.z-k.z; if(dx*dx+dz*dz>(1.4+0.4*z.sc)**2||Math.abs(z.pos.y-k.y)>2) return;
    z.kartT=now+700; const dmg=Math.round(10+Math.abs(vf)*2.4); if(net.role==='client') netSend({type:'zhit',id:net.id,z:z.id,dmg}); else zombieHurt(z,dmg,net.id);
    dmgNum(z.pos.clone().setY(z.pos.y+1.6*z.sc),dmg,'hp'); sfxAt('kart_hit',z.pos); k.vx*=0.6; k.vz*=0.6; k.sqV-=1.2; burst(z.pos.clone().setY(z.pos.y+1),6,4,0.08,goreMat); }); } }
// everyone else's view of a buggy someone else is driving: glide to where they say it is (a little ahead, by its speed)
function interpKart(k,dt){ const T=k.tgt, age=Math.min(0.25,(performance.now()-T.t)/1000), tx=T.x+T.vx*age, tz=T.z+T.vz*age, f=Math.min(1,dt*12);
  if(Math.hypot(tx-k.x,tz-k.z)>8){ k.x=tx; k.z=tz; k.y=T.y; } else { k.x+=(tx-k.x)*f; k.z+=(tz-k.z)*f; k.y+=(T.y-k.y)*f; }
  k.yaw+=angDiff(T.yaw,k.yaw)*f; k.pitch+=(T.pitch-k.pitch)*f; k.roll+=(T.roll-k.roll)*f; k.steer+=(T.steer-k.steer)*f; k.vx=T.vx; k.vz=T.vz; k.vf=T.vx*-Math.sin(k.yaw)+T.vz*-Math.cos(k.yaw); k.slip=0; k.thr=T.thr||0; }
// a parked buggy settles onto whatever is under it (and drops if that goes away)
function settleKart(k,dt){ k.vf=0; k.thr=0; k.slip=0; k.steer*=Math.exp(-dt*3);
  if(Math.hypot(k.vx,k.vz)>0.05){ const c=Math.exp(-dt*3); k.vx*=c; k.vz*=c; const nx=k.x+k.vx*dt, nz=k.z+k.vz*dt; if(!kartHits(k,nx,nz,k.yaw,k.x,k.z)){ k.x=nx; k.z=nz; } else { k.vx=k.vz=0; } } else { k.vx=k.vz=0; }
  k.settleT-=dt; if(k.settleT>0&&!k.air) return; k.settleT=0.3;
  const w=kartGround(k,near(k.x,k.z,1)), gC=(w[0]+w[1]+w[2]+w[3])/4;
  if(k.y>gC+0.02){ k.air=true; k.vy-=GRAV*Math.max(dt,0.016); k.y=Math.max(gC,k.y+k.vy*Math.max(dt,0.016)); if(k.y<=gC){ if(k.vy<-5) sfxAt('kart_land',_kz.set(k.x,k.y,k.z)); k.vy=0; k.air=false; } k.settleT=0; }
  else { k.y=gC; k.air=false; k.vy=0; k.pitch=Math.atan2((w[0]+w[1]-w[2]-w[3])/2,KWB); k.roll=Math.atan2((w[1]+w[3]-w[0]-w[2])/2,KTRACK); } }
const kartPuffs=[]; let puffGeo=null;
function kartPuff(pos,col,vel,size,life){ if(!puffGeo) puffGeo=new THREE.IcosahedronGeometry(0.22,0); let p=kartPuffs.find(q=>!q.m.visible);
  if(!p){ if(kartPuffs.length>=60) return; p={m:new THREE.Mesh(puffGeo,new THREE.MeshLambertMaterial({transparent:true,depthWrite:false}))}; scene.add(p.m); kartPuffs.push(p); }
  p.m.visible=true; p.m.position.copy(pos); p.m.material.color.setHex(col); p.v=vel.clone(); p.t=0; p.life=life; p.size=size; p.m.scale.setScalar(size); p.m.rotation.set(Math.random()*3,Math.random()*3,0); }
function stepPuffs(dt){ for(const p of kartPuffs){ if(!p.m.visible) continue; p.t+=dt; if(p.t>=p.life){ p.m.visible=false; continue; } const f=p.t/p.life;
  p.m.position.addScaledVector(p.v,dt); p.v.multiplyScalar(Math.exp(-dt*2)); p.v.y+=dt*0.4; p.m.scale.setScalar(p.size*(1+2.2*f)); p.m.material.opacity=0.42*(1-f)*(1-f); } }
function kartModel(k,dt,dCam){ kartPose(k); k.g.visible=dCam<240; if(dCam>90) return;
  k.sqV+=(-140*k.sq-12*k.sqV)*dt; k.sq=Math.max(-0.08,Math.min(0.06,k.sq+k.sqV*dt));
  k.body.position.y=k.sq; k.body.rotation.x=k.lean; k.body.rotation.z=k.croll;
  const vf=k.vf||0; k.spinA+=vf/KWR*dt;
  // each wheel follows the ground under it on its spring
  const ps=dCam<40&&!k.air?near(k.x,k.z,1):null; if(ps) kartGround(k,ps);
  k.wheels.forEach((w,i)=>{ w.spin.rotation.x=-k.spinA; if(w.front) w.p.rotation.y=-k.steer;
    let off=0; if(ps){ const p=kartPoint(k,w.x,0,w.z,_ku); off=Math.max(-0.1,Math.min(0.1,k.wh[i]-p.y)); } w.p.position.y+=((KWR+off)-w.p.position.y)*Math.min(1,dt*20); });
  k.sw.rotation.z=k.steer*2.4;
  k.flagT+=dt*(6+Math.abs(vf)*0.8); k.flag.rotation.y=Math.sin(k.flagT)*(0.35-Math.min(0.25,Math.abs(vf)*0.02))+Math.sin(k.flagT*2.3)*0.12;
  // dust off the back wheels on grass and dirt, exhaust puffs from the pipe
  k.puffT-=dt; if(k.puffT<=0&&dCam<70){ k.puffT=0.06; const sp=Math.abs(vf);
    if(!k.air&&(sp>3.5||k.slip>2)&&roadDistAt(k.x,k.z)>ROAD_HW+0.3&&!townAt(k.x,k.z,0)) for(const sx of [-0.75,0.75]){ const p=kartPoint(k,sx,0.15,0.95,_ku); kartPuff(p,0xc9b58f,new THREE.Vector3((Math.random()-.5)*1.5,0.8+Math.random(),(Math.random()-.5)*1.5),0.5+Math.random()*0.4,0.9+sp*0.04); }
    if(k.driver&&Math.random()<0.35+(k.thr>0.1?0.4:0)){ const p=kartPoint(k,-0.34,0.86,1.3,_ku); kartPuff(p,0x8a8a8a,new THREE.Vector3(Math.sin(k.yaw)*0.6,0.5,Math.cos(k.yaw)*0.6),0.25,0.7); } } }
// standing people get pushed aside by a buggy, never stuck inside it
function kartShove(k,E){ if(!E||E.kart) return; const fx=-Math.sin(k.yaw), fz=-Math.cos(k.yaw);
  if(Math.abs(E.pos.x-k.x)>3||Math.abs(E.pos.z-k.z)>3||E.pos.y>k.y+1.35||E.pos.y+1.7<k.y+0.3) return;
  for(const a of [-0.8,0,0.8]){ const cx=k.x-fx*a, cz=k.z-fz*a, dx=E.pos.x-cx, dz=E.pos.z-cz, d=Math.hypot(dx,dz), m=0.72+R; if(d<m){ const nx=d>1e-3?dx/d:fz, nz=d>1e-3?dz/d:-fx; E.pos.x=cx+nx*m; E.pos.z=cz+nz*m; } } }
function seatWorld(k,s,out){ const sl=KART_SEATS[s]; return kartPoint(k,sl[0],sl[1],sl[2],out); }
function enterKart(k,s){ if(k.seats[s]||P.kart||isDead()||P.sky) return; if(edit) exitEdit(false); fireHeld=false; heldPiece=null; P.crouch=false; P.emote=null;
  k.seats[s]=ME(); P.kart={k,seat:s}; if(s===0){ k.driver=ME(); k.local=true; k.tgt=null; sfx('kart_start'); } else sfx('kart_in'); if(mode==='build') selectPick(); }
function kartForget(){ if(!P.kart) return; const k=P.kart.k, s=P.kart.seat; if(k.seats[s]===ME()) k.seats[s]=null; if(s===0){ k.driver=null; k.local=false; kartPark={k,until:performance.now()+1500}; } P.kart=null; }
let kartPark=null;
function exitKart(place){ if(!P.kart) return; const k=P.kart.k, s=P.kart.seat; const vx=k.vx, vz=k.vz; kartForget(); if(s===0){ k.vx=k.vz=0; }
  if(place===false) return;
  const tries=[[s?1.6:-1.6,0.12],[s?-1.6:1.6,0.12],[0,2.15],[0,-2.25],[s?2.4:-2.4,0.12]], ps0=near(k.x,k.z,1); propsNear(k.x,k.z,ps0); karts.forEach(o=>{ if(Math.abs(o.x-k.x)<6&&Math.abs(o.z-k.z)<6) ps0.add(o.solid); });
  let spot=null; for(const [ax,az] of tries){ const p=kartPoint(k,ax,0,az,_ku); const [gy]=groundAt(p.x,p.z,k.y+1.2,ps0); if(gy>k.y+1.2) continue;
    let clear=true; for(const q of ps0) for(const b of q.boxes) if(ovl(b,p.x,p.z)&&b[1]<gy+H_STAND&&b[4]>gy+0.05){ clear=false; break; } if(clear){ spot=[p.x,gy,p.z]; break; } }
  if(!spot){ const p=kartPoint(k,0,1.5,0,_ku); spot=[p.x,p.y,p.z]; } // nowhere beside it: hop out on top
  P.pos.set(spot[0],spot[1],spot[2]); P.vel.set(vx*0.5,1.5,vz*0.5); P.onGround=false; P.fallTop=null; sfx('kart_out'); }
// the buggy in your state, so friends see you in it (the driver also sends where it is)
function kartNet(){ if(!P.kart) return undefined; const k=P.kart.k, s=P.kart.seat; if(s!==0) return [k.id,1];
  return [k.id,0,+k.x.toFixed(2),+k.y.toFixed(2),+k.z.toFixed(2),+k.yaw.toFixed(3),+k.pitch.toFixed(3),+k.roll.toFixed(3),+k.vx.toFixed(2),+k.vz.toFixed(2),+k.steer.toFixed(2),+(k.thr||0).toFixed(1)]; }
function kartParkNet(){ if(!kartPark||performance.now()>kartPark.until) return undefined; const k=kartPark.k; return [k.id,+k.x.toFixed(2),+k.y.toFixed(2),+k.z.toFixed(2),+k.yaw.toFixed(3)]; }
function kartFromState(pl,m){ if(!karts) return; const kk=m.k, mine=ME();
  for(const k of karts) for(let s=0;s<2;s++) if(k.seats[s]===pl.id&&!(kk&&kk[0]===k.id&&kk[1]===s)){ k.seats[s]=null; if(s===0&&k.driver===pl.id){ k.driver=null; k.tgt=null; } }
  pl.kart=null;
  if(kk){ const k=karts[kk[0]], s=kk[1]; if(k){
    if(k.seats[s]===mine){ // we both got in at once: the leader (or the lower id) keeps the seat
      if(pl.id==='h'||(mine!=='h'&&pl.id<mine)){ exitKart(true); toast('Someone got in first'); } else return; }
    k.seats[s]=pl.id; pl.kart={k,seat:s};
    if(s===0){ k.driver=pl.id; k.local=false; k.tgt={x:kk[2],y:kk[3],z:kk[4],yaw:kk[5],pitch:kk[6],roll:kk[7],vx:kk[8],vz:kk[9],steer:kk[10],thr:kk[11]||0,t:performance.now()}; } } }
  if(m.kp){ const k=karts[m.kp[0]]; if(k&&!k.driver){ k.x=m.kp[1]; k.y=m.kp[2]; k.z=m.kp[3]; k.yaw=m.kp[4]; k.vx=k.vz=0; } } }
function kartLeft(id){ if(!karts) return; for(const k of karts) for(let s=0;s<2;s++) if(k.seats[s]===id){ k.seats[s]=null; if(s===0){ k.driver=null; k.tgt=null; } } }
function kartSnapshot(){ return karts?karts.filter(k=>Math.hypot(k.x-k.home.x,k.z-k.home.z)>0.3||Math.abs(angDiff(k.yaw,k.home.yaw))>0.05).map(k=>[k.id,+k.x.toFixed(2),+k.y.toFixed(2),+k.z.toFixed(2),+k.yaw.toFixed(3)]):[]; }
function applyKartSnapshot(ks){ if(!karts||!ks) return; for(const [id,x,y,z,yaw] of ks){ const k=karts[id]; if(k){ k.x=x; k.y=y; k.z=z; k.yaw=yaw; k.vx=k.vz=0; k.settleT=0; } } }
function resetKarts(){ if(!karts) return; if(P.kart){ kartForget(); P.onGround=false; } kartPark=null;
  for(const k of karts){ Object.assign(k,{x:k.home.x,y:k.home.y,z:k.home.z,yaw:k.home.yaw,pitch:0,roll:0,vx:0,vz:0,vy:0,steer:0,air:false,seats:[null,null],driver:null,local:false,tgt:null,settleT:0}); kartPose(k); } }
function kartTargets(consider){ if(!karts) return; for(const k of karts){ if(Math.abs(k.x-P.pos.x)>5||Math.abs(k.z-P.pos.z)>5||k.air) continue;
  for(let s=0;s<2;s++){ if(k.seats[s]) continue; const p=kartPoint(k,s?0.95:-0.95,0,0.1,_ku); consider(p.x,k.y,p.z,2.3,{kind:'kart',k,s,label:s?'Ride as passenger':'Drive'}); } } }
// how a rider sits: posed in the seat, placed by the buggy
const _ZV=new THREE.Vector3();
function seatInfo(E,look){ return E.kart?{k:E.kart.k,s:E.kart.seat,look}:null; }
function seatPose(T,S,A){ const st=S.seat.k.steer||0, drive=S.seat.s===0, look=Math.max(-1.3,Math.min(1.3,angDiff(S.seat.look,S.yaw)));
  A.lag=0; A.stepT=0; T.hipY=0.94; T.hipsX=T.hipsY=T.hipsZ=0; T.spX=-0.05; T.spY=0;
  T.hpL=T.hpR=1.45; T.hpLz=-0.12; T.hpRz=0.12; T.knL=T.knR=-1.3; T.anL=T.anR=-0.12;
  if(S.seat.gunP) return;
  T.chX=0.02; T.chY=look*0.3; T.nkY=look*0.55; T.nkX=S.pitch*0.35; T.nkZ=0; T.wrR=0;
  if(drive){ T.shL=1.05-st*0.3; T.shR=1.05+st*0.3; T.shLz=-0.14; T.shRz=0.14; T.elL=T.elR=0.8; T.chZ=-st*0.07; }
  else { T.shL=0.4; T.shLz=-0.2; T.elL=1.0; T.shR=2.55; T.shRz=0.42; T.elR=0.75; T.chZ=0.04; } }
function seatPlace(H,S){ const k=S.seat.k, G=H.group, r=H.rig; seatWorld(k,S.seat.s,_ku);
  G.rotation.set(k.pitch,S.yaw,k.roll); _kz.set(0,1,0).applyEuler(G.rotation); G.position.copy(_ku).addScaledVector(_kz,-0.94);
  r.pick.visible=false; if(!S.seat.gunP){ r.gun.visible=r.pump.visible=r.hammer.visible=r.plan.visible=false; for(const m of GUN_MODELS) if(r[m]) r[m].visible=false; } }
function animateRig(H,S,dt){
  if(S.seat){ const look=S.yaw, gunP=S.seat.s===1&&!!S.gun; S.seat.look=look; S.seat.gunP=gunP; if(!gunP){ S.gun=false; S.yaw=S.seat.k.yaw; S.reload=null; }
    S.vel=_ZV; S.onGround=true; S.crouch=false; S.emote=null; S.slope=0; S.building=false; S.editing=false; S.swingT=0; S.sky=null; S.item=false; }
  animateRig0(H,S,dt); if(S.seat) seatPlace(H,S); }
// engine: a single-cylinder putter that revs with speed, plus tyre skid; for your buggy or the nearest one running
let kEng=null;
function kartAudio(dt){ if(!AC||!karts) return;
  if(!kEng){ const o1=AC.createOscillator(), o2=AC.createOscillator(), sh=AC.createWaveShaper(), lp=AC.createBiquadFilter(), g=AC.createGain(), am=AC.createGain(), lfo=AC.createOscillator(), lg=AC.createGain();
    o1.type='sawtooth'; o2.type='square'; const cv=new Float32Array(256); for(let i=0;i<256;i++){ const x=i/128-1; cv[i]=Math.tanh(x*2.2); } sh.curve=cv; lp.type='lowpass'; lp.Q.value=2;
    const m1=AC.createGain(), m2=AC.createGain(); m1.gain.value=0.6; m2.gain.value=0.35; o1.connect(m1).connect(sh); o2.connect(m2).connect(sh); sh.connect(lp).connect(am).connect(g).connect(master);
    lfo.type='sine'; lfo.connect(lg).connect(am.gain); am.gain.value=0.6; lg.gain.value=0.4; g.gain.value=0; o1.start(); o2.start(); lfo.start();
    const sn=AC.createBufferSource(); sn.buffer=noiseBuf; sn.loop=true; const sf=AC.createBiquadFilter(); sf.type='bandpass'; sf.Q.value=1.4; const sg=AC.createGain(); sg.gain.value=0; sn.connect(sf).connect(sg).connect(master); sn.start();
    kEng={o1,o2,lp,g,lfo,sg,sf,rpm:0}; }
  let best=null, bd=45; if(P.kart){ best=P.kart.k; bd=0; } else for(const k of karts){ if(!k.driver) continue; const d=Math.hypot(k.x-P.pos.x,k.z-P.pos.z); if(d<bd){ bd=d; best=k; } }
  const now=AC.currentTime, on=best&&playing&&!document.hidden;
  if(on){ const sp=Math.abs(best.vf||0), g1=sp<6?sp/6:(sp-4)/9.5, rpm=Math.min(1.1,0.18+0.82*g1)+(best.thr>0.1?0.08:0)+(best.air&&best.thr>0.1?0.25:0); kEng.rpm+=(rpm-kEng.rpm)*Math.min(1,dt*6);
    const f=26+kEng.rpm*62, vol=(bd===0?0.075:0.07*Math.pow(1-bd/45,2))*(0.75+0.35*Math.abs(best.thr||0));
    kEng.o1.frequency.setTargetAtTime(f,now,0.05); kEng.o2.frequency.setTargetAtTime(f*0.5,now,0.05); kEng.lfo.frequency.setTargetAtTime(f*0.25,now,0.05); kEng.lp.frequency.setTargetAtTime(260+kEng.rpm*1300,now,0.08); kEng.g.gain.setTargetAtTime(vol,now,0.1);
    const skid=!best.air&&best.slip>2.2?Math.min(1,(best.slip-2.2)/4):0, paved=roadDistAt(best.x,best.z)<ROAD_HW+0.6||townAt(best.x,best.z,0);
    kEng.sf.frequency.setTargetAtTime(paved?1700:600,now,0.1); kEng.sg.gain.setTargetAtTime(skid*(bd===0?0.06:0.05*Math.pow(1-bd/45,2)),now,0.06); }
  else { kEng.g.gain.setTargetAtTime(0,now,0.15); kEng.sg.gain.setTargetAtTime(0,now,0.1); } }
function stepKarts(dt){ if(!karts) return; const me=ME();
  if(P.kart&&(isDead()||!karts.includes(P.kart.k))) kartForget();
  for(const k of karts){ const dCam=Math.hypot(k.x-camera.position.x,k.z-camera.position.z);
    if(k.local&&k.seats[0]===me){ const inp=playing&&k.inp?k.inp:{fw:0,st:0,hb:false}; k.inp=null; let t=dt; while(t>1e-5){ const h=Math.min(t,1/60); simKart(k,inp,h); t-=h; } }
    else if(k.driver&&k.tgt) interpKart(k,dt);
    else if(dCam<160) settleKart(k,dt);
    kartModel(k,dt,dCam); if(Math.hypot(k.vx,k.vz)>0.3||k.driver){ kartShove(k,P); if(B&&B.active) kartShove(k,B); } }
  if(P.kart){ const k=P.kart.k; seatWorld(k,P.kart.seat,_ku); _kz.set(0,1,0).applyEuler(k.g.rotation); P.pos.copy(_ku).addScaledVector(_kz,-0.94); P.vel.set(k.vx,k.air?k.vy:0,k.vz); P.onGround=true; P.fallTop=null; P.crouch=false; P.emote=null; }
  stepPuffs(dt); kartAudio(dt);
  const hud=$('kartHud'); if(hud){ const on=!!P.kart&&playing; if(hud.hidden===on) hud.hidden=!on; if(on){ const v=Math.round(Math.abs(P.kart.k.vf||0)*3.6); if(hud._v!==v){ hud._v=v; $('kartSpd').textContent=v; } } } }

/* ---------- targeting ---------- */""")
rep("function animateRig(H,S,dt){\n  const G=H.group, r=H.rig, A=H.anim; A.t+=dt;","function animateRig0(H,S,dt){\n  const G=H.group, r=H.rig, A=H.anim; A.t+=dt;")
rep("  // ----- apply (smoothed) -----\n  const set=(o,ax,v,f)=>{ o.rotation[ax]=lerp(o.rotation[ax],v,f||sm); };","  if(S.seat) seatPose(T,S,A);\n  // ----- apply (smoothed) -----\n  const set=(o,ax,v,f)=>{ o.rotation[ax]=lerp(o.rotation[ax],v,f||sm); };")
# hooks: movement, physics, falling, actions, interact, camera, network, frame
rep("function moveBody(E,fw,st,jump,dt){ if(E.sky){","function moveBody(E,fw,st,jump,dt){ if(E.kart){ if(E.kart.seat===0) E.kart.k.inp={fw,st,hb:!!jump}; return; } if(E.sky){")
rep("  if(E.sky){ skyPhys(dt,E); return; }\n  updatePhase(E);","  if(E.kart){ E.onGround=true; return; }\n  if(E.sky){ skyPhys(dt,E); return; }\n  updatePhase(E);")
rep("  if(P.sky){ P.fallTop=null; return; }","  if(P.sky||P.kart){ P.fallTop=null; return; }")
rep("function fireDown(src){\n  if(isDead()||P.sky) return;","function fireDown(src){\n  if(isDead()||P.sky||(P.kart&&(P.kart.seat===0||mode!=='gun'))) return;")
rep("  if(E===P&&isDead()||E.sky) return false;","  if(E===P&&isDead()||E.sky||E.kart) return false;")
rep("function enterEdit(){\n  if(P.sky) return;","function enterEdit(){\n  if(P.sky||P.kart) return;")
rep("if(!I||P.useT>0||isDead()||P.sky) return;","if(!I||P.useT>0||isDead()||P.sky||(P.kart&&P.kart.seat===0)) return;")
rep("  if(!playing||isDead()||edit||invOpen||P.sky) return null;","  if(P.kart) return playing&&!isDead()&&!invOpen?{kind:'kartout',label:'Get out'}:null;\n  if(!playing||isDead()||edit||invOpen||P.sky) return null;")
rep("consider(q.x,q.y-1.2,q.z,2.4,{kind:'door',p,c,label:dr.open?'Close door':'Open door'}); }); });\n  return best; }","consider(q.x,q.y-1.2,q.z,2.4,{kind:'door',p,c,label:dr.open?'Close door':'Open door'}); }); });\n  kartTargets(consider);\n  return best; }")
rep("  else if(t.kind==='door') toggleDoor(t.p,t.c,false); }","  else if(t.kind==='door') toggleDoor(t.p,t.c,false);\n  else if(t.kind==='kart') enterKart(t.k,t.s);\n  else if(t.kind==='kartout') exitKart(true); }")
rep("const solidNear=(E)=>{ const ps=near(E.pos.x,E.pos.z); if(E.phase&&E.phase.size) E.phase.forEach(p=>ps.delete(p)); if(props.length) propsNear(E.pos.x,E.pos.z,ps); return ps; };",
    "const solidNear=(E)=>{ const ps=near(E.pos.x,E.pos.z); if(E.phase&&E.phase.size) E.phase.forEach(p=>ps.delete(p)); if(props.length) propsNear(E.pos.x,E.pos.z,ps); if(karts) for(const k of karts) if(Math.abs(k.x-E.pos.x)<5&&Math.abs(k.z-E.pos.z)<5&&!(E.kart&&E.kart.k===k)) ps.add(k.solid); return ps; };")
rep("let camY=0, camDip=0, skyCamK=0;","let camY=0, camDip=0, skyCamK=0, kartCamK=0;")
rep("  const side=0.6-0.05*adsK-0.3*skyCamK, back=2.9-1.35*adsK+3.4*skyCamK, up=0.18+0.08*adsK+1.0*skyCamK;",
    "  kartCamK+=((P.kart?(P.kart.seat===0||adsK<0.5?1:0.4):0)-kartCamK)*Math.min(1,lastDt*3);\n  const side=0.6-0.05*adsK-0.3*skyCamK-0.35*kartCamK, back=2.9-1.35*adsK+3.4*skyCamK+1.4*kartCamK, up=0.18+0.08*adsK+1.0*skyCamK+0.45*kartCamK;")
rep("P.emote?EMOTE_IDS.indexOf(P.emote.id)+1:0]};","P.emote?EMOTE_IDS.indexOf(P.emote.id)+1:0],k:kartNet(),kp:kartParkNet()};")
rep("  if(pl.fresh){ pl.pos.copy(pl.tgt); pl.fresh=false; }\n}","  if(pl.fresh){ pl.pos.copy(pl.tgt); pl.fresh=false; }\n  kartFromState(pl,m);\n}")
rep("sky:(pl.flags&128)?'glide':(pl.flags&64)?'fall':null},dt);","sky:(pl.flags&128)?'glide':(pl.flags&64)?'fall':null,seat:seatInfo(pl,pl.dyaw)},dt);")
rep("emote:P.emote,sky:P.sky?P.sky.phase:null},dt);","emote:P.emote,sky:P.sky?P.sky.phase:null,seat:seatInfo(P,P.yaw)},dt);")
rep("function dropPlayer(id){ const pl=net.players.get(id); if(!pl) return;","function dropPlayer(id){ kartLeft(id); const pl=net.players.get(id); if(!pl) return;")
rep("function respawn(){ animEvent(localHero,'revive'); P.sky=null;","function respawn(){ animEvent(localHero,'revive'); P.sky=null; kartForget();")
rep("function clearBuilds(){ if(edit) exitEdit(false);","function clearBuilds(){ resetKarts(); if(edit) exitEdit(false);")
rep("applyDoorSnapshot(m.ds);","applyDoorSnapshot(m.ds); applyKartSnapshot(m.ks);")
rep("ds:doorSnapshot(),","ds:doorSnapshot(),ks:kartSnapshot(),")
rep("stepShakes(dt); stepPlayers(dt);","stepShakes(dt); stepKarts(dt); stepPlayers(dt);")
rep("buildWorld(); initChests(); spawnFloorLoot();","buildWorld(); initChests(); spawnFloorLoot(); initKarts();")
# HUD: speed while you're in a buggy
rep('<div class="hud" id="chestBar" hidden>','<div class="hud" id="kartHud" hidden><b id="kartSpd">0</b><span>km/h</span></div>\n<div class="hud" id="chestBar" hidden>')
rep("#chestBar{left:50%;","#kartHud{left:50%;bottom:150px;transform:translateX(-50%);display:flex;align-items:baseline;gap:5px;font:800 italic 15px/1 var(--font-hud);color:#e9edf2;text-shadow:0 1px 3px #000}\n#kartHud b{font-size:30px;color:#fff;min-width:44px;text-align:right}\n#chestBar{left:50%;")
# sounds
rep("    case 'sky_start':","""    case 'kart_start': for(let n=0;n<5;n++) noise(900,0.07,0.07,3,n*0.09,'bandpass',600); for(let n=0;n<7;n++) knock(70+n*6,0.09,0.22,4,0.5+n*0.07); noise(200,0.5,0.08,0.8,0.5,'lowpass',260); break;
    case 'kart_in': knock(160,0.06,0.18,3); noise(1400,0.12,0.05,1.2,0.02,'bandpass',900); break;
    case 'kart_out': knock(140,0.06,0.16,3); noise(500,0.18,0.05,0.8,0,'lowpass',300); break;
    case 'kart_bump': knock(85,0.16,0.45,3); noise(240,0.25,0.25,0.8,0,'lowpass',180); knock(1300,0.04,0.12,6,0.01); break;
    case 'kart_land': knock(70,0.18,0.4,2.5); noise(300,0.2,0.18,0.8,0,'lowpass',200); knock(420,0.05,0.1,4,0.03); break;
    case 'kart_hit': knock(110,0.12,0.45,3); noise(700,0.18,0.22,1,0,'bandpass',300); break;
    case 'sky_start':""")
