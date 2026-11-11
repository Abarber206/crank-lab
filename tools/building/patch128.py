# ---------- 128. knocked down: a proper crawl. Low on the belly, propped on the forearms; one arm reaches out flat-handed as
# the opposite knee is drawn up out to the side, then the arm pulls back and the leg pushes; hips and ribs twist against
# each other and the body rolls a little from side to side. Lying still, the head sinks and the chest heaves ----------
a=s.index("    A.crawl=(A.crawl||0)+dt*(1.2+Math.min(1.5,sp)*4.5);"); b=s.index("    for(const k of GUN_MODELS) if(r[k]) r[k].visible=false; r.gun.visible=r.pump.visible=r.hammer.visible=r.plan.visible=false; r.pick.visible=false;\n    if(H.glider) H.glider.visible=false; return; }",a)
s=s[:a]+r"""    A.crawl=(A.crawl||0)+dt*(0.6+Math.min(1.5,sp)*5.2); const c1=Math.sin(A.crawl), c2=-c1, mvK=Math.min(1,sp/0.5), br=Math.sin(A.t*2.6), P1=Math.max(0,c1), P2=Math.max(0,c2), N1=Math.max(0,-c1), N2=Math.max(0,-c2);
    G.position.y=S.pos.y+(0.24+0.025*Math.abs(Math.cos(A.crawl))*mvK)*e; G.rotation.z=0.09*c1*mvK*e;                       // low, rolling towards the reaching arm
    r.hips.position.y=lerp(r.hips.position.y,0.94,sm); r.hips.position.x=lerp(r.hips.position.x,0,sm); set(r.hips,'x',0); set(r.hips,'y',0.24*c1*mvK); set(r.hips,'z',0.08*c1*mvK);
    set(r.spine,'x',-0.16-0.02*br); set(r.spine,'y',-0.1*c1*mvK); set(r.spine,'z',0); set(r.chest,'x',-0.22-0.035*br*(1-mvK)); set(r.chest,'y',-0.22*c1*mvK); set(r.chest,'z',0);
    set(r.neck,'x',-0.32-0.4*mvK); set(r.neck,'y',0.18*c1*mvK+0.25*(1-mvK)); set(r.neck,'z',0);                                 // head up to see where you are going; down when you stop
    // arms: out ahead and wide; the reaching one stretches, the other bends as it drags the body up to it
    set(r.armL.sh,'x',2.45+0.42*c1*mvK); set(r.armR.sh,'x',2.45+0.42*c2*mvK); set(r.armL.sh,'z',-0.5-0.12*N1*mvK); set(r.armR.sh,'z',0.5+0.12*N2*mvK); set(r.armL.sh,'y',0); set(r.armR.sh,'y',0);
    set(r.armL.el,'x',1.25-0.75*P1*mvK+0.45*N1*mvK); set(r.armR.el,'x',1.25-0.75*P2*mvK+0.45*N2*mvK); set(r.armL.wr,'x',0.35); set(r.armR.wr,'x',0.35);
    // legs: the knee opposite the reaching arm comes up and out, then straightens to push
    for(const [L,up,sx] of [[r.legL,P2,-1],[r.legR,P1,1]]){ set(L.hp,'x',-0.05+0.6*up*mvK); set(L.hp,'z',sx*(0.12+0.5*up*mvK)); set(L.hp,'y',sx*1.25*up*mvK); set(L.kn,'x',-0.2-1.05*up*mvK); set(L.an,'x',0.75); }
    A.handL=A.handR='flat'; A.turnL=A.turnR=0;
"""+s[b:]
