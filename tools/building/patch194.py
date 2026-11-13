# patch194: houses furnished on the walls and ceilings (housedecor.js): paintings, lamps, rugs, curtains; doors with
# panels in lighter colours (they read as black holes in the dim rooms); interior lighting tuned (the sun barely reaches
# in, so stray light can't leak through as hard-edged patches)
rep("function buildWorld(){",open('/home/claude/mg/housedecor.js').read().rstrip()+"\nfunction buildWorld(){")
rep("""      const p=addPiece(Object.assign({},q,{owner:'world',instant:true})); p.town=t; if(q.mask!=null&&q.mask!==p.mask){ p.mask=q.mask; buildPiece(p); } } batchTown(t); }""",
"""      const p=addPiece(Object.assign({},q,{owner:'world',instant:true})); p.town=t; if(q.mask!=null&&q.mask!==p.mask){ p.mask=q.mask; buildPiece(p); } }
    if(!t.decorPlan){ try{ planHouseDecor(t); }catch(e){ console.warn('decor',e); } } if(t.decorPlan) t.decorPlan.forEach((_,k)=>{ const p=pieces.get(k); if(p&&p.group&&!p.group.children.some(m=>m.userData.decor)) addHouseDecor(p); });
    batchTown(t); }""")
rep("""  p.scaf=null; p.group=makeGroup(p,null,true); scene.add(p.group);""","""  p.scaf=null; p.group=makeGroup(p,null,true); scene.add(p.group); if(p.owner==='world'&&p.town&&p.town.decorPlan) addHouseDecor(p);""")
rep("""  p.group.children.forEach(m=>{ if(!m.isMesh) return; let ov=m.userData.ov;""","""  p.group.children.forEach(m=>{ if(!m.isMesh||m.userData.decor) return; let ov=m.userData.ov;""")
# doors: raised panels, lighter colours
rep("""  const parts=[{geo:panel,M:new THREE.Matrix4(),col:new THREE.Color(1,1,1)}];""","""  const parts=[{geo:panel,M:new THREE.Matrix4(),col:new THREE.Color(1,1,1)}];
  for(const fs of [-1,1]) for(const [py,ph] of [[h*0.7,h*0.38],[h*0.27,h*0.34]]){ const pg=X?new THREE.BoxGeometry(0.016,ph,tw*0.62):new THREE.BoxGeometry(tw*0.62,ph,0.016); // two raised panels each side
    const o=X?new THREE.Vector3(fs*(th/2+0.006),py,tw/2+0.01):new THREE.Vector3(tw/2+0.01,py,fs*(th/2+0.006)); parts.push({geo:pg,M:new THREE.Matrix4().makeTranslation(o.x,o.y,o.z),col:new THREE.Color(0.86,0.86,0.86)}); }""")
rep("""const col=p.skin?[0x7a2e2a,0x3b4a5a,0x5a3d26,0x2f5a46][(p.i*7+p.j*3)&3]:{wood:0x8a5a32,brick:0x6e4a36,metal:0x7d8794}[p.mat]||0x8a5a32;""","""const col=p.skin?[0xa8483a,0x5d7a96,0x9a6a3c,0x4f8a6c,0xe8e2d4][(p.i*7+p.j*3)%5]:{wood:0xa8743e,brick:0x8e6448,metal:0x9aa4b0}[p.mat]||0xa8743e;""")
rep("""    batchTown(t); }
  buildSidewalks();
}""","""    batchTown(t); }
  buildSidewalks();
  if(typeof FOREST!=='undefined'&&FOREST.trees) try{ indoorBuild(); }catch(e){ console.warn('indoor',e); } // (again, now the buildings stand)
}""")
