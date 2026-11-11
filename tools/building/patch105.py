# ---------- 105. every town is its own place: a theme for its houses (materials, colours, storeys, spacing, garages)
# and a landmark on a lot of its own that you can spot from far off ----------
rep("function planHouses(t){","""const TOWN_THEME=[
  {w:0.3,b:0.3,two:0.25,gap:1,set:2,gar:0.6,paint:{siding:[5,0],panel:[0,1,3]}},      // Rustwood: sheet-metal works town, water tower
  {w:1,b:1,two:0.7,gap:1,set:2,gar:0.3,paint:{siding:[1,4,0]}},                       // Pebble Point: blue and white clapboard, lighthouse
  {w:0.5,b:0.85,two:0.55,gap:1,set:2,gar:0.42},                                       // Kettle Creek: a bit of everything, the big kettle
  {w:0.05,b:0.97,two:0.92,gap:1,set:2,gar:0.1,paint:{stucco:[0,1,2]}},                // Lantern Row: tall stucco row houses, clock tower
  {w:0.85,b:1,two:0.3,gap:2,set:2,gar:0.35,paint:{siding:[2,0,4]}},                   // Mossy Mill: green cottages spread out, windmill
  {w:0.55,b:1,two:0.5,gap:1,set:3,gar:0.3},                                           // Hollow Hill: set well back from the street, radio mast
  {w:0,b:0.5,two:0.2,gap:1,set:2,gar:0.5,paint:{stucco:[3],panel:[1,2]}},             // Cinder Flats: dark low works housing, smokestack
  {w:0.9,b:1,two:0.45,gap:2,set:2,gar:0.5,paint:{siding:[3,5,0]}},                    // Brambleford: yellow and red farm houses, silos
  {w:0,b:0.6,two:0.8,gap:1,set:2,gar:0.3,paint:{stucco:[1,3],panel:[2,3]}},           // Copper Ridge: tall brick and steel, copper dome
  {w:0.6,b:1,two:0.5,gap:2,set:2,gar:0.6,paint:{siding:[0,1,2,3],stucco:[0,2]}} ];    // Willow Bend: pastel suburb, bandstand
function planHouses(t){""")
rep("  const shapes=[[2,2],[3,2],[2,3]]; let k=0;","""  const TH=TOWN_THEME[TOWNS.indexOf(t)%TOWN_THEME.length];
  { const pr=seeded(t.seed+31337), quads=[[1,1],[-1,1],[1,-1],[-1,-1]]; for(let q=3;q>0;q--){ const j=Math.floor(pr()*(q+1)); [quads[q],quads[j]]=[quads[j],quads[q]]; }
    t.poi=null; const SEA_=WGEN.sea();
    if(SEA_&&TOWNS.indexOf(t)===0){ let s_=50; while(s_<260&&terrainH(t.x+SEA_.nx*s_,t.z+SEA_.nz*s_)>SEA_.Y+1.1) s_+=2; const x=t.x+SEA_.nx*(s_-3), z=t.z+SEA_.nz*(s_-3); t.poi={x,z,y:terrainH(x,z)+1.2,shore:true}; } // the lighthouse stands on the shore
    else for(const [sx,sz] of quads){ const i0=ci+(sx>0?2:-5), j0=cj+(sz>0?2:-5); if(!free(i0,j0,3,3)||!inTown(i0,j0,3,3)) continue;
      for(let p=0;p<3;p++) for(let q=0;q<3;q++) used.add(key(i0+p,j0+q)); t.poi={x:(i0+1.5)*CELL,z:(j0+1.5)*CELL};
      for(let u=-7.4;u<=7.4;u+=0.8) for(let w=-7.4;w<=7.4;w+=0.8){ const c=worldCell(t.poi.x+u,t.poi.z+w); if(c>=0) WORLD.GRASS[c]=0; } break; } }
  const shapes=[[2,2],[3,2],[2,3]]; let k=0;""")
rep("front=sd>0?2:-2-deep; // a front-yard row","front=sd>0?TH.set:-TH.set-deep; // a front-yard row")
rep("const m=r(), mat=m<0.5?'wood':m<0.85?'brick':'metal', roof=r()<0.6?'brick':'wood', floors=r()<0.55?2:1;","const m=r(), mat=m<TH.w?'wood':m<TH.b?'brick':'metal', roof=r()<0.6?'brick':'wood', floors=r()<TH.two?2:1;")
rep("skin:{style,paint:Math.floor(rs()*HOUSE_PAINT[style].length),roof:Math.floor(rs()*4)}});","skin:{style,paint:TH.paint&&TH.paint[style]?TH.paint[style][Math.floor(rs()*TH.paint[style].length)]:Math.floor(rs()*HOUSE_PAINT[style].length),roof:Math.floor(rs()*4)}});")
rep("        if(gr()<0.42){ const X_=","        if(gr()<TH.gar){ const X_=")
rep("      s+=along+1; } }\n  t.houses=out; return out;","      s+=along+TH.gap; } }\n  t.houses=out; return out;")
rep("function buildRails(){","""/* Landmarks: one per town, built from plain shapes in one mesh, solid where you'd expect. */
let _lmBuilt=false;
function buildLandmarks(){ if(_lmBuilt) return; _lmBuilt=true; const col=new THREE.Color();
  TOWNS.forEach((t,k)=>{ const L=t.poi; if(!L) return; let parts=[]; const Y0=L.y!=null?L.y:t.h;
    const put=(g,c,x,y,z,rot)=>{ if(rot){ if(rot[0]) g.rotateX(rot[0]); if(rot[2]) g.rotateZ(rot[2]); if(rot[1]) g.rotateY(rot[1]); } g.translate(x,y,z); if(g.index) g=g.toNonIndexed(); g.computeVertexNormals(); col.setHex(c);
      const n=g.attributes.position.count, ca=new Float32Array(n*3); for(let q=0;q<n;q++){ ca[q*3]=col.r; ca[q*3+1]=col.g; ca[q*3+2]=col.b; } g.setAttribute('color',new THREE.BufferAttribute(ca,3)); parts.push(g); };
    const box=(w,h,d,x,y,z,c,rot)=>put(new THREE.BoxGeometry(w,h,d),c,x,y+h/2,z,rot);
    const cyl=(rt,rb,h,x,y,z,c,seg,rot)=>put(new THREE.CylinderGeometry(rt,rb,h,seg||16),c,x,y+h/2,z,rot);
    const sph=(r,x,y,z,c)=>put(new THREE.SphereGeometry(r,16,12),c,x,y,z);
    const solid=(x0,z0,x1,z1,h)=>{ const nx=Math.max(1,Math.ceil((x1-x0)/2.4)), nz=Math.max(1,Math.ceil((z1-z0)/2.4));
      for(let a=0;a<nx;a++) for(let b=0;b<nz;b++){ const xa=L.x+x0+(x1-x0)*a/nx, xb=L.x+x0+(x1-x0)*(a+1)/nx, za=L.z+z0+(z1-z0)*b/nz, zb=L.z+z0+(z1-z0)*(b+1)/nz;
        STATICS.push({x:(xa+xb)/2,z:(za+zb)/2,solid:{boxes:[[xa,Y0-2.5,za,xb,Y0+h,zb]],key:'lm'+STATICS.length}}); } };
    const disc=(x,z,r,h)=>{ const n=Math.max(2,Math.ceil(r*2/0.7)); for(let q=0;q<n;q++){ const xa=-r+2*r*q/n, xb=-r+2*r*(q+1)/n, xm=(xa+xb)/2, hd=Math.sqrt(Math.max(0.01,r*r-xm*xm)); solid(x+xa,z-hd,x+xb,z+hd,h); } }; // a round footprint, in strips
    const flush=(spin)=>{ if(!parts.length) return; const pos=[],nor=[],cc=[]; parts.forEach(g=>{ pos.push(...g.attributes.position.array); nor.push(...g.attributes.normal.array); cc.push(...g.attributes.color.array); }); parts=[];
      const g=new THREE.BufferGeometry(); g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3)); g.setAttribute('normal',new THREE.Float32BufferAttribute(nor,3)); g.setAttribute('color',new THREE.Float32BufferAttribute(cc,3)); g.computeBoundingSphere();
      const m=new THREE.Mesh(g,new THREE.MeshLambertMaterial({vertexColors:true})); m.castShadow=m.receiveShadow=true; m.position.set(L.x,Y0,L.z);
      if(spin){ m.position.set(L.x+spin[0],Y0+spin[1],L.z+spin[2]); m.onBeforeRender=()=>{ m.rotation.z=performance.now()*0.00035; }; } else { m.updateMatrix(); m.matrixAutoUpdate=false; } scene.add(m); return m; };
    if(L.shore){ cyl(5.7,6.6,2.6,0,-2.6,0,0x8f8a80,22); cyl(5.3,5.7,0.22,0,-0.02,0,0xb9b3a4,22); disc(0,0,5.5,0.2); } // a stone base out on the shore
    else { box(13.4,0.1,13.4,0,0,0,0xb9b3a4); box(12.6,0.14,12.6,0,0,0,0xcfc9ba); } // a paved lot
    const kind=k===0?1:k===1?0:k%10; // the coastal town gets the lighthouse
    if(kind===0||kind===99){ // water tower
      for(const [sx,sz] of [[1,1],[-1,1],[1,-1],[-1,-1]]){ cyl(0.16,0.24,9.2,sx*2.3,0,sz*2.3,0x6e5a4c,8); solid(sx*2.3-0.35,sz*2.3-0.35,sx*2.3+0.35,sz*2.3+0.35,9.2); } solid(-0.4,-0.4,0.4,0.4,9.2); solid(-0.35,3.2,0.35,3.6,9.3);
      for(const y of [3,6]){ box(4.6,0.14,0.14,0,y,2.3,0x6e5a4c); box(4.6,0.14,0.14,0,y,-2.3,0x6e5a4c); box(0.14,0.14,4.6,2.3,y,0,0x6e5a4c); box(0.14,0.14,4.6,-2.3,y,0,0x6e5a4c); }
      cyl(3.5,3.5,0.3,0,9.1,0,0x5d4b40); cyl(3.3,3.3,4.2,0,9.4,0,0xa8533a); cyl(3.36,3.36,0.35,0,10.3,0,0x7c3b2a); cyl(3.36,3.36,0.35,0,12.4,0,0x7c3b2a);
      cyl(0.25,3.5,1.7,0,13.6,0,0x8a4631); sph(0.3,0,15.4,0,0xd9d4c8); box(0.5,9.3,0.08,0,0,3.4,0x57483e); cyl(0.3,0.3,9.2,0,0,0,0x57483e,8);
    } else if(kind===1){ // lighthouse
      const R=y=>2.7-1.25*y/14; for(let s=0;s<4;s++) cyl(R((s+1)*3.5),R(s*3.5),3.5,0,s*3.5,0,s%2?0xc8443c:0xf2efe6,18);
      cyl(2.3,2.3,0.3,0,14,0,0x3a3f46); for(let a=0;a<12;a++) cyl(0.05,0.05,1,Math.cos(a*0.5236)*2.2,14.3,Math.sin(a*0.5236)*2.2,0x3a3f46,6); cyl(2.25,2.25,0.08,0,15.25,0,0x3a3f46);
      cyl(1.25,1.25,2.1,0,14.3,0,0xfff0a8,12); cyl(0.15,1.75,1.5,0,16.4,0,0xc8443c,12); sph(0.28,0,18,0,0x3a3f46); box(1.1,2.1,0.2,0,0,2.62,0x4a3a30); disc(0,0,2.9,14);
    } else if(kind===2){ // the big kettle
      cyl(0.45,0.7,7,0,0,0,0x8f959c,12); cyl(1.6,0.5,0.6,0,6.9,0,0x8f959c,12); cyl(2.9,2.3,0.9,0,7.5,0,0xd8392f); cyl(3.1,2.9,1.6,0,8.4,0,0xe04436); cyl(2.2,3.1,1.3,0,10,0,0xd8392f);
      cyl(0.9,2.2,0.5,0,11.3,0,0x2e3238); sph(0.4,0,12,0,0x2e3238); cyl(0.3,0.55,3,3.4,8.6,0,0xd8392f,10,[0,0,-0.75]); put(new THREE.TorusGeometry(1.7,0.17,8,18,Math.PI),0x2e3238,-0.2,11.3,0); disc(0,0,0.9,7);
    } else if(kind===3){ // clock tower with lanterns
      box(3.6,1.2,3.6,0,0,0,0x9a9388); box(3.1,11.5,3.1,0,1.2,0,0xd9cdb4); box(3.7,0.45,3.7,0,12.7,0,0x9a9388); box(2.6,2.2,2.6,0,13.15,0,0xd9cdb4); cyl(0.05,2.6,3.2,0,15.35,0,0x3e4a5a,4,[0,Math.PI/4,0]); sph(0.22,0,18.7,0,0xe3c04a);
      for(const [x,z,ry] of [[0,1.58,0],[0,-1.58,0],[1.58,0,1],[-1.58,0,1]]){ cyl(1.05,1.05,0.1,x,10,z,0xf6f2e6,20,ry?[0,0,Math.PI/2]:[Math.PI/2,0,0]); box(ry?0.14:0.09,0.8,ry?0.09:0.14,x*1.04,10.5,z*1.04,0x22262c); box(ry?0.14:0.5,0.09,ry?0.5:0.14,x*1.04+(ry?0:0.22),10.5,z*1.04+(ry?0.22:0),0x22262c); }
      box(1,2.2,0.15,0,1.2,1.56,0x4a3a30); for(const [x,z] of [[5,5],[-5,5],[5,-5],[-5,-5]]){ cyl(0.07,0.1,3.2,x,0,z,0x22262c,8); box(0.42,0.5,0.42,x,3.2,z,0xffd98a); cyl(0.05,0.34,0.25,x,3.7,z,0x22262c,4,[0,Math.PI/4,0]); solid(x-0.22,z-0.22,x+0.22,z+0.22,3.6); }
      solid(-1.95,-1.95,1.95,1.95,13);
    } else if(kind===4){ // windmill
      cyl(1.9,3.1,9.5,0,0,0,0xe9e1cc,8); cyl(0.2,2.3,2,0,9.5,0,0x6b4a32,8); box(1.1,2.1,0.2,0,0,2.9,0x5a3d28); box(0.9,0.9,0.15,0,5,2.35,0x9fc4d8); cyl(0.3,0.3,1.4,0,9.2,2,0x5a3d28,8,[Math.PI/2,0,0]); disc(0,0,3.3,9.5);
      flush(); for(let b=0;b<4;b++){ const a=b*Math.PI/2+0.3, g1=new THREE.BoxGeometry(0.16,7,0.12); g1.translate(0,3.6,0); g1.rotateZ(a); put(g1,0x5a3d28,0,0,0); const g2=new THREE.BoxGeometry(1.3,5,0.06); g2.translate(0.7,4.4,0); g2.rotateZ(a); put(g2,0xf3ecd8,0,0,0); }
      cyl(0.45,0.45,0.5,0,-0.25,0,0x5a3d28,10,[Math.PI/2,0,0]); flush([0,9.9,2.75]);
    } else if(kind===5){ // radio mast and its hut
      for(let s=0;s<6;s++){ const r0=1-0.13*s, r1=1-0.13*(s+1); cyl(r1,r0,4,0,s*4,0,s%2?0xf2efe6:0xd8392f,4,[0,Math.PI/4,0]); }
      cyl(0.04,0.06,3,0,24,0,0x8f959c,6); sph(0.28,0,27.1,0,0xff4a3a); for(const [y,ry] of [[17,0.4],[20,2.6]]) cyl(0.7,0.15,0.35,Math.sin(ry)*0.75,y,Math.cos(ry)*0.75,0xe8e6e0,12,[Math.PI/2,ry,0]);
      box(3.4,2.6,3,4.2,0,-3,0x8c8f8a); box(3.7,0.25,3.3,4.2,2.6,-3,0x55585c); box(0.9,1.9,0.12,4.2,0,-1.47,0x3a4a5a); solid(-1.15,-1.15,1.15,1.15,24); solid(2.35,-4.65,6.05,-1.35,2.85);
    } else if(kind===6){ // smokestack and boiler house
      cyl(1.3,2.3,19,-2.5,0,0,0x8a4a3a,14); cyl(1.42,1.42,0.9,-2.5,19,0,0x2e2a28,14); cyl(1.62,1.72,0.7,-2.5,14,0,0xe9e4d8,14); cyl(1.9,2,0.7,-2.5,9,0,0xe9e4d8,14);
      box(6,4.2,5.4,3,0,0,0x6e4438); box(6.4,0.3,5.8,3,4.2,0,0x35302e); box(1.6,2.4,0.14,3,0,2.72,0x2e2a28); for(const x of [1.2,4.8]) box(1,1,0.12,x,2.2,2.72,0xffd98a); cyl(0.35,0.35,2.6,-0.6,2.5,0,0x55585c,8,[0,0,Math.PI/2]);
      disc(-2.5,0,2.5,19); solid(-0.15,-2.85,6.15,2.85,4.5); solid(-2,-0.45,0.2,0.45,3);
    } else if(kind===7){ // grain silos
      for(const x of [-2.6,2.6]){ cyl(2.3,2.3,10,x,0,0,0xc3c9cf,18); for(const y of [2.5,5,7.5]) cyl(2.34,2.34,0.12,x,y,0,0x9aa1a8,18); sph(2.3,x,10,0,0xaeb5bc); cyl(0.2,0.2,0.6,x,12.2,0,0x8f959c,8); disc(x,0,2.5,11); }
      box(1.2,13.5,1.2,0,0,-2.6,0xb5483a); box(1.6,1.2,1.6,0,13.5,-2.6,0x8a3428); cyl(0.14,0.14,3.2,-1.3,13.2,-1.5,0x8f959c,8,[0.5,0,1.05]); cyl(0.14,0.14,3.2,1.3,13.2,-1.5,0x8f959c,8,[0.5,0,-1.05]); box(0.5,10,0.08,-2.6,0,2.33,0x6c7279); solid(-0.75,-3.35,0.75,-1.85,13.5);
    } else if(kind===8){ // copper-domed rotunda
      cyl(4.4,4.6,0.35,0,0,0,0xbdb5a4,10); cyl(3.9,4.1,0.35,0,0.35,0,0xcac2b0,10); cyl(2.6,2.6,5.2,0,0.7,0,0xd9cdb4,10); for(let a=0;a<10;a++) cyl(0.24,0.28,5.2,Math.cos(a*0.6283)*3.3,0.7,Math.sin(a*0.6283)*3.3,0xefe8d8,10);
      cyl(3.9,3.9,0.5,0,5.9,0,0xcac2b0,10); const dome=new THREE.SphereGeometry(3.5,18,10,0,Math.PI*2,0,Math.PI/2); put(dome,0x4fa58c,0,6.4,0); cyl(0.5,0.9,0.7,0,9.8,0,0x3f8a74,10); cyl(0.05,0.14,2.4,0,10.5,0,0xe3c04a,8); box(1.1,2.3,0.2,0,0.7,2.62,0x4a3a30); disc(0,0,4.6,0.35); disc(0,0,4.1,0.7); disc(0,0,3.7,6.4);
    } else { // bandstand
      cyl(3.6,3.8,0.4,0,0,0,0xcac2b0,8); for(let a=0;a<8;a++){ const x=Math.cos(a*0.7854+0.3927)*3.25, z=Math.sin(a*0.7854+0.3927)*3.25; cyl(0.11,0.13,2.7,x,0.4,z,0xf4f1ea,8); solid(x-0.2,z-0.2,x+0.2,z+0.2,3.1); } disc(0,0,3.75,0.4);
      cyl(3.7,3.7,0.22,0,3.1,0,0xf4f1ea,8); cyl(0.25,4.2,1.9,0,3.32,0,0x4f7d5c,8); sph(0.3,0,5.4,0,0xe3c04a); for(const z of [5.3,-5.3]){ box(2.2,0.1,0.55,0,0.5,z,0x7a5536); box(2.2,0.6,0.1,0,0.6,z+Math.sign(z)*0.25,0x7a5536); for(const x of [-0.9,0.9]) box(0.1,0.5,0.5,x,0,z,0x2e3238); solid(-1.15,z-0.35,1.15,z+0.4,z>0?1.2:1.2); }
      for(const [x,z] of [[5.2,0],[-5.2,0]]){ cyl(0.5,0.6,0.5,x,0,z,0x9a9388,10); sph(0.75,x,1,z,0x4f8a4a); disc(x,z,0.8,1.7); }
    }
    flush(); });
}
function buildRails(){""")
rep("syncMats(); buildRails();","syncMats(); buildRails(); buildLandmarks();")
rep("  g.setLineDash([]);\n  return c;","  g.setLineDash([]);\n  TOWNS.forEach(t=>{ if(!t.poi) return; const x=X(t.poi.x-SPAWN[0]), y=X(t.poi.z-SPAWN[2]), q=Math.max(4,7/mpp); g.fillStyle='#ffd24a'; g.strokeStyle='#3a2c10'; g.lineWidth=1.5; g.beginPath(); g.moveTo(x,y-q); g.lineTo(x+q,y); g.lineTo(x,y+q); g.lineTo(x-q,y); g.closePath(); g.fill(); g.stroke(); }); // landmarks\n  return c;")
