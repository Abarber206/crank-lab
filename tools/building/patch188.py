# patch188: guns differ by rarity in shape (kit: grips, sights, scope, brake/compensator, laser, longer magazines;
# gunkit.js) in your hands, on the ground and in the inventory pictures
rep("function iconModel(id){",open('/home/claude/mg/gunkit.js').read().rstrip()+"\nfunction iconModel(id){")
rep("""m.material.emissive.setHex(GW.rarity==='legendary'?0x3a2400:GW.rarity==='epic'?0x1e0a30:0x0a0a0a); }); }""","""m.material.emissive.setHex(GW.rarity==='legendary'?0x3a2400:GW.rarity==='epic'?0x1e0a30:0x0a0a0a); }); applyGunKit(gunSrc(r,mdl),mdl,GW.rarity,r); }""")
rep("""    w.traverse(o=>{ if(o.isMesh&&o.userData.trim){ o.material=o.material.clone(); o.material.color.setHex(RCOL[LW.rarity]); } o.visible=o.visible!==false; });""","""    w.traverse(o=>{ if(o.isMesh&&o.userData.trim){ o.material=o.material.clone(); o.material.color.setHex(RCOL[LW.rarity]); } o.visible=o.visible!==false; });
    applyGunKit(w,LW.model,LW.rarity,lootTmpl.rig);""")
rep("""    w.traverse(o=>{ if(o.isMesh&&o.userData.trim){ o.material=o.material.clone(); o.material.color.setHex(RCOL[LW.rarity]); } });
    w.rotation.set(Math.PI/2,0,Math.PI/2);""","""    w.traverse(o=>{ if(o.isMesh&&o.userData.trim){ o.material=o.material.clone(); o.material.color.setHex(RCOL[LW.rarity]); } });
    applyGunKit(w,LW.model,LW.rarity,lootTmpl.rig);
    w.rotation.set(Math.PI/2,0,Math.PI/2);""")
