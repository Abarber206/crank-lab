# ---------- 102. dead-end streets finish in a round turnaround with the sidewalk carried around it ----------
rep("function buildSidewalks(){","""const BULB_R=6.8, BULB_IN=3;
function townBulbs(t){ if(t.bulbs) return t.bulbs; const Ls=t.streetL;
  t.dead=t.ends.map(e=>!WORLD.roads.some(r=>!r.street&&[r.pts[0],r.pts[r.pts.length-1]].some(p=>Math.hypot(SPAWN[0]+p[0]-e[0],SPAWN[2]+p[1]-e[1])<3)));
  return t.bulbs=t.ends.map((e,k)=>{ const ox=(e[0]-t.x)/Ls, oz=(e[1]-t.z)/Ls; return t.dead[k]?[e[0]-ox*BULB_IN,e[1]-oz*BULB_IN,ox,oz]:null; }).filter(Boolean); }
function buildSidewalks(){""")
rep("    for(const X of [true,false]) for(const sd of [-1,1]){ const off=sd*(ROAD_HW+WALK_W/2), a=X?[t.x-Ls,t.z+off]:[t.x+off,t.z-Ls], b=X?[t.x+Ls,t.z+off]:[t.x+off,t.z+Ls]; quad(a,b,y,0); SIDEWALKS.push([a,b]); }",
"""    const bulbs=townBulbs(t), dd=t.dead, cutB=Math.sqrt(BULB_R*BULB_R-ROAD_HW*ROAD_HW)+BULB_IN-0.25; // the sidewalks stop where the turnaround's ring takes over
    for(const X of [true,false]) for(const sd of [-1,1]){ const off=sd*(ROAD_HW+WALK_W/2), c0=dd[X?0:2]?cutB:0, c1=dd[X?1:3]?cutB:0, a=X?[t.x-Ls+c0,t.z+off]:[t.x+off,t.z-Ls+c0], b=X?[t.x+Ls-c1,t.z+off]:[t.x+off,t.z+Ls-c1]; quad(a,b,y,0); SIDEWALKS.push([a,b]); }
    for(const [cx,cz,ox,oz] of bulbs){ const th=Math.PI-Math.asin(ROAD_HW/BULB_R), n=36, rr=BULB_R+WALK_W/2, pt=k=>{ const a=-th+2*th*k/n, ca=Math.cos(a), sa=Math.sin(a); return [cx+(ox*ca-oz*sa)*rr,cz+(oz*ca+ox*sa)*rr]; };
      let v=0; for(let k=0;k<n;k++){ const a=pt(k-0.04), b=pt(k+1.04); v=quad(a,b,y+0.001,v); SIDEWALKS.push([pt(k),pt(k+1)]); }
      const R2=BULB_R+WALK_W+0.6; for(let u=-R2;u<=R2;u+=0.8) for(let w=-R2;w<=R2;w+=0.8) if(u*u+w*w<R2*R2){ const c=worldCell(cx+u,cz+w); if(c>=0) GR[c]=0; }
      const cg=new THREE.CircleGeometry(BULB_R+0.12,44); cg.rotateX(-Math.PI/2); const P_=cg.attributes.position, U_=cg.attributes.uv; for(let q=0;q<P_.count;q++) U_.setXY(q,(cx+P_.getX(q))/7.2,(cz+P_.getZ(q))/24);
      const cm=new THREE.Mesh(cg,new THREE.MeshLambertMaterial({map:roadPlainTex,polygonOffset:true,polygonOffsetFactor:-2,polygonOffsetUnits:-4*(8+WORLD.roads.length)})); cm.position.set(cx,t.h+0.03,cz); cm.receiveShadow=true; cm.updateMatrix(); cm.matrixAutoUpdate=false; scene.add(cm); }""")
# on the minimap and the big map
rep("    g.fillStyle=col; TOWNS.forEach(t=>{ if(Math.abs(t.x-ox)<R+10&&Math.abs(t.z-oz)<R+10){ g.beginPath(); g.arc(tx(t.x),tz(t.z),(PLAZA_R+(w-ROAD_HW*2)/2)*sc,0,7); g.fill(); } }); }",
    "    g.fillStyle=col; TOWNS.forEach(t=>{ if(Math.abs(t.x-ox)<R+60&&Math.abs(t.z-oz)<R+60){ g.beginPath(); g.arc(tx(t.x),tz(t.z),(PLAZA_R+(w-ROAD_HW*2)/2)*sc,0,7); g.fill(); for(const b of townBulbs(t)){ g.beginPath(); g.arc(tx(b[0]),tz(b[1]),(BULB_R+(w-ROAD_HW*2)/2)*sc,0,7); g.fill(); } } }); }")
rep("    g.fillStyle=col; WORLD.towns.forEach(t=>{ g.beginPath(); g.arc(X(t.u),X(t.v),(PLAZA_R/mpp)+w/2+1,0,7); g.fill(); }); }",
    "    g.fillStyle=col; WORLD.towns.forEach(t=>{ g.beginPath(); g.arc(X(t.u),X(t.v),(PLAZA_R/mpp)+w/2+1,0,7); g.fill(); });\n    TOWNS.forEach(t=>{ for(const b of townBulbs(t)){ g.beginPath(); g.arc(X(b[0]-SPAWN[0]),X(b[1]-SPAWN[2]),BULB_R/mpp+(w-7.2)/2,0,7); g.fill(); } }); }")
