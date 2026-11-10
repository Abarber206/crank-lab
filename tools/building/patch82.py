# ---------- 82. scarier, livelier creatures (same designs): they claw up out of the ground, heave as they breathe, shudder
# and snap their heads, reach for you and speed up when close, pounce on the strike, recoil when shot, and screech again mid-chase ----------
rep("  const ty=z.type, sp=Math.hypot(z.vel.x,z.vel.z), mv=Math.min(1,sp/1.5), run=ty==='runner';\n  z.walk+=dt*(run?2.6+sp*2.4:ty==='brute'?1.2+sp*1.4:1.4+sp*1.6);",
r"""  const ty=z.type, sp=Math.hypot(z.vel.x,z.vel.z), mv=Math.min(1,sp/1.5), run=ty==='runner';
  // how close its prey is (you, or Buddy): within 10 m it goes into a frenzy
  let dPrey=z.pos.distanceTo(P.pos); if(isDead()||P.down) dPrey=99; if(typeof AB!=='undefined'&&AB&&AB.active&&!AB.dead&&!AB.down) dPrey=Math.min(dPrey,z.pos.distanceTo(AB.pos));
  z.fz=(z.fz||0)+((dPrey<10?1-dPrey/10:0)-(z.fz||0))*Math.min(1,dt*4); const fz=z.fz;
  z.walk+=dt*(run?2.6+sp*2.4:ty==='brute'?1.2+sp*1.4:1.4+sp*1.6)*(1+0.35*fz);
  // clawing up out of the ground when it appears
  if(z.rise===undefined){ z.rise=1; if(z.pos.distanceTo(P.pos)<70) burst(z.pos.clone().setY(z.pos.y+0.1),10,3.2,0.09,typeof dustMat!=='undefined'?dustMat:undefined); }
  if(z.rise>0){ z.rise=Math.max(0,z.rise-dt/0.9); const e=z.rise*z.rise; g.position.y-=e*1.7*z.sc; g.rotation.x=-0.5*e; g.rotation.z=Math.sin(z.id*3.1)*0.3*e; if(Math.random()<dt*14&&z.pos.distanceTo(P.pos)<50) burst(z.pos.clone().setY(z.pos.y+0.05),1,2.2,0.07,typeof dustMat!=='undefined'?dustMat:undefined); }
  else { g.rotation.x=0; g.rotation.z=0; }
  // a shudder runs through it every few seconds; and mid-chase it throws its head back and screeches again
  z.shT=(z.shT===undefined?1+Math.random()*4:z.shT)-dt; if(z.shT<=0){ z.shT=2.5+Math.random()*5; z.sh=0.22; } z.sh=Math.max(0,(z.sh||0)-dt); const shk=z.sh>0?Math.sin(z.sh*90)*z.sh*1.6:0;
  if(z.spotted&&z.scr<=0&&z.atk<=0&&dPrey<30&&dPrey>5){ z.rsT=(z.rsT===undefined?4+Math.random()*8:z.rsT)-dt; if(z.rsT<=0){ z.rsT=7+Math.random()*9; z.scr=0.7; const n2=performance.now(); if(n2-zScreechAt>900){ zScreechAt=n2; zsfx('screech',z.pos); } } }""")
# breathing heave + shudder + frenzy lean in the spine; recoil when hit
rep("  R.spine.rotation.x=R.tilt-lurch+raise*0.32-strike*0.42+scr*(run?0.7:0.4)+thW*0.25-thF*0.35;",
    "  const br=Math.sin(now*0.0034+z.id)*(ty==='brute'?0.05:0.035)*(1-mv*0.5), rec=Math.max(0,z.hitFlash||0)/0.12;\n  R.spine.rotation.x=R.tilt-lurch+raise*0.32-strike*0.42+scr*(run?0.7:0.4)+thW*0.25-thF*0.35+br-fz*0.16*(1-raise)+rec*0.4+shk*0.25;")
rep("  R.spine.rotation.y=(ty==='brute'?s*0.12*mv:0)-thW*0.45+thF*0.35; R.spine.rotation.z=-roll*0.85;","  R.spine.rotation.y=(ty==='brute'?s*0.12*mv:0)-thW*0.45+thF*0.35+shk*0.5; R.spine.rotation.z=-roll*0.85+shk*0.3;")
# arms reach out and claw at you in a frenzy (alternating grabs), instead of just hanging
rep("  R.armL.rotation.x=aB+(run?-s*sw:Math.sin(z.walk*0.9)*sw)+raise*2.3-strike*0.3;\n  R.armR.rotation.x=aB+(run?s*sw:-Math.sin(z.walk*0.9+0.6)*sw)+raise*2.0-strike*0.3-thW*2.7+thF*1.4;",
    "  const grab=run?0:fz*(1-raise)*(1-scr), gL=grab*(0.95+0.45*Math.sin(z.walk*1.7)), gR=grab*(0.95+0.45*Math.sin(z.walk*1.7+Math.PI));\n  R.armL.rotation.x=aB+(run?-s*sw:Math.sin(z.walk*0.9)*sw)+raise*2.3-strike*0.3+gL+shk*0.4;\n  R.armR.rotation.x=aB+(run?s*sw:-Math.sin(z.walk*0.9+0.6)*sw)+raise*2.0-strike*0.3-thW*2.7+thF*1.4+gR*(z.thr>0?0:1)-shk*0.4;")
# the strike is a pounce: Runners leave the ground; the head snaps down to bite
rep("  const lg=strike*(run?0.6:0.35)*z.sc; g.position.x-=Math.sin(z.yaw)*lg; g.position.z-=Math.cos(z.yaw)*lg;","  const lg=strike*(run?0.75:0.45)*z.sc; g.position.x-=Math.sin(z.yaw)*lg; g.position.z-=Math.cos(z.yaw)*lg; g.position.y+=strike*(run?0.28:ty==='brute'?0.05:0.1)*z.sc;")
rep("  R.head.rotation.x=R.headTilt+scr*0.6+raise*0.15-strike*0.1;","  R.head.rotation.x=R.headTilt+scr*0.75+raise*0.3-strike*0.45+rec*0.5+0.1*fz*Math.sin(now*0.02+z.id); R.head.rotation.z+=shk*1.2;")
# twitchier head the closer it gets
rep("z.twT=0.25+Math.random()*1.4;","z.twT=(0.25+Math.random()*1.4)*(1-0.6*fz);")
