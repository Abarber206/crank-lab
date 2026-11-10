# ---------- 48. buggies bump off each other (each driver's game pushes its own buggy out and bounces it) ----------
rep("  { const dx=k.x-SPAWN[0], dz=k.z-SPAWN[2], d=Math.hypot(dx,dz); if(d>WORLD_EDGE){","""  for(const o of karts){ if(o===k||Math.abs(o.x-k.x)>4||Math.abs(o.z-k.z)>4||Math.abs(o.y-k.y)>1.5) continue;
    const fx2=-Math.sin(k.yaw), fz2=-Math.cos(k.yaw), ox2=-Math.sin(o.yaw), oz2=-Math.cos(o.yaw); let best=null;
    for(const a of [-0.85,0,0.85]) for(const b of [-0.85,0,0.85]){ const dx=(k.x-fx2*a)-(o.x-ox2*b), dz=(k.z-fz2*a)-(o.z-oz2*b), d=Math.hypot(dx,dz); if(d<1.35&&(!best||d<best.d)) best={d,dx,dz}; }
    if(best){ const d=best.d||1e-3, nx=best.dx/d, nz=best.dz/d; k.x+=nx*(1.35-d); k.z+=nz*(1.35-d);
      const rvx=k.vx-o.vx, rvz=k.vz-o.vz, vn=rvx*nx+rvz*nz; if(vn<0){ k.vx-=1.5*vn*nx; k.vz-=1.5*vn*nz; if(vn<-3){ sfxAt('kart_bump',_kz.set(k.x,k.y+0.5,k.z)); k.sqV-=Math.min(2,-vn*0.15); if(P.kart&&P.kart.k===k) shake=Math.max(shake,Math.min(0.2,-vn*0.02)); } } } }
  { const dx=k.x-SPAWN[0], dz=k.z-SPAWN[2], d=Math.hypot(dx,dz); if(d>WORLD_EDGE){""")
