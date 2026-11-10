# ---------- 50. houses get real rooms (an inner wall with a doorway on each floor) and much more furniture ----------
# more furniture shapes: TV stand with a TV, armchair, wardrobe, nightstand with a lamp, desk with a chair
rep("    else { // bed: frame, mattress, blanket, pillows, headboard","""    else if(variant===5){ propPart(rbox(1.6,0.5,0.45,0.02),dk,g,0,0.25,0,0,0,0,0); for(const x of [-0.4,0.4]) propPart(rbox(0.74,0.4,0.02,0.01),wood,g,x,0.25,-0.23,0,0,0,0);
      propPart(rbox(1.15,0.68,0.06,0.02),0x15171b,g,0,0.9,0.05,0,0,0,0); propPart(rbox(1.07,0.6,0.01,0.005),0x2a3a4e,g,0,0.9,0.015,0,0,0,0); propPart(rbox(0.2,0.06,0.18,0.02),0x15171b,g,0,0.53,0.05,0,0,0,0); }
    else if(variant===6){ propPart(rbox(0.9,0.36,0.86,0.06),F,g,0,0.3,0,0,0,0,0); propPart(rbox(0.6,0.12,0.66,0.05),F,g,0,0.52,-0.05,0,0,0,0); propPart(rbox(0.9,0.5,0.2,0.07),F,g,0,0.66,0.33,0,0,0,0); for(const x of [-0.38,0.38]) propPart(rbox(0.16,0.56,0.86,0.06),F,g,x,0.44,0,0,0,0,0); }
    else if(variant===7){ propPart(rbox(1.1,2.0,0.58,0.02),wood,g,0,1.0,0,0,0,0,0); for(const x of [-0.27,0.27]){ propPart(rbox(0.52,1.9,0.02,0.01),dk,g,x,1.0,-0.295,0,0,0,0); propPart(rbox(0.03,0.22,0.03,0.01),0xd8c27a,g,x*0.15,1.05,-0.31,0,0,0,0); } }
    else if(variant===8){ propPart(rbox(0.5,0.55,0.4,0.02),wood,g,0,0.28,0,0,0,0,0); propPart(rbox(0.44,0.18,0.02,0.01),dk,g,0,0.4,-0.205,0,0,0,0); propPart(new THREE.CylinderGeometry(0.04,0.06,0.3,10),0xd8c27a,g,0.08,0.7,0.05,0,0,0,0); propPart(new THREE.CylinderGeometry(0.1,0.15,0.2,14,1,true),0xf6ecd0,g,0.08,0.92,0.05,0,0,0,0); }
    else if(variant===9){ propPart(rbox(1.3,0.05,0.6,0.02),wood,g,0,0.74,0.15,0,0,0,0); for(const x of [-0.6,0.6]) propPart(rbox(0.05,0.72,0.56,0.02),dk,g,x,0.36,0.15,0,0,0,0);
      const c=new THREE.Group(); c.position.set(0,0,-0.35); g.add(c); propPart(rbox(0.46,0.07,0.44,0.03),F,c,0,0.46,0,0,0,0,0); propPart(rbox(0.46,0.5,0.06,0.03),F,c,0,0.75,-0.2,0,0,0,0); propPart(new THREE.CylinderGeometry(0.03,0.03,0.4,6),0x3a3d42,c,0,0.22,0,0,0,0,0); propPart(rbox(0.5,0.03,0.5,0.02),0x3a3d42,c,0,0.03,0,0,0,0,0); }
    else { // bed: frame, mattress, blanket, pillows, headboard""")
rep("  if(p.kind==='furn'){ const E=[[1.0,0.95,0.45],[0.8,0.8,0.85],[0.6,2.0,0.2],[1.3,1.8,0.33],[0.75,0.7,1.08]][p.ft||0],","  if(p.kind==='furn'){ const E=[[1.0,0.95,0.45],[0.8,0.8,0.85],[0.6,2.0,0.2],[1.3,1.8,0.33],[0.75,0.7,1.08],[0.8,1.25,0.25],[0.48,0.9,0.45],[0.55,2.0,0.3],[0.25,0.9,0.2],[0.65,0.78,0.55]][p.ft||0],")
# the room plan: one inner wall per floor, on a cell line clear of the stairs, with a doorway; furniture room by room
a=s.index("// furniture in the inner corners of each house's ground floor"); b=s.index("function yardTrees(add,r){")
s=s[:a]+r"""// a house's inner wall on floor l: the cell line (parallel to the front if possible) that keeps clear of the stairs
function housePartition(h,l){ if(h._part&&h._part[l]!==undefined) return h._part[l]; h._part=h._part||{};
  const C=CELL, IN=WT/2, x0=h.i0*C, x1=(h.i0+h.w)*C, z0=h.j0*C, z1=(h.j0+h.d)*C, st=h.floors>1?houseStair(h).cells:[], frontX=h.side==='n'||h.side==='s';
  const hitsStair=(ax,az,bx,bz)=>st.some(([i,j])=>{ const sx0=i*C+0.3, sx1=(i+1)*C-0.3, sz0=j*C+0.3, sz1=(j+1)*C-0.3; return Math.max(ax,bx)>sx0&&Math.min(ax,bx)<sx1&&Math.max(az,bz)>sz0&&Math.min(az,bz)<sz1; });
  const cands=[]; for(let b=1;b<h.d;b++) cands.push({X:true,z:z0+b*C,a:x0+IN,b:x1-IN}); for(let a=1;a<h.w;a++) cands.push({X:false,x:x0+a*C,a:z0+IN,b:z1-IN});
  cands.sort((p,q)=>(q.X===frontX)-(p.X===frontX));
  const pick=cands.find(c=>!(c.X?hitsStair(c.a,c.z,c.b,c.z):hitsStair(c.x,c.a,c.x,c.b)))||null;
  if(pick){ pick.door=pick.a+(pick.b-pick.a)*0.5+(((h.id*7+l)%3)-1)*1.2; } // the doorway somewhere near the middle
  return h._part[l]=pick; }
function partitionFix(h,l){ const P_=housePartition(h,l); if(!P_) return null; const C=CELL, y0=l*LVL, top=(l+1)*LVL-FT-0.01, th=0.14, dw=1.25, dh=2.15, parts={inner:[],beam:[]}, boxes=[];
  const ci=P_.X?Math.floor((P_.a+P_.b)/2/C):Math.floor(P_.x/C-0.5)+0, cj=P_.X?Math.floor(P_.z/C-0.5):Math.floor((P_.a+P_.b)/2/C), o=new THREE.Vector3((ci+.5)*C,y0-FT/2,(cj+.5)*C);
  const seg=(s0,s1,ya,yb,k,solid)=>{ if(s1-s0<0.02) return; const b=P_.X?[s0,y0+ya,P_.z-th/2,s1,y0+yb,P_.z+th/2]:[P_.x-th/2,y0+ya,s0,P_.x+th/2,y0+yb,s1];
    const g=new THREE.BoxGeometry(b[3]-b[0],b[4]-b[1],b[5]-b[2]); g.translate((b[0]+b[3])/2-o.x,(b[1]+b[4])/2-o.y,(b[2]+b[5])/2-o.z); parts[k].push(g); if(solid) boxes.push(b); };
  const d0=P_.door-dw/2, d1=P_.door+dw/2;
  seg(P_.a,d0,0,top-y0,'inner',true); seg(d1,P_.b,0,top-y0,'inner',true); seg(d0,d1,dh,top-y0,'inner',true); // wall each side of the doorway and the wall over it
  for(const e of [d0,d1]) seg(e-0.05,e+0.05,0,dh,'beam',false); seg(d0-0.05,d1+0.05,dh,dh+0.08,'beam',false); // a door frame
  const out=[]; for(const k in parts){ if(!parts[k].length) continue; const g=mergeGeos(parts[k]); g.computeBoundingSphere(); if(k==='inner') g.setAttribute('inside',new THREE.BufferAttribute(new Float32Array(g.attributes.position.count).fill(1),1)); out.push([g,k]); }
  return {cell:[ci,cj],boxes,parts:out}; }
// furniture, room by room: each cell that isn't the stairs gets a piece against one of its outside walls (never across
// the front door); the front room is the living room, the back room the kitchen and dining room (or a bedroom in a
// one-storey house); upstairs are bedrooms and a study
function houseFurniture(add){ for(const t of TOWNS){ if(!t.houses.length) planHouses(t);
  for(const h of t.houses){ const q=seeded(t.seed+h.id*131+7), C=CELL, IN=WT/2+0.05, x0=h.i0*C, x1=(h.i0+h.w)*C, z0=h.j0*C, z1=(h.j0+h.d)*C;
    const st=h.floors>1?houseStair(h).cells:[], SZ=[[2.0,0.9],[1.6,1.7],[1.2,0.4],[2.6,0.66],[1.5,2.16],[1.6,0.5],[0.95,0.9],[1.1,0.6],[0.5,0.4],[1.3,1.1]], TALL={2:1,7:1,3:1};
    const D=doorOf(h);
    for(let l=h.L;l<h.L+h.floors;l++){ const P_=housePartition(h,l), up=l>h.L; const used={};
      for(let a=0;a<h.w;a++) for(let b=0;b<h.d;b++){ const i=h.i0+a, j=h.j0+b; if(st.some(c=>c[0]===i&&c[1]===j)) continue;
        const cx=(i+.5)*C, cz=(j+.5)*C, front=P_?(P_.X?Math.sign(cz-P_.z)===Math.sign(D.z-P_.z):Math.sign(cx-P_.x)===Math.sign(D.x-P_.x)):true;
        const room=up?(front?'study':'bed'):(front?'living':(h.floors>1?'kitchen':'bed2'));
        const pool={living:[0,5,6,2],kitchen:[3,1,2],bed:[4,7,8],study:[9,2,6,4],bed2:[4,3,7]}[room], key=room+(used[room]=(used[room]||0)+1);
        const ft=pool[(used[room]-1+(q()*2|0))%pool.length], [W,Dp]=SZ[ft];
        // the outside walls of this cell, but not the one with the front door
        const sides=[]; if(b===0) sides.push([cx,z0+IN,0,1,'n']); if(b===h.d-1) sides.push([cx,z1-IN,0,-1,'s']); if(a===0) sides.push([x0+IN,cz,1,0,'w']); if(a===h.w-1) sides.push([x1-IN,cz,-1,0,'e']);
        const ok=sides.filter(sd=>!(l===h.L&&sd[4]===h.side&&Math.hypot(D.x-sd[0],D.z-sd[1])<2.6)); if(!ok.length) continue;
        const sd=ok[q()*ok.length|0], along=(sd[2]?1:0), off=TALL[ft]?(q()<0.5?-1:1)*(2.5-0.2-W/2):(q()-.5)*0.8;
        const x=sd[0]+sd[2]*(Dp/2+0.03)+(along?0:off), z=sd[1]+sd[3]*(Dp/2+0.03)+(along?off:0), yaw=Math.atan2(-sd[2],-sd[3]);
        const p=add('furn',x,z,1,yaw); p.ft=ft; p.yard=true; p.g.children[0].geometry=propVariant('furn',ft).geo; p.base=l*LVL; p.g.position.y=p.base; p.boxes=propBoxes(p); } } } } }
"""+s[b:]
# the inner walls ride on a floor piece of the house (they break and come back with it)
rep("function housePieces(h){ const out=housePieces0(h); if(h.garage) out.push(...garagePieces(h)); return out; }",
"""function housePieces(h){ const out=housePieces0(h); if(h.garage) out.push(...garagePieces(h));
  for(let l=h.L;l<h.L+h.floors;l++){ const fx=partitionFix(h,l); if(!fx) continue; const q=out.find(p=>p.type==='floor'&&p.l===l&&p.i===fx.cell[0]&&p.j===fx.cell[1]); if(!q) continue;
    q.fix=q.fix?{boxes:q.fix.boxes.concat(fx.boxes),parts:q.fix.parts.concat(fx.parts)}:{boxes:fx.boxes,parts:fx.parts}; }
  return out; }""")
