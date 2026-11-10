# ---------- 116. houses have real rooms: the back of each floor is walled into separate rooms, each with its own doorway,
# and every room is one thing (living room, kitchen, bedroom, bathroom, study) holding only what belongs there ----------
rep("const fv=variant%10, sty=Math.floor(variant/10)%6,","const fv=variant%20, sty=Math.floor(variant/20)%6,")
rep("    else { // bed: frame, mattress, blanket, pillows, headboard",r"""    else if(fv===10){ // cooker: hob, oven door, knobs, and an extractor hood on the wall above
      propPart(rbox(0.76,0.88,0.62,0.02),0xe9e9e4,g,0,0.44,0.01,0,0,0,0); propPart(rbox(0.78,0.03,0.64,0.01),0x1c1e22,g,0,0.895,0,0,0,0,0);
      for(const [x,z] of [[-0.19,-0.14],[0.19,-0.14],[-0.19,0.16],[0.19,0.16]]){ propPart(new THREE.CylinderGeometry(0.1,0.1,0.02,14),0x3a3d42,g,x,0.915,z,0,0,0,0); propPart(new THREE.CylinderGeometry(0.05,0.05,0.022,10),0x16181b,g,x,0.917,z,0,0,0,0); }
      propPart(rbox(0.6,0.42,0.02,0.01),0x23262b,g,0,0.38,-0.305,0,0,0,0); propPart(rbox(0.56,0.03,0.04,0.01),0xb9c0c8,g,0,0.65,-0.33,0,0,0,0);
      for(const x of [-0.27,-0.09,0.09,0.27]) propPart(new THREE.CylinderGeometry(0.028,0.028,0.035,10),0x2a2d33,g,x,0.79,-0.315,Math.PI/2,0,0,0);
      propPart(rbox(0.78,0.12,0.5,0.02),0xb9c0c8,g,0,1.74,0.07,0,0,0,0); propPart(rbox(0.3,0.44,0.26,0.02),0xa9b0b8,g,0,2.02,0.18,0,0,0,0); }
    else if(fv===11){ // toilet: cistern, bowl, seat
      const W_=0xf3f3ef; propPart(rbox(0.44,0.4,0.2,0.04),W_,g,0,0.62,0.27,0,0,0,0); propPart(rbox(0.47,0.04,0.23,0.015),W_,g,0,0.835,0.27,0,0,0,0); propPart(new THREE.CylinderGeometry(0.025,0.025,0.03,10),0xb9c0c8,g,0.1,0.865,0.27,0,0,0,0);
      propPart(rbox(0.26,0.4,0.2,0.04),W_,g,0,0.2,0.12,0,0,0,0);
      const bowl=new THREE.CylinderGeometry(0.2,0.12,0.4,18); bowl.scale(1,1,1.3); propPart(bowl,W_,g,0,0.2,-0.08,0,0,0,0);
      const seat=new THREE.CylinderGeometry(0.22,0.22,0.035,20); seat.scale(1,1,1.3); propPart(seat,0xe6e6e0,g,0,0.418,-0.08,0,0,0,0);
      const pan=new THREE.CylinderGeometry(0.14,0.14,0.012,18); pan.scale(1,1,1.35); propPart(pan,0x8fb9cc,g,0,0.434,-0.08,0,0,0,0); }
    else if(fv===12){ // bath: a tub with a rim, water in it, taps at one end
      const W_=0xf3f3ef; propPart(rbox(1.7,0.2,0.78,0.05),W_,g,0,0.1,0,0,0,0,0); for(const z of [-0.345,0.345]) propPart(rbox(1.7,0.42,0.09,0.04),W_,g,0,0.37,z,0,0,0,0); for(const x of [-0.8,0.8]) propPart(rbox(0.1,0.42,0.78,0.04),W_,g,x,0.37,0,0,0,0,0);
      propPart(rbox(1.52,0.02,0.62,0.005),0x9fd0e0,g,0,0.44,0,0,0,0,0);
      propPart(new THREE.CylinderGeometry(0.02,0.02,0.16,8),0xb9c0c8,g,0.8,0.66,0,0,0,0,0); propPart(rbox(0.14,0.03,0.04,0.01),0xb9c0c8,g,0.74,0.74,0,0,0,0,0); for(const z of [-0.1,0.1]) propPart(new THREE.CylinderGeometry(0.03,0.03,0.04,8),0xb9c0c8,g,0.8,0.6,z,0,0,0,0);
      propPart(rbox(0.5,0.02,0.3,0.01),F,g,-0.5,0.585,-0.345,0,0,0.0,0); } // a towel over the side
    else if(fv===13){ // washstand: cupboard, basin and tap, a mirror on the wall
      const W_=0xf3f3ef; propPart(rbox(0.9,0.8,0.48,0.02),wood,g,0,0.4,0.01,0,0,0,0); for(const x of [-0.22,0.22]){ propPart(rbox(0.4,0.62,0.02,0.01),dk,g,x,0.4,-0.235,0,0,0,0); propPart(rbox(0.02,0.12,0.02,0.005),0xb9c0c8,g,x*0.3,0.5,-0.25,0,0,0,0); }
      propPart(rbox(0.94,0.05,0.52,0.015),W_,g,0,0.825,0,0,0,0,0);
      const bs=new THREE.CylinderGeometry(0.2,0.15,0.07,18); bs.scale(1.25,1,0.85); propPart(bs,W_,g,0,0.885,-0.04,0,0,0,0); const bw=new THREE.CylinderGeometry(0.16,0.16,0.01,18); bw.scale(1.25,1,0.85); propPart(bw,0xbcd9e4,g,0,0.922,-0.04,0,0,0,0);
      propPart(new THREE.CylinderGeometry(0.016,0.016,0.16,8),0xb9c0c8,g,0,0.93,0.18,0,0,0,0); propPart(rbox(0.03,0.025,0.12,0.008),0xb9c0c8,g,0,1.0,0.13,0,0,0,0);
      propPart(rbox(0.76,0.86,0.02,0.01),dk,g,0,1.55,0.25,0,0,0,0); propPart(rbox(0.68,0.78,0.02,0.005),0xb7d0de,g,0,1.55,0.238,0,0,0,0); }
    else { // bed: frame, mattress, blanket, pillows, headboard""")

# footprints (the kitchen run was boxed off-centre by more than it is)
rep("  if(p.kind==='furn'){ const E=[[1.0,0.95,0.45],[0.8,0.8,0.85],[0.6,2.0,0.2],[1.3,1.8,0.33],[0.75,0.7,1.08],[0.8,1.25,0.25],[0.48,0.9,0.45],[0.55,2.0,0.3],[0.25,0.9,0.2],[0.65,0.78,0.55]][p.ft||0], q=Math.abs(Math.sin(p.g.rotation.y))>0.7, ex=q?E[2]:E[0], ez=q?E[0]:E[2], o=p.ft===3?0.33:0;",
    "  if(p.kind==='furn'){ const E=FURN_E[p.ft||0], q=Math.abs(Math.sin(p.g.rotation.y))>0.7, ex=q?E[2]:E[0], ez=q?E[0]:E[2], o=p.ft===3?0.1:0;")
rep("function propBoxes0(p){","""const FURN_E=[[1.0,0.95,0.45],[0.8,0.8,0.85],[0.6,2.0,0.2],[1.2,1.8,0.33],[0.75,0.7,1.08],[0.8,1.25,0.25],[0.48,0.9,0.45],[0.55,2.0,0.3],[0.25,0.9,0.2],[0.65,0.78,0.55],[0.4,0.92,0.33],[0.25,0.84,0.38],[0.87,0.6,0.41],[0.47,0.9,0.27]];
const FURN_SZ=[[2.0,0.9],[1.6,1.7],[1.2,0.4],[2.4,0.66],[1.5,2.16],[1.6,0.5],[0.95,0.9],[1.1,0.6],[0.5,0.4],[1.3,1.1],[0.8,0.66],[0.5,0.76],[1.74,0.82],[0.94,0.54]];
// the floor a piece of furniture covers [x0,z0,x1,z1], the same box it is solid in
function furnFoot(ft,x,z,yaw){ const E=FURN_E[ft], q=Math.abs(Math.sin(yaw))>0.7, ex=q?E[2]:E[0], ez=q?E[0]:E[2], o=ft===3?0.1:0, ox=q?0:o*Math.cos(yaw), oz=q?-o*Math.sin(yaw):0; return [x-ex+ox,z-ez+oz,x+ex+ox,z+ez+oz]; }
function propBoxes0(p){""")

# rooms
a=s.index("function innerWalls(h,l){"); b=s.index("function innerWallGeo(axis,mask){")
s=s[:a]+r"""// The rooms of one floor. The first wall splits the house front and back. The back is then walled into separate rooms,
// one per stretch of that wall, each with its own doorway from the front room; a deep back room keeps a bathroom at
// its far end, through a door. Then each room is given one purpose: a house always has somewhere to sit, cook and sleep.
function houseRooms(h,l){ if(h._rooms&&h._rooms[l]) return h._rooms[l]; h._rooms=h._rooms||{};
  const C=CELL, P_=housePartition(h,l), st=h.floors>1?houseStair(h).cells:[], D=doorOf(h), up=l>h.L, two=h.floors>1, DOOR=511&~18;
  const front=[], cols=new Map(), walls=[], rooms=[], doors=[];
  for(let a=0;a<h.w;a++) for(let b=0;b<h.d;b++){ const i=h.i0+a, j=h.j0+b; if(st.some(c=>c[0]===i&&c[1]===j)) continue;
    const cx=(i+.5)*C, cz=(j+.5)*C, fr=P_?(P_.X?Math.sign(cz-P_.z)===Math.sign(D.z-P_.z):Math.sign(cx-P_.x)===Math.sign(D.x-P_.x)):true;
    if(fr) front.push([i,j]); else { const k=P_.X?i:j; if(!cols.has(k)) cols.set(k,[]); cols.get(k).push([i,j]); } }
  const keys=[...cols.keys()].sort((a,b)=>a-b), far=c=>P_.X?Math.abs((c[1]+.5)*C-P_.z):Math.abs((c[0]+.5)*C-P_.x);
  for(const k of keys) cols.get(k).sort((a,b)=>far(a)-far(b));
  const wall=(axis,i,j,mask)=>{ walls.push({type:'wall',axis,i,j,l,mask,mat:h.mat,inner:1}); if(mask!==511) doors.push(axis==='x'?[i*C-1.0,(j+.5)*C-0.95,i*C+1.0,(j+.5)*C+0.95]:[(i+.5)*C-0.95,j*C-1.0,(i+.5)*C+0.95,j*C+1.0]); };
  // the first wall: a doorway in every stretch, so each back room opens off the front room
  if(P_){ const n0=Math.ceil((P_.a-0.3)/C), n1=Math.floor((P_.b+0.3)/C); for(let k=n0;k<n1;k++){ if(P_.X) wall('z',k,Math.round(P_.z/C),DOOR); else wall('x',Math.round(P_.x/C),k,DOOR); } }
  // solid walls between neighbouring back rooms
  for(let n=0;n+1<keys.length;n++){ if(keys[n+1]!==keys[n]+1) continue; for(const c of cols.get(keys[n])){ if(!cols.get(keys[n+1]).some(e=>P_.X?e[1]===c[1]:e[0]===c[0])) continue;
      if(P_.X) wall('x',keys[n+1],c[1],511); else wall('z',c[0],keys[n+1],511); } }
  const n=keys.length, deep=keys.filter(k=>cols.get(k).length>1); let types=[], openKitchen=false, suite=null;
  if(!two){ if(deep.length){ suite=deep[(h.id+1)%deep.length]; const rest=['kitchen','study','study']; types=keys.map(k=>k===suite?'bed':rest.shift()); openKitchen=!types.includes('kitchen'); }
    else if(n>=3) types=['kitchen','bath','bed']; else if(n===2){ types=['bed','bath']; openKitchen=true; } else { types=['bed']; openKitchen=true; }
    if(!suite&&h.id%2) types.reverse(); }
  else if(!up){ types=['kitchen','bath','study']; openKitchen=n===0; }
  else if(n===1&&deep.length){ suite=keys[0]; types=['bed2']; }
  else types=['bath','bed2','study'];
  const near=c=>Math.hypot((c[0]+.5)*C-D.x,(c[1]+.5)*C-D.z); front.sort((a,b)=>near(a)-near(b));
  if(front.length){ if(up) rooms.push({type:'bed',cells:front}); else if(openKitchen&&front.length>1){ rooms.push({type:'living',cells:front.slice(0,-1)}); rooms.push({type:'kitchen',cells:front.slice(-1)}); } else rooms.push({type:'living',cells:front}); }
  keys.forEach((k,m)=>{ const cs=cols.get(k), ty=types[m]||'study';
    if(k===suite&&cs.length>1){ rooms.push({type:ty,cells:[cs[0]]}); rooms.push({type:'bath',cells:cs.slice(1)}); const p=cs[0], q=cs[1]; if(P_.X) wall('z',k,Math.max(p[1],q[1]),DOOR); else wall('x',Math.max(p[0],q[0]),k,DOOR); }
    else rooms.push({type:ty,cells:cs}); });
  return h._rooms[l]={rooms,walls,doors}; }
function innerWalls(h,l){ return houseRooms(h,l).walls.map(w=>Object.assign({},w)); }
"""+s[b:]

a=s.index("// furniture, room by room: each cell that isn't the stairs"); b=s.index("function yardTrees(add,r){")
s=s[:a]+r"""// furniture, room by room: each room is furnished from its own list (a bathroom gets a toilet, washstand and bath; a
// kitchen its units, cooker and table; a bedroom a bed with a bedside table, a wardrobe...), most needed first, each
// piece against an outside wall wherever it fits clear of the others, the doorways and the front door
// furniture is lit like the rooms it stands in (indoors nothing gets the sun, so it used to look grey against the walls)
let furnMat=null; function furnMaterial(){ if(!furnMat){ furnMat=new THREE.MeshLambertMaterial({vertexColors:true}); furnMat.onBeforeCompile=sh=>{ sh.fragmentShader=sh.fragmentShader.replace('#include <emissivemap_fragment>','#include <emissivemap_fragment>\n  totalEmissiveRadiance+=diffuseColor.rgb*0.4;'); }; } return furnMat; }
function houseFurniture(add){ const BESIDE={8:4,10:3}, SZ=FURN_SZ, ENDS={2:1,7:1,3:1,10:1,11:1,12:1,13:1}, LISTS={living:[0,5,6,2,6],kitchen:[3,10,1],bed:[4,8,7,9],bed2:[4,8,7],bath:[11,13,12],study:[9,2,6]};
  for(const t of TOWNS){ if(!t.houses.length) planHouses(t);
  for(const h of t.houses){ const q=seeded(t.seed+h.id*131+7), C=CELL, IN=WT/2+0.05, x0=h.i0*C, x1=(h.i0+h.w)*C, z0=h.j0*C, z1=(h.j0+h.d)*C, D=doorOf(h);
    for(let l=h.L;l<h.L+h.floors;l++){ const R=houseRooms(h,l), placed=R.doors.map(b=>b.slice()); if(l===h.L) placed.push([D.x-1.2,D.z-1.2,D.x+1.2,D.z+1.2]);
      const fits=(f,G)=>!placed.some(b=>f[0]<b[2]+G&&b[0]<f[2]+G&&f[1]<b[3]+G&&b[1]<f[3]+G);
      for(const rm of R.rooms){ const sty=(h.id*3+l+(q()*3|0))%6; // a house keeps to a couple of colourways
        const put=(ft,x,z,yaw)=>{ const p=add('furn',x,z,1,yaw); p.ft=ft; p.yard=true; p.room=rm.type; p.g.children[0].geometry=propVariant('furn',ft+20*sty).geo; p.g.children[0].material=furnMaterial(); p.base=l*LVL; p.g.position.y=p.base; p.boxes=propBoxes(p); return p; };
        // the outside walls of this room, but not the one with the front door
        const sides=[]; for(const [i,j] of rm.cells){ const a=i-h.i0, b=j-h.j0, cx=(i+.5)*C, cz=(j+.5)*C;
          if(b===0) sides.push([cx,z0+IN,0,1,'n',i,j]); if(b===h.d-1) sides.push([cx,z1-IN,0,-1,'s',i,j]); if(a===0) sides.push([x0+IN,cz,1,0,'w',i,j]); if(a===h.w-1) sides.push([x1-IN,cz,-1,0,'e',i,j]); }
        const ok=sides.filter(sd=>!(l===h.L&&sd[4]===h.side&&Math.hypot(D.x-sd[0],D.z-sd[1])<2.6)); if(!ok.length) continue;
        const got={}; let made=0; const most=rm.cells.length*2+1;
        for(const ft of LISTS[rm.type]){ if(made>=most) break; const by=got[BESIDE[ft]]; if(ft===8&&!by) continue; const [W,Dp]=SZ[ft], lim=2.3-W/2, cand=[];
          // the bedside table goes by the bed, the cooker at the end of the kitchen units
          if(by){ const al=by.sd[2]?1:0, mid=al?by.sd[1]:by.sd[0], gap=ft===8?0.1:0.03; for(const s_ of (q()<0.5?[1,-1]:[-1,1])) cand.push([by.sd,(s_>0?by.f[al?3:2]+gap+W/2:by.f[al?1:0]-gap-W/2)-mid,1]); }
          if(ft!==8){ const order=ok.slice(); for(let k=order.length-1;k>0;k--){ const m=q()*(k+1)|0; [order[k],order[m]]=[order[m],order[k]]; }
            for(const sd of order){ const s_=q()<0.5?-1:1; for(const o of (ft===4?[s_*0.6,-s_*0.6,0]:ENDS[ft]?[s_*lim,-s_*lim,0]:[(q()-.5)*0.8,s_*lim,-s_*lim])) cand.push([sd,o]); } }
          for(const [sd,off,tight] of cand){ const along=sd[2]?1:0, x=sd[0]+sd[2]*(Dp/2+0.03)+(along?0:off), z=sd[1]+sd[3]*(Dp/2+0.03)+(along?off:0), yaw=Math.atan2(-sd[2],-sd[3]), f=furnFoot(ft,x,z,yaw);
            const lo=(along?sd[6]:sd[5])*C+0.17, hi=lo+C-0.34; if((along?f[1]:f[0])<lo||(along?f[3]:f[2])>hi) continue; // inside its own stretch of wall
            if(!fits(f,tight?0.02:0.3)) continue;
            put(ft,x,z,yaw); placed.push(f); made++; if(!got[ft]) got[ft]={sd,f}; break; } } } } } } }
"""+s[b:]
