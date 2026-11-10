# ---------- 53. zombies glide smoothly on a friend's screen: each update is a fresh fix (position + speed), and the zombie
#               is steered toward where that fix says it is now, instead of drifting further each frame and snapping back ----------
rep("    z.tgt.set(s[2],s[3],s[4]); z.yawT=s[5]; z.vel.set(s[8]||0,0,s[9]||0);","    z.tgt.set(s[2],s[3],s[4]); z.netP=(z.netP||new THREE.Vector3()).set(s[2],s[3],s[4]); z.netT=performance.now(); z.yawT=s[5]; z.vel.set(s[8]||0,0,s[9]||0);")
rep("""  horde.zs.forEach(z=>{ z.tgt.x+=z.vel.x*Math.min(dt,0.05)*0.5; z.tgt.z+=z.vel.z*Math.min(dt,0.05)*0.5;
    if(z.pos.distanceTo(z.tgt)>5) z.pos.copy(z.tgt); else z.pos.lerp(z.tgt,k);""","""  const now=performance.now();
  horde.zs.forEach(z=>{ if(z.netP){ const age=Math.min(0.25,(now-z.netT)/1000); z.tgt.set(z.netP.x+z.vel.x*age,z.netP.y,z.netP.z+z.vel.z*age); }
    const d=z.pos.distanceTo(z.tgt); if(d>9) z.pos.copy(z.tgt); else z.pos.lerp(z.tgt,1-Math.exp(-dt*(d>2?14:9)));""")
