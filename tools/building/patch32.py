# ---------- 32. steep mountainsides: you can't walk up them, and you slide (or fall) down them; no hurt grunt ----------
rep("const RUN=6.0, CROUCH_SPD=3.2,","""/* Ground steeper than 45 degrees (where the hillside turns to bare rock) can't be walked up: you stop at its foot or
   walk along it. Stand or land on it and you lose your footing and slide down it, steering only a little and unable to
   jump, until the ground levels out. Sliding never counts as a fall, but going off a near-vertical face does. Builds
   are always solid footing, so you can still build your way up a cliff. */
const SLOPE_MAX=1.0;
function slopeAt(x,z){ const e=0.8, gx=(terrainH(x+e,z)-terrainH(x-e,z))/(2*e), gz=(terrainH(x,z+e)-terrainH(x,z-e))/(2*e); return [Math.hypot(gx,gz),gx,gz]; }
const RUN=6.0, CROUCH_SPD=3.2,""")
# walking: never up a slope that's too steep (the uphill part of your step is dropped, so you slide along its foot)
rep("""  const nz=oz+E.vel.z*dt;
  if(blocked(E.pos.x,nz,E.pos.x,oz,E.pos.y,h,step,ps)) E.vel.z=0; else E.pos.z=nz;
  const f=E.pos.y;""","""  const nz=oz+E.vel.z*dt;
  if(blocked(E.pos.x,nz,E.pos.x,oz,E.pos.y,h,step,ps)) E.vel.z=0; else E.pos.z=nz;
  if((E.onGround||E.slideT>0)&&(E.pos.x!==ox||E.pos.z!==oz)){ const tN=terrainH(E.pos.x,E.pos.z), tO=terrainH(ox,oz), md=Math.hypot(E.pos.x-ox,E.pos.z-oz);
    if(tN-tO>md*SLOPE_MAX&&E.pos.y<=terrainUnder(ox,oz)+0.05){ const [s,gx,gz]=slopeAt(E.pos.x,E.pos.z);
      if(s>SLOPE_MAX&&groundAt(E.pos.x,E.pos.z,E.pos.y+step,ps)[0]<=terrainUnder(E.pos.x,E.pos.z)+1e-3){ const ux=gx/s, uz=gz/s, vd=E.vel.x*ux+E.vel.z*uz;
        if(vd>0){ E.vel.x-=vd*ux; E.vel.z-=vd*uz; } const tx=ox+E.vel.x*dt, tz=oz+E.vel.z*dt;
        if(terrainH(tx,tz)-tO<=Math.hypot(tx-ox,tz-oz)*SLOPE_MAX+0.002&&!blocked(tx,tz,ox,oz,E.pos.y,h,step,ps)){ E.pos.x=tx; E.pos.z=tz; } else { E.pos.x=ox; E.pos.z=oz; } } } }
  if(E.slideT>0) E.slideT-=dt;
  const f=E.pos.y;""")
rep("""    const [g,sl]=groundAt(E.pos.x,E.pos.z,f+step,ps), nf=f+E.vel.y*dt;
    if(E.onGround&&g>=f-0.6){""","""    const [g,sl]=groundAt(E.pos.x,E.pos.z,f+step,ps), nf=f+E.vel.y*dt;
    const steep=!sl&&g<=terrainUnder(E.pos.x,E.pos.z)+1e-3?slopeAt(E.pos.x,E.pos.z):null;
    if(steep&&steep[0]>SLOPE_MAX&&(E.onGround?g>=f-0.6:nf<=g)){
      // no footing: slide down the face. Keep only the motion along it, so gravity carries you downhill
      const [s,gx,gz]=steep, nl=Math.hypot(gx,1,gz), nx_=-gx/nl, ny_=1/nl, nz_=-gz/nl, vn=E.vel.x*nx_+E.vel.y*ny_+E.vel.z*nz_;
      if(vn<0){ E.vel.x-=vn*nx_; E.vel.y-=vn*ny_; E.vel.z-=vn*nz_; }
      const fr=Math.exp(-dt*0.5); E.vel.x*=fr; E.vel.z*=fr;
      E.pos.y=g; E.onGround=false; E.coyT=0; E.groundSlab=null; E.slideT=0.15; E.slideSoft=s<2.6; }
    else if(E.onGround&&g>=f-0.6){""")
# while sliding you can only steer a little
rep("    const a=(E.onGround?ACC_G:ACC_A)*dt, dx=tx-E.vel.x, dz=tz-E.vel.z, d=Math.hypot(dx,dz);","    const a=(E.onGround?ACC_G:E.slideT>0?ACC_A*0.15:ACC_A)*dt, dx=tx-E.vel.x, dz=tz-E.vel.z, d=Math.hypot(dx,dz);")
rep("  if(E.onGround||mag>0.02){\n    const a=","  if(E.onGround||(mag>0.02&&!(E.slideT>0&&mag<0.02))){\n    const a=")
# a slide isn't a fall (a sheer drop still is)
rep("  if(P.sky||P.kart){ P.fallTop=null; return; }","  if(P.sky||P.kart){ P.fallTop=null; return; }\n  if(P.slideT>0&&P.slideSoft){ P.fallTop=P.pos.y; return; }")
# no grunt when you get hurt (the red flash and the hit marker stay)
rep("    case 'hurt': { const p=0.9+Math.random()*0.2; voice({f0:190*p,f1:130*p,dur:0.2,vol:0.32,vowel:VOW.HAH,vowel2:VOW.HUH,breath:0.35,fry:0.15,jitter:0.03,attack:0.012}); knock(160,0.08,0.18,2); }","    case 'hurt': break;")
