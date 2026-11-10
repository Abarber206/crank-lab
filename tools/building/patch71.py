# ---------- 71. the glider carries much further when you fly it level (about 4.5 m forward per metre lost, was ~2.2);
# and a tree you hit no longer blinks out for a frame when it swaps between the forest and its own wobbling mesh ----------
rep("    const G0=-0.42, TRIM=12, VMAX=33, VMIN=6;","    const G0=-0.22, TRIM=13, VMAX=33, VMIN=6;")
rep("const dive=gl?0:Math.max(0,Math.min(1,(-S.vel.y-38)/20)), gam=Math.atan2(S.vel.y,Math.hypot(S.vel.x,S.vel.z)+0.01), want=gl?Math.max(-0.95,Math.min(0.5,-0.2+(gam+0.42)*0.9))",
    "const dive=gl?0:Math.max(0,Math.min(1,(-S.vel.y-38)/20)), gam=Math.atan2(S.vel.y,Math.hypot(S.vel.x,S.vel.z)+0.01), want=gl?Math.max(-0.95,Math.min(0.5,-0.2+(gam+0.22)*0.9))")
rep("  if(moving&&!p.g.parent){ treeMesh(p); scene.add(p.g); forestDirty=true; FOREST.t=0; }\n  else if(!moving&&p.g.parent){ scene.remove(p.g); p.g.scale.set(p.s,p.s*(p.hs||1),p.s); p.g.rotation.x=p.g.rotation.z=0; forestDirty=true; FOREST.t=0; } }",
    "  if(moving&&!p.g.parent){ treeMesh(p); scene.add(p.g); forestDirty=true; FOREST.t=0; stepForest(0); }\n  else if(!moving&&p.g.parent){ scene.remove(p.g); p.g.scale.set(p.s,p.s*(p.hs||1),p.s); p.g.rotation.x=p.g.rotation.z=0; forestDirty=true; FOREST.t=0; stepForest(0); } } // swap in the same frame: never neither, never both")
