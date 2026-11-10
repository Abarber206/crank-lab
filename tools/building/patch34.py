# ---------- 34. forests: thousands of trees, in many sizes, drawn in two levels of detail; front-yard trees and gardens ----------
# placement: woods and meadows from a noise field, pines higher up and on the rocky mountain faces
old=s[s.index("  for(const [kind,n] of [['tree',520],['pine',520],['rock',220],['car',15]]){ let made=0;"):s.index("  // parked cars: on a road's shoulder, lined up with it")]
new=r"""  /* Trees: about 9,000, grown from a noise field of woods and meadows. In the woods they stand close (4 m apart or
     so); out in the meadows they're scattered and grow bigger. Broadleaf trees fill the valleys, pines take over
     higher up and climb the rocky mountain faces (not the sheerest cliffs or the snow). Every tree has its own size
     and height, from saplings to giants. Rocks and junk cars are placed as before. */
  const woods=(x,z)=>{ const n=0.65*gnoise(x*0.0042,z*0.0042,4411)+0.35*gnoise(x*0.013,z*0.013,4417); return sstep(-0.15,0.45,n); };
  const roomyT=(x,z,gap)=>!propsNear(x,z,[],1).some(q=>Math.hypot(q.x-x,q.z-z)<(q.kind==='tree'||q.kind==='pine'?gap:q.kind==='car'?7:5));
  { let made=0; const WANT=9000;
    for(let k=0;k<160000&&made<WANT;k++){
      const x=SPAWN[0]+(r()*2-1)*RR, z=SPAWN[2]+(r()*2-1)*RR, u=x-SPAWN[0], v=z-SPAWN[2], d2=u*u+v*v; if(d2>RR*RR||d2<(FLAT_R+14)*(FLAT_R+14)) continue;
      const c=worldCell(x,z); if(c<0||WORLD.SNOW[c]>60||roadDistAt(x,z)<6.5||townAt(x,z,7)) continue;
      const w=woods(x,z), rock=WORLD.ROCK[c], h=terrainH(x,z), [sl]=slopeAt(x,z); if(sl>1.55) continue;
      if(r()>0.1+0.9*w) continue; // meadows keep a few lone trees
      const high=sstep(25,85,h), rocky=rock>110;
      const kind=rocky||r()<0.15+0.75*high?'pine':'tree'; if(kind==='tree'&&rocky) continue;
      if(rocky&&r()<0.35) continue; // thinner on the rock
      const gap=w>0.55?(kind==='pine'?3.6:4.4):(kind==='pine'?5:6.5); if(!roomyT(x,z,gap)) continue;
      const big=w>0.55?0:0.35, sz=(r()+r())/2, s=kind==='pine'?0.75+sz*1.7+big:0.7+sz*1.45+big, hs=0.82+r()*0.48;
      const p=add(kind,x,z,s); p.hs=hs; p.g.scale.set(p.s,p.s*hs,p.s); p.tint=0.88+r()*0.22; p.boxes=propBoxes(p); made++; } }
  for(const [kind,n] of [['rock',220],['car',15]]){ let made=0;
    while(made<n&&tries<90000){ tries++;
      const x=SPAWN[0]+(r()*2-1)*RR, z=SPAWN[2]+(r()*2-1)*RR;
      const u=x-SPAWN[0], v=z-SPAWN[2], d2=u*u+v*v; if(d2>RR*RR||d2<18*18) continue;
      const c=worldCell(x,z); if(c<0||WORLD.SNOW[c]>50||roadDistAt(x,z)<8||townAt(x,z,8)) continue;
      const rock=WORLD.ROCK[c];
      if(kind==='rock'){ if(rock<90&&r()<0.8) continue; } else if(rock>120) continue;
      if(!roomy(x,z,kind)) continue;
      add(kind,x,z,kind==='rock'?.8+r()*.7:1); made++; } }
  yardTrees(add,r);
"""
s=s.replace(old,new)
# trees are drawn by the forest system (instanced, two levels of detail); a tree only gets its own mesh while it moves
rep("""function buildPropMesh(p,r){
  const g=new THREE.Group(); g.position.set(p.x,0,p.z); g.rotation.y=r()*Math.PI*2; const v=propVariant(p.kind,p.id%8);""","""function buildPropMesh(p,r){
  if(p.kind==='tree'||p.kind==='pine'){ const g=new THREE.Group(); g.position.set(p.x,0,p.z); g.rotation.y=r()*Math.PI*2; g.scale.setScalar(p.s); p.lazy=true; return g; } // (not in the scene: see the forest)
  const g=new THREE.Group(); g.position.set(p.x,0,p.z); g.rotation.y=r()*Math.PI*2; const v=propVariant(p.kind,p.id%8);""")
rep("if(p.kind==='tree'||p.kind==='pine'){ const t=(p.kind==='tree'?.42:.34)*s+0.05; return [[x-t,0,z-t,x+t,3.2*s,z+t]]; }","if(p.kind==='tree'||p.kind==='pine'){ const t=(p.kind==='tree'?.42:.34)*s+0.05; return [[x-t,0,z-t,x+t,3.2*s*(p.hs||1),z+t]]; }")
rep("function propMeshesNear(x,z){ const out=[]; propsNear(x,z,[]).forEach(p=>p.g.traverse(m=>{ if(m.isMesh&&m.userData.piece) out.push(m); })); return out; }",
    "function propMeshesNear(x,z){ const out=[]; propsNear(x,z,[]).forEach(p=>{ if(p.lazy){ treeMesh(p); if(!p.g.parent) p.g.updateMatrixWorld(true); } p.g.traverse(m=>{ if(m.isMesh&&m.userData.piece) out.push(m); }); }); return out; }")
rep("props.forEach(p=>{ if(townAt(p.x,p.z,6)){ p.gone=true;","props.forEach(p=>{ if(!p.yard&&townAt(p.x,p.z,6)){ p.gone=true;")
rep("  for(const p of props){\n    if(p.wob>0){","  stepForest(dt);\n  for(const p of props){\n    if(p.lazy) treeAnim(p);\n    if(p.wob>0){")
rep("    for(const p of props){ const far=(p.x-cx)*(p.x-cx)+(p.z-cz)*(p.z-cz)>400*400; p.g.visible=!far&&(p.alive||p.dying>0); }","    for(const p of props){ if(p.lazy) continue; const far=(p.x-cx)*(p.x-cx)+(p.z-cz)*(p.z-cz)>400*400; p.g.visible=!far&&(p.alive||p.dying>0); }")
rep("function propRevive(p){ p.alive=true; p.hp=p.maxHp; p.grow=0; p.dying=0; p.g.visible=true; p.g.scale.setScalar(p.s*0.01); propCullT=0; }",
    "function propRevive(p){ p.alive=true; p.hp=p.maxHp; p.grow=0; p.dying=0; p.g.visible=true; p.g.scale.setScalar(p.s*0.01); propCullT=0; forestDirty=true; }")
rep("  if(p.hp<=0) propBreak(p,quiet);\n","  if(p.hp<=0) propBreak(p,quiet);\n  if(p.lazy) forestDirty=true;\n")
rep("/* materials: infinite by default; switch it off in Settings to farm for your builds */",r"""/* ---------- the forest ----------
   Thousands of trees can't each be their own object, so they're drawn as instanced meshes: within 130 m every tree
   is the full model (eight broadleaf and eight pine shapes), further out a much simpler one (a few blobs or cones on
   a trunk), and past 1.5 km the haze has them. Each tree keeps its own turn, size, height and a slightly different
   green. The lists are rebuilt a few times a second as you move. A tree that's being chopped, falling or growing
   back gets its own mesh while it moves, then rejoins the forest. */
const FOREST={near:null,far:null,lastX:1e9,lastZ:1e9,t:0}; let forestDirty=true;
const NEAR_TREE=130, FAR_TREE=1500;
function farTreeGeo(kind,v){ const q=seeded(5303+v*977+(kind==='pine'?31:0)), parts=[], put=(g,col)=>{ g=g.index?g.toNonIndexed():g; g.computeVertexNormals(); const n=g.attributes.position.count, c=new Float32Array(n*3), cc=new THREE.Color(col); for(let i=0;i<n;i++){ c[i*3]=cc.r; c[i*3+1]=cc.g; c[i*3+2]=cc.b; } g.setAttribute('color',new THREE.BufferAttribute(c,3)); parts.push(g); };
  if(kind==='tree'){ put(new THREE.CylinderGeometry(.3,.4,3.4,5).translate(0,1.7,0),0x6e4a2b);
    for(const [x,y,z,rr,col] of [[0,4.4,0,2.0,0x3f8434],[0.9,4.0,0.4,1.4,0x46903a],[-0.8,4.1,-0.5,1.45,0x4a943d],[0.1,5.3,0.1,1.4,0x58a845]]) put(new THREE.IcosahedronGeometry(rr*(0.9+q()*0.2),0).translate(x,y,z),col); }
  else { put(new THREE.CylinderGeometry(.22,.34,2.8,5).translate(0,1.4,0),0x5e3e24);
    for(const [rr,y,hh,col] of [[2.2,3.1,2.4,0x2c6e44],[1.65,4.3,2.1,0x337c4b],[1.05,5.4,1.8,0x3d8f57]]) put(new THREE.ConeGeometry(rr*(0.95+q()*0.1),hh,7).translate(0,y,0),col); }
  const out=new THREE.BufferGeometry(); for(const k of ['position','normal','color']){ let len=0; parts.forEach(g=>len+=g.attributes[k].array.length); const A=new Float32Array(len); let o=0; parts.forEach(g=>{ A.set(g.attributes[k].array,o); o+=g.attributes[k].array.length; }); out.setAttribute(k,new THREE.BufferAttribute(A,3)); }
  return out; }
function initForest(){ const trees=props.filter(p=>p.lazy), mk=(geo,mat,n,shadow)=>{ const m=new THREE.InstancedMesh(geo,mat,Math.max(1,n)); m.setColorAt(0,new THREE.Color(1,1,1)); m.count=0; m.frustumCulled=false; m.castShadow=shadow; m.receiveShadow=true;
    m.instanceMatrix.setUsage(THREE.DynamicDrawUsage); m.instanceColor.setUsage(THREE.DynamicDrawUsage); scene.add(m); return m; };
  FOREST.near={}; FOREST.far={};
  for(const kind of ['tree','pine']){ const n=trees.filter(p=>p.kind===kind).length;
    FOREST.near[kind]=[...Array(8)].map((_,v)=>{ const V=propVariant(kind,v); return mk(V.geo,V.mat,trees.filter(p=>p.kind===kind&&p.id%8===v).length,true); });
    FOREST.far[kind]=[...Array(4)].map((_,v)=>mk(farTreeGeo(kind,v),propVariant(kind,0).mat,trees.filter(p=>p.kind===kind&&p.id%4===v).length,false)); }
  FOREST.trees=trees; forestDirty=true; }
const _fc=new THREE.Color(), _fm=new THREE.Matrix4();
function stepForest(dt){ if(!FOREST.near) return; FOREST.t-=dt; const cx=camera.position.x, cz=camera.position.z;
  const moved=Math.hypot(cx-FOREST.lastX,cz-FOREST.lastZ);
  if(!(forestDirty&&FOREST.t<=0)&&!(moved>6&&FOREST.t<=0)) return; FOREST.t=0.2; forestDirty=false; FOREST.lastX=cx; FOREST.lastZ=cz;
  const cnt=new Map(); const push=(m,p)=>{ const i=cnt.get(m)||0; p.g.updateMatrix(); _fm.copy(p.g.matrix); m.setMatrixAt(i,_fm); const t=p.tint||1; m.setColorAt(i,_fc.setRGB(t,t*(0.97+0.06*((p.id*37)%10)/10),t)); cnt.set(m,i+1); };
  const N2=NEAR_TREE*NEAR_TREE, F2=FAR_TREE*FAR_TREE;
  for(const p of FOREST.trees){ if(p.gone||!p.alive||p.g.parent) continue; const dx=p.x-cx, dz=p.z-cz, d2=dx*dx+dz*dz; if(d2>F2) continue;
    if(d2<N2) push(FOREST.near[p.kind][p.id%8],p); else if(d2<420000||(d2<1000000?p.id%2===0:p.id%3===0)) push(FOREST.far[p.kind][p.id%4],p); } // deep in the haze, every other (then every third) tree is plenty
  for(const set of [FOREST.near,FOREST.far]) for(const kind in set) for(const m of set[kind]){ const n=cnt.get(m)||0; m.count=n; if(n){ m.instanceMatrix.needsUpdate=true; m.instanceColor.needsUpdate=true; } } }
// a tree's own mesh (for the pickaxe to hit, and while it shakes, falls or grows)
function treeMesh(p){ if(p.g.children.length) return p.g.children[0]; const V=propVariant(p.kind,p.id%8), m=new THREE.Mesh(V.geo,V.mat); m.castShadow=m.receiveShadow=true; m.userData.piece=p; p.g.add(m); return m; }
function treeAnim(p){ const moving=p.wob>0||p.dying>0||(p.alive&&p.grow<1);
  if(moving&&!p.g.parent){ treeMesh(p); scene.add(p.g); forestDirty=true; FOREST.t=0; }
  else if(!moving&&p.g.parent){ scene.remove(p.g); p.g.scale.set(p.s,p.s*(p.hs||1),p.s); p.g.rotation.x=p.g.rotation.z=0; forestDirty=true; FOREST.t=0; } }
/* ---------- front yards and back gardens ----------
   Every house gets a tree or two in the front yard (small and medium ones, clear of the path and the driveway) and
   bigger ones out back where there's room; a flower bed along the front wall, round shrubs at the corners and a
   mailbox by the sidewalk. The yard trees are real trees (they farm and grow back); the garden pieces are one mesh
   per town, just for looks. */
function yardFrame(t,h){ const C=CELL, X=h.side==='n'||h.side==='s';
  const fN=h.side==='n'||h.side==='w', x0=h.i0*C, x1=(h.i0+h.w)*C, z0=h.j0*C, z1=(h.j0+h.d)*C;
  // u along the front, w out from the front wall (toward the street, negative w goes behind the house)
  if(X){ const fz=fN?z0:z1, s=fN?-1:1; return {len:x1-x0,depth:z1-z0,p:(u,w)=>[x0+u,fz+s*w]}; }
  const fx=fN?x0:x1, s=fN?-1:1; return {len:z1-z0,depth:x1-x0,p:(u,w)=>[fx+s*w,z0+u]}; }
function yardTrees(add,r){
  const free=(t,x,z,pad)=>{ if(Math.hypot(x-t.x,z-t.z)>t.R+6) return false; if(Math.abs(x-t.x)<ROAD_HW+WALK_W+1.4||Math.abs(z-t.z)<ROAD_HW+WALK_W+1.4) return false;
    for(const h of t.houses){ if(x>h.i0*CELL-pad&&x<(h.i0+h.w)*CELL+pad&&z>h.j0*CELL-pad&&z<(h.j0+h.d)*CELL+pad) return false; const G=h.garage; if(G&&x>G.i*CELL-pad&&x<(G.i+1)*CELL+pad&&z>G.j*CELL-pad&&z<(G.j+1)*CELL+pad) return false; }
    for(const rd of WORLD.roads){ if(rd.street) continue; if(roadDistAt(x,z)<ROAD_HW+2) return false; } return true; };
  for(const t of TOWNS){ if(!t.houses.length) planHouses(t);
    for(const h of t.houses){ const f=yardFrame(t,h), gside=h.garage?1:0;
      // front yard: one or two smallish trees in the corners, clear of the path (middle) and the garage side
      const spots=[[0.18,2.6],[0.82,2.6]]; for(const [fu,fw] of spots){ if(r()<0.25) continue; const u=f.len*fu+(r()-.5)*0.8; if(Math.abs(u-f.len/2)<2.2) continue; if(gside&&fu>0.6) continue;
        const [x,z]=f.p(u,fw+(r()-.5)*0.6); if(!free(t,x,z,1.6)) continue; if(propsNear(x,z,[],1).some(q=>Math.hypot(q.x-x,q.z-z)<3.5)) continue;
        const p=add(r()<0.75?'tree':'pine',x,z,0.55+r()*0.45); p.hs=0.85+r()*0.35; p.g.scale.set(p.s,p.s*p.hs,p.s); p.tint=0.9+r()*0.18; p.yard=true; p.boxes=propBoxes(p); }
      // back garden: bigger trees behind the house, where nothing else is
      for(let n=0;n<3;n++){ if(r()<0.35) continue; const u=f.len*(0.15+r()*0.7), w=-(f.depth+3+r()*4); const [x,z]=f.p(u,w); if(!free(t,x,z,2.2)) continue;
        if(propsNear(x,z,[],1).some(q=>Math.hypot(q.x-x,q.z-z)<4.5)) continue; const p=add(r()<0.6?'tree':'pine',x,z,0.8+r()*0.8); p.hs=0.85+r()*0.4; p.g.scale.set(p.s,p.s*p.hs,p.s); p.tint=0.88+r()*0.2; p.yard=true; p.boxes=propBoxes(p); } } } }
let gardenMeshes=[];
function buildGardens(){ const flowers=[0xe8456b,0xf2c014,0xffffff,0xa45ee5,0xff8a3d,0xe23a3a], q=seeded(77123);
  for(const t of TOWNS){ const parts=[], put=(g,col,x,y,z,ry=0)=>{ g=g.index?g.toNonIndexed():g.clone(); g.rotateY(ry); g.translate(x,y,z); const n=g.attributes.position.count, c=new Float32Array(n*3), cc=new THREE.Color(col); for(let i=0;i<n;i++){ c[i*3]=cc.r; c[i*3+1]=cc.g; c[i*3+2]=cc.b; } g.setAttribute('color',new THREE.BufferAttribute(c,3)); parts.push(g); };
    const y0=t.h;
    for(const h of t.houses){ const f=yardFrame(t,h), X=h.side==='n'||h.side==='s', ry=X?0:Math.PI/2, mid=f.len/2;
      // flower beds along the front wall, either side of the door: dark soil, a brick edge, rows of flowers
      for(const sd of [-1,1]){ if(h.garage&&sd>0&&f.len<11) continue; const a=sd<0?0.6:mid+1.2, b=sd<0?mid-1.2:f.len-0.6, L=b-a; if(L<1.2) continue;
        const [cx,cz]=f.p((a+b)/2,0.55); put(new THREE.BoxGeometry(L,0.12,0.8),0x4a3424,cx,y0+0.06,cz,ry); put(new THREE.BoxGeometry(L+0.1,0.16,0.08),0x9a5a42,...f.p((a+b)/2,0.98).reduce((o,v,i)=>(o[i?2:0]=v,o),[0,y0+0.08,0]),ry);
        const col=flowers[Math.floor(q()*flowers.length)], col2=flowers[Math.floor(q()*flowers.length)];
        for(let u=a+0.2;u<b-0.1;u+=0.32){ for(const w of [0.35,0.72]){ const [x,z]=f.p(u+(q()-.5)*0.1,w+(q()-.5)*0.08); put(new THREE.IcosahedronGeometry(0.09+q()*0.04,0),q()<0.75?col:col2,x,y0+0.2+q()*0.08,z); put(new THREE.CylinderGeometry(0.012,0.012,0.16,3),0x3f7a2e,x,y0+0.12,z); } } }
      // round shrubs at the front corners
      for(const fu of [0.25,f.len-0.25]){ if(h.garage&&fu>mid) continue; const [x,z]=f.p(fu,0.4); const rr=0.45+q()*0.2; put(new THREE.IcosahedronGeometry(rr,1).scale(1,0.85,1),0x3d7a32,x,y0+rr*0.7,z); }
      // a mailbox by the sidewalk, beside the front path
      { const [x,z]=f.p(mid+1.25,(X?Math.abs((h.side==='n'?h.j0*CELL:(h.j0+h.d)*CELL)-t.z):Math.abs((h.side==='w'?h.i0*CELL:(h.i0+h.w)*CELL)-t.x))-(ROAD_HW+WALK_W)-0.45);
        put(new THREE.BoxGeometry(0.09,1.05,0.09),0x5a4030,x,y0+0.52,z,ry); put(new THREE.BoxGeometry(0.24,0.24,0.46),[0x2a2d33,0x8a2a2a,0x2f5d8a,0xe0ddd5][Math.floor(q()*4)],x,y0+1.12,z,ry+Math.PI/2);
        put(new THREE.BoxGeometry(0.03,0.16,0.07),0xd23a2a,...[x+(X?0.14:0),y0+1.2,z+(X?0:0.14)],ry); } }
    if(!parts.length) continue;
    const out=new THREE.BufferGeometry(); for(const k of ['position','normal','color']){ let len=0; parts.forEach(g=>len+=g.attributes[k].array.length); const A=new Float32Array(len); let o=0; parts.forEach(g=>{ A.set(g.attributes[k].array,o); o+=g.attributes[k].array.length; }); out.setAttribute(k,new THREE.BufferAttribute(A,3)); }
    out.computeBoundingSphere(); const m=new THREE.Mesh(out,new THREE.MeshLambertMaterial({vertexColors:true})); m.castShadow=true; m.receiveShadow=true; m.matrixAutoUpdate=false; m.userData.town=t; scene.add(m); gardenMeshes.push(m); } }
/* materials: infinite by default; switch it off in Settings to farm for your builds */""")
rep("buildWorld(); initChests(); spawnFloorLoot(); initKarts();","buildWorld(); initChests(); spawnFloorLoot(); initKarts(); initForest(); buildGardens();")
# far gardens hide with their town
rep("    townBatch.forEach((b,t)=>{ const on=Math.hypot(t.x-cx,t.z-cz)<700; b.meshes.forEach(m=>{ m.visible=on; }); }); }","    townBatch.forEach((b,t)=>{ const on=Math.hypot(t.x-cx,t.z-cz)<700; b.meshes.forEach(m=>{ m.visible=on; }); }); gardenMeshes.forEach(m=>{ m.visible=Math.hypot(m.userData.town.x-cx,m.userData.town.z-cz)<450; }); }")
# no chests inside tree trunks
rep("if(c<0||townAt(x,z,8)||roadDistAt(x,z)<7||WORLD.SNOW[c]>30||WORLD.ROCK[c]>150||chests.some(q=>Math.hypot(q.x-x,q.z-z)<70)) continue;","if(c<0||townAt(x,z,8)||roadDistAt(x,z)<7||WORLD.SNOW[c]>30||WORLD.ROCK[c]>150||chests.some(q=>Math.hypot(q.x-x,q.z-z)<70)||propsNear(x,z,[],1).some(q=>Math.hypot(q.x-x,q.z-z)<2.6)) continue;")
