# patch184: swimmers go over the falls. Near the lagoon's mouth a current pulls anyone in the water toward the edge (gently
# at first, hard right at the lip); in the water you're no longer held at the edge, so you're carried over, fall with the
# water and are eliminated when you hit the sea far below (a big splash). Walkers on the cliffs are still held at the edge,
# and boats still stop short of it.
rep("""function keepOnIsland(E){ const u=E.pos.x-SPAWN[0], v=E.pos.z-SPAWN[2], d=Math.hypot(u,v); if(d<MAP_R-40) return; const er=WGEN.edgeR(u,v)-1.2; if(d<=er) return;""",
"""function keepOnIsland(E,dt){ const u=E.pos.x-SPAWN[0], v=E.pos.z-SPAWN[2], d=Math.hypot(u,v); if(E===P&&P.overFalls&&d<MAP_R-60) P.overFalls=false; if(d<MAP_R-40) return; const er=WGEN.edgeR(u,v)-1.2;
  if(E===P&&!P.sky&&!P.kart){ const S=WGEN.sea();
    if(P.overFalls){ if(P.pos.y<WGEN.OCEAN_Y+0.4&&!isDead()){ burst(P.pos.clone().setY(WGEN.OCEAN_Y+0.1),26,6,0.1,splashMat); sfx('step_water'); fallHurt(9999); } return; } // over the falls: nothing holds you, the sea below ends it
    if(S&&d>er-34&&WGEN.seaW(u*(er-4)/d,v*(er-4)/d)>0&&P.pos.y<S.Y+0.8&&waterAt(P.pos.x,P.pos.z)>-999){ // in the lagoon near its mouth: the current takes you
      const nx=u/d, nz=v/d, k=Math.max(0,1-(er-d)/34), sp=0.6+5.4*k*k; if(dt){ P.pos.x+=nx*sp*dt; P.pos.z+=nz*sp*dt; }
      if(d>er-0.6){ P.overFalls=true; if(P.vel){ P.vel.x+=nx*3; P.vel.z+=nz*3; } return; } }
    if(S&&d>er-12&&P.pos.y<S.Y-2.5&&WGEN.seaW(u*(er-14)/d,v*(er-14)/d)>0){ P.overFalls=true; return; } } // (already dropping past the lip)
  if(d<=er) return;""")
rep("""skyMove(E,fw,st,jump,dt); keepOnIsland(E); return; } moveBody0(E,fw,st,jump,dt); keepOnIsland(E); }""","""skyMove(E,fw,st,jump,dt); keepOnIsland(E,dt); return; } moveBody0(E,fw,st,jump,dt); keepOnIsland(E,dt); }""")
rep("""    if(P.pos.y<-20) respawn();""","""    if(P.pos.y<(P.overFalls?WGEN.OCEAN_Y-30:-20)) respawn(); // (going over the falls is a long way down: the sea ends it, not this)""")
