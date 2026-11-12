# patch170: the other two points of interest: Crater Labs (where Copper Ridge was) and Timber Yard (Mossy Mill).
POI_JS=open('/home/claude/mg/poi.js').read()
# the module is already in from patch169; replace it with the current one (all four sites)
i=s.index("/* ---------- points of interest ----------"); j=s.index("function buildWorld(){",i)
s=s[:i]+POI_JS+"\n"+s[j:]
rep("""const POI_ON={castle:1,factory:1};""","""const POI_ON={castle:1,factory:1,labs:1,timber:1};""")
# battle royale bots loot the points of interest too (their ground-floor loot spots), not only town houses
rep("""      if(Math.hypot(x-S.tx,z-S.tz)>S.tr*0.92+4&&S.ph>0) continue; const d=Math.hypot(x-b.pos.x,z-b.pos.z)+Math.random()*25; if(d<bs){ bs=d; best=h; } } }
  return best; }""","""      if(Math.hypot(x-S.tx,z-S.tz)>S.tr*0.92+4&&S.ph>0) continue; const d=Math.hypot(x-b.pos.x,z-b.pos.z)+Math.random()*25; if(d<bs){ bs=d; best=h; } }
    if(t.kind){ if(!t.botSpots){ t.botSpots=[]; for(const bl of planPOI(t)) for(const k of ['chest','floor']) for(const s of bl.spots[k]) if(Math.abs(s.y-t.h)<0.5) t.botSpots.push({poiX:s.x,poiZ:s.z}); }
      for(const h of t.botSpots){ if(h.brVisit&&performance.now()-h.brVisit<90000) continue; if(Math.hypot(h.poiX-S.tx,h.poiZ-S.tz)>S.tr*0.92+4&&S.ph>0) continue;
        const d=Math.hypot(h.poiX-b.pos.x,h.poiZ-b.pos.z)+Math.random()*25; if(d<bs){ bs=d; best=h; } } } }
  return best; }""")
rep("""      if(h) brRouteInto(b,h,(h.i0+h.w/2)*CELL,(h.j0+h.d/2)*CELL);""","""      if(h&&h.poiX!=null){ b.dest={pts:[[h.poiX,h.poiZ,1.2]],i:0,linger:3+Math.random()*3}; h.brVisit=performance.now(); }
      else if(h) brRouteInto(b,h,(h.i0+h.w/2)*CELL,(h.j0+h.d/2)*CELL);""")
