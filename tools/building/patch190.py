# patch190: light indoors and under the trees (indoor.js): rooms are dim, the ground under a canopy is in shade
rep("const _fc=new THREE.Color(), _fm=new THREE.Matrix4();\nfunction stepForest(",open('/home/claude/mg/indoor.js').read().rstrip()+"\nconst _fc=new THREE.Color(), _fm=new THREE.Matrix4();\nfunction stepForest(")
rep("  FOREST.trees=trees; forestDirty=true; }","  FOREST.trees=trees; forestDirty=true; try{ indoorBuild(); }catch(e){ console.warn('indoor',e); } }")
rep("  stepOcean(lastDt);","  stepOcean(lastDt); stepIndoor(lastDt);")
rep("  iconR.render(sc,cam); const url=iconR.domElement.toDataURL('image/png');","  const im0=INDOOR.u.map.value; if(INDOOR.dummy) INDOOR.u.map.value=INDOOR.dummy; iconR.render(sc,cam); INDOOR.u.map.value=im0; const url=iconR.domElement.toDataURL('image/png');")
