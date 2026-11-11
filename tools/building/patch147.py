# patch147: rivers run into the sea. A river's path used to stop at the water's edge as it was traced, but the beach in
# front of it still stood above sea level for some metres, so a strip of sand cut every river mouth off from the sea.
# Each river that reaches the sea now carries its channel on, along its last heading, through the beach until it is
# out in water a metre deep (the sea's own surface fills the cut, so the river and the sea meet as one sheet of water).
rep("""    const RV=WORLD.rivers=routeRivers(); WORLD.bridges=[];""","""    const RV=WORLD.rivers=routeRivers(); WORLD.bridges=[];
    { const S=WGEN.sea(); if(S) for(const rv of RV){ if(rv.into>=0) continue; const p=rv.pts, n=p.length; if(n<6) continue; const L=p[n-1], A=p[n-6];
        let dx=L[0]-A[0], dz=L[1]-A[1]; const dl=Math.hypot(dx,dz)||1; dx/=dl; dz/=dl; let deep=0;
        for(let k=1;k<=60&&deep<4;k++){ const u=L[0]+dx*2*k, v=L[1]+dz*2*k; if(Math.abs(u)>WHALF-4||Math.abs(v)>WHALF-4) break; p.push([u,v,S.Y,L[3],L[4],L[5]]); if(WORLD.at(WH,u,v)<S.Y-1.0) deep++; else deep=0; }
        if(p.length>n) p.forEach((q,i)=>{ if(i>=n-12&&q[2]>S.Y) q[2]=S.Y+(q[2]-S.Y)*Math.max(0,(n-1-i)/12); }); } }""")
