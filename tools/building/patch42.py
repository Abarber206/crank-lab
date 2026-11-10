# ---------- 42. nothing grows or stands on a front path, a driveway or a sidewalk ----------
rep("function yardFrame(t,h){",r"""// is (x,z) on (or within pad of) a front path or driveway of this town? (sidewalks along the streets are kept clear separately)
function onWalk(t,x,z,pad){ const seg=(ax,az,bx,bz,w)=>{ const dx=bx-ax, dz=bz-az, L2=dx*dx+dz*dz||1e-6; let f=((x-ax)*dx+(z-az)*dz)/L2; f=f<0?0:f>1?1:f; return Math.hypot(x-ax-dx*f,z-az-dz*f)<w/2+pad; };
  for(const h of t.houses){ const D=doorOf(h), X=h.side==='n'||h.side==='s', across=X?D.z-t.z:D.x-t.x, edge=Math.sign(across)*(ROAD_HW+WALK_W-0.1);
    if(seg(D.x,D.z,X?D.x:t.x+edge,X?t.z+edge:D.z,WALK_W)) return true;
    if(h.garage){ const f=garageFrame(h), m=f.p(2.5,0.02), a2=f.X?m[1]-t.z:m[0]-t.x, e2=Math.sign(a2)*(ROAD_HW+0.05); if(seg(m[0],m[1],f.X?m[0]:t.x+e2,f.X?t.z+e2:m[1],3.4)) return true; } }
  return Math.abs(x-t.x)<ROAD_HW+WALK_W+pad||Math.abs(z-t.z)<ROAD_HW+WALK_W+pad; }
function yardFrame(t,h){""")
# yard trees keep their trunks and canopies off the paths
rep("        const [x,z]=f.p(u,fw+(r()-.5)*0.6); if(!free(t,x,z,1.6)) continue;","        const [x,z]=f.p(u,fw+(r()-.5)*0.6); if(!free(t,x,z,1.6)||onWalk(t,x,z,1.4)) continue;")
rep("const [x,z]=f.p(u,w); if(!free(t,x,z,2.2)) continue;","const [x,z]=f.p(u,w); if(!free(t,x,z,2.2)||onWalk(t,x,z,2.0)) continue;")
# garden pieces: skip any flower, shrub or bed piece that would sit on a path
rep("parts=[], put=(g,col,x,y,z,ry=0)=>{ g=g.index?g.toNonIndexed():g.clone();","parts=[], put=(g,col,x,y,z,ry=0)=>{ if(col!==0x5a4030&&col!==0xd23a2a&&!(g.parameters&&g.parameters.height===0.24)&&onWalk(t,x,z,0.15)) return; g=g.index?g.toNonIndexed():g.clone();")
