# ---------- 74. houses get a ceiling: a floor at the top of the walls under the roof, so inside you see a ceiling instead
# of the open roof (and the attic hides the gaps up at the gables). Some attics hold a chest: pickaxe through the ceiling. ----------
rep("  // pitched roof: two slopes meeting at a ridge along the longer side\n  const top=L+h.floors;",
    "  // pitched roof: two slopes meeting at a ridge along the longer side\n  const top=L+h.floors;\n  for(let a=0;a<w;a++) for(let b=0;b<d;b++) P_.push({type:'floor',i:i0+a,j:j0+b,l:top,mat:'wood',ceil:1}); // the ceiling (the attic floor)")
rep("    const cr=seeded(t.seed+h.id*977+5); s.chest.forEach(p=>{ if(cr()>0.45) return; const yaw=Math.atan2(t.x-p.x,t.z-p.z)+Math.PI; addChest(p.x,p.y,p.z,yaw); }); }",
    """    const cr=seeded(t.seed+h.id*977+5); s.chest.forEach(p=>{ if(cr()>0.45) return; const yaw=Math.atan2(t.x-p.x,t.z-p.z)+Math.PI; addChest(p.x,p.y,p.z,yaw); });
    if(cr()<0.35){ const top=h.L+h.floors, x=(h.i0+h.w/2)*CELL+(h.w%2?0:CELL*0.5), z=(h.j0+h.d/2)*CELL+(h.d%2?0:CELL*0.5), [gy]=groundAt(x,z,top*LVL+0.8,near(x,z)); // up in the attic
      if(gy>top*LVL-0.3) addChest(x,gy,z,h.w>=h.d?0:Math.PI/2); } }""")
