# ---------- 64. the glider flies like a glider: look down to dive and build speed, look up to trade that speed for lift
# (a short climb), hold the nose up too long and it stalls and drops. Airspeed is kept as energy, not set directly. ----------
rep("""    const fwd=9+Math.max(-4.5,Math.min(7,fw*7)); tx=fx*fwd+rx*st*5; tz=fz*fwd+rz*st*5; acc=5;
    ty=-6.5-(fw>0.3?1.6:0)+(fw<-0.3?1.2:0); E.vel.y+=(ty-E.vel.y)*Math.min(1,dt*(S.gt<0.6?4:2)); }""",
"""    // flight path angle follows where you look (and W dives a little more, S flares); airspeed is energy:
    // diving adds speed, climbing spends it, drag pulls it back toward the trim speed; too slow and the nose won't stay up
    const G0=-0.42, TRIM=12, VMAX=33, VMIN=6;
    if(S.as==null){ S.as=Math.max(10,Math.min(20,Math.hypot(E.vel.x,E.vel.z)+6)); S.gam=G0; }
    let gt=G0+(E.pitch||0)*1.15-(fw>0.3?0.14:0)+(fw<-0.3?0.16:0); gt=Math.max(-1.15,Math.min(0.42,gt));
    const lift=Math.max(0,Math.min(1,(S.as-8)/9)); gt=Math.min(gt,G0+(0.42-G0)*lift); if(S.as<8.5) gt=Math.min(gt,G0-0.25*(1-S.as/8.5)); // stall: the nose drops
    S.gam+=(gt-S.gam)*Math.min(1,dt*(S.gt<0.6?2:3.2));
    S.as+=(0.6*GRAV*(Math.sin(G0)-Math.sin(S.gam))-0.22*(S.as-TRIM))*dt; S.as=Math.max(VMIN,Math.min(VMAX,S.as));
    const hs=S.as*Math.cos(S.gam); tx=fx*hs+rx*st*4.5; tz=fz*hs+rz*st*4.5; acc=7+S.as*0.4;
    ty=S.as*Math.sin(S.gam); E.vel.y+=(ty-E.vel.y)*Math.min(1,dt*(S.gt<0.6?4:5)); }""")
# leaving the glider forgets its airspeed (a fresh deploy starts from your fall)
rep("function deployGlider(E){ if(!E.sky||E.sky.phase!=='fall') return; E.sky.phase='glide'; E.sky.gt=0;","function deployGlider(E){ if(!E.sky||E.sky.phase!=='fall') return; E.sky.phase='glide'; E.sky.gt=0; E.sky.as=null;")
# the rider and glider pitch with the flight path: nose down in a dive, leaning back as it climbs
rep("const dive=gl?0:Math.max(0,Math.min(1,(-S.vel.y-38)/20)), want=gl?-0.2:-(1.18+0.32*dive);",
    "const dive=gl?0:Math.max(0,Math.min(1,(-S.vel.y-38)/20)), gam=Math.atan2(S.vel.y,Math.hypot(S.vel.x,S.vel.z)+0.01), want=gl?Math.max(-0.95,Math.min(0.5,-0.2+(gam+0.42)*0.9)):-(1.18+0.32*dive);")
