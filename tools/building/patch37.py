# ---------- 37. furniture: sofas, dining sets, bookshelves, kitchens and beds in the houses, farmable for wood ----------
rep("  rock:{hp:360,mat:'brick',per:[7,10],snd:'stone'},","  rock:{hp:360,mat:'brick',per:[7,10],snd:'stone'}, furn:{hp:160,mat:'wood',per:[4,7],snd:'chop'},")
rep("  } else if(p.kind==='rock'){\n    propPart(rockGeo(","""  } else if(p.kind==='furn'){ const F=[0x6b7f99,0x9a5f4a,0x7d8c5a,0x8a6fa0][q()*4|0], wood=0x8a5a36, dk=0x5e3d24;
    if(variant===0){ // sofa: base, cushions, back, arms, little legs
      propPart(rbox(2.0,0.32,0.86,0.06),F,g,0,0.3,0,0,0,0,0); for(const x of [-0.48,0.48]) propPart(rbox(0.92,0.14,0.7,0.06),F,g,x,0.52,-0.05,0,0,0,0);
      propPart(rbox(2.0,0.52,0.2,0.07),F,g,0,0.66,0.33,0,0,0,0); for(const x of [-0.92,0.92]) propPart(rbox(0.18,0.62,0.86,0.07),F,g,x,0.46,0,0,0,0,0);
      for(const x of [-0.9,0.9]) for(const z of [-0.36,0.36]) propPart(new THREE.CylinderGeometry(0.03,0.03,0.14,6),dk,g,x,0.07,z,0,0,0,0);
      propPart(rbox(0.4,0.36,0.12,0.05),0xe8dcc0,g,-0.62,0.72,0.18,-0.2,0,0,0); }
    else if(variant===1){ // dining table with four chairs
      propPart(rbox(1.6,0.06,0.9,0.02),wood,g,0,0.76,0,0,0,0,0); for(const x of [-0.72,0.72]) for(const z of [-0.37,0.37]) propPart(rbox(0.06,0.73,0.06,0.01),dk,g,x,0.37,z,0,0,0,0);
      for(const [x,z,r] of [[-0.4,-0.68,0],[0.4,-0.68,0],[-0.4,0.68,Math.PI],[0.4,0.68,Math.PI]]){ const c=new THREE.Group(); c.position.set(x,0,z); c.rotation.y=r; g.add(c);
        propPart(rbox(0.44,0.05,0.42,0.02),wood,c,0,0.45,0,0,0,0,0); propPart(rbox(0.44,0.5,0.05,0.02),wood,c,0,0.72,0.19,0,0,0,0); for(const a of [-0.18,0.18]) for(const b of [-0.17,0.17]) propPart(rbox(0.04,0.44,0.04,0.01),dk,c,a,0.22,b,0,0,0,0); } }
    else if(variant===2){ // bookshelf full of books
      propPart(rbox(1.2,2.0,0.36,0.02),wood,g,0,1.0,0.02,0,0,0,0); propPart(rbox(1.1,1.9,0.04,0.01),dk,g,0,1.0,-0.14,0,0,0,0);
      for(let k=0;k<5;k++){ const y=0.12+k*0.42; propPart(rbox(1.1,0.03,0.32,0.01),wood,g,0,y,0,0,0,0,0); let x=-0.5; while(x<0.48){ const bw=0.04+q()*0.05, bh=0.22+q()*0.12; propPart(rbox(bw,bh,0.22,0.005),[0x8a2a2a,0x2f5d8a,0x3f7a3a,0xd9b24a,0x6b3f8a,0xe0ddd5][q()*6|0],g,x+bw/2,y+0.015+bh/2,-0.02,0,0,q()<0.1?0.2:0,0); x+=bw+0.005; } } }
    else if(variant===3){ // kitchen: counter with a worktop and doors, a sink, and a tall fridge at the end
      propPart(rbox(1.6,0.86,0.6,0.02),0xe8e4da,g,-0.25,0.43,0,0,0,0,0); propPart(rbox(1.66,0.05,0.64,0.01),0x3a3d42,g,-0.25,0.885,-0.01,0,0,0,0);
      for(const x of [-0.85,-0.45,-0.05,0.35]) propPart(rbox(0.36,0.7,0.02,0.01),0xd9d4c8,g,x,0.43,-0.31,0,0,0,0);
      propPart(rbox(0.5,0.04,0.36,0.02),0xa9b0b8,g,-0.4,0.91,0,0,0,0,0); propPart(rbox(0.72,1.8,0.66,0.06),0xf2f2ee,g,0.92,0.9,0,0,0,0,0); propPart(rbox(0.03,0.4,0.03,0.01),0x9aa0a6,g,0.62,1.2,-0.34,0,0,0,0); }
    else { // bed: frame, mattress, blanket, pillows, headboard
      propPart(rbox(1.5,0.3,2.1,0.04),wood,g,0,0.2,0,0,0,0,0); propPart(rbox(1.42,0.2,2.0,0.08),0xf4f1ea,g,0,0.44,0,0,0,0,0); propPart(rbox(1.46,0.06,1.35,0.03),F,g,0,0.55,-0.32,0,0,0,0);
      for(const x of [-0.35,0.35]) propPart(rbox(0.55,0.14,0.36,0.07),0xffffff,g,x,0.6,0.78,0,0,0,0); propPart(rbox(1.56,0.9,0.08,0.03),dk,g,0,0.6,1.06,0,0,0,0); }
  } else if(p.kind==='rock'){
    propPart(rockGeo(""")
rep("  if(p.kind==='rock'){ const a=1.05*s, c=.9*s; return [[x-a,0,z-c,x+a,1.35*s,z+c]]; }","""  if(p.kind==='rock'){ const a=1.05*s, c=.9*s; return [[x-a,0,z-c,x+a,1.35*s,z+c]]; }
  if(p.kind==='furn'){ const E=[[1.0,0.95,0.45],[0.8,0.8,0.85],[0.6,2.0,0.2],[1.3,1.8,0.33],[0.75,0.7,1.08]][p.ft||0], q=Math.abs(Math.sin(p.g.rotation.y))>0.7, ex=q?E[2]:E[0], ez=q?E[0]:E[2], o=p.ft===3?0.33:0; // (the kitchen is off-centre: the fridge end)
    const ox=q?0:o*Math.cos(p.g.rotation.y), oz=q?-o*Math.sin(p.g.rotation.y):0; return [[x-ex+ox,0,z-ez+oz,x+ex+ox,E[1],z+ez+oz]]; }""")
rep("  yardTrees(add,r);\n","  yardTrees(add,r);\n  houseFurniture(add);\n")
rep("function yardTrees(add,r){","""// furniture in the inner corners of each house's ground floor (not where the stairs are), backs to the wall
function houseFurniture(add){ for(const t of TOWNS){ if(!t.houses.length) planHouses(t);
  for(const h of t.houses){ const q=seeded(t.seed+h.id*131+7), C=CELL, IN=WT/2+0.12, x0=h.i0*C+IN, x1=(h.i0+h.w)*C-IN, z0=h.j0*C+IN, z1=(h.j0+h.d)*C-IN;
    const stairs=h.floors>1?houseStair(h).cells:[], inStair=(x,z)=>stairs.some(([i,j])=>x>i*C-0.3&&x<(i+1)*C+0.3&&z>j*C-0.3&&z<(j+1)*C+0.3);
    const SZ=[[2.0,0.9],[1.6,1.7],[1.2,0.4],[2.6,0.66],[1.5,2.16]], picks=h.floors>1?[0,1,2,3]:[0,3,4,1,2]; let n=0;
    for(const [cx,cz,sx,sz] of [[x0,z0,1,1],[x1,z0,-1,1],[x0,z1,1,-1],[x1,z1,-1,-1]]){ if(n>=3) break;
      const ft=picks[(n+(q()*2|0))%picks.length]; n++; const [W,D]=SZ[ft];
      // back against the side wall (the one that isn't the front), running along it
      const side=h.side==='n'||h.side==='s'; // front wall runs along x: put the item against the x-facing (side) wall
      let x,z,yaw; if(side){ x=cx+sx*(D/2+0.05); z=cz+sz*(W/2+0.1); yaw=Math.atan2(-sx,0); } else { x=cx+sx*(W/2+0.1); z=cz+sz*(D/2+0.05); yaw=Math.atan2(0,-sz); }
      if(inStair(x,z)||inStair(x+(side?0:sx*W/2),z+(side?sz*W/2:0))) continue;
      const p=add('furn',x,z,1,yaw); p.ft=ft; p.yard=true; p.g.children[0].geometry=propVariant('furn',ft).geo; p.boxes=propBoxes(p); } } } }
function yardTrees(add,r){""")
rep("  const g=new THREE.Group(); g.position.set(p.x,0,p.z); g.rotation.y=r()*Math.PI*2; const v=propVariant(p.kind,p.id%8);","  const g=new THREE.Group(); g.position.set(p.x,0,p.z); g.rotation.y=r()*Math.PI*2; const v=propVariant(p.kind,p.kind==='furn'?0:p.id%8);")
# not dots on the minimap
rep("propsNear(ox,oz,[],Math.ceil(R/PCELL)+1).forEach(p=>{ const px=tx(p.x), pz=tz(p.z); if(px<-4||pz<-4||px>S+4||pz>S+4) return;","propsNear(ox,oz,[],Math.ceil(R/PCELL)+1).forEach(p=>{ if(p.kind==='furn') return; const px=tx(p.x), pz=tz(p.z); if(px<-4||pz<-4||px>S+4||pz>S+4) return;")
rep("byKind={tree:[],pine:[],rock:[],car:[]}","byKind={tree:[],pine:[],rock:[],car:[],furn:[]}")
