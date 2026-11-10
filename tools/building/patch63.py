# ---------- 63. hero overhaul: fuller, smoother limbs with seamless joints, mitten hands instead of stick fingers, a soft
# nose, none of the little specks (rivets, laces, straps, knee and thigh blocks), and running that eases in and out with
# a proper arm swing ----------
# arms
rep("    part(limbGeo(.046,.038,.25),C.jacket,sh);","    part(limbGeo(.055,.046,.25),C.jacket,sh);")
rep("    part(sph(.039),fc,el,0,0,0,null,null,0.008);\n    part(limbGeo(.04,.03,.21),fc,el);\n    part(new THREE.TorusGeometry(.043,.009,8,18),C.jacketD,el,0,-.02,0,[Math.PI/2,0,0],null,0);\n    part(limbGeo(.039,.039,.04),C.jacketD,el,0,-.18,0,null,null,0.006);",
    "    part(sph(.047),fc,el,0,0,0,null,null,0.008);\n    part(limbGeo(.046,.035,.21),fc,el);\n    part(limbGeo(.038,.037,.035),C.jacketD,el,0,-.182,0,null,null,0.006);")
rep("    part(rbox(.056,.074,.036,.016),C.glove,wr,0,-.035,0,null,null,0.007);\n    const fing=grp(wr,0,-.075,0);\n    for(let f=0;f<4;f++) part(limbGeo(.0072,.0062,.05+(f===1||f===2?.006:0)),C.glove,fing,-.019+f*.0127,0,-.002,null,null,0.004);\n    part(rbox(.062,.011,.04,.004),C.packD,wr,0,-.072,-.002,null,null,0);\n    part(rbox(.019,.05,.022,.008),C.glove,wr,-sx*.034,-.048,-.016,[0,0,sx*.4],null,0.006);",
    "    part(limbGeo(.03,.034,.03),C.glove,wr,0,.012,0,null,null,0);                     // wrist\n    part(rbox(.064,.07,.036,.02),C.glove,wr,0,-.035,0,null,null,0.007);                // palm\n    const fing=grp(wr,0,-.068,0);\n    part(rbox(.06,.054,.032,.015),C.glove,fing,0,-.025,-.002,null,null,0.004);        // fingers, one soft mitten that curls\n    part(rbox(.024,.046,.025,.011),C.glove,wr,-sx*.036,-.046,-.016,[0,0,sx*.4],null,0.006); // thumb")
# legs
rep("    part(limbGeo(.076,.056,.4),C.pants,hp); part(sph(.074),C.pants,hp,0,-.02,0,null,[1,.7,1]);\n    part(rbox(.022,.1,.08,.008),C.pantsD,hp,sx*.074,-.19,0,null,null,0.005);",
    "    part(limbGeo(.085,.063,.4),C.pants,hp); part(sph(.083),C.pants,hp,0,-.02,0,null,[1,.75,1]);")
rep("    part(sph(.058),C.pants,kn,0,0,0,null,null,0.008);\n    part(rbox(.08,.1,.035,.016),C.pantsD,kn,0,-.02,-.05,null,null,0.006);\n    part(limbGeo(.056,.04,.36),C.pants,kn); part(sph(.052),C.pants,kn,0,-.1,.008,null,[.95,1.6,1],0); // calf",
    "    part(sph(.064),C.pants,kn,0,0,0,null,null,0.008);\n    part(limbGeo(.063,.045,.36),C.pants,kn); part(sph(.056),C.pants,kn,0,-.1,.008,null,[.95,1.6,1],0); // calf")
rep("    for(let q=0;q<3;q++) part(rbox(.045,.005,.007,.002),0xe9e2d0,an,0,-.04-q*.018,-.075-q*.016,[.55,0,0],null,0); // laces\n","")
rep("    part(limbGeo(.055,.055,.035),C.packD,an,0,.04,0,null,null,0.005);\n","")
# face: one soft nose instead of a cone with a ball on it
rep("  { const ng=new THREE.ConeGeometry(.02,.055,10); ng.rotateX(-1.25); part(ng,C.skin,rig.head,0,.112,-.128,null,[1,1,.9],0); part(sph(.014),C.skin,rig.head,0,.093,-.138,null,[1.25,.8,1],0); } // nose",
    "  part(sph(.022),C.skin,rig.head,0,.104,-.124,[-.35,0,0],[.82,1.15,1.05],0); // nose")
# jacket: no rivets
rep("[-1,1].forEach(sx=>{ part(rbox(.075,.07,.02,.012),C.jacketL,rig.chest,sx*.11,.07,-.11,null,null,0.004); part(rbox(.012,.012,.012,.004),C.steel,rig.chest,sx*.1,.17,-.124,null,null,0); });",
    "[-1,1].forEach(sx=>{ part(rbox(.075,.07,.02,.012),C.jacketL,rig.chest,sx*.11,.07,-.11,null,null,0.004); });")
# smoother running: the stride eases in and out with speed, arms swing through with elbows that open and close
rep("  if(S.onGround){\n    const stride=S.crouch?0.95:1.45;\n    A.phase+=sp*dt/stride*Math.PI;\n    const s1=Math.sin(A.phase), c1=Math.cos(A.phase), amp=(S.crouch?0.55:0.78)*k;",
    "  if(S.onGround){\n    const stride=S.crouch?0.95:1.45;\n    A.phase+=sp*dt/stride*Math.PI;\n    A.kS=lerp(A.kS||0,k,Math.min(1,dt*7)); const kRaw=k; { const k=A.kS; // ease into and out of the run\n    const s1=Math.sin(A.phase), c1=Math.cos(A.phase), amp=(S.crouch?0.55:0.78)*k;")
rep("    if(bounceArms){ T.shL=-0.85*k*s1*cm; T.shR=0.85*k*s1*cm; T.elL=T.elR=0.35+0.95*k; T.shLz=-0.1-0.08*k; T.shRz=0.1+0.08*k; }",
    "    if(bounceArms){ const sw=0.95*k*cm, lag=Math.sin(A.phase-0.25); T.shL=-sw*lag; T.shR=sw*lag; T.elL=0.3+0.75*k+0.35*k*Math.max(0,-lag); T.elR=0.3+0.75*k+0.35*k*Math.max(0,lag); T.shLz=-0.08-0.1*k; T.shRz=0.08+0.1*k; }")
rep("burst(_fp,2,1.1,0.05,dustMat); A.dustCd=0.12; } } }","burst(_fp,2,1.1,0.05,dustMat); A.dustCd=0.12; } } }\n    } // eased stride")
