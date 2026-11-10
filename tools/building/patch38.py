# ---------- 38. not every house has a chest (about 45% do, seeded so a party agrees) ----------
rep("    s.chest.forEach(p=>{ const yaw=Math.atan2(t.x-p.x,t.z-p.z)+Math.PI; addChest(p.x,p.y,p.z,yaw); }); }","    const cr=seeded(t.seed+h.id*977+5); s.chest.forEach(p=>{ if(cr()>0.45) return; const yaw=Math.atan2(t.x-p.x,t.z-p.z)+Math.PI; addChest(p.x,p.y,p.z,yaw); }); }")
