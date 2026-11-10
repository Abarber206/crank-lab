# ---------- 55. house windows get glass: a faintly tinted, glossy pane with a cross of glazing bars ----------
rep("  if(p.type==='wall') add(p.skin?houseWallGeo(p.axis,p.mask==null?511:p.mask,p.out||1):wallGeo(p.axis,p.mask==null?511:p.mask),0,0,0);",
"""  if(p.type==='wall') add(p.skin?houseWallGeo(p.axis,p.mask==null?511:p.mask,p.out||1):wallGeo(p.axis,p.mask==null?511:p.mask),0,0,0);
  if(p.type==='wall'&&p.skin&&!mat&&p.mask!=null&&!(p.mask&16)&&(p.mask&2)){ const gg=windowGlassGeo(p.axis); add(gg.glass,0,0,0,0,0,glassMat()); add(gg.bars,0,0,0,0,0,M.beam); }
  else if(p.type==='wall'){}""")
rep("function makeGroup(p,mat,real){",r"""let _glassMat=null; const _glassGeo={};
function glassMat(){ return _glassMat||(_glassMat=new THREE.MeshPhongMaterial({color:0xcfe6f2,transparent:true,opacity:0.3,shininess:120,specular:0xffffff,depthWrite:false,side:THREE.DoubleSide})); }
function windowGlassGeo(axis){ if(_glassGeo[axis]) return _glassGeo[axis]; const w=CELL/3, h=LVL/3, X=axis==='x';
  const glass=new THREE.PlaneGeometry(w-0.04,h-0.04); if(X) glass.rotateY(Math.PI/2);
  const bars=mergeGeos([new THREE.BoxGeometry(X?0.05:0.05,h,X?0.05:0.05),new THREE.BoxGeometry(X?0.05:w,0.05,X?w:0.05)]);
  return _glassGeo[axis]={glass,bars}; }
function makeGroup(p,mat,real){""")
rep("byMat.forEach((ms,mat)=>{ const mm=new THREE.Mesh(mergeWorld(ms),mat); mm.castShadow=mm.receiveShadow=true;","byMat.forEach((ms,mat)=>{ const mm=new THREE.Mesh(mergeWorld(ms),mat); mm.castShadow=!mat.transparent; mm.receiveShadow=true;")
rep("add(gg.glass,0,0,0,0,0,glassMat()); add(gg.bars,0,0,0,0,0,M.beam); }","add(gg.glass,0,0,0,0,0,glassMat()); const gm=p.group?null:null; add(gg.bars,0,0,0,0,0,M.beam); }")
rep("    if(real){ m.castShadow=true; m.receiveShadow=true; m.userData.piece=p; } g.add(m); };","    if(real){ m.castShadow=!m.material.transparent; m.receiveShadow=true; m.userData.piece=p; } g.add(m); };")
