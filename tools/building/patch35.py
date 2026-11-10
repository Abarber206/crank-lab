# ---------- 35. skydive in every mode; the mountains are the edge of the map; the buggy can't climb cliffs ----------
rep("function skyDropAllowed(){ return settings.skyDrop!==false&&settings.mode!=='horde'&&!horde.on&&!botOn(); }","function skyDropAllowed(){ return settings.skyDrop!==false; }")
rep("  if(!P.everPlayed){ P.everPlayed=true; if(!net.role&&skyDropAllowed()) skyDrop(SPAWN[0],SPAWN[2],SKY_FIRST); }","  if(!P.everPlayed){ P.everPlayed=true; if((!net.role||!party.live)&&skyDropAllowed()) skyDrop(SPAWN[0],SPAWN[2],SKY_FIRST); }")
rep("function botFire(eye,dist,s){\n","function botFire(eye,dist,s){\n  if(BT&&BT.sky) return; // no shooting at someone still in the sky\n")
# no invisible circle: the outer mountains (too steep to climb) are the edge. A hard stop only far out, where the land ends
rep("    if(d>MAP_R){ const nx=dx/d, nz=dz/d; E.pos.x=SPAWN[0]+nx*MAP_R; E.pos.z=SPAWN[2]+nz*MAP_R;","    if(d>WORLD_EDGE){ const nx=dx/d, nz=dz/d; E.pos.x=SPAWN[0]+nx*WORLD_EDGE; E.pos.z=SPAWN[2]+nz*WORLD_EDGE;")
rep("const RUN=6.0, CROUCH_SPD=3.2,","const WORLD_EDGE=2150; // where the land itself ends (far beyond the climbable ground)\nconst RUN=6.0, CROUCH_SPD=3.2,")
rep("if(d>MAP_R-2){ k.x=SPAWN[0]+dx/d*(MAP_R-2); k.z=SPAWN[2]+dz/d*(MAP_R-2); k.vx*=0.3; k.vz*=0.3; } }","if(d>WORLD_EDGE){ k.x=SPAWN[0]+dx/d*WORLD_EDGE; k.z=SPAWN[2]+dz/d*WORLD_EDGE; k.vx*=0.3; k.vz*=0.3; } }")
rep("  if(Math.hypot(c.x-SPAWN[0],c.z-SPAWN[2])>MAP_R-2) return {ok:false,reason:'Edge of the map'};","  if(Math.hypot(c.x-SPAWN[0],c.z-SPAWN[2])>WORLD_EDGE-2) return {ok:false,reason:'Edge of the map'};")
rep("  g.setLineDash([10,8]); g.strokeStyle='rgba(255,255,255,.55)'; g.lineWidth=2; g.beginPath(); g.arc(X(0),X(0),MAP_R/mpp,0,7); g.stroke(); // the edge of the island\n","")
# the buggy: on steep ground (not builds) the tyres lose their grip and it slides back down
rep("  if(ground){\n    if(inp.fw>0.1){ if(vf<-0.3)","""  let slick=false;
  if(ground){ const [ts]=slopeAt(k.x,k.z), onB=KART_WHEELS.some(([wx,wz],i)=>{ const p=kartPoint(k,wx,0,wz,_ku); return k.wh[i]>terrainUnder(p.x,p.z)+0.08; }); slick=!onB&&ts>0.78; }
  if(ground&&slick){ // too steep: no traction, it slides down the hill
    vf-=GRAV*Math.sin(k.pitch)*dt; vl-=GRAV*Math.sin(k.roll)*dt*0.8; vl*=Math.exp(-1.2*dt); vf*=Math.exp(-0.4*dt); }
  else if(ground){
    if(inp.fw>0.1){ if(vf<-0.3)""")
# horde: every new horde game starts with a drop from the sky too
rep("  if(!net.role){ clearBuilds(); respawn(); }\n  syncBot(); refreshTeamMarkers();","  if(!net.role){ clearBuilds(); respawn(); if(skyDropAllowed()){ const a=Math.random()*6.283; skyDrop(SPAWN[0]+Math.cos(a)*20,SPAWN[2]+Math.sin(a)*20,SKY_MATCH); } }\n  syncBot(); refreshTeamMarkers();")
# the Respawn button puts you back up in the sky
rep("$('respawn').addEventListener('click',()=>{ respawn(); });","$('respawn').addEventListener('click',()=>{ respawn(); if(skyDropAllowed()){ const a=Math.random()*6.283, r=12+Math.random()*25; skyDrop(SPAWN[0]+Math.cos(a)*r,SPAWN[2]+Math.sin(a)*r,SKY_BACK); } });")
