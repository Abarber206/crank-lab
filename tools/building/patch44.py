# ---------- 44. let go of the glider (Jump) to freefall again, Jump to redeploy; a livelier hang under the glider ----------
rep("    if((jump&&!S.jumpWas&&S.t>1.0)||above<SKY_AUTO) deployGlider(E);","    if((jump&&!S.jumpWas&&S.t>(S.released?0.5:1.0))||above<(S.released?40:SKY_AUTO)) deployGlider(E);")
rep("  } else { S.gt=(S.gt||0)+dt;\n","  } else { S.gt=(S.gt||0)+dt;\n    if(jump&&!S.jumpWas&&S.gt>0.6&&above>30){ S.phase='fall'; S.t=0; S.released=true; S.jumpWas=jump; if(E===P) sfx('sky_start'); return; } // let go\n")
rep("""    const sw=Math.sin(t*1.8)*0.12;
    set(r.armL.sh,'x',-2.75); set(r.armR.sh,'x',-2.75); set(r.armL.sh,'z',-0.28); set(r.armR.sh,'z',0.28); set(r.armL.el,'x',0.3); set(r.armR.el,'x',0.3);
    set(r.legL.hp,'x',0.18+sw); set(r.legR.hp,'x',0.12-sw); set(r.legL.hp,'z',-0.06); set(r.legR.hp,'z',0.06); set(r.legL.kn,'x',-0.3); set(r.legR.kn,'x',-0.22); set(r.neck,'x',0.12); }""",
"""    // hanging under the bar: the body swings like a pendulum into turns, the legs trail back with speed and dangle, the arms pull the bar
    const yr=Math.max(-1,Math.min(1,(A.yawRate||0)*0.5)), spd=Math.min(1,Math.hypot(S.vel.x,S.vel.z)/16), sw=Math.sin(t*1.7)*0.1*(1-0.5*spd), kick=Math.sin(t*2.3)*0.08;
    set(r.armL.sh,'x',-2.7+yr*0.12); set(r.armR.sh,'x',-2.7-yr*0.12); set(r.armL.sh,'z',-0.3); set(r.armR.sh,'z',0.3); set(r.armL.el,'x',0.35+Math.max(0,yr)*0.5); set(r.armR.el,'x',0.35+Math.max(0,-yr)*0.5);
    set(r.legL.hp,'x',0.15-0.35*spd+sw+kick); set(r.legR.hp,'x',0.1-0.35*spd-sw-kick*0.7); set(r.legL.hp,'z',-0.06-yr*0.15); set(r.legR.hp,'z',0.06-yr*0.15); set(r.legL.kn,'x',-0.25-0.2*Math.max(0,Math.sin(t*2.3))); set(r.legR.kn,'x',-0.2-0.2*Math.max(0,-Math.sin(t*2.3)));
    set(r.neck,'x',0.1); set(r.neck,'y',yr*0.3); }""")
rep("A.skyZ=lerp(A.skyZ||0,Math.max(-0.45,Math.min(0.45,-(A.yawRate||0)*(gl?0.14:0.07))),Math.min(1,dt*4));","A.skyZ=lerp(A.skyZ||0,Math.max(-0.55,Math.min(0.55,-(A.yawRate||0)*(gl?0.2:0.07)))+(gl?Math.sin(A.t*1.1)*0.03:0),Math.min(1,dt*3));")
