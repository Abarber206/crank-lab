/* ---------- house staircases ----------
   Two-storey houses get a real staircase: a straight run of 20 steps along an inside wall, rising to a landing at the
   end wall, under an opening cut in the upper floor (a stairwell) with a railing round it. The steps are solid boxes
   you walk up step by step, not a ramp. The stairs belong to the ground-floor piece of the top cell and the railing to
   the upper floor there, so they break and come back with those pieces. */
function housePlainMat(s){ return houseMat('w'+s.style+'plain'+s.paint,()=>{ const t=houseWallSet(s.style,'plain'); return new THREE.MeshPhongMaterial({map:t.map,normalMap:t.normal,color:HOUSE_PAINT[s.style][s.paint],shininess:s.style==='panel'?18:6,specular:0x111111}); },'HOUSE_PAINT','w'+s.style+'plain'); }
function houseStair(h){
  if(h._stair) return h._stair;
  const {i0,j0,w,d,L}=h, C=CELL, Y0=L*LVL, IN=WT/2, X=w>=d, masks={};
  // run along the longer side, up to the far end; on the side away from the front door
  let lo, cells;
  if(X){ lo=h.side!=='n'; const row=lo?0:d-1; cells=[[i0+w-1,j0+row],[i0+w-2,j0+row]]; masks[cells[0]]=lo?12:3; masks[cells[1]]=lo?13:7; }
  else { lo=h.side!=='w'; const col=lo?0:w-1; cells=[[i0+col,j0+d-1],[i0+col,j0+d-2]]; masks[cells[0]]=lo?10:5; masks[cells[1]]=lo?11:7; }
  // (s,t,y): s back from the inner face of the end wall, t in from the inner face of the side wall, y up from the floor
  const xEnd=(i0+w)*C-IN, zEnd=(j0+d)*C-IN, xLo=i0*C+IN, zLo=j0*C+IN;
  const P2=(s,t)=>X?[xEnd-s,lo?zLo+t:zEnd-t]:[lo?xLo+t:xEnd-t,zEnd-s];
  const box=(s0,s1,t0,t1,y0,y1)=>{ const a=P2(s0,t0), b=P2(s1,t1); return [Math.min(a[0],b[0]),Y0+y0,Math.min(a[1],b[1]),Math.max(a[0],b[0]),Y0+y1,Math.max(a[1],b[1])]; };
  const V3=(s,t,y)=>{ const p=P2(s,t); return new THREE.Vector3(p[0],Y0+y,p[1]); };
  const N=20, RISE=LVL/(N+1), SW=1.25, TW=2.5-IN, LAND=1.4, S1=7.5-IN, TR=(S1-LAND)/N;
  const geo=b=>{ const g=new THREE.BoxGeometry(b[3]-b[0],b[4]-b[1],b[5]-b[2]); g.translate((b[0]+b[3])/2,(b[1]+b[4])/2,(b[2]+b[5])/2); return g; };
  const stairs={boxes:[],parts:{tread:[],inner:[],beam:[]}}, rail={boxes:[],parts:{beam:[]}};
  // landing, level with the upper floor, on a post
  const land=box(0,LAND,0,TW,LVL-0.26,LVL); stairs.boxes.push(land); stairs.parts.tread.push(geo(land));
  stairs.parts.beam.push(geo(box(LAND-0.12,LAND,TW-0.12,TW,0,LVL-0.26)));
  // the steps: solid underneath (a closed staircase), hardwood treads with a little nosing
  for(let k=0;k<N;k++){ const s0=S1-(k+1)*TR, s1=S1-k*TR, top=(k+1)*RISE;
    stairs.boxes.push(box(s0,s1,0,SW,0,top));
    stairs.parts.inner.push(geo(box(s0,s1,0,SW,0,top-0.04)));
    stairs.parts.tread.push(geo(box(s0,Math.min(S1+0.02,s1+0.03),0,SW+0.03,top-0.04,top))); }
  // handrail up the open side of the steps
  const hr=[[S1-TR/2,RISE],[LAND+TR/2,LVL-RISE]];
  hr.forEach(([s,y])=>stairs.parts.beam.push(geo(box(s-0.05,s+0.05,SW-0.05,SW+0.05,y,y+0.95))));
  for(let k=2;k<N-1;k+=4){ const s=S1-(k+0.5)*TR, y=(k+1)*RISE; stairs.parts.beam.push(beamGeo(V3(s,SW,y),V3(s,SW,y+0.9),0.035)); } // balusters
  stairs.parts.beam.push(beamGeo(V3(S1-TR/2,SW,RISE+0.95),V3(LAND+TR/2,SW,LVL-RISE+0.95),0.07));
  // railing round the stairwell on the upper floor (the landing side stays open: that's the way off the stairs)
  rail.boxes.push(box(LAND,S1,TW-0.05,TW+0.05,LVL,LVL+1.0), box(S1-0.05,S1+0.05,0,TW,LVL,LVL+1.0));
  const posts=[[LAND,TW],[LAND+(S1-LAND)/3,TW],[LAND+2*(S1-LAND)/3,TW],[S1,TW],[S1,TW/2],[S1,0.06]];
  posts.forEach(([s,t])=>rail.parts.beam.push(geo(box(s-0.05,s+0.05,t-0.05,t+0.05,LVL,LVL+1.0))));
  for(const y of [0.5,0.97]){ rail.parts.beam.push(beamGeo(V3(LAND,TW,LVL+y),V3(S1,TW,LVL+y),y>0.9?0.07:0.04), beamGeo(V3(S1,TW,LVL+y),V3(S1,0.06,LVL+y),y>0.9?0.07:0.04)); }
  for(let s=LAND+0.3;s<S1-0.1;s+=0.32) rail.parts.beam.push(beamGeo(V3(s,TW,LVL),V3(s,TW,LVL+0.97),0.03));
  for(let t=0.36;t<TW-0.1;t+=0.32) rail.parts.beam.push(beamGeo(V3(S1,t,LVL),V3(S1,t,LVL+0.97),0.03));
  // merge each set into one geometry per material, placed relative to the floor piece it belongs to
  const centre=(c,l)=>new THREE.Vector3((c[0]+0.5)*C,l*LVL-FT/2,(c[1]+0.5)*C);
  const pack=(set,c,l)=>{ const o=centre(c,l), out=[];
    for(const k in set.parts){ const list=set.parts[k]; if(!list.length) continue; const g=mergeGeos(list); g.translate(-o.x,-o.y,-o.z); g.computeVertexNormals();
      if(k==='inner') g.setAttribute('inside',new THREE.BufferAttribute(new Float32Array(g.attributes.position.count).fill(1),1));
      g.computeBoundingSphere(); out.push([g,k]); }
    return {boxes:set.boxes,parts:out}; };
  h._stair={cells,masks,top:cells[0],stairs:pack(stairs,cells[0],L),rail:pack(rail,cells[0],L+1)};
  return h._stair;
}

/* ---------- sidewalks: a concrete path from every front door to the town square ---------- */
const WALK_W=1.7, SIDEWALKS=[]; let sidewalkMesh=null;
const walkTex=(()=>{ const W=128, Hh=128, c=document.createElement('canvas'); c.width=W; c.height=Hh; const g=c.getContext('2d');
  g.fillStyle='#a3a098'; g.fillRect(0,0,W,Hh);
  for(let i=0;i<2500;i++){ const v=Math.random(); g.fillStyle=v<.5?'rgba(70,66,60,.16)':'rgba(255,255,250,.2)'; g.fillRect(Math.random()*W,Math.random()*Hh,1+Math.random()*1.5,1+Math.random()*1.5); }
  g.fillStyle='rgba(60,56,50,.55)'; g.fillRect(0,0,W,2);                       // expansion joint, every slab
  g.fillStyle='rgba(90,86,78,.35)'; g.fillRect(0,0,4,Hh); g.fillRect(W-4,0,4,Hh); // worn edges
  const t=new THREE.CanvasTexture(c); t.wrapS=t.wrapT=THREE.RepeatWrapping; t.anisotropy=Math.min(8,renderer.capabilities.getMaxAnisotropy()); return t; })();
function doorOf(h){ const C=CELL, a=Math.floor(h.w/2), b=Math.floor(h.d/2);
  if(h.side==='w') return {x:h.i0*C,z:(h.j0+b+0.5)*C,nx:-1,nz:0}; if(h.side==='e') return {x:(h.i0+h.w)*C,z:(h.j0+b+0.5)*C,nx:1,nz:0};
  if(h.side==='n') return {x:(h.i0+a+0.5)*C,z:h.j0*C,nx:0,nz:-1}; return {x:(h.i0+a+0.5)*C,z:(h.j0+h.d)*C,nx:0,nz:1}; }
function buildSidewalks(){
  if(sidewalkMesh) return; const pos=[], nor=[], uv=[], idx=[], {GRASS:GR}=WORLD;
  const inHouse=(t,x,z)=>t.houses.some(h=>x>h.i0*CELL-0.9&&x<(h.i0+h.w)*CELL+0.9&&z>h.j0*CELL-0.9&&z<(h.j0+h.d)*CELL+0.9);
  const clear=(t,a,b)=>{ const L=Math.hypot(b[0]-a[0],b[1]-a[1]); for(let s=0.6;s<L-0.3;s+=0.5){ const k=s/L; if(inHouse(t,a[0]+(b[0]-a[0])*k,a[1]+(b[1]-a[1])*k)) return false; } return true; };
  const quad=(a,b,y,v0)=>{ const dx=b[0]-a[0], dz=b[1]-a[1], L=Math.hypot(dx,dz); if(L<0.05) return v0; const sx=-dz/L*WALK_W/2, sz=dx/L*WALK_W/2, o=pos.length/3, v1=v0+L/1.6;
    pos.push(a[0]+sx,y,a[1]+sz, a[0]-sx,y,a[1]-sz, b[0]+sx,y,b[1]+sz, b[0]-sx,y,b[1]-sz); for(let q=0;q<4;q++) nor.push(0,1,0); uv.push(0,v0,1,v0,0,v1,1,v1);
    const up=(A,B,Cc)=>{ const ax=pos[B*3]-pos[A*3], az=pos[B*3+2]-pos[A*3+2], cx=pos[Cc*3]-pos[A*3], cz=pos[Cc*3+2]-pos[A*3+2]; return az*cx-ax*cz>0; };
    const t1=[o,o+2,o+1], t2=[o+1,o+2,o+3]; [t1,t2].forEach(tr=>{ if(!up(...tr)) tr.reverse(); idx.push(...tr); });
    for(let s=0;s<=L;s+=1) for(const off of [-0.8,0,0.8]){ const c=worldCell(a[0]+dx*s/L-dz/L*off,a[1]+dz*s/L+dx/L*off); if(c>=0) GR[c]=0; } // no grass on the path
    return v1; };
  for(const t of TOWNS){ const Ls=t.streetL, y=t.h+0.045;
    // a sidewalk down each side of both streets
    for(const X of [true,false]) for(const sd of [-1,1]){ const off=sd*(ROAD_HW+WALK_W/2), a=X?[t.x-Ls,t.z+off]:[t.x+off,t.z-Ls], b=X?[t.x+Ls,t.z+off]:[t.x+off,t.z+Ls]; quad(a,b,y,0); SIDEWALKS.push([a,b]); }
    // and a front path from every door straight out to the sidewalk of the street it faces
    for(const h of t.houses){ const D=doorOf(h), a=[D.x+D.nx*0.14,D.z+D.nz*0.14], X=h.side==='n'||h.side==='s', across=X?a[1]-t.z:a[0]-t.x, edge=Math.sign(across)*(ROAD_HW+WALK_W-0.1);
      const b=X?[a[0],t.z+edge]:[t.x+edge,a[1]]; quad(a,b,y+0.002,0); SIDEWALKS.push([a,b]); } }
  const g=new THREE.BufferGeometry(); g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3)); g.setAttribute('normal',new THREE.Float32BufferAttribute(nor,3)); g.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2)); g.setIndex(idx); g.computeBoundingSphere();
  sidewalkMesh=new THREE.Mesh(g,new THREE.MeshLambertMaterial({map:walkTex,polygonOffset:true,polygonOffsetFactor:-2,polygonOffsetUnits:-7})); sidewalkMesh.receiveShadow=true; sidewalkMesh.matrixAutoUpdate=false; scene.add(sidewalkMesh);
}
