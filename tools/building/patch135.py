# patch135: swimming. In water too deep to stand in you float with your head above the surface: a breaststroke when
# you move, treading water when you don't. No shooting or aiming while swimming (your weapon is put away), a weaker
# jump, and no fall damage landing in deep water (a big splash instead). Everyone uses it: you, friends, Buddy, the bot.
rep("""function waterAt(x,z){ const c=worldCell(x,z); return c<0?-1e4:WORLD.WS[c]; }""",
"""function waterAt(x,z){ const c=worldCell(x,z); return c<0?-1e4:WORLD.WS[c]; }
const SWIM_D=1.3; // deep water holds a body up this far under its surface (see terrainUnder)
function waterDepth(x,z){ const w=waterAt(x,z); return w>-999?w-terrainH(x,z):0; }
// floating in water too deep to stand in: the water's surface there, or null
function swimSurface(pos){ const w=waterAt(pos.x,pos.z); return w>-999&&w-terrainH(pos.x,pos.z)>SWIM_D+0.08&&pos.y<w-SWIM_D+0.2?w:null; }""")
rep("function moveBody(E,fw,st,jump,dt){ if(E.kart){","function moveBody(E,fw,st,jump,dt){ E.swim=!E.kart&&!E.sky&&swimSurface(E.pos)!==null; if(E.kart){")
rep("if(jump&&(E.onGround||E.coyT>0)&&E.vel.y<=0.5){ E.vel.y=JUMP;","if(jump&&(E.onGround||E.coyT>0)&&E.vel.y<=0.5){ E.vel.y=E.swim?JUMP*0.6:JUMP;")
rep("const canAim=()=>mode==='gun'&&!edit&&P.reloadT<=0;","const canAim=()=>mode==='gun'&&!edit&&P.reloadT<=0&&!P.swim;")
rep("""function playerShoot(cont){
  if(net.dead) return;""","""function playerShoot(cont){
  if(net.dead) return;
  if(P.swim){ P.burstLeft=0; return; } // no shooting while swimming""")
rep("""function botFire(eye,dist,s){
  if(BT&&BT.sky) return;""","""function botFire(eye,dist,s){
  if(BT&&BT.sky) return; if(B.swim) return; // nor while it swims""")
rep("function allyFire(z){ const eye=","function allyFire(z){ if(AB.swim){ AB.fireT=0.3; return; } const eye=")
rep("if(P.onGround||isDead()){ if(P.fallTop!=null&&P.onGround&&!isDead()){ const drop=P.fallTop-P.pos.y; if(drop>FALL_SAFE) fallHurt(drop); } P.fallTop=null; return; }",
    """if(P.onGround||isDead()){ if(P.fallTop!=null&&P.onGround&&!isDead()){ const drop=P.fallTop-P.pos.y, wd=waterDepth(P.pos.x,P.pos.z);
      if(wd>=1.0){ if(drop>2.5){ const w=waterAt(P.pos.x,P.pos.z); burst(P.pos.clone().setY(w+0.05),Math.min(26,8+drop*0.6),3+Math.min(4,drop*0.12),0.09,splashMat); sfx('step_water'); camDip=Math.min(camDip,-0.15); } } // deep water breaks the fall
      else if(drop>FALL_SAFE) fallHurt(drop); } P.fallTop=null; return; }""")
# the swimmer's pose: everything they hold is put away
rep("""function animateRig(H,S,dt){
  if(S.seat){""","""function animateRig(H,S,dt){
  S.swimW=!S.seat&&!S.sky&&S.pos&&!H.anim.dead?swimSurface(S.pos):null;
  if(S.swimW!==null){ S.gun=false; S.building=false; S.editing=false; S.reload=null; S.emote=null; S.item=false; S.swingT=0; S.crouch=false; }
  if(S.seat){""")
rep("""  // ----- knocked down: face down, dragging yourself along on your forearms -----""",
"""  // ----- swimming: head out of the water; a breaststroke when moving, treading water when still -----
  if(S.swimW!=null){ A.swimT=Math.min(1,(A.swimT||0)+dt*3); A.downT=0; const e=A.swimT*A.swimT*(3-2*A.swimT), set=(o,ax,v)=>{ o.rotation[ax]=lerp(o.rotation[ax],v,sm); }, W=S.swimW;
    const mvK=A.swimMv=lerp(A.swimMv||0,Math.min(1,sp/(S.down?0.8:1.6)),Math.min(1,dt*4)), bob=Math.sin(A.t*2.1)*0.035*(1-0.5*mvK);
    A.swC=((A.swC||0)+dt*(0.55+0.45*mvK)*(S.down?0.6:1))%1; const c=A.swC, TAU=Math.PI*2, reach=0.5+0.5*Math.cos(TAU*c), out=Math.max(0,Math.sin(TAU*c)), legB=Math.max(0,-Math.sin(TAU*c)), surge=0.06*out*mvK;
    // the body: upright treading water, nearly flat swimming; the hips just under the surface, so the head is always out
    A.swX=lerp(A.swX||0,-(0.1+1.05*mvK)*e,Math.min(1,dt*5)); const th=A.swX, hipW=lerp(W-0.44,W-0.2,mvK)+bob+surge, hY=0.94;
    r.hips.position.y=hY; r.hips.position.x=0; G.rotation.x=th; G.rotation.z=0;
    const fx=-Math.sin(S.yaw), fz=-Math.cos(S.yaw), hipStand=S.pos.y+hY; G.position.x=S.pos.x+hY*Math.sin(th)*fx; G.position.z=S.pos.z+hY*Math.sin(th)*fz; G.position.y=lerp(hipStand,hipW,e)-hY*Math.cos(th);
    set(r.hips,'x',0); set(r.hips,'y',0); set(r.hips,'z',0);
    set(r.spine,'x',lerp(-0.02,0.12+0.06*out,mvK)); set(r.spine,'y',0); set(r.spine,'z',0); set(r.chest,'x',lerp(0.04,0.1+0.08*out,mvK)); set(r.chest,'y',0); set(r.chest,'z',0);
    set(r.neck,'x',lerp(0.05,0.55,mvK)); set(r.neck,'y',lerp(0.15*Math.sin(A.t*0.7),0,mvK)); set(r.neck,'z',0);                                   // the chin up out of the water
    // arms: sculling out to the sides when treading; a breaststroke pull (out, round and in) then shooting forward when swimming
    const sc=Math.sin(A.t*3.2);
    for(const [a,sx] of [[r.armL,-1],[r.armR,1]]){ set(a.sh,'x',lerp(0.45+0.08*sc,1.75+1.15*reach,mvK)); set(a.sh,'z',sx*lerp(1.05+0.18*sc,0.22+0.95*out,mvK)); set(a.sh,'y',sx*lerp(0.25*sc,-0.2*out,mvK));
      set(a.el,'x',lerp(0.55,0.2+1.35*(1-reach),mvK)); set(a.wr,'x',lerp(0.1,0.25,mvK)); }
    // legs: an eggbeater kick treading water; the frog kick (knees up and out, then a snap back together) swimming
    let q=0; for(const [L,sx] of [[r.legL,-1],[r.legR,1]]){ const eg=Math.sin(A.t*4.2+q*Math.PI); q++;
      set(L.hp,'x',lerp(0.55+0.25*eg,0.12+0.55*legB,mvK)); set(L.hp,'z',sx*lerp(0.32+0.1*eg,0.12+0.5*legB,mvK)); set(L.hp,'y',sx*lerp(0.2,0.35*legB,mvK));
      set(L.kn,'x',lerp(-1.05+0.35*eg,-0.12-1.55*legB,mvK)); set(L.an,'x',lerp(0.35,0.45+0.4*legB,mvK)); }
    A.handL=A.handR='flat'; A.turnL=A.turnR=0;
    for(const k of GUN_MODELS) if(r[k]) r[k].visible=false; if(r.heldMag) r.heldMag.visible=false; if(r.heldShell) r.heldShell.visible=false;
    r.gun.visible=r.pump.visible=r.hammer.visible=r.plan.visible=false; r.pick.visible=false; if(H.glider) H.glider.visible=false;
    // ripples where you break the surface
    A.rip=(A.rip||0)-dt; if(A.rip<=0&&S.pos.distanceTo(camera.position)<45){ A.rip=mvK>0.3?0.22:0.7; burst(_swV.set(S.pos.x+fx*0.5*mvK,W+0.04,S.pos.z+fz*0.5*mvK),mvK>0.3?4:2,0.9+1.4*mvK,0.05,splashMat); }
    return; }
  A.swimT=0;
  // ----- knocked down: face down, dragging yourself along on your forearms -----""")
rep("function animateRig0(H,S,dt){","const _swV=new THREE.Vector3();\nfunction animateRig0(H,S,dt){")
# no crosshair while swimming (you can't shoot)
rep("body.scoped #cross{opacity:0}","body.scoped #cross{opacity:0}\nbody.swim #cross{opacity:0}")
rep("""function animateHero(dt){""","""function animateHero(dt){ if(document.body.classList.contains('swim')!==!!P.swim) document.body.classList.toggle('swim',!!P.swim);""")
