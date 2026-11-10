# ---------- 81. chests are solid; the dividing walls inside houses are real wall pieces ----------
# (a) chests: you bump into them (and can stand on them) until they're opened and gone
rep("if(VANS) for(const v of VANS) if(Math.abs(v.x-E.pos.x)<7&&Math.abs(v.z-E.pos.z)<7) ps.add(v.solid);",
    "if(VANS) for(const v of VANS) if(Math.abs(v.x-E.pos.x)<7&&Math.abs(v.z-E.pos.z)<7) ps.add(v.solid); if(typeof chests!=='undefined') for(const c of chests) if(Math.abs(c.x-E.pos.x)<3&&Math.abs(c.z-E.pos.z)<3&&c.g.visible&&!(c.open&&(c.goneT||0)>1.2)){ const s=c.solid||(c.solid={boxes:[[0,0,0,0,0,0]],key:'chest'+c.id,isChest:true}), X=Math.abs(Math.sin(c.yaw))<0.7, hx=X?0.5:0.34, hz=X?0.34:0.5, b=s.boxes[0]; b[0]=c.x-hx; b[1]=c.y; b[2]=c.z-hz; b[3]=c.x+hx; b[4]=c.y+0.62; b[5]=c.z+hz; ps.add(s); }")
# (b) inside walls: each 5 m stretch is its own wall piece (full height, proper thickness, a real doorway with a door), so
# it joins the outside walls and ceiling with no gaps, and breaking it or the floor under it no longer takes the other out
rep("""  for(let l=h.L;l<h.L+h.floors;l++){ const fx=partitionFix(h,l); if(!fx) continue; const q=out.find(p=>p.type==='floor'&&p.l===l&&p.i===fx.cell[0]&&p.j===fx.cell[1]); if(!q) continue;
    q.fix=q.fix?{boxes:q.fix.boxes.concat(fx.boxes),parts:q.fix.parts.concat(fx.parts)}:{boxes:fx.boxes,parts:fx.parts}; }""",
"""  for(let l=h.L;l<h.L+h.floors;l++) for(const q of innerWalls(h,l)) out.push(Object.assign(q,{skin:h.skin,key:`w${q.axis}${q.i}_${q.j}_${q.l}`,dir:0}));""")
rep("function partitionFix(h,l){",r"""function innerWalls(h,l){ const P_=housePartition(h,l); if(!P_) return []; const C=CELL, out=[], DOOR=511&~18;
  const n0=Math.ceil((P_.a-0.3)/C), n1=Math.floor((P_.b+0.3)/C); if(n1<=n0) return [];
  const dk=Math.max(n0,Math.min(n1-1,Math.floor(P_.door/C))); // the stretch with the doorway
  for(let k=n0;k<n1;k++) out.push(P_.X?{type:'wall',axis:'z',i:k,j:Math.round(P_.z/C),l,mask:k===dk?DOOR:511,mat:h.mat,inner:1}:{type:'wall',axis:'x',i:Math.round(P_.x/C),j:k,l,mask:k===dk?DOOR:511,mat:h.mat,inner:1});
  return out; }
function innerWallGeo(axis,mask){ const key='in'+axis+mask; let g=houseGeoCache.get(key); if(g) return g; g=wallGeo(axis,mask).clone(); g.setAttribute('inside',new THREE.BufferAttribute(new Float32Array(g.attributes.position.count).fill(1),1)); houseGeoCache.set(key,g); return g; }
function partitionFix(h,l){""")
rep("  if(p.type==='wall') add(p.skin?houseWallGeo(p.axis,p.mask==null?511:p.mask,p.out||1):wallGeo(p.axis,p.mask==null?511:p.mask),0,0,0);",
    "  if(p.type==='wall') add(p.skin?(p.inner?innerWallGeo(p.axis,p.mask==null?511:p.mask):houseWallGeo(p.axis,p.mask==null?511:p.mask,p.out||1)):wallGeo(p.axis,p.mask==null?511:p.mask),0,0,0);")
