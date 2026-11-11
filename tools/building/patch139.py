# patch139: the knocked-down crawl, properly. Each leg in turn is drawn up along the ground (the thigh out to the
# side, the knee bent, the shin and the inside of the foot flat on the ground), then pushes the body forward as the
# knee straightens and the leg slides back in; the feet lie toes-down instead of pointing up into the air
rep("for(const [L,up,sx] of [[r.legL,P2,-1],[r.legR,P1,1]]){ set(L.hp,'x',-0.05+0.15*up*mvK); set(L.hp,'z',sx*(0.12+0.8*up*mvK)); set(L.hp,'y',sx*1.4*up*mvK); set(L.kn,'x',-0.2-1.2*up*mvK); set(L.an,'x',0.75); }",
    "for(const [L,up,sx] of [[r.legL,P2,-1],[r.legR,P1,1]]){ const u=up*mvK; set(L.hp,'x',-0.05+0.1*u); set(L.hp,'z',sx*(0.1+1.0*u)); set(L.hp,'y',sx*-1.5*Math.min(1,u*2.5)); set(L.kn,'x',-0.15-1.5*u); set(L.an,'x',0.2+0.3*u); }")
