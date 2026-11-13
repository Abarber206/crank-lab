# patch185: more bots in battle royale (30 players, not 20), and bots that know when they're beaten: a bot you've nearly
# finished breaks off and runs (zigzagging while you can see it), heals once it's out of sight, and comes back when it's
# patched up. Skilled bots are braver: when they're low most of them don't run but keep pushing you instead.
rep("const BR_N=19,","const BR_N=29,")
rep("const BR_NAMES=['Rook2',","const BR_NAMES=['Onyx','Pike','Marlow','Zephyr','Grit','Lark','Tundra','Fennel','Cobalt','Rook2',")
rep("""function brMakeBot(i){ const o=OUTFITS""","""function brMakeBot(i){ const sk=0.25+Math.random()*0.6, o=OUTFITS""")
rep("""swingT:0,thinkT:Math.random()*0.4,stuckT:0,sideT:0,sideDir:1,skill:0.25+Math.random()*0.6,aw:new Map(),""","""swingT:0,thinkT:Math.random()*0.4,stuckT:0,sideT:0,sideDir:1,skill:sk,brave:Math.random()<(sk-0.4)*1.8,flee:false,aw:new Map(),""")
rep("'20 drop in · one walks out'","(BR_N+1)+' drop in · one walks out'")
rep("Math.ceil(20/TS)","Math.ceil((BR_N+1)/TS)")
rep("'Solo · 20 players'","'Solo · '+(BR_N+1)+' players'")
rep("Math.ceil(20/ts)","Math.ceil((BR_N+1)/ts)")
rep("Drop in with 19 bots,","Drop in with 29 bots,")
# the fight: run when beaten (unless brave), push when brave
rep("""    b.strafeT-=dt; if(b.strafeT<=0){ b.strafe=-b.strafe; b.strafeT=0.5+Math.random()*1.2; } strafe=b.strafe*(0.5+0.5*b.skill);
    if(b.hp<45""","""    b.strafeT-=dt; if(b.strafeT<=0){ b.strafe=-b.strafe; b.strafeT=0.5+Math.random()*1.2; } strafe=b.strafe*(0.5+0.5*b.skill);
    { const eh=b.hp+b.sh, th=(T.hp||0)+(T.sh||0), hurtAgo=now-(b.hurtAt||0);
      if(b.flee&&(eh>=70||hurtAgo>14000&&!b.los)) b.flee=false;                                  // patched up (or long since shot at): back in
      if(!b.flee&&!b.brave&&eh<40&&hurtAgo<1200&&th>eh+15) b.flee=true;                            // nearly finished, by someone healthier: run
      if(b.flee){ const dx=b.pos.x-T.pos.x, dz=b.pos.z-T.pos.z, dd=Math.hypot(dx,dz)||1; goal={x:b.pos.x+dx/dd*40,z:b.pos.z+dz/dd*40,r:0.5}; face=null; run=true; strafe=b.los?b.strafe*0.7:0; }
      else if(b.brave&&eh<45&&b.los) goal={x:T.pos.x,z:T.pos.z,r:Math.min(want*0.6,5)}; }        // brave: keep pushing
    if(b.hp<45""")
