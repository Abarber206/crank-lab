# ---------- 97. breaking a build: the piece comes apart into big slabs of itself (in its own colour: house walls break as
# painted wall, not bare planks) that burst away from the hit, tumble, land on the floor it stood on and settle, on top of
# the small debris and dust; a nearby break kicks the camera ----------
rep("function shatterFx(p,point){\n  const c=pieceCenter(p); point=point||c;\n  if(c.distanceTo(P.pos)<70){",
    "function shatterFx(p,point){\n  const c=pieceCenter(p); point=point||c;\n  if(c.distanceTo(P.pos)<70){ slabsFor(p,point); if(c.distanceTo(P.pos)<7) shake=Math.max(shake,0.07);")
rep("// pieces of the actual material: planks for wood, bricks for brick, panels for metal, scattered from the whole piece",
r"""// the piece itself in big pieces: a wall as its nine tiles, a floor / stair / roof as four quarters
const slabGeos={}, slabMats=new Map();
function slabMat(p){ const base=p.group&&p.group.children.find(m=>m.isMesh&&m.userData.piece===p); if(!p.skin) return matFor[p.mat][p.type==='wall'?'wall':'floor'];
  const hex=base&&base.material.color?base.material.color.getHex():0xcfc8b8, k=p.type==='cone'?'r'+hex:'h'+hex; let m=slabMats.get(k); if(!m){ m=new THREE.MeshLambertMaterial({color:hex}); slabMats.set(k,m); } return m; }
function slabsFor(p,origin){ const bb=pieceAABB(p), mat=slabMat(p), wall=p.type==='wall', X=p.axis==='x', out=[];
  if(wall){ const tw=CELL/3, th=LVL/3, key='w'+(X?'x':'z'), geo=slabGeos[key]||(slabGeos[key]=X?new THREE.BoxGeometry(WT,th,tw):new THREE.BoxGeometry(tw,th,WT)), mask=p.mask==null?511:p.mask;
    for(let r=0;r<3;r++) for(let c2=0;c2<3;c2++){ if(!(mask>>(r*3+c2)&1)) continue; const y=p.l*LVL+(r+.5)*th, h=(c2+.5)*tw; out.push([geo,X?p.i*CELL:p.i*CELL+h,y,X?p.j*CELL+h:p.j*CELL]); } }
  else { const geo=slabGeos.f||(slabGeos.f=new THREE.BoxGeometry(CELL/2,FT,CELL/2)), cx=(bb[0]+bb[3])/2, cz=(bb[2]+bb[5])/2, y=p.type==='floor'?(bb[1]+bb[4])/2:bb[1]+(bb[4]-bb[1])*0.5;
    for(const [a,b] of [[-1,-1],[1,-1],[-1,1],[1,1]]) out.push([geo,cx+a*CELL/4,y,cz+b*CELL/4]); }
  const fy=wall?p.l*LVL+0.06:null;
  for(const [geo,x,y,z] of out){ const m=getMesh(geo,mat); m.scale.set(1,1,1); m.position.set(x,y,z); m.rotation.set(0,0,0);
    const v=new THREE.Vector3(x-origin.x,(y-origin.y)*0.5,z-origin.z), d=Math.max(0.6,v.length()); v.normalize().multiplyScalar(5.5/d+1.2+Math.random()*1.2); v.y+=1.6+Math.random()*1.6;
    if(wall){ const n=X?'x':'z', s=Math.sign(origin[n]-(X?p.i*CELL:p.j*CELL)||((Math.random()<.5)?1:-1)); v[n]-=s*(1.5+Math.random()*2.5); } // a wall blows away from whoever hit it
    spawnChunk(m,v,1.5+Math.random()*0.9,3.2); if(fy!=null) chunks[chunks.length-1].fy=fy; } }
// pieces of the actual material: planks for wood, bricks for brick, panels for metal, scattered from the whole piece""")
rep("    const gy=terrainH(c.m.position.x,c.m.position.z)+0.05;\n    if(c.m.position.y<gy){ c.m.position.y=gy; c.v.y*=-.3; c.v.x*=.6; c.v.z*=.6; c.w.multiplyScalar(0.6); }",
    "    const gy=Math.max(terrainH(c.m.position.x,c.m.position.z)+0.05,c.fy||-1e9);\n    if(c.m.position.y<gy){ c.m.position.y=gy; if(c.fy!=null&&c.v.y<-3&&!c.hitS&&c.m.position.distanceTo(P.pos)<25){ c.hitS=1; sfxAt('knock_small',c.m.position); } c.v.y*=-.3; c.v.x*=.6; c.v.z*=.6; c.w.multiplyScalar(0.5); if(c.fy!=null&&Math.abs(c.v.y)<1.2){ c.v.y=0; c.w.multiplyScalar(0.3); } }")
rep("    case 'rb_tick':","    case 'knock_small': knock(260+Math.random()*240,0.05,0.16,4); break;\n    case 'rb_tick':")
