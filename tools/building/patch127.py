# ---------- 127. being hit and going down, for the new bodies. A hit staggers you away from where it came from: the body
# twists and bends with it, the knees give a little. Death is a collapse, not a plank falling: the knees buckle and the
# body folds, then it goes over on to its back, its front or its side (away from the shot) and settles in a sprawl ----------
rep("  else if(ev==='hurt'){ A.hurt=1; A.hurtSide=Math.random()<.5?-1:1; }",
    "  else if(ev==='hurt'){ A.hurt=1; A.hurtSide=Math.random()<.5?-1:1; if(arg&&arg.isVector3){ A.hurtFrom=arg.clone(); A.hurtNew=true; } }")
rep("  else if(ev==='die'){ A.dead=true; A.deadT=0; }","  else if(ev==='die'){ A.dead=true; A.deadT=0; A.deadHow=null; }")
rep("function dmgDirFrom(pos){","function dmgDirFrom(pos){ if(pos&&pos.isVector3&&typeof localHero!=='undefined'){ localHero.anim.hurtFrom=pos.clone(); localHero.anim.hurtNew=true; }")
rep("  animEvent(B.h,'hurt'); B.lastHurtAt=performance.now();","  animEvent(B.h,'hurt',P.pos); B.lastHurtAt=performance.now();")
# bodies stay to be seen
rep("if(pl){ pl.alive=false; animEvent(pl.h,'die'); setTimeout(()=>{ if(!pl.alive) pl.h.group.visible=false; },900); } return; }","if(pl){ pl.alive=false; animEvent(pl.h,'die'); setTimeout(()=>{ if(!pl.alive) pl.h.group.visible=false; },2600); } return; }")
rep("if(pl){ pl.alive=false; animEvent(pl.h,'die'); setTimeout(()=>{ if(!pl.alive) pl.h.group.visible=false; },900); }\n","if(pl){ pl.alive=false; animEvent(pl.h,'die'); setTimeout(()=>{ if(!pl.alive) pl.h.group.visible=false; },2600); }\n")
rep("B.h.group.visible=false; } },850); }","B.h.group.visible=false; } },2400); }")
rep("animEvent(B.h,'die'); setTimeout(()=>{ if(B&&!B.alive) B.h.group.visible=false; },900);","animEvent(B.h,'die'); setTimeout(()=>{ if(B&&!B.alive) B.h.group.visible=false; },2600);")
rep("animEvent(AB.h,'die'); setTimeout(()=>{ if(AB&&AB.dead) AB.h.group.visible=false; },900);","animEvent(AB.h,'die'); setTimeout(()=>{ if(AB&&AB.dead) AB.h.group.visible=false; },2600);")

# where the hit came from, in the body's own terms (front +1 .. behind -1, right +1 .. left -1)
rep("  // ----- death -----\n  if(A.dead){","""  if(A.hurtNew){ A.hurtNew=false; const hx=A.hurtFrom.x-S.pos.x, hz=A.hurtFrom.z-S.pos.z, hl=Math.hypot(hx,hz)||1; A.hurtF=(hx*fx+hz*fz)/hl; const sd=(hx*rx+hz*rz)/hl; if(Math.abs(sd)>0.15) A.hurtSide=sd>0?1:-1; A.hurtSd=sd; }
  // ----- death -----
  if(A.dead){""")
a=s.index("    A.deadT+=dt; const f=Math.min(1,A.deadT/0.6), e=f*f*(3-2*f);"); b=s.index("    r.gun.visible=r.pump.visible=r.hammer.visible=r.plan.visible=false; r.pick.visible=false;\n    return;\n  }",a)
s=s[:a]+r"""    A.deadT+=dt; const t=A.deadT, cl=x=>Math.max(0,Math.min(1,x)), ez=x=>x*x*(3-2*x);
    if(A.deadHow==null){ const f=A.hurtF==null?0.5:A.hurtF, sd=A.hurtSd||0; A.deadHow=Math.abs(sd)>0.75?2:f<-0.2?1:0; A.deadSide=sd?Math.sign(sd):(Math.random()<0.5?-1:1); A.deadV=Math.random(); A.hip0=r.hips.position.y; } // shot from the front: on to the back; from behind: on to the face; from the side: over sideways
    const how=A.deadHow, sdn=A.deadSide, k1=ez(cl(t/0.3)), k2=ez(cl((t-0.22)/0.6)), bump=t>0.82&&t<1.1?Math.sin((t-0.82)/0.28*Math.PI)*0.035:0;
    // first the legs give and the body folds; then it goes over, turning about the hips while they sink to the ground
    const hipL=lerp(A.hip0||0.94,0.56,k1), ang=1.52*k2, hh=lerp(hipL,how===2?0.2:0.15,k2)+bump, sy=Math.sin(S.yaw), cy=Math.cos(S.yaw);
    r.hips.position.y=hipL; r.hips.position.x=0;
    if(how===2){ G.rotation.x=0; G.rotation.z=-sdn*ang; const dxl=hipL*Math.sin(sdn*ang); G.position.set(S.pos.x-cy*dxl,S.pos.y+hh-hipL*Math.cos(ang),S.pos.z+sy*dxl); } // falls away from the side it was hit on
    else { const a=(how===1?-1:1)*ang, dzl=hipL*Math.sin(a); G.rotation.z=0; G.rotation.x=a; G.position.set(S.pos.x-sy*dzl,S.pos.y+hh-hipL*Math.cos(a),S.pos.z-cy*dzl); }
    const B1={hpL:0.95,hpR:0.8,knL:-1.55,knR:-1.4,anL:0.5,anR:0.5,hpLz:-0.05,hpRz:0.05,spX:how===0?0.12:how===1?-0.4:-0.15,chX:how===0?0.05:how===1?-0.25:-0.1,chY:0,nkX:how===0?0.25:-0.45,nkY:0,shL:0.25,shR:0.2,shLz:-0.18,shRz:0.18,elL:0.5,elR:0.45},
      F=[{hpL:0.2,hpR:0.6,knL:-0.45,knR:-1.05,anL:-0.2,anR:0,hpLz:-0.28,hpRz:0.2,spX:-0.05,chX:-0.1,chY:0.1,nkX:-0.25,nkY:0.6,shL:0,shR:-0.1,shLz:-1.25,shRz:0.85,elL:0.35,elR:0.9},      // on the back, arms thrown out
         {hpL:-0.12,hpR:-0.3,knL:-0.3,knR:-0.8,anL:-0.6,anR:-0.5,hpLz:-0.15,hpRz:0.3,spX:0.05,chX:0.05,chY:-0.15,nkX:-0.3,nkY:-0.8,shL:0.3,shR:2.6,shLz:-0.9,shRz:0.5,elL:1.2,elR:0.5}, // on the front, head turned, an arm up by it
         {hpL:0.75,hpR:0.4,knL:-1.15,knR:-0.7,anL:0,anR:0,hpLz:0,hpRz:0,spX:0.3,chX:0.15,chY:0.2*sdn,nkX:0.25,nkY:0,shL:0.9,shR:0.6,shLz:-0.2,shRz:0.2,elL:0.9,elR:0.7}][how],           // on the side, curled
      v=(k)=>lerp(B1[k]*k1,F[k]*(k==='nkY'&&A.deadV<0.5?-1:1),k2), sv=(o,ax,k)=>{ o.rotation[ax]=lerp(o.rotation[ax],v(k),Math.min(1,dt*16)); };
    sv(r.legL.hp,'x','hpL'); sv(r.legR.hp,'x','hpR'); sv(r.legL.kn,'x','knL'); sv(r.legR.kn,'x','knR'); sv(r.legL.an,'x','anL'); sv(r.legR.an,'x','anR'); sv(r.legL.hp,'z','hpLz'); sv(r.legR.hp,'z','hpRz');
    sv(r.spine,'x','spX'); sv(r.chest,'x','chX'); sv(r.chest,'y','chY'); sv(r.neck,'x','nkX'); sv(r.neck,'y','nkY'); r.hips.rotation.set(0,0,0); r.chest.rotation.z=lerp(r.chest.rotation.z,0,0.2); r.spine.rotation.y=0; r.neck.rotation.z=lerp(r.neck.rotation.z,how===2?0.3*sdn:0,0.2);
    sv(r.armL.sh,'x','shL'); sv(r.armR.sh,'x','shR'); sv(r.armL.sh,'z','shLz'); sv(r.armR.sh,'z','shRz'); sv(r.armL.el,'x','elL'); sv(r.armR.el,'x','elR'); r.armL.sh.rotation.y=r.armR.sh.rotation.y=0; r.armL.wr.rotation.set(0,0,0); r.armR.wr.rotation.set(0,0,0);
    r.eyes.forEach(e=>e.scale.y=lerp(e.scale.y,0.12,0.2)); r.lids.forEach(l=>{ l.position.y=lerp(l.position.y,.1475,0.2); l.scale.y=lerp(l.scale.y,1.1,0.2); }); r.mouth.scale.y=lerp(r.mouth.scale.y,2.2,0.2);
    for(const k of GUN_MODELS) if(r[k]) r[k].visible=false; if(r.heldMag) r.heldMag.visible=false; if(r.heldShell) r.heldShell.visible=false;
"""+s[b:]

# a hit: thrown back from the front, pitched forward from behind, turned by the side it lands on; the knees give
rep("  T.spX+=0.25*A.hurt; T.nkX+=0.3*A.hurt; T.chZ+=0.12*A.hurt*A.hurtSide;",
    "  { const h=A.hurt, hf=A.hurtF==null?0.5:A.hurtF, e=h*h*(3-2*h); T.spX+=(hf>-0.2?-0.2:0.32)*e; T.chX+=(hf>-0.2?-0.12:0.15)*e; T.nkX+=(hf>-0.2?0.28:0.35)*e; T.chZ+=0.14*e*A.hurtSide; T.chY+=0.3*e*A.hurtSide; T.hipsY-=0.12*e*A.hurtSide; T.hipsZ+=0.05*e*A.hurtSide;\n    if(S.onGround&&!S.crouch){ T.hipY-=0.05*e; T.knL-=0.26*e; T.knR-=0.2*e; T.hpL+=0.13*e; T.hpR+=0.1*e; } if(!gun&&!building){ T.shLz-=0.25*e; T.shRz+=0.25*e; T.elL+=0.5*e; T.elR+=0.5*e; } }")
rep("  else if(ev==='revive'){ A.dead=false; A.deadT=0; H.group.rotation.x=0; H.group.rotation.z=0; }","  else if(ev==='revive'){ A.dead=false; A.deadT=0; A.deadHow=null; H.group.rotation.x=0; H.group.rotation.z=0; }")
