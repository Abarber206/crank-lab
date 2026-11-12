# patch182: the rest of the decoration can be destroyed too: road and town signs, stop signs, street lights, field
# fences, mailboxes and each town's landmark (a landmark is one big object: bring it down and it's gone).
# signs, lights and fences: grouped by what touches what, just before they're merged
rep("""function buildSigns(){ const grey=[], dark=[], pale=[], faces=new Map(), placed=[], roads=WORLD.roads;""","""function buildSigns(){ const grey=[], dark=[], pale=[], faces=new Map(), placed=[], roads=WORLD.roads, sigS0=STATICS.length;""")
rep("""  const add=(list,mat)=>{ if(!list.length) return; const g=mergeGeos(list); g.computeBoundingSphere(); const m=new THREE.Mesh(g,mat); m.castShadow=true; m.receiveShadow=true; m.matrixAutoUpdate=false; scene.add(m); };""",
    """  let grouped=false; const add=(list,mat)=>{ if(!grouped){ grouped=true; const all=[]; for(const [Lq,mq] of [[fenceW,'wood'],[grey,'metal'],[dark,'metal'],[pale,'metal']]) for(const q of Lq){ q.userData.mat=mq; all.push(q); } faces.forEach(f=>f.geos.forEach(q=>{ q.userData.mat='metal'; all.push(q); }));
      decoGroup(all,STATICS.slice(sigS0).filter(st=>/^(sign|lamp|fence)/.test(st.solid.key))); decoReady(); } // (each sign, light and fence panel its own object)
    if(!list.length) return; const g=mergeGeos(list); decoRegister(list,g); g.computeBoundingSphere(); const m=new THREE.Mesh(g,mat); m.castShadow=true; m.receiveShadow=true; m.matrixAutoUpdate=false; scene.add(m); };""")
# mailboxes (the flower beds and shrubs stay: there's nothing solid to hit)
rep("""  for(const t of TOWNS){ const parts=[], put=(g,col,x,y,z,ry=0)=>{ if(col!==0x5a4030&&col!==0xd23a2a&&!(g.parameters&&g.parameters.height===0.24)&&onWalk(t,x,z,0.15)) return; g=g.index?g.toNonIndexed():g.clone(); g.rotateY(ry); g.translate(x,y,z);""",
    """  for(const t of TOWNS){ const gS0=STATICS.length, parts=[], put=(g,col,x,y,z,ry=0)=>{ if(col!==0x5a4030&&col!==0xd23a2a&&!(g.parameters&&g.parameters.height===0.24)&&onWalk(t,x,z,0.15)) return; g=g.index?g.toNonIndexed():g.clone(); g.rotateY(ry); g.translate(x,y,z); g.userData.col=col;""")
rep("""    if(!parts.length) continue;
    const out=new THREE.BufferGeometry(); for(const k of ['position','normal','color']){""","""    if(!parts.length) continue;
    { const ms=STATICS.slice(gS0).filter(st=>/^mail/.test(st.solid.key)); if(ms.length){ parts.forEach(g=>{ if(g.userData.col===0x5a4030||g.userData.col===0xd23a2a||[0x2a2d33,0x8a2a2a,0x2f5d8a,0xe0ddd5].includes(g.userData.col)) g.userData.mat='metal'; });
        decoGroup(parts.filter(g=>g.userData.mat),ms); decoReady(); } }
    const out=new THREE.BufferGeometry(); for(const k of ['position','normal','color']){""")
rep("""    out.computeBoundingSphere(); const m=new THREE.Mesh(out,new THREE.MeshLambertMaterial({vertexColors:true})); m.castShadow=true; m.receiveShadow=true; m.matrixAutoUpdate=false; m.userData.town=t; scene.add(m); gardenMeshes.push(m); } }""",
    """    decoRegister(parts,out); out.computeBoundingSphere(); const m=new THREE.Mesh(out,new THREE.MeshLambertMaterial({vertexColors:true})); m.castShadow=true; m.receiveShadow=true; m.matrixAutoUpdate=false; m.userData.town=t; scene.add(m); gardenMeshes.push(m); } }""")
# landmarks: each one whole (its meshes hide when it breaks)
rep("""function buildLandmarks(){ if(_lmBuilt) return; _lmBuilt=true; const col=new THREE.Color();""","""function buildLandmarks(){ if(_lmBuilt) return; const c0=scene.children.length, s0=STATICS.length; buildLandmarks0();
  const meshes=scene.children.slice(c0), stats=STATICS.slice(s0).filter(st=>/^lm/.test(st.solid.key));
  for(const t of TOWNS){ const L=t.poi; if(!L) continue; const o=decoNewObj('brick',1500); o.meshes=meshes.filter(m=>{ if(!m.geometry) return false; m.updateMatrixWorld(true); if(!m.geometry.boundingSphere) m.geometry.computeBoundingSphere(); const p=m.geometry.boundingSphere.center.clone().applyMatrix4(m.matrixWorld); return Math.hypot(p.x-L.x,p.z-L.z)<30; });
    for(const st of stats) if(Math.hypot(st.x-L.x,st.z-L.z)<30){ st.solid.dobj=o; st.solid.deco=1; o.statics.push(st); }
    o.boxes0=o.statics.map(st=>st.solid.boxes.map(b=>b.slice())); o.c.set(L.x,(L.y!=null?L.y:t.h)+4,L.z); o.ready=true; o.piece.mat=o.mat; } }
function buildLandmarks0(){ if(_lmBuilt) return; _lmBuilt=true; const col=new THREE.Color();""")
